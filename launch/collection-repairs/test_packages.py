import unittest,tempfile,zipfile,json
from pathlib import Path
from unittest.mock import patch
from package_repairs import safe_names,recover,archive,encode,manifest,sha,old_inventory
class Checks(unittest.TestCase):
 def test_paths(self):
  for names in [['../x'],['/x'],['a\\b'],['a//b'],['a/./b'],['CON.txt'],['x.'],['X','x'],['a','a']]:
   with self.subTest(names=names),self.assertRaises(AssertionError):safe_names(names)
 def test_recovery_and_mutations(self):
  for mode in ['valid','corrupt','extra','missing','bad-required','wrong-trust','duplicate']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as d:
    root=Path(d);files={'a.html':b'html','a.blend':b'source','a.glb':b'model'}
    inv=encode({'required':list(files) if mode!='bad-required' else ['a.html'],'files':manifest(files)})
    if mode=='corrupt':files['a.glb']=b'changed'
    if mode=='extra':files['extra']=b'x'
    if mode=='missing':del files['a.blend']
    files['inventory.json']=inv;path=root/'a.zip';archive(files,path)
    if mode=='duplicate':
     with zipfile.ZipFile(path,'a') as z:z.writestr('A.HTML',b'alias')
    def run():
     with patch('socket.socket',side_effect=AssertionError('network forbidden')),patch('subprocess.Popen',side_effect=AssertionError('process forbidden')):
      return recover(path,'0'*64 if mode=='wrong-trust' else sha(inv),root/'recovered')
    if mode=='valid':self.assertTrue(run()['readback'])
    else:
     with self.assertRaises(AssertionError):run()
 def test_inventory_schemas(self):
  for content in [{'a':{'sha256':sha(b'a'),'bytes':1}},{'files':[{'path':'a','sha256':sha(b'a'),'bytes':1}]}]:
   self.assertEqual(old_inventory({'a':b'a','inventory.json':encode(content)})['entries_checked'],1)
  with self.assertRaises(AssertionError):old_inventory({'a':b'b','inventory.json':encode({'a':{'sha256':sha(b'a')}})})
if __name__=='__main__':unittest.main(verbosity=2)
