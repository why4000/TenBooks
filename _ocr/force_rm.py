import os, sys

def force_rmtree(root):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                os.remove(fp)
            except OSError as e:
                print("  file fail:", fp, e)
        for d in dirnames:
            dp = os.path.join(dirpath, d)
            try:
                os.rmdir(dp)
            except OSError as e:
                print("  dir fail:", dp, e)
    try:
        os.rmdir(root)
        print("OK", root)
    except OSError as e:
        # show what remains
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                print("  remains:", os.path.join(dirpath, f))
        print("FAIL", root, e)

for p in sys.argv[1:]:
    if os.path.isdir(p):
        force_rmtree(p)
