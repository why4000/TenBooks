import os, re, shutil, filecmp

SRC = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24\book-to-skill"
DST = r"C:\Users\Administrator\.trae-cn\skills"
PAIRS = [("ryryc", "human-use-of-human-beings")]


def sync(src, dst):
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(dst, topdown=False):
        rel = os.path.relpath(root, dst)
        sroot = os.path.join(src, rel) if rel != "." else src
        for f in files:
            if not os.path.exists(os.path.join(sroot, f)):
                os.remove(os.path.join(root, f))
                print("  removed extra:", os.path.join(rel, f))
    copied = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        droot = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(droot, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(droot, f))
            copied += 1
    return copied


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
    n = sync(os.path.join(SRC, slug), os.path.join(DST, name))
    print("=" * 72)
    print(f"SYNCED {slug} -> {name}: {n} files")
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
        print("  [%s] name=%s desc_len=%d" % (label, fm.get("name") if fm else "!!解析失败", len(fm.get("description", "")) if fm else 0))
        print("        章节文件=%d  索引行=%d  引用章节=%d" % (len(ch), idx_rows, len(cited)))
        print("        孤儿=%s  失效引用=%s  占位符=%s" % (orphan or "无", missing_ref or "无", ph or "无"))

    diffs = []
    for root, dirs, files in os.walk(os.path.join(SRC, slug)):
        rel = os.path.relpath(root, os.path.join(SRC, slug))
        for f in files:
            a = os.path.join(root, f)
            b = os.path.join(DST, name, rel, f)
            if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
                diffs.append(os.path.join(rel, f))
    print("  源↔安装 差异文件: %s" % (diffs or "无（完全同步）"))
    for fn in ["SKILL.md", "glossary.md", "patterns.md", "cheatsheet.md"]:
        p = os.path.join(SRC, slug, fn)
        print("    %-14s %5.1f KB" % (fn, os.path.getsize(p) / 1024))
