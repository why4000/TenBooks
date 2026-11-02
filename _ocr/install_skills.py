import os, shutil

SRC = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能\SkillFromBooks\2026-10-24\book-to-skill"
DST = r"C:\Users\Administrator\.trae-cn\skills"

MAP = {
    "ljml":   "rui-media-phenomenology",
    "dyxyly": "li-first-principles",
    "xtzm":   "meadows-systems-thinking",
    "qmyx":   "campbell-hero-journey",
    "sk":     "kelly-out-of-control",
    "mzdxj":  "mao-selected-works",
    "gckzl":  "engineering-cybernetics",
    "dyzx":   "meditations-on-first-philosophy",
    "ryryc":  "human-use-of-human-beings",
    "ysdlc":  "ride-of-a-lifetime",
}
SKIP = ["ryrcyt"]

def copytree(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d)
        else:
            shutil.copy2(s, d)

for slug, name in MAP.items():
    src = os.path.join(SRC, slug)
    dst = os.path.join(DST, name)
    if os.path.exists(dst):
        print(f"SKIP-EXISTS {name}")
        continue
    copytree(src, dst)
    n = sum(len(f) for _, _, f in os.walk(dst))
    print(f"OK {slug:8s} -> {name:32s} ({n} files)")

print("\nSKIPPED:", SKIP)
print("Installed dirs:", sorted(os.listdir(DST)))
