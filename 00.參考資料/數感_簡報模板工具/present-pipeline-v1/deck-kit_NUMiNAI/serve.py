#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
serve.py — 年度主管會議簡報的「本機小伺服器」

用途：讓簡報在瀏覽器裡按「儲存」時，直接把修改寫回同一個 .html 檔，
     不用跳任何檔案視窗。

使用：
    python3 serve.py            # 啟動，印出網址
    python3 serve.py --open     # 啟動並自動開瀏覽器（開資料夾裡最新的 .html；--file xxx.html 指定）
    python3 serve.py --port 8765

只綁 127.0.0.1（別台電腦連不到），Python 3 標準庫，不用裝任何套件。
Ctrl+C 或關掉終端機視窗就停。
"""

import argparse
import io
import re
import datetime
import json
import mimetypes
import os
import posixpath
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ── 設定 ──────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_OVERRIDE = None                 # --file 指定
def _default_index():
    """預設開哪一份：--file 指定的；否則資料夾裡最新修改的 .html（不含 _ 開頭與隱藏檔）。"""
    if INDEX_OVERRIDE:
        return INDEX_OVERRIDE
    cands = [f for f in os.listdir(ROOT) if f.lower().endswith('.html') and not f.startswith(('.', '_'))]
    if not cands:
        return 'index.html'
    cands.sort(key=lambda f: os.path.getmtime(os.path.join(ROOT, f)), reverse=True)
    return cands[0]
BACKUP_DIR = os.path.join(ROOT, 'backups')
BACKUP_KEEP = 20
PORT_START = 8765
PORT_END = 8775
MAX_BODY = 64 * 1024 * 1024          # 64MB 上限，避免誤傳巨檔

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.htm': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.mjs': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.mp3': 'audio/mpeg',
    '.txt': 'text/plain; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8',
}


class SafeName(Exception):
    """檔名不合法。"""


def resolve_target(raw):
    """把 ?file= 的值轉成「這個資料夾裡的某個 .html」的絕對路徑。

    只接受本資料夾內、不含路徑分隔、副檔名為 .html 的單純檔名。
    """
    if not raw:
        raise SafeName('缺少 file 參數')
    name = urllib.parse.unquote(raw)
    if '\x00' in name:
        raise SafeName('檔名含非法字元')
    if os.path.isabs(name) or name.startswith('~'):
        raise SafeName('不接受絕對路徑')
    if '/' in name or '\\' in name:
        raise SafeName('不接受路徑，只能是本資料夾內的檔名')
    if name in ('.', '..') or name.startswith('.'):
        raise SafeName('不接受隱藏檔或相對路徑')
    if not name.lower().endswith('.html'):
        raise SafeName('只能寫入 .html 檔')

    target = os.path.realpath(os.path.join(ROOT, name))
    root_real = os.path.realpath(ROOT)
    if os.path.dirname(target) != root_real:
        raise SafeName('目標不在簡報資料夾內')
    return target


def make_backup(target):
    """把舊檔備份到 backups/<name>_<YYYYMMDD-HHMMSS>.html，只留最近 BACKUP_KEEP 份。"""
    if not os.path.exists(target):
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    base = os.path.basename(target)
    stem, ext = os.path.splitext(base)
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    # 同一秒內連按多次儲存 → 加序號。序號取「這一秒已有的最大值 + 1」，
    # 不能只看檔案在不在（舊的可能已被清掉，重用會讓新備份被誤判成最舊）。
    prefix = '%s_%s' % (stem, stamp)
    seq = -1
    try:
        for f in os.listdir(BACKUP_DIR):
            if f.startswith(prefix) and f.endswith(ext):
                seq = max(seq, _backup_order(stem, ext, f)[1])
    except OSError:
        pass
    if seq < 0:
        dest = os.path.join(BACKUP_DIR, '%s%s' % (prefix, ext))
    else:
        dest = os.path.join(BACKUP_DIR, '%s-%d%s' % (prefix, seq + 1, ext))
    shutil.copy2(target, dest)
    prune_backups(stem, ext)
    return dest


def _backup_order(stem, ext, fname):
    """從檔名 <stem>_<YYYYMMDD-HHMMSS>[-N]<ext> 取出排序用的 (時間, 序號)。"""
    mid = fname[len(stem) + 1:len(fname) - len(ext)]      # YYYYMMDD-HHMMSS[-N]
    parts = mid.split('-')
    stamp = '-'.join(parts[:2])
    try:
        seq = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        seq = 0
    return (stamp, seq)


def prune_backups(stem, ext):
    """只留最近 BACKUP_KEEP 份。"""
    try:
        items = [f for f in os.listdir(BACKUP_DIR)
                 if f.startswith(stem + '_') and f.endswith(ext)]
    except OSError:
        return
    items.sort(key=lambda f: _backup_order(stem, ext, f))
    for old in items[:-BACKUP_KEEP]:
        try:
            os.remove(os.path.join(BACKUP_DIR, old))
        except OSError:
            pass


def atomic_write(target, data):
    """先寫暫存檔再 rename，避免寫到一半斷電留下半份檔案。"""
    fd, tmp = tempfile.mkstemp(prefix='.save-', suffix='.tmp', dir=ROOT)
    try:
        with os.fdopen(fd, 'wb') as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        if os.path.exists(target):                 # 保留原本的權限
            shutil.copymode(target, tmp)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class Handler(SimpleHTTPRequestHandler):
    server_version = 'DeckServe/1.0'
    extensions_map = dict(MIME)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    # ── MIME ──
    def guess_type(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext in MIME:
            return MIME[ext]
        t = mimetypes.guess_type(path)[0]
        return t or 'application/octet-stream'

    # ── 每個回應都不快取，改完不會看到舊版 ──
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    # ── GET ──
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ('/__alive', '/__alive/'):
            self.send_json(200, {'ok': True, 'serve': 'deck', 'root': ROOT})
            return
        if path in ('/__build', '/__build/'):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            name = (q.get('file') or [_default_index()])[0]
            self.send_json(200, {'ok': True, 'build': _build_stamp(os.path.join(ROOT, os.path.basename(name)))})
            return
        if path in ('', '/'):
            self.path = '/' + urllib.parse.quote(_default_index())
        super().do_GET()

    def do_HEAD(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ('', '/'):
            self.path = '/' + urllib.parse.quote(_default_index())
        super().do_HEAD()

    # ── POST /save?file=xxx.html ──
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if posixpath.normpath(parsed.path) != '/save':
            self.send_json(404, {'ok': False, 'error': '只支援 POST /save'})
            return

        qs = urllib.parse.parse_qs(parsed.query)
        raw = (qs.get('file') or [''])[0]
        try:
            target = resolve_target(raw)
        except SafeName as e:
            self.send_json(400, {'ok': False, 'error': str(e)})
            return

        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            length = 0
        if length <= 0:
            self.send_json(400, {'ok': False, 'error': '沒有內容（Content-Length 是 0）'})
            return
        if length > MAX_BODY:
            self.send_json(413, {'ok': False, 'error': '內容太大'})
            return

        try:
            data = self.rfile.read(length)
        except Exception as e:
            self.send_json(400, {'ok': False, 'error': '讀取內容失敗：%s' % e})
            return
        if len(data) != length:
            self.send_json(400, {'ok': False, 'error': '內容不完整'})
            return
        try:
            data.decode('utf-8')
        except UnicodeDecodeError:
            self.send_json(400, {'ok': False, 'error': '內容不是 UTF-8'})
            return

        # 分頁載入的版本比磁碟上的舊（AI 已重建）→ 拒絕，免得把新版面蓋掉；修改仍留在瀏覽器（localStorage）
        try:
            mine = _build_stamp(data.decode('utf-8')[:8192])
            disk = _build_stamp(target) if os.path.exists(target) else ''
        except Exception:
            mine, disk = '', ''
        if mine and disk and mine != disk:
            self.send_json(409, {'ok': False, 'stale': True, 'error': '這個檔案已經被重建過（你的分頁是舊版），請重新整理後再儲存；你改的字會留在這台電腦。'})
            return

        try:
            backup = make_backup(target)
            atomic_write(target, data)
        except Exception as e:
            self.send_json(500, {'ok': False, 'error': '寫檔失敗：%s' % e})
            return

        now = datetime.datetime.now()
        sys.stderr.write('[save] %s  %d bytes  %s\n' % (
            os.path.basename(target), len(data),
            ('備份 ' + os.path.basename(backup)) if backup else '（原本沒有這個檔）'))
        self.send_json(200, {
            'ok': True,
            'bytes': len(data),
            'saved': now.strftime('%H:%M'),
            'file': os.path.basename(target),
            'backup': os.path.basename(backup) if backup else None,
        })

    def log_message(self, fmt, *args):
        sys.stderr.write('%s - %s\n' % (self.log_date_time_string(), fmt % args))


def bind(port_start, port_end):
    last = None
    for port in range(port_start, port_end + 1):
        try:
            httpd = HTTPServer(('127.0.0.1', port), Handler)
            return httpd, port
        except OSError as e:
            last = e
            continue
    raise SystemExit('連接埠 %d–%d 都被占用了，請先關掉其他伺服器。(%s)'
                     % (port_start, port_end, last))


_STAMP_RE = re.compile(r'<meta name="deck-build" content="([^"]*)"')
def _build_stamp(path_or_text):
    """HTML 裡的 build 戳記（<meta name="deck-build">）；沒有就回空字串。"""
    try:
        txt = path_or_text if '<' in path_or_text[:4096] else io.open(path_or_text, encoding='utf-8').read(8192)
    except Exception:
        return ''
    m = _STAMP_RE.search(txt)
    return m.group(1) if m else ''


def main():
    ap = argparse.ArgumentParser(description='簡報本機伺服器（可直接存檔）')
    ap.add_argument('--port', type=int, default=PORT_START, help='起始連接埠（預設 8765）')
    ap.add_argument('--open', action='store_true', help='啟動後自動開瀏覽器')
    ap.add_argument('--file', help='要開的 html 檔名（預設：資料夾裡最新的 .html）')
    args = ap.parse_args()
    global INDEX_OVERRIDE
    INDEX_OVERRIDE = args.file

    httpd, port = bind(args.port, max(args.port, PORT_END))
    url = 'http://127.0.0.1:%d/%s' % (port, urllib.parse.quote(_default_index()))

    print('簡報伺服器已啟動')
    print('  資料夾：%s' % ROOT)
    print('  連接埠：%d' % port)
    print('  網址　：%s' % url)
    print('  停止　：按 Ctrl+C，或直接關掉這個視窗')
    sys.stdout.flush()

    if args.open:
        try:
            subprocess.Popen(['open', url])
        except Exception as e:
            print('（自動開啟瀏覽器失敗，請手動貼上網址：%s）' % e)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n已停止。')
    finally:
        httpd.server_close()


if __name__ == '__main__':
    main()
