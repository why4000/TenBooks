import pymupdf, os, sys, shutil

def render(pdf, outdir, dpi=300, max_pages=None):
    os.makedirs(outdir, exist_ok=True)
    d = pymupdf.open(pdf)
    n = len(d)
    if max_pages:
        n = min(n, max_pages)
    for i in range(n):
        fn = os.path.join(outdir, f"p{i+1:04d}.png")
        if os.path.exists(fn):
            continue
        page = d[i]
        pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
        pix.save(fn)
        if (i + 1) % 25 == 0:
            print(f"  rendered {i+1}/{n}", flush=True)
    d.close()
    print(f"RENDER_DONE {outdir} {n}", flush=True)
    return n

if __name__ == "__main__":
    pdf = sys.argv[1]
    outdir = sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    maxp = int(sys.argv[4]) if len(sys.argv) > 4 else None
    render(pdf, outdir, dpi, maxp)
