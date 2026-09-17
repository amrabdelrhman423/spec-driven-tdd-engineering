#!/usr/bin/env python3
"""
Skill Builder & Validator CLI for Multi-Agent Workspaces (Claude & AGY)
Supports creating, validating, linting, and synchronizing Agent Skills.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class SkillValidationError(Exception):
    pass

def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extract and parse simple YAML frontmatter from markdown content."""
    pattern = r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise SkillValidationError("Missing YAML frontmatter delimiters ('---') at start of file.")
    
    raw_yaml = match.group(1)
    body = match.group(2)
    
    data = {}
    current_key = None
    multiline_value = []
    
    for line in raw_yaml.splitlines():
        line_strip = line.strip()
        if not line_strip or line_strip.startswith("#"):
            continue
        
        kv_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if kv_match:
            if current_key and multiline_value:
                data[current_key] = " ".join(multiline_value).strip()
                multiline_value = []
            current_key = kv_match.group(1)
            val = kv_match.group(2).strip()
            if val in (">", ">-", "|", "|-"):
                multiline_value = []
            elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                data[current_key] = val[1:-1]
            else:
                data[current_key] = val
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            multiline_value.append(line_strip.strip("\"'"))
        else:
            continue
            
    if current_key and multiline_value:
        data[current_key] = " ".join(multiline_value).strip()
        
    return data, body

def find_markdown_links(content: str) -> List[Tuple[str, str]]:
    """Extract local markdown links [text](target), ignoring fenced code blocks."""
    # Strip fenced code blocks (```...```)
    content_no_code = re.sub(r"```[\s\S]*?```", "", content)
    # Strip inline code (`...`)
    content_no_code = re.sub(r"`[^`\n]+`", "", content_no_code)

    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, content_no_code)
    local_links = []
    for label, url in matches:
        clean_url = url.split("#")[0].strip()
        if clean_url and not clean_url.startswith(("http://", "https://", "mailto:", "ftp://", "file://")):
            local_links.append((label, clean_url))
    return local_links

def validate_skill(skill_dir: Path) -> List[str]:
    """Validate a skill folder structure, frontmatter, and link integrity."""
    issues = []
    skill_dir = skill_dir.resolve()
    
    if not skill_dir.is_dir():
        return [f"Directory not found: {skill_dir}"]
        
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"Missing required SKILL.md in {skill_dir}"]
        
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Cannot read SKILL.md: {e}"]
        
    # Check frontmatter
    try:
        frontmatter, body = parse_frontmatter(content)
    except SkillValidationError as e:
        return [str(e)]
        
    skill_name = frontmatter.get("name")
    if not skill_name:
        issues.append("Frontmatter missing required 'name' field.")
    else:
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", skill_name):
            issues.append(f"Invalid skill name '{skill_name}': must be lowercase alphanumeric with hyphens.")
        if skill_name != skill_dir.name:
            issues.append(f"Skill name '{skill_name}' does not match directory name '{skill_dir.name}'.")
            
    description = frontmatter.get("description")
    if not description:
        issues.append("Frontmatter missing required 'description' field.")
    else:
        if len(description.strip()) < 20:
            issues.append("Skill description is too short (< 20 characters). Describe when and why the agent should use this skill.")
        # Check if description uses third-person or trigger phrasing
        desc_lower = description.lower()
        if not any(token in desc_lower for token in ["use this skill", "activate this skill", "trigger", "when", "guides", "enables", "provides"]):
            issues.append("Warning: Skill description should clearly specify triggering conditions (e.g., 'Use this skill when...').")

    # Progressive disclosure check: SKILL.md should be lean
    line_count = len(content.splitlines())
    if line_count > 600:
        issues.append(f"Warning: SKILL.md is long ({line_count} lines). Consider moving detailed guides to references/ for progressive disclosure.")

    # Validate relative markdown links
    links = find_markdown_links(content)
    for label, rel_path in links:
        target = (skill_dir / rel_path).resolve()
        if not target.exists():
            issues.append(f"Broken markdown link '[{label}]({rel_path})': target '{target}' does not exist.")
            
    return issues

def scaffold_skill(root_dir: Path, skill_name: str, description: Optional[str] = None) -> Path:
    """Create a new dual-compatible skill scaffold."""
    skill_name = skill_name.strip().lower().replace("_", "-")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", skill_name):
        raise ValueError(f"Invalid skill name '{skill_name}'. Must be hyphenated lowercase alphanumeric.")
        
    agents_dir = root_dir / ".agents" / "skills" / skill_name
    agents_dir.mkdir(parents=True, exist_ok=True)
    
    (agents_dir / "references").mkdir(exist_ok=True)
    (agents_dir / "templates").mkdir(exist_ok=True)
    (agents_dir / "scripts").mkdir(exist_ok=True)
    (agents_dir / "examples").mkdir(exist_ok=True)
    
    desc_text = description or f"Use this skill when the user asks to perform {skill_name.replace('-', ' ')} tasks or workflows."
    
    skill_md = f"""---
name: {skill_name}
description: >-
  {desc_text}
---

# {skill_name.replace('-', ' ').title()}

## Overview
Briefly describe the capability and purpose of this skill.

## Workflow Instructions

1. **Step 1: Preparation**
   - Review requirements and inspect relevant resources.
   - Reference guide: [references/guide.md](./references/guide.md)

2. **Step 2: Execution**
   - Follow standard runbook procedures.
   - Use provided templates: [templates/template.md](./templates/template.md)

3. **Step 3: Verification**
   - Verify outputs against acceptance criteria.

## Progressive Disclosure Links
- **Detailed Reference**: [references/guide.md](./references/guide.md)
- **Templates**: [templates/template.md](./templates/template.md)
- **Examples**: [examples/README.md](./examples/README.md)
"""
    (agents_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    
    # Create starter reference file
    ref_md = f"""# {skill_name.replace('-', ' ').title()} - Detailed Reference

This document contains deep technical details, architectural decisions, and edge-case handling.
The agent reads this file progressively when required.
"""
    (agents_dir / "references" / "guide.md").write_text(ref_md, encoding="utf-8")
    
    # Create starter template file
    template_md = f"""# {skill_name.replace('-', ' ').title()} Template

Fill in this template when executing the workflow.
"""
    (agents_dir / "templates" / "template.md").write_text(template_md, encoding="utf-8")

    # Create starter example
    example_md = f"""# Example for {skill_name}

Reference implementation demonstrating input, execution, and expected output.
"""
    (agents_dir / "examples" / "README.md").write_text(example_md, encoding="utf-8")
    
    # Sync to Claude directory
    sync_skills(root_dir)
    return agents_dir

def sync_skills(root_dir: Path) -> List[str]:
    """Synchronize skills between .agents/skills and .claude/skills."""
    agents_skills = root_dir / ".agents" / "skills"
    claude_skills = root_dir / ".claude" / "skills"
    
    synced = []
    if not agents_skills.exists():
        return synced
        
    claude_skills.mkdir(parents=True, exist_ok=True)
    
    for item in agents_skills.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            dest = claude_skills / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            synced.append(item.name)
            
    return synced

def main():
    parser = argparse.ArgumentParser(description="Skill Builder & Validator for Claude and AGY Agents")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Scaffold command
    new_parser = subparsers.add_parser("new", help="Scaffold a new skill")
    new_parser.add_argument("name", help="Name of the skill (e.g. tdd-sdd)")
    new_parser.add_argument("--desc", help="Description for YAML frontmatter", default=None)
    
    # Validate command
    val_parser = subparsers.add_parser("validate", help="Validate a skill or all skills")
    val_parser.add_argument("target", nargs="?", help="Skill name or path to validate (omit for all)")
    
    # Sync command
    subparsers.add_parser("sync", help="Synchronize .agents/skills to .claude/skills")
    
    # List command
    subparsers.add_parser("list", help="List all installed skills and their validation status")

    args = parser.parse_args()
    root_dir = Path.cwd()
    
    if args.command == "new":
        try:
            created = scaffold_skill(root_dir, args.name, args.desc)
            print(f"[SUCCESS] Created skill '{args.name}' at: {created}")
            print(f"[SUCCESS] Synced to Claude directory: {root_dir / '.claude' / 'skills' / args.name}")
        except Exception as e:
            print(f"[ERROR] Failed to scaffold skill: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "sync":
        synced = sync_skills(root_dir)
        print(f"[SUCCESS] Synced {len(synced)} skills to .claude/skills: {', '.join(synced) if synced else 'None'}")
        
    elif args.command == "validate":
        skills_to_check = []
        if args.target:
            p = Path(args.target)
            if p.is_dir():
                skills_to_check.append(p)
            else:
                agent_path = root_dir / ".agents" / "skills" / args.target
                if agent_path.is_dir():
                    skills_to_check.append(agent_path)
                else:
                    print(f"[ERROR] Skill not found: {args.target}", file=sys.stderr)
                    sys.exit(1)
        else:
            agent_skills = root_dir / ".agents" / "skills"
            if agent_skills.exists():
                for s in agent_skills.iterdir():
                    if s.is_dir():
                        skills_to_check.append(s)
                        
        if not skills_to_check:
            print("No skills found to validate.")
            sys.exit(0)
            
        all_passed = True
        for s in skills_to_check:
            issues = validate_skill(s)
            warnings = [i for i in issues if i.startswith("Warning:")]
            errors = [i for i in issues if not i.startswith("Warning:")]
            
            print(f"\n--- Checking: {s.name} ---")
            if errors:
                all_passed = False
                print(f"[FAIL] {len(errors)} error(s):")
                for err in errors:
                    print(f"  * {err}")
            else:
                print("[PASS] Frontmatter, structure, and links are valid.")
                
            if warnings:
                print(f"[WARN] {len(warnings)} warning(s):")
                for w in warnings:
                    print(f"  * {w}")
                    
        if not all_passed:
            sys.exit(1)
            
    elif args.command == "list":
        agent_skills = root_dir / ".agents" / "skills"
        if not agent_skills.exists():
            print("No .agents/skills directory found.")
            return
        print("Installed Skills:")
        for s in agent_skills.iterdir():
            if s.is_dir():
                skill_md = s / "SKILL.md"
                if skill_md.exists():
                    try:
                        fm, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                        desc = fm.get("description", "No description")
                        print(f" - {s.name}: {desc[:80]}...")
                    except Exception:
                        print(f" - {s.name} (Invalid SKILL.md)")
                else:
                    print(f" - {s.name} (Missing SKILL.md)")

if __name__ == "__main__":
    main()
