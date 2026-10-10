"""Local demo HTTP API. Bind to loopback; not a production server."""
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,parse_qs
from core import ROOT,process,analytics
class Handler(BaseHTTPRequestHandler):
 def send(self,status,data,kind='application/json'):
  body=json.dumps(data).encode() if kind=='application/json' else data
  self.send_response(status); self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
 def do_GET(self):
  path=urlparse(self.path).path
  if path=='/api/analytics': self.send(200,analytics())
  elif path=='/health': self.send(200,{'status':'ok'})
  elif path=='/': self.send(200,(ROOT/'dashboard.html').read_bytes(),'text/html; charset=utf-8')
  else: self.send(404,{'error':'Not found'})
 def do_POST(self):
  url=urlparse(self.path)
  if url.path!='/api/verify': return self.send(404,{'error':'Not found'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=5000000: return self.send(413,{'error':'Provide an image up to 5 MB'})
   mode=parse_qs(url.query).get('mode',['raw'])[0]
   if mode not in ('raw','threshold'): return self.send(400,{'error':'Invalid mode'})
   result=process(self.rfile.read(length),'upload',mode=mode)
   self.send(200 if result['api_ok'] else 422,result)
  except (ValueError,OSError): self.send(400,{'error':'Invalid request'})
if __name__=='__main__':
 print('VerifyLens: http://127.0.0.1:8000'); HTTPServer(('127.0.0.1',8000),Handler).serve_forever()
