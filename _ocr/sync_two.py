import os, shutil

SRC = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24\book-to-skill"
DST = r"C:\Users\Administrator\.trae-cn\skills"
PAIRS = [("gckzl", "engineering-cybernetics"), ("mzdxj", "mao-selected-works")]

def sync(src, dst):
    os.makedirs(dst, exist_ok=True)
    # 删除 dest 中 source 没有的文件
    for root, dirs, files in os.walk(dst, topdown=False):
        rel = os.path.relpath(root, dst)
        sroot = os.path.join(src, rel) if rel != "." else src
        for f in files:
            if not os.path.exists(os.path.join(sroot, f)):
                os.remove(os.path.join(root, f))
                print("  removed extra:", os.path.join(rel, f))
    # 递归复制
    copied = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        droot = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(droot, exist_ok=True)
        for f in files:
            s = os.path.join(root, f)
            d = os.path.join(droot, f)
            shutil.copy2(s, d)
            copied += 1
    return copied

for slug, name in PAIRS:
    s = os.path.join(SRC, slug)
    d = os.path.join(DST, name)
    n = sync(s, d)
    print(f"SYNCED {slug} -> {name}: {n} files")
