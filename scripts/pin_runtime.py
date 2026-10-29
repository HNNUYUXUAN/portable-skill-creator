"""Maintainer operation: retrieve immutable release metadata, never credentials."""
import json, urllib.request
from pathlib import Path
url = 'https://github.com/astral-sh/uv/releases/download/0.13.6/uv-x86_64-pc-windows-msvc.zip'
checksum = urllib.request.urlopen(url+'.sha256', timeout=30).read().decode().split()[0]
assert len(checksum)==64 and all(c in '0123456789abcdef' for c in checksum)
pin = {'uv_version': '0.13.6', 'url': url, 'sha256': checksum, 'python': '3.12.14'}
p = Path(__file__).resolve().parents[1] / 'assets' / 'runtime.json'
p.parent.mkdir(exist_ok=True)
p.write_text(json.dumps(pin, indent=2)+'\n', encoding='utf-8')
print(json.dumps(pin))
