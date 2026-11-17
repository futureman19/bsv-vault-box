import copy,json,pathlib,unittest
import consolidate as c
import check_package as p
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.man=json.loads((c.HERE/'upstream/candidate-manifest.json').read_bytes());cls.inputs=[json.loads(x.read_bytes()) for x in sorted((c.HERE/'inputs').glob('*.json'))]
    def test_roster(self):
        d=c.aggregate(self.man,self.inputs);self.assertEqual(d['coverage'],{'Country':195,'Ocean':5,'Moon':1});self.assertEqual(d['counts'],{'needs-user-review':73,'candidate-with-limitations':128})
    def test_duplicate_manifest_rejected(self):
        m=copy.deepcopy(self.man);m['items'].append(m['items'][0]);self.assertRaises(AssertionError,c.aggregate,m,self.inputs)
    def test_path_aliases_rejected(self):
        for path in ['a//b','a/./b','NUL','a/COM1.txt','a/trailing.']:
            self.assertRaises(ValueError,p.records,c.enc([{'path':path,'bytes':1}]))
    def test_duplicates_rejected(self):
        d=copy.deepcopy(self.inputs);d[0]['entries'].append(d[0]['entries'][0]);self.assertRaises(AssertionError,c.aggregate,self.man,d)
    def test_missing_id_rejected(self):
        d=copy.deepcopy(self.inputs);d[-1]['entries'].pop();self.assertRaises(AssertionError,c.aggregate,self.man,d)
    def test_changed_viewer_rejected(self):
        d=copy.deepcopy(self.inputs);d[0]['entries'][0]['viewer']['sha256']='0'*64;self.assertRaises(AssertionError,c.aggregate,self.man,d)
    def test_approval_rejected(self):
        d=copy.deepcopy(self.inputs);d[0]['entries'][0]['user_final_approved']=True;self.assertRaises(AssertionError,c.aggregate,self.man,d)
    def test_all_raw_reviews_preserved(self):
        d=c.aggregate(self.man,self.inputs);original={e['id']:e for b in self.inputs for e in b['entries']}
        for r in d['entries']:self.assertEqual(r['independent_review'],original[r['id']]);self.assertFalse(r['final_user_approved'])
    def test_known_holds_baseline(self):
        d={r['id']:r for r in c.aggregate(self.man,self.inputs)['entries']}
        for id in ['iceland','morocco','rwanda','united-states','bosnia-and-herzegovina']:self.assertEqual(d[id]['verdict'],'needs-user-review')
        self.assertIsNotNone(d['morocco']['last_approved_baseline']);self.assertIsNone(d['united-states']['last_approved_baseline'])
    def test_deterministic(self):self.assertEqual(c.enc(c.aggregate(self.man,self.inputs)),c.enc(c.aggregate(self.man,self.inputs)))
    def test_unsafe_paths(self):
        for path in ['../evil','/evil','C:/evil','a\\evil']:self.assertRaises(ValueError,p.records,c.enc([{'path':path,'bytes':1}]))
    def test_duplicate_paths(self):self.assertRaises(ValueError,p.records,c.enc([{'path':'a','bytes':1}]*2))
if __name__=='__main__':unittest.main(verbosity=2)
