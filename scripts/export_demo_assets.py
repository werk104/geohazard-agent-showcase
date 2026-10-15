#!/usr/bin/env python3
"""Export exact-data visualizations for this showcase. Never run during Pages builds.
Usage: python scripts/export_demo_assets.py --source /path/to/the/four/tiffs
Requires numpy, Pillow, rasterio. Does not modify inputs or prediction masks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
RED=np.array([247,58,70],dtype=np.float32)
ALPHA=0.55
GAMMA=1.15

def write_image(path,array):
    image=Image.fromarray(array.astype(np.uint8))
    if path.suffix=='.webp':image.save(path,lossless=True,method=6)
    else:image.save(path,optimize=True)

def valid(a,nodata):
    ok=np.isfinite(a)
    if nodata is not None:ok &= a!=nodata
    return np.all(ok,axis=0)

def rgb_stretch(rgb,ok,limits):
    out=np.zeros(rgb.shape,np.float32)
    for band,(lo,hi) in enumerate(limits):out[band]=np.clip((rgb[band]-lo)/(hi-lo),0,1)**(1/GAMMA)
    out=np.rint(np.moveaxis(out,0,-1)*255).astype(np.uint8)
    out[~ok]=[16,43,59]
    return out

def align_rgb(rgb,src,target,nodata):
    dest=np.full((3,target.height,target.width),-9999,dtype=np.float32)
    for i in range(3):
        reproject(source=rgb[i],destination=dest[i],src_transform=src.transform,src_crs=src.crs,
                  dst_transform=target.transform,dst_crs=target.crs,src_nodata=nodata,dst_nodata=-9999,
                  resampling=Resampling.bilinear)
    return dest,valid(dest,-9999)

def overlay(rgb,foreground):
    out=rgb.copy()
    out[foreground]=np.rint(rgb[foreground].astype(np.float64)*(1-ALPHA)+RED.astype(np.float64)*ALPHA).astype(np.uint8)
    assert np.array_equal(out[~foreground],rgb[~foreground])
    return out

def mask_read(ds):
    m=ds.read(1,masked=True)
    values=set(np.unique(m.compressed()).tolist())
    if not values.issubset({0,1}):raise ValueError(f'Expected 0/1 mask, got {values}')
    return np.ma.filled(m==1,False)

def same_grid(a,b):return a.crs==b.crs and a.shape==b.shape and a.transform.almost_equals(b.transform)

def summary(path,ds):
    return {'name':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':ds.width,'height':ds.height,'bands':ds.count,'dtype':ds.dtypes[0],'pixelSize':[float(v) for v in ds.res]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);args=ap.parse_args()
    out=ROOT/'assets/images';out.mkdir(parents=True,exist_ok=True)
    source=args.source
    files=[source/x for x in ['滑坡识别示例.tif','滑坡识别示例_结果.tif','裂缝识别示例.tif','裂缝识别示例_结果.tif']]
    report={'purpose':'Static visualizations of user-provided rasters; no inference or accuracy evaluation.','sources':[],'processing':{}}
    with rasterio.open(files[0]) as image,rasterio.open(files[1]) as mask:
        if image.count!=26:raise ValueError('Landslide input must have 26 bands')
        if image.crs is None or mask.crs is None:raise ValueError('Missing CRS')
        pre=image.read([3,2,1]);post=image.read([15,14,13])
        ok_pre=valid(pre,image.nodata);ok_post=valid(post,image.nodata)
        limits=[]
        for i in range(3):
            values=np.concatenate([pre[i][ok_pre],post[i][ok_post]])
            lo,hi=np.percentile(values,[2,98]);limits.append([float(lo),float(hi)])
        # Retain input grid for the PRE/POST comparison. Do not invent finer satellite detail.
        pre_native=rgb_stretch(pre,ok_pre,limits);post_native=rgb_stretch(post,ok_post,limits)
        write_image(out/'landslide-pre-native.webp',pre_native)
        write_image(out/'landslide-post-native.webp',post_native)
        # Warp the RGB only onto the prediction's georeferenced grid; retain every mask pixel.
        pre_aligned,valid_pre=align_rgb(pre,image,mask,image.nodata)
        post_aligned,valid_post=align_rgb(post,image,mask,image.nodata)
        pre_rgb=rgb_stretch(pre_aligned,valid_pre,limits);post_rgb=rgb_stretch(post_aligned,valid_post,limits)
        foreground=mask_read(mask);display_foreground=foreground&valid_post
        over=overlay(post_rgb,display_foreground)
        write_image(out/'landslide-input.webp',post_rgb)
        write_image(out/'landslide-overlay.webp',over)
        write_image(out/'landslide-mask.png',foreground.astype(np.uint8)*255)
        # Contact sheet contains the original 399x327 views, without upscaling.
        pad=18;head=52;foot=40
        canvas=Image.new('RGB',(2*image.width+3*pad,image.height+head+foot),(16,43,59))
        draw=ImageDraw.Draw(canvas)
        try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
        except OSError:font=ImageFont.load_default()
        draw.text((pad,17),'PRE / TRUE COLOR',font=font,fill=(185,229,214))
        draw.text((2*pad+image.width,17),'POST / TRUE COLOR',font=font,fill=(185,229,214))
        canvas.paste(Image.fromarray(pre_native),(pad,head));canvas.paste(Image.fromarray(post_native),(2*pad+image.width,head))
        draw.text((pad,head+image.height+12),'B4 / B3 / B2  |  Shared 2-98% stretch  |  Input grid: 10 m',font=font,fill=(173,194,200))
        canvas.save(out/'temporal-inputs.webp',lossless=True,method=6)
        report['sources'] += [summary(files[0],image),summary(files[1],mask)]
        report['processing']['landslide']={
            'mappingBasis':'User supplied 26-band order; TIFF has no band descriptions.',
            'preRGBChannelsOneBased':[3,2,1],'postRGBChannelsOneBased':[15,14,13],
            'sharedRGBPercentileLimits':limits,'percentiles':[2,98],'displayGamma':GAMMA,
            'sameOriginalGrid':same_grid(image,mask),'sourceCRSEqualsResultCRS':image.crs==mask.crs,
            'alignment':'RGB bilinear warp to result grid; prediction mask was not resampled, dilated, eroded, or edited.',
            'resultForegroundPixels':int(foreground.sum()),'foregroundOutsideValidRGB':int((foreground&~valid_post).sum()),
            'imageValidPixelsOnResultGrid':int(valid_post.sum()),'overlayAlpha':ALPHA,
            'maskOutput':'0 -> black, 1 -> white; 255 in preview is foreground display intensity, not source nodata.',
            'exportShape':[mask.height,mask.width]}
    with rasterio.open(files[2]) as image,rasterio.open(files[3]) as mask:
        if image.count!=3:raise ValueError('Crack input must be RGB')
        if not same_grid(image,mask):raise ValueError('Crack source/result need explicit alignment before export')
        rgb=np.moveaxis(image.read([1,2,3]),0,-1)
        foreground=mask_read(mask)
        over=overlay(rgb,foreground)
        write_image(out/'crack-input.webp',rgb);write_image(out/'crack-overlay.webp',over)
        write_image(out/'crack-mask.png',foreground.astype(np.uint8)*255)
        report['sources'] += [summary(files[2],image),summary(files[3],mask)]
        report['processing']['crack']={'sameOriginalGrid':True,'rgbProcessing':'Original uint8 RGB, no contrast stretch or resampling.',
            'resultForegroundPixels':int(foreground.sum()),'overlayAlpha':ALPHA,'exportShape':[mask.height,mask.width]}
    report['processing']['allExports']='New PNG/WebP images without georeferencing, EXIF, or original TIFF metadata; source rasters remain unchanged.'
    (ROOT/'assets/DEMO_PROCESSING.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Exported real RGB, masks, temporal pair, and pixel-registered overlays.')
    print(json.dumps({k:{x:y for x,y in v.items() if x in ['sameOriginalGrid','resultForegroundPixels','foregroundOutsideValidRGB','exportShape']} for k,v in report['processing'].items() if isinstance(v,dict)},ensure_ascii=False))
if __name__=='__main__':main()
