"""Gera ícones e tela de abertura Neovia para o projeto Android do Capacitor.
Uso: python3 tools/android_icons.py <pasta res do Android> <icon-512.png> <neovia-mark.png>"""
import sys, os, glob
from PIL import Image
res, icon, mark = sys.argv[1:4]
ic = Image.open(icon).convert('RGBA'); mk = Image.open(mark).convert('RGBA')
adaptive = os.path.join(res, 'mipmap-anydpi-v26')
if os.path.isdir(adaptive):
    for f in glob.glob(os.path.join(adaptive, '*')): os.remove(f)
    os.rmdir(adaptive)
for n, s in {'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}.items():
    d = os.path.join(res, 'mipmap-'+n); os.makedirs(d, exist_ok=True)
    for f in ('ic_launcher','ic_launcher_round','ic_launcher_foreground'):
        ic.resize((s, s), Image.LANCZOS).save(os.path.join(d, f+'.png'))
for f in glob.glob(os.path.join(res, 'drawable*', 'splash.png')):
    w, h = Image.open(f).size; s = min(w, h)//3
    bg = Image.new('RGBA', (w, h), (20, 20, 20, 255)); m = mk.copy(); m.thumbnail((s, s), Image.LANCZOS)
    bg.paste(m, ((w-m.width)//2, (h-m.height)//2), m); bg.convert('RGB').save(f)
print('ícones e splash gerados')
