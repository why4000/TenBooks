import os, re, sys, json

BASE = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24\book-to-skill"

def parse_fm(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end].strip()
    d = {}
    for line in fm.split("\n"):
        m = re.match(r"^([a-zA-Z_]+)\s*:\s*(.*)$", line)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return d

for name in sorted(os.listdir(BASE)):
    d = os.path.join(BASE, name, )
    if not os.path.isdir(d):
        continue
    sp = os.path.join(d, "SKILL.md")
    print("=" * 70)
    print("DIR:", name)
    if not os.path.exists(sp):
        print("  !! NO SKILL.md, files:", os.listdir(d))
        continue
    txt = open(sp, encoding="utf-8").read()
    fm = parse_fm(txt)
    print("  name:", fm.get("name") if fm else "!! INVALID FRONTMATTER")
    print("  desc len:", len(fm.get("description", "")) if fm else 0)
    files = sorted(os.listdir(d))
    sub = sorted(os.listdir(os.path.join(d, "chapters"))) if os.path.isdir(os.path.join(d, "chapters")) else []
    print("  files:", files)
    print("  chapters/:", sub)
    # referenced links in SKILL.md
    refs = re.findall(r"\]\(([^)]+)\)", txt)
    refs = [r for r in refs if not r.startswith("http")]
    missing = []
    for r in refs:
        p = os.path.join(d, r.split("#")[0])
        if not os.path.exists(p):
            missing.append(r)
    print("  refs:", refs)
    if missing:
        print("  !! MISSING REFS:", missing)
    # check chapters cited by name in Chapter Index table
    cited = re.findall(r"chapters/([^\s|)]+)", txt)
    print("  cited chapter files:", cited)
    for c in cited:
        if not os.path.exists(os.path.join(d, "chapters", c)):
            print("  !! CITED CHAPTER MISSING:", c)
