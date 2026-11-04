#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""keep_edits.py — 重新產生 HTML 之後，把老師在瀏覽器裡改的字（<script id="deck-edits">）搬回新檔。
用法：python3 keep_edits.py 舊的.html 新的.html
（把舊檔的 deck-edits 標籤複製到新檔 </body> 之前；新檔若已有就覆蓋。重建前先跑一次，修改就不會被蓋掉。）"""
import io, re, sys
if len(sys.argv) != 3:
    print(__doc__); sys.exit(1)
old, new = sys.argv[1], sys.argv[2]
o = io.open(old, encoding='utf-8').read()
m = re.search(r'<script id="deck-edits" type="application/json">.*?</script>\n?', o, re.S)
if not m:
    print('舊檔沒有 deck-edits，不用搬'); sys.exit(0)
tag = m.group(0)
n = io.open(new, encoding='utf-8').read()
n = re.sub(r'<script id="deck-edits" type="application/json">.*?</script>\n?', '', n, flags=re.S)
if '</body>' not in n:
    print('新檔找不到 </body>'); sys.exit(2)
n = n.replace('</body>', tag + '</body>', 1)
io.open(new, 'w', encoding='utf-8').write(n)
print('已把 deck-edits 搬到', new)
