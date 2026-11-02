import json,struct,math
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parent

def load(path):
 b=Path(path).read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n]),b[28+n:]
def view(j,b,i):
 v=j['bufferViews'][i];return b[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]
def accessor(j,b,i):
 a=j['accessors'][i];v=j['bufferViews'][a['bufferView']];d={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];n={'VEC3':3,'VEC2':2,'SCALAR':1,'VEC4':4}[a['type']];return np.ndarray((a['count'],n),dtype=d,buffer=b,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',np.dtype(d).itemsize*n),np.dtype(d).itemsize)).copy()
def uv(x,y,z,rear=False):
 u=.5+np.arctan2(np.asarray(x)/1.86,-np.asarray(y)/1.44)/(2*np.pi)
 if rear:u=np.where(u<.5,u+1,u)
 return np.stack([u,(np.asarray(z)-.04)/1.60],axis=-1)
def save(j,b,path):
 b=bytes(b);b+=b'\0'*((-len(b))%4);j['buffers'][0]['byteLength']=len(b);s=json.dumps(j,separators=(',',':')).encode();s+=b' '*((-len(s))%4);Path(path).write_bytes(struct.pack('<III',0x46546c67,2,28+len(s)+len(b))+struct.pack('<II',len(s),0x4e4f534a)+s+struct.pack('<II',len(b),0x004e4942)+b)
