from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]

SHARED_SKILL_DIRS = [root / "skills"]
TEMPLATE_SKILL_GLOB = root / "templates" / "*" / ".cursor" / "skills"

errors = []


def validate_skill_dir(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        errors.append(f"Missing SKILL.md: {skill_dir}")
        return

    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append(f"Missing frontmatter: {skill_file}")
        return

    frontmatter = text.split("---", 2)[1]
    if "name:" not in frontmatter:
        errors.append(f"Missing name frontmatter: {skill_file}")
    if "description:" not in frontmatter:
        errors.append(f"Missing description frontmatter: {skill_file}")


def collect_skill_dirs() -> list[Path]:
    skill_dirs: list[Path] = []

    for base in SHARED_SKILL_DIRS:
        if not base.exists():
            continue
        for skill_dir in sorted(base.iterdir()):
            if skill_dir.is_dir():
                skill_dirs.append(skill_dir)

    for template_skills in sorted(root.glob("templates/*/.cursor/skills")):
        for skill_dir in sorted(template_skills.iterdir()):
            if skill_dir.is_dir():
                skill_dirs.append(skill_dir)

    return skill_dirs


skill_dirs = collect_skill_dirs()

for skill_dir in skill_dirs:
    validate_skill_dir(skill_dir)

if errors:
    print("\n".join(errors))
    sys.exit(1)

print(f"All {len(skill_dirs)} skills are valid.")
