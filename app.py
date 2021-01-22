#!/usr/bin/env python

import http.server, json, logging, os, socketserver
from subprocess import check_output
from retrying import retry

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

port = int(os.environ.get('PORT', 8080))
interface = os.environ.get('INTERFACE', 'hci0')

@retry(stop_max_delay=30000)
def readBeewiSensor(s_hci, s_mac) :
   logging.info('Reading %s', s_mac)
   raw_input = check_output(['gatttool', '-i', s_hci, '-b', s_mac, '--char-read', '--handle=0x003f'], timeout=10);
   octet_list  = raw_input.decode('utf-8').split(':')[1].strip().split(' ')

   temperature = int(octet_list[2] + octet_list[1], 16)
   if (temperature > 0x8000):
      temperature = temperature - 0x10000
   temperature = temperature / 10.0

   return {
      'temperature': temperature,
      'humidity': int(octet_list[4], 16),
      'battery': int(octet_list[9], 16)
   }

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/favicon.ico'):
            return

        mac = self.path.split('?')[0][1:]

        try:
            data = readBeewiSensor(interface, mac)

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data), 'utf8'))
        except Exception as inst:
             self.send_response(500)
             self.send_header('Content-type','text/html')
             self.end_headers()
             self.wfile.write(bytes(str(inst), 'utf8'))
             logging.exception('Error')

httpd = socketserver.TCPServer(('', port), Handler)
try:
   httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
