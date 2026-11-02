"""Book OCR driver: render pages -> Windows OCR -> clean text."""
import pymupdf, os, sys, subprocess, shutil, time

BASE = r"\\Temp2657\Disk4_Tech\MY07_SKILLS\SKL15-书转技能"
BOOKS = os.path.join(BASE, "BOOKS")
WORK = os.path.join(BASE, "SkillFromBooks", "2026-10-24", "_ocr")
EXTRACT = os.path.join(BASE, "SkillFromBooks", "2026-10-24", "_extracted")

MAP = {
    "gckzl":  {"pdf": "工程控制论-钱学森.pdf", "text": False},
    "ryryc":  {"pdf": "人有人的用处.pdf", "text": False},
    "ryrcyt": {"pdf": "人有人的用处：控制论与社会 ([美]维纳) .pdf", "text": False},
    "dyzx":   {"pdf": "第一哲学沉思集.pdf", "text": True},
}

def render(pdf, outdir, dpi=300):
    os.makedirs(outdir, exist_ok=True)
    d = pymupdf.open(pdf)
    n = len(d)
    t0 = time.time()
    for i in range(n):
        fn = os.path.join(outdir, f"p{i+1:04d}.png")
        if os.path.exists(fn):
            continue
        d[i].get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY).save(fn)
        if (i + 1) % 50 == 0:
            print(f"  rendered {i+1}/{n} ({time.time()-t0:.0f}s)", flush=True)
    d.close()
    print(f"  render done: {n} pages in {time.time()-t0:.0f}s", flush=True)
    return n

def extract_text_layer(pdf, out_path):
    d = pymupdf.open(pdf)
    parts = []
    for i in range(len(d)):
        parts.append(f"===== PAGE p{i+1:04d} =====\n" + d[i].get_text())
    d.close()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"  text layer extracted: {len(d) if False else 'ok'}")

def run_ocr(imgdir, out_path):
    ps = os.path.join(WORK, "ocr_win.ps1")
    cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps,
           "-ImageDir", imgdir, "-OutFile", out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("  OCR stdout tail:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(empty)")
    if r.returncode != 0:
        print("  OCR STDERR:", r.stderr[:500])
        raise SystemExit(1)

def main():
    key = sys.argv[1]
    cfg = MAP[key]
    pdf = os.path.join(BOOKS, cfg["pdf"])
    imgdir = os.path.join(WORK, "img_" + key)
    raw = os.path.join(WORK, key + "_raw.txt")
    final = os.path.join(EXTRACT, cfg["pdf"] + ".txt")

    t0 = time.time()
    print(f"[{key}] start: {cfg['pdf']}", flush=True)

    if cfg["text"]:
        extract_text_layer(pdf, raw)
    else:
        render(pdf, imgdir)
        run_ocr(imgdir, raw)

    r = subprocess.run([sys.executable, os.path.join(WORK, "clean_text.py"), raw, final],
                       capture_output=True, text=True)
    print(" ", r.stdout.strip(), r.stderr.strip()[:300])

    if os.path.isdir(imgdir):
        shutil.rmtree(imgdir, ignore_errors=True)

    kb = os.path.getsize(final) / 1024
    print(f"[{key}] COMPLETE {time.time()-t0:.0f}s, {kb:.1f} KB -> {final}", flush=True)

if __name__ == "__main__":
    main()
