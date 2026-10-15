#!/usr/bin/env python3
"""Stage only public static assets for the optional GitHub Actions workflow."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_site'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
for name in ['index.html','.nojekyll','css','js','assets','config','docs']:
    src=ROOT/name
    if src.is_dir():shutil.copytree(src,OUT/name)
    else:shutil.copy2(src,OUT/name)
print('Staged public static files in _site/')
