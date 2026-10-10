import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
root=Path(__file__).resolve().parent; dest=root/'samples'; dest.mkdir(exist_ok=True)
# Pillow ships a portable default font; no platform-specific path required.
font=ImageFont.load_default(size=30); records=[]
for kind in ('membership','employee','student'):
 for i in range(4):
  expected={'Name':f'Alex Demo {i}','Document ID':f'DEMO-{kind.upper()}-{i:03}','Date of Birth':f'200{i}-03-15'}
  for condition in ('clean','blurred','low_contrast','missing_field'):
   im=Image.new('RGB',(1100,440),'white'); d=ImageDraw.Draw(im)
   ink=(205,205,205) if condition=='low_contrast' else (0,0,0)
   d.text((35,25),f'FICTIONAL {kind.upper()} CARD - NOT VALID ID',font=font,fill=ink)
   for j,(key,value) in enumerate(expected.items()):
    if condition=='missing_field' and key=='Document ID': continue
    d.text((35,110+j*70),f'{key}: {value}',font=font,fill=ink)
   if condition=='blurred': im=im.filter(ImageFilter.GaussianBlur(3))
   filename=f'{kind}_{i}_{condition}.png'; im.save(dest/filename)
   records.append(dict(file=filename,kind=kind,condition=condition,expected=expected))
(root/'manifest.json').write_text(json.dumps(records,indent=2)); print(f'Generated {len(records)} fictional documents')
