import unittest
from core import ROOT,extract,process,analytics
class Checks(unittest.TestCase):
 def test_clean_fields(self):
  fields,_=extract((ROOT/'samples/membership_0_clean.png').read_bytes())
  self.assertEqual(fields['Document ID'],'DEMO-MEMBERSHIP-000')
 def test_missing_field(self):
  fields,_=extract((ROOT/'samples/membership_0_missing_field.png').read_bytes()); self.assertFalse(fields['Document ID'])
 def test_invalid_image(self):
  r=process(b'invalid','invalid_test'); self.assertFalse(r['api_ok']); self.assertEqual(r['reason'],'ocr_error')
 def test_mode(self):
  with self.assertRaises(ValueError): extract(b'',mode='invalid')
 def test_metrics(self):
  self.assertGreater(analytics()['requests'],0)
if __name__=='__main__': unittest.main()
