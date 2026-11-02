import os, json, re

BASE = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24"

BOOKS = [
    {"slug": "ljml", "title": "理解媒介：从对象到现象", "author": "芮必峰", "type": "媒介/哲学"},
    {"slug": "dyxyly", "title": "第一性原理", "author": "李善友", "type": "思维/创新"},
    {"slug": "xtzm", "title": "系统之美", "author": "德内拉·梅多斯", "type": "系统思考"},
    {"slug": "qmyx", "title": "千面英雄", "author": "约瑟夫·坎贝尔", "type": "神话/原型"},
    {"slug": "sk", "title": "失控", "author": "凯文·凯利", "type": "复杂系统"},
    {"slug": "mzdxj", "title": "毛泽东选集", "author": "毛泽东", "type": "哲学/战略"},
    {"slug": "gckzl", "title": "工程控制论", "author": "钱学森", "type": "控制论/工程"},
    {"slug": "dyzx", "title": "第一哲学沉思集", "author": "笛卡尔", "type": "哲学/认识论"},
    {"slug": "ryryc", "title": "人有人的用处：控制论与社会", "author": "N. 维纳", "type": "控制论/社会"},
    {"slug": "ysdlc", "title": "一生的旅程", "author": "罗伯特·艾格", "type": "领导力/传记"},
]

def read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def extract_frontmatter_desc(text):
    m = re.search(r"description:\s*(.+)", text)
    return m.group(1).strip() if m else ""

def parse_skill_md(text):
    frameworks = []
    lines = text.split("\n")
    cur = None
    for line in lines:
        if line.startswith("### "):
            if cur:
                frameworks.append(cur)
            name = line[4:].strip()
            cur = {"name": name, "desc": "", "use_when": ""}
        elif cur and line.startswith("- **Use when**"):
            cur["use_when"] = line.replace("- **Use when**", "").strip()
        elif cur and line.strip().startswith("- **Key insight**"):
            cur["desc"] = line.split("**Key insight**:", 1)[-1].strip()
        elif cur and not line.startswith("#") and line.strip() and not cur["desc"]:
            if "**Key insight**" not in line and "Use when" not in line:
                pass
    if cur:
        frameworks.append(cur)
    # fallback: get all ### headings
    headings = [l[4:].strip() for l in lines if l.startswith("### ")]
    if not frameworks:
        frameworks = [{"name": h, "desc": "", "use_when": ""} for h in headings]
    return frameworks, headings

def parse_chapter_md(text):
    lines = text.split("\n")
    title = ""
    core = ""
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
        if line.startswith("## Core Idea") or line.startswith("## 核心思想"):
            # get next non-empty line
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip() and not lines[j].startswith("#"):
                    core = lines[j].strip()
                    break
    return {"title": title, "core": core}

def parse_glossary(text):
    terms = []
    for line in text.split("\n"):
        m = re.match(r"\*\*(.+?)\*\*\s*[—\-]\s*(.+)", line.strip())
        if m:
            terms.append({"term": m.group(1), "def": m.group(2)})
    return terms

def parse_patterns(text):
    patterns = []
    cur = None
    for line in text.split("\n"):
        if line.startswith("## Pattern"):
            if cur:
                patterns.append(cur)
            cur = {"name": line.split(":", 1)[-1].strip(), "when": "", "how": []}
        elif cur and "**When to use**" in line:
            cur["when"] = line.split("**When to use**:", 1)[-1].strip()
    if cur:
        patterns.append(cur)
    return patterns

def parse_verified_yaml(text):
    caps = []
    cur = {}
    in_cap = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("- capability_id:"):
            if cur:
                caps.append(cur)
            cur = {"capability_id": s.split(":", 1)[1].strip()}
        elif cur and s.startswith("one_liner:"):
            cur["one_liner"] = s.split(":", 1)[1].strip()
        elif cur and s.startswith("importance:"):
            cur["importance"] = s.split(":", 1)[1].strip()
        elif cur and s.startswith("intents:"):
            cur["intents"] = []
        elif cur and s.startswith("- ") and "intents" in cur:
            cur.setdefault("intents", []).append(s[2:].strip())
        elif cur and s.startswith("keywords:"):
            m = re.search(r"\[(.+?)\]", s)
            if m:
                cur["keywords"] = [k.strip() for k in m.group(1).split(",")]
        elif cur and s.startswith("description:"):
            cur["description"] = s.split(":", 1)[1].strip()
        elif cur and s.startswith("destination:"):
            cur["destination"] = s.split(":", 1)[1].strip()
    if cur:
        caps.append(cur)
    return caps

data = {"books": []}

for book in BOOKS:
    slug = book["slug"]
    bts = os.path.join(BASE, "book-to-skill", slug)
    cjs = os.path.join(BASE, "cangjie-skill", slug)
    
    skill_text = read(os.path.join(bts, "SKILL.md"))
    frameworks, headings = parse_skill_md(skill_text)
    
    # chapters
    chapters = []
    ch_dir = os.path.join(bts, "chapters")
    if os.path.isdir(ch_dir):
        for fn in sorted(os.listdir(ch_dir)):
            if fn.endswith(".md"):
                ct = read(os.path.join(ch_dir, fn))
                ch = parse_chapter_md(ct)
                ch["file"] = fn
                ch["content"] = ct[:3000]
                chapters.append(ch)
    
    glossary = parse_glossary(read(os.path.join(bts, "glossary.md")))
    patterns = parse_patterns(read(os.path.join(bts, "patterns.md")))
    
    # cangjie
    vy = read(os.path.join(cjs, ".cangjie", "capabilities", "verified.yaml"))
    capabilities = parse_verified_yaml(vy)
    
    book_data = {
        **book,
        "frameworks": frameworks,
        "framework_headings": headings,
        "chapters": chapters,
        "glossary": glossary,
        "patterns": patterns,
        "capabilities": capabilities,
        "skill_text": skill_text[:5000],
    }
    data["books"].append(book_data)

# write as JS variable
out = os.path.join(BASE, "app", "js", "data.js")
with open(out, "w", encoding="utf-8") as f:
    f.write("window.SKILL_DATA = ")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.write(";")

print(f"Generated data.js with {len(data['books'])} books")
for b in data["books"]:
    print(f"  {b['slug']}: {len(b['frameworks'])} frameworks, {len(b['chapters'])} chapters, {len(b['capabilities'])} capabilities")
