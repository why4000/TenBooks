import os, re, json

SK = r"C:\Users\Administrator\.trae-cn\skills"
EXPECT = {
    "rui-media-phenomenology", "li-first-principles", "meadows-systems-thinking",
    "campbell-hero-journey", "kelly-out-of-control", "mao-selected-works",
    "engineering-cybernetics", "meditations-on-first-philosophy",
    "human-use-of-human-beings", "ride-of-a-lifetime",
}
PRESERVE = {"avionics-tech-review", "git-commit", "security-best-practices", "spec-to-implementation"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

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

rows = []
errors = []
names_seen = {}

for d in sorted(os.listdir(SK)):
    p = os.path.join(SK, d)
    if not os.path.isdir(p):
        continue
    sp = os.path.join(p, "SKILL.md")
    if not os.path.exists(sp):
        if d in EXPECT:
            errors.append(f"{d}: SKILL.md 缺失")
        continue
    txt = open(sp, encoding="utf-8").read()
    fm = parse_fm(txt)
    if not fm:
        errors.append(f"{d}: frontmatter 无法解析")
        continue
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        errors.append(f"{d}: name 缺失")
    if not NAME_RE.match(name):
        errors.append(f"{d}: name '{name}' 不符合命名规范")
    if name != d:
        errors.append(f"{d}: name '{name}' 与目录名不一致")
    if name in names_seen:
        errors.append(f"{d}: name 与 {names_seen[name]} 重名")
    names_seen[name] = d
    if not desc or len(desc) < 30:
        errors.append(f"{d}: description 过短或缺失")

    # 引用校验
    refs = [r for r in re.findall(r"\]\(([^)]+)\)", txt) if not r.startswith("http")]
    missing = [r for r in refs if not os.path.exists(os.path.join(p, r.split("#")[0]))]
    if missing:
        errors.append(f"{d}: 引用失效 {missing}")

    # 附属文件
    ch = sorted(os.listdir(os.path.join(p, "chapters"))) if os.path.isdir(os.path.join(p, "chapters")) else []
    ch_cited = sorted(set(re.findall(r"chapters/([^\s|)]+\.md)", txt)))
    orphan = [c for c in ch if c not in ch_cited]
    rows.append({
        "dir": d, "name": name, "desc_len": len(desc),
        "chapters": len(ch), "cited": len(ch_cited), "orphan": orphan,
        "files": sum(len(f) for _, _, f in os.walk(p))
    })

print(f"{'目录':32s} {'章节':>4s} {'引用':>4s} {'文件':>4s}  description长度")
for r in rows:
    print(f"{r['dir']:32s} {r['chapters']:4d} {r['cited']:4d} {r['files']:4d}  {r['desc_len']}")

print("\n--- 结果 ---")
installed = set(os.listdir(SK))
print("预期 10 个:", "全部存在" if EXPECT <= installed else f"缺失 {EXPECT - installed}")
print("原有 4 个:", "完好" if PRESERVE <= installed else f"缺失 {PRESERVE - installed}")
print("目录总数:", len([d for d in installed if os.path.isdir(os.path.join(SK, d))]))
print("孤儿章节:", [(r['dir'], r['orphan']) for r in rows if r['orphan']] or "无")
print("错误:", errors if errors else "无")
