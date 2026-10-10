import json
from core import ROOT,process,analytics,connect
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(); p.add_argument('--reset',action='store_true'); args=p.parse_args()
 if args.reset:
  with connect() as c: c.execute('DELETE FROM runs')
 for item in json.loads((ROOT/'manifest.json').read_text()):
  for mode in ('raw','threshold'):
   process((ROOT/'samples'/item['file']).read_bytes(),item['file'],item['kind'],item['condition'],mode,item['expected'])
 result=analytics(); (ROOT/'benchmark_results.json').write_text(json.dumps(result,indent=2)); print(json.dumps({k:v for k,v in result.items() if k!='recent'},indent=2))
