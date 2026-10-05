"""Build the deployed site from the single-file WEBSITE.html.

Moves every embedded base64 product photo out into img/<id>.jpg so the page
itself is small and renders immediately; photos then load lazily.
Usage: python3 build.py /path/to/WEBSITE.html
"""
import base64, os, re, sys

src = open(sys.argv[1], encoding='utf-8').read()
os.makedirs('img', exist_ok=True)
for f in os.listdir('img'):
    os.remove(os.path.join('img', f))

def extract(m):
    key, ext, data = m.group(1), m.group(2), m.group(3)
    ext = 'jpg' if ext == 'jpeg' else ext
    with open(f'img/{key}.{ext}', 'wb') as fh:
        fh.write(base64.b64decode(data))
    return f'"{key}": "img/{key}.{ext}"'

out, n = re.subn(r'"([a-z0-9-]+)":\s*"data:image/(\w+);base64,([A-Za-z0-9+/=]+)"', extract, src)
open('index.html', 'w', encoding='utf-8').write(out)
print(f'{n} images extracted; index.html is {len(out.encode()) // 1024} KB')
