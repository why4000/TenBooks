import os, sys
from PIL import Image

def slice_dir(indir, outdir, chunk_h=2000, overlap=100):
    os.makedirs(outdir, exist_ok=True)
    for fn in sorted(os.listdir(indir)):
        if not fn.endswith(".png"):
            continue
        im = Image.open(os.path.join(indir, fn))
        w, h = im.size
        if h <= chunk_h:
            im.save(os.path.join(outdir, fn))
            continue
        base = fn[:-4]
        y = 0
        k = 0
        while y < h:
            k += 1
            box = (0, y, w, min(y + chunk_h, h))
            im.crop(box).save(os.path.join(outdir, f"{base}_s{k:02d}.png"))
            if y + chunk_h >= h:
                break
            y += chunk_h - overlap
        print(f"{fn}: {w}x{h} -> {k} chunks")

if __name__ == "__main__":
    slice_dir(sys.argv[1], sys.argv[2])
