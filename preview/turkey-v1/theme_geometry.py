# Included by setup.py into the standalone author.py.
ceramic=mat('Iznik / ivory floral glaze',(.78,.74,.63),.27)
maptex(ceramic,'ceramic-color.png','Base Color');maptex(ceramic,'ceramic-roughness.png','Roughness',True)
blue=mat('Iznik / cobalt glaze',(.012,.05,.22),.24);maptex(blue,'cobalt-roughness.png','Roughness',True)
ivory=mat('Iznik / ivory inset',(.79,.76,.65),.3)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
red=mat('Iznik / tomato red relief',(.54,.031,.019),.3)
green=mat('Iznik / turquoise foliage',(.014,.22,.17),.32)
seam=mat('Seam / deep cobalt',(.008,.018,.05),.7)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(ivory if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ceramic / front' if sy<0 else 'Ceramic / rear',(0,sy*1.145,.83),(3.26,.19,1.46),ceramic,bevel=.014)
for sx in [-1,1]:cube('Ceramic / side',(sx*1.745,0,.83),(.23,2.48,1.46),ceramic,bevel=.014)
cube('Ceramic / clasp seat',(0,-1.255,1.36),(.56,.075,.47),blue,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ceramic / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),blue,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),blue,lid,.045)
cube('Ornament / ivory panel',(0,0,1.989),(3.20,1.86,.038),ivory,lid,.015)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Cobalt / foot',(sx*1.47,sy*.91,-.075),(.49,.43,.30),blue,bevel=.07)
