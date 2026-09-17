import shutil
import tempfile
import unittest
from pathlib import Path

from tools.skill_builder import (
    parse_frontmatter,
    find_markdown_links,
    validate_skill,
    scaffold_skill,
    sync_skills,
    SkillValidationError
)

class TestSkillBuilder(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # Frontmatter Parsing Tests
    def test_parse_valid_frontmatter(self):
        content = """---
name: my-skill
description: Use this skill when testing frontmatter parsing.
---
# Skill Content
Body text here.
"""
        fm, body = parse_frontmatter(content)
        self.assertEqual(fm["name"], "my-skill")
        self.assertEqual(fm["description"], "Use this skill when testing frontmatter parsing.")
        self.assertIn("# Skill Content", body)

    def test_parse_multiline_folded_frontmatter(self):
        content = """---
name: multiline-skill
description: >-
  This is a multiline description
  spanning several lines of text.
---
Body text.
"""
        fm, _ = parse_frontmatter(content)
        self.assertEqual(fm["name"], "multiline-skill")
        self.assertIn("multiline description spanning several lines", fm["description"])

    def test_parse_missing_frontmatter_raises(self):
        content = "# No frontmatter\nJust body text."
        with self.assertRaises(SkillValidationError):
            parse_frontmatter(content)

    # Markdown Link Parsing Tests
    def test_find_markdown_links(self):
        content = """
# Links Test
Check [local guide](./references/guide.md) and [another](templates/sample.md#heading).
External [Google](https://google.com) should be ignored.
Inline code `[fake](broken.md)` should be ignored.
```markdown
[fenced](also_broken.md)
```
"""
        links = find_markdown_links(content)
        targets = [target for _, target in links]
        self.assertIn("./references/guide.md", targets)
        self.assertIn("templates/sample.md", targets)
        self.assertNotIn("https://google.com", targets)
        self.assertNotIn("broken.md", targets)
        self.assertNotIn("also_broken.md", targets)

    # Scaffolding & Validation Tests
    def test_scaffold_creates_valid_skill(self):
        skill_name = "test-workflow"
        created_path = scaffold_skill(self.test_dir, skill_name, "Use this skill when running test workflow procedures.")
        self.assertTrue(created_path.exists())
        self.assertTrue((created_path / "SKILL.md").exists())
        self.assertTrue((created_path / "references" / "guide.md").exists())
        self.assertTrue((created_path / "templates" / "template.md").exists())
        self.assertTrue((created_path / "examples" / "README.md").exists())

        # Validate newly scaffolded skill
        issues = validate_skill(created_path)
        errors = [i for i in issues if not i.startswith("Warning:")]
        self.assertEqual(errors, [])

    def test_validate_broken_link_detection(self):
        skill_path = self.test_dir / ".agents" / "skills" / "broken-link-skill"
        skill_path.mkdir(parents=True)
        bad_md = """---
name: broken-link-skill
description: Use this skill when testing broken link detection.
---
# Broken Link Skill
See [missing file](./references/missing.md).
"""
        (skill_path / "SKILL.md").write_text(bad_md, encoding="utf-8")
        issues = validate_skill(skill_path)
        self.assertTrue(any("Broken markdown link" in i for i in issues))

    def test_validate_mismatched_name(self):
        skill_path = self.test_dir / ".agents" / "skills" / "actual-name"
        skill_path.mkdir(parents=True)
        bad_md = """---
name: wrong-name
description: Use this skill when testing mismatched names.
---
# Content
"""
        (skill_path / "SKILL.md").write_text(bad_md, encoding="utf-8")
        issues = validate_skill(skill_path)
        self.assertTrue(any("does not match directory name" in i for i in issues))

    # Sync Tests
    def test_sync_skills(self):
        scaffold_skill(self.test_dir, "sync-skill", "Use this skill when testing sync functionality.")
        claude_path = self.test_dir / ".claude" / "skills" / "sync-skill"
        self.assertTrue(claude_path.exists())
        self.assertTrue((claude_path / "SKILL.md").exists())

if __name__ == "__main__":
    unittest.main()
