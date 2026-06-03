from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
skills_dir = root / "skills"

errors = []

for skill_dir in sorted(skills_dir.iterdir()):
    if not skill_dir.is_dir():
        continue
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        errors.append(f"Missing SKILL.md: {skill_dir}")
        continue
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append(f"Missing frontmatter: {skill_file}")
    if "name:" not in text.split("---", 2)[1]:
        errors.append(f"Missing name frontmatter: {skill_file}")
    if "description:" not in text.split("---", 2)[1]:
        errors.append(f"Missing description frontmatter: {skill_file}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("All skills are valid.")
