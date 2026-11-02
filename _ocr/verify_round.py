import os, re, filecmp

SRC = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24\book-to-skill"
DST = r"C:\Users\Administrator\.trae-cn\skills"
PAIRS = [("gckzl", "engineering-cybernetics"), ("mzdxj", "mao-selected-works")]

def parse_fm(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    out = {}
    for line in text[3:end].strip().split("\n"):
        m = re.match(r"^([a-zA-Z_-]+)\s*:\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out

for slug, name in PAIRS:
    print("=" * 72)
    print(f"{slug}  ->  {name}")
    for label, base in (("源", os.path.join(SRC, slug)), ("安装", os.path.join(DST, name))):
        sp = os.path.join(base, "SKILL.md")
        txt = open(sp, encoding="utf-8").read()
        fm = parse_fm(txt)
        ch = sorted(os.listdir(os.path.join(base, "chapters")))
        cited = sorted(set(re.findall(r"chapters/([^\s|)]+\.md)", txt)))
        idx_rows = len(re.findall(r"\| \[ch\d\d\]", txt))
        refs = [r for r in re.findall(r"\]\(([^)]+)\)", txt) if not r.startswith("http")]
        missing_ref = [r for r in refs if not os.path.exists(os.path.join(base, r.split("#")[0]))]
        orphan = [c for c in ch if c not in cited]
        ph = re.findall(r"Temp2657|SkillFromBooks|C:\\\\Users|\{\{|TODO|PLACEHOLDER", txt)
        print(f"  [{label}] name={fm.get('name') if fm else '!!解析失败'} desc_len={len(fm.get('description','')) if fm else 0}")
        print(f"        章节文件={len(ch)}  索引行={idx_rows}  引用章节={len(cited)}")
        print(f"        孤儿={orphan if orphan else '无'}  失效引用={missing_ref if missing_ref else '无'}  占位符={ph if ph else '无'}")

    # 源与安装逐文件比对
    diffs = []
    for root, dirs, files in os.walk(os.path.join(SRC, slug)):
        rel = os.path.relpath(root, os.path.join(SRC, slug))
        for f in files:
            a = os.path.join(root, f)
            b = os.path.join(DST, name, rel, f)
            if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
                diffs.append(os.path.join(rel, f))
    print(f"  源↔安装 差异文件: {diffs if diffs else '无（完全同步）'}")

    # 各文件增量规模
    for fn in ["SKILL.md", "glossary.md", "patterns.md", "cheatsheet.md"]:
        p = os.path.join(SRC, slug, fn)
        print(f"    {fn:14s} {os.path.getsize(p)/1024:5.1f} KB")
