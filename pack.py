#!/usr/bin/env python3
"""
Skill Packager - Validates and creates a distributable .zip file of a skill folder

Usage:
    python pack.py [path/to/skill-folder] [output-directory]
    python pack.py validate [path/to/skill-folder]

Example:
    python pack.py skills/idea2mvp
    python pack.py skills/idea2mvp ./dist
    python pack.py validate skills/idea2mvp
"""

import sys
import re
import zipfile
from pathlib import Path

def _parse_frontmatter(text):
    """Parse simple YAML frontmatter (key: value pairs) without external dependencies."""
    result = {}
    for line in text.splitlines():
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)', line)
        if not m:
            continue
        key = m.group(1)
        value = m.group(2).strip()
        # Strip surrounding quotes
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        result[key] = value
    return result


def validate_skill(skill_path):
    """Basic validation of a skill."""
    skill_path = Path(skill_path)

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = _parse_frontmatter(match.group(1))
    if not frontmatter:
        return False, "Frontmatter is empty or invalid"

    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    return True, "Skill is valid!"


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .zip file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .zip file (defaults to current directory)

    Returns:
        Path to the created .zip file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.zip"

    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .zip file: {e}")
        return None


def _resolve_skill_path():
    """Resolve skill path by auto-detecting from skills/ directory."""
    skills_root = Path.cwd() / "skills"
    if not skills_root.is_dir():
        print(f"❌ Error: skills directory not found: {skills_root}")
        sys.exit(1)
    subdirs = [d for d in skills_root.iterdir() if d.is_dir()]
    if not subdirs:
        print(f"❌ Error: No skill folders found in {skills_root}")
        sys.exit(1)
    elif len(subdirs) == 1:
        return subdirs[0]
    else:
        print("Found multiple skill folders:")
        for i, d in enumerate(subdirs, 1):
            print(f"  {i}. {d.name}")
        choice = input("Please select a skill folder (number): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(subdirs):
                return subdirs[idx]
            else:
                print("❌ Error: Invalid selection")
                sys.exit(1)
        except ValueError:
            print("❌ Error: Invalid input")
            sys.exit(1)


def main():
    # Handle "validate" subcommand
    if len(sys.argv) >= 2 and sys.argv[1] == "validate":
        skill_path = sys.argv[2] if len(sys.argv) > 2 else _resolve_skill_path()
        valid, message = validate_skill(skill_path)
        print(message)
        sys.exit(0 if valid else 1)

    # Package mode
    try:
        skill_path = sys.argv[1]
    except IndexError:
        skill_path = _resolve_skill_path()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
