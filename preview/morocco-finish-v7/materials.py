from pathlib import Path
from PIL import Image,ImageEnhance,ImageFilter,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parent
im=Image.open(R/'references/primary.png').convert('RGB')
def rect(points,size):
 w,h=size;A=[];B=[]
 for (x,y),(u,v) in zip([(0,0),(w,0),(w,h),(0,h)],points):A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
 return im.transform(size,Image.Transform.PERSPECTIVE,np.linalg.solve(A,B),Image.Resampling.BICUBIC)
edge=rect([(418,513),(892,414),(890,468),(420,579)],(800,100));edge.save(R/'references/wood-rectified.png')
wood=edge.crop((25,12,275,65));wood.save(R/'references/wood-source-swatch.png')
# Single observed rosette plus interlocking neighbors; no brass, terrain, or central wood.
lid=rect([(138,383),(572,300),(894,389),(415,500)],(1000,760));lid.save(R/'references/lid-rectified.png')
source=lid.crop((405,606,605,718));source.save(R/'references/tile-source-swatch.png')
# Recover three stable pigment classes from the actual photographed motif;
# this removes low-order lighting instead of embedding the entire lid photo.
a=np.asarray(source,dtype=float);lum=a.mean(2);green=(a[:,:,1]-a[:,:,0]>2)&(a[:,:,1]>a[:,:,2]*1.07)
# Dark pigment has priority over green hue: shaded black accents also have a green bias.
dark=lum<88
cream=(lum>125)&~green&~dark
labels=np.where(dark,0,np.where(cream,2,np.where(green,1,0)))
labels=np.asarray(Image.fromarray(labels.astype('uint8')).filter(ImageFilter.MedianFilter(3)))
palette=np.array([[8,12,10],[12,64,39],[202,193,160]],dtype=np.uint8)
tile=Image.fromarray(palette[labels]);tile.save(R/'maps/tile-repeat.png')
# Mirrored grain exemplars avoid invented uniform stripes and wrap seams.
w=np.asarray(wood,dtype=float);low=np.asarray(wood.filter(ImageFilter.GaussianBlur(9)),dtype=float)
w=np.clip(np.array([91,65,46])+(w-low)*1.1+(low-low.mean((0,1)))*.35,0,255).astype('uint8')
w=np.concatenate([w,w[:,::-1]],axis=1)
Image.fromarray(w).resize((1024,128),Image.Resampling.LANCZOS).save(R/'maps/cedar-edge.jpg',quality=94,subsampling=0,optimize=True)
# Entire lid projection atlas: only narrow ceramic border samples this map.
W,H=1024,768;xx,yy=np.meshgrid(np.linspace(-1.785,1.785,W),np.linspace(1.33,-1.33,H))
d=np.stack([yy+1.33,1.785-xx,1.33-yy,xx+1.785]);face=d.argmin(0);dist=d.min(0)
# Integer repeats at each inset contour. Adjacent miter sides meet at phase zero.
s=np.choose(face,[xx+1.785,yy+1.33,1.785-xx,1.33-yy])
length=np.choose(face,[3.57,2.66,3.57,2.66]); repeats=np.choose(face,[6,4,6,4])
u=np.mod((s-dist)/np.maximum(length-2*dist,.01)*repeats,1);v=np.clip(dist/.36,0,1)
# Mirror the repeat coordinate so its endpoints share identical source pixels.
u=1-np.abs(2*u-1)
atlas=palette[labels[np.minimum((v*111).astype(int),111),np.minimum((u*199).astype(int),199)]]
Image.fromarray(atlas).save(R/'maps/ceramic-atlas.png',optimize=True)
(R/'material-provenance.json').write_text(json.dumps({'body_linear_factor':.90,'body_RGB_and_UV_bytes':'preserved exactly','wood_source_rectified_crop':[25,12,275,65],'wood_finish_target_srgb':[91,65,46],'wood_detail_gain':1.1,'tile_source_rectified_crop':[405,606,605,718],'tile_pigment_palette':palette.tolist(),'tile_repeats_per_edge':[6,4,6,4],'dark_priority_luminance':88,'cream_min_luminance':125,'tile_border_width':.36,'method':'Primary-art extracted motif classified into three pigments to remove lighting. Mirrored source wood grain with cooler lower saturation brown. Dark-first pigment classification with median-3 edge cleanup. No complete lid photo pasted. Hidden border repeats extrapolated; inset-contour integer repeats and mirrored phase-matched miter sampling.'},indent=2))
board=Image.new('RGB',(1000,460),'#222222');board.paste(source.resize((600,336)),(0,25));board.paste(wood.resize((660,128)),(0,330));ImageDraw.Draw(board).text((10,5),'ACTUAL PRIMARY: rectified rosette and cedar source patches',fill='white');board.save(R/'references/source-swatch-board.png')
