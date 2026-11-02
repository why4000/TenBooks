import re, sys, os

CJK = r"\u4e00-\u9fff\u3400-\u4dbf"

def clean(text):
    lines = text.split("\n")
    out = []
    for ln in lines:
        if ln.startswith("====="):
            out.append(ln)
            continue
        s = ln
        # 去掉 CJK 字符之间的空格（Windows OCR 会在每个汉字间插空格）
        prev = None
        while prev != s:
            prev = s
            s = re.sub(r"([" + CJK + r"]) +([" + CJK + r"])", r"\1\2", s)
        # 中文与标点之间空格
        s = re.sub(r"([" + CJK + r"]) +([，。、；：？！“”‘’（）《》〈〉—…·])", r"\1\2", s)
        s = re.sub(r"([，。、；：？！“”‘’（）《》〈〉—…·]) +([" + CJK + r"])", r"\1\2", s)
        # 中文与数字/字母之间保留单空格，但压缩多空格
        s = re.sub(r"  +", " ", s).strip()
        out.append(s)
    # 合并被 OCR 拆行的段落：若行尾非句末标点且下一行非标题，则拼接
    result = []
    for ln in out:
        if ln.startswith("====="):
            result.append(ln)
            continue
        if not ln:
            result.append("")
            continue
        if result and result[-1] and not result[-1].startswith("====="):
            last = result[-1]
            if last[-1] not in "。！？；：”』》）…" and not re.match(r"^第[一二三四五六七八九十百]+[章节]", ln) and not re.match(r"^\d+[\.·、]", ln):
                if len(last) > 12 and not last.endswith("-"):
                    result[-1] = last + ln
                    continue
        result.append(ln)
    return "\n".join(result)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        raw = f.read()
    txt = clean(raw)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"CLEANED -> {dst} ({len(txt)} chars)")
