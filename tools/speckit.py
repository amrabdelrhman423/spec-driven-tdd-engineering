#!/usr/bin/env python3
"""
Spec-Kit CLI: Automation tool for Spec-Driven Development (SDD)
Inspired by GitHub Spec-Kit (https://github.com/github/spec-kit).
Manages .specify/ specifications, technical plans, and TDD tasks.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# UTF-8 console safety for Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SPECIFY_DIR = ROOT_DIR / ".specify"
TEMPLATES_DIR = ROOT_DIR / ".agents" / "skills" / "spec-driven-tdd-engineering" / "templates"

def ensure_specify_dir():
    SPECIFY_DIR.mkdir(parents=True, exist_ok=True)
    (SPECIFY_DIR / "specs").mkdir(parents=True, exist_ok=True)

def cmd_init(args):
    ensure_specify_dir()
    constitution_path = SPECIFY_DIR / "constitution.md"
    if constitution_path.exists():
        print(f"[INFO] Constitution already exists at: {constitution_path}")
    else:
        tmpl = TEMPLATES_DIR / "speckit_constitution_template.md"
        if tmpl.exists():
            content = tmpl.read_text(encoding="utf-8")
        else:
            content = "# Project Constitution\n\nMandatory SDD & TDD standards.\n"
        constitution_path.write_text(content, encoding="utf-8")
        print(f"[SUCCESS] Initialized constitution at: {constitution_path}")

def cmd_specify(args):
    ensure_specify_dir()
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = SPECIFY_DIR / "specs" / feature
    feat_dir.mkdir(parents=True, exist_ok=True)
    
    spec_file = feat_dir / "spec.md"
    if spec_file.exists() and not args.force:
        print(f"[WARN] Specification already exists: {spec_file} (use --force to overwrite)")
        return
        
    tmpl = TEMPLATES_DIR / "speckit_specification_template.md"
    if tmpl.exists():
        content = tmpl.read_text(encoding="utf-8").replace("[Feature Name]", feature.replace("-", " ").title())
    else:
        content = f"# Feature Specification: {feature}\n\nDefine requirements here.\n"
    spec_file.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Created specification at: {spec_file}")

def cmd_plan(args):
    ensure_specify_dir()
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = SPECIFY_DIR / "specs" / feature
    feat_dir.mkdir(parents=True, exist_ok=True)
    
    plan_file = feat_dir / "plan.md"
    if plan_file.exists() and not args.force:
        print(f"[WARN] Technical plan already exists: {plan_file} (use --force to overwrite)")
        return
        
    tmpl = TEMPLATES_DIR / "speckit_plan_template.md"
    if tmpl.exists():
        content = tmpl.read_text(encoding="utf-8").replace("[Feature Name]", feature.replace("-", " ").title())
    else:
        content = f"# Technical Plan: {feature}\n\nDefine technical architecture here.\n"
    plan_file.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Created technical plan at: {plan_file}")

def cmd_tasks(args):
    ensure_specify_dir()
    feature = args.feature.strip().lower().replace("_", "-")
    feat_dir = SPECIFY_DIR / "specs" / feature
    feat_dir.mkdir(parents=True, exist_ok=True)
    
    tasks_file = feat_dir / "tasks.md"
    if tasks_file.exists() and not args.force:
        print(f"[WARN] Tasks file already exists: {tasks_file} (use --force to overwrite)")
        return
        
    tmpl = TEMPLATES_DIR / "speckit_tasks_template.md"
    if tmpl.exists():
        content = tmpl.read_text(encoding="utf-8").replace("[Feature Name]", feature.replace("-", " ").title())
    else:
        content = f"# Implementation Tasks: {feature}\n\n- [ ] Task 1\n"
    tasks_file.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Created implementation tasks at: {tasks_file}")

def cmd_status(args):
    ensure_specify_dir()
    specs_dir = SPECIFY_DIR / "specs"
    if not specs_dir.exists() or not any(specs_dir.iterdir()):
        print("[INFO] No feature specifications found under .specify/specs/")
        return
        
    print(f"\n{'FEATURE':<30} | {'SPEC':<6} | {'PLAN':<6} | {'TASKS':<18}")
    print("-" * 70)
    
    for feat in sorted(specs_dir.iterdir()):
        if not feat.is_dir():
            continue
        has_spec = "YES" if (feat / "spec.md").exists() else "NO"
        has_plan = "YES" if (feat / "plan.md").exists() else "NO"
        
        tasks_file = feat / "tasks.md"
        if tasks_file.exists():
            text = tasks_file.read_text(encoding="utf-8")
            total_tasks = len(re.findall(r"- \[[ xX]\]", text))
            done_tasks = len(re.findall(r"- \[[xX]\]", text))
            task_str = f"{done_tasks}/{total_tasks} complete" if total_tasks else "0 tasks"
        else:
            task_str = "MISSING"
            
        print(f"{feat.name:<30} | {has_spec:<6} | {has_plan:<6} | {task_str:<18}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Spec-Kit CLI for Spec-Driven Development (SDD)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # init
    subparsers.add_parser("init", help="Initialize .specify/ and constitution.md")
    
    # specify
    spec_parser = subparsers.add_parser("specify", help="Scaffold a feature specification")
    spec_parser.add_argument("feature", help="Feature name (e.g. user-auth)")
    spec_parser.add_argument("--force", action="store_true", help="Overwrite if exists")
    
    # plan
    plan_parser = subparsers.add_parser("plan", help="Scaffold a technical plan")
    plan_parser.add_argument("feature", help="Feature name (e.g. user-auth)")
    plan_parser.add_argument("--force", action="store_true", help="Overwrite if exists")
    
    # tasks
    tasks_parser = subparsers.add_parser("tasks", help="Scaffold implementation tasks")
    tasks_parser.add_argument("feature", help="Feature name (e.g. user-auth)")
    tasks_parser.add_argument("--force", action="store_true", help="Overwrite if exists")
    
    # status
    subparsers.add_parser("status", help="Show status of all specifications and tasks")

    args = parser.parse_args()
    
    cmds = {
        "init": cmd_init,
        "specify": cmd_specify,
        "plan": cmd_plan,
        "tasks": cmd_tasks,
        "status": cmd_status
    }
    cmds[args.command](args)

if __name__ == "__main__":
    main()
