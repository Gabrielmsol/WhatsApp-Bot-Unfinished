# Neste arquivo cabe uma classe responsavel por enviar mensagens ao whats app
#
#
import json
import requests

class Mouth:
    def __init__(self, app):
        self.app = app
        self.RECIPIENT_WAID = None
    
    def to_talk(self, RECIPIENT_WAID):
        self.RECIPIENT_WAID = RECIPIENT_WAID
    
    
    def send_default_message(self):

        url = f"https://graph.facebook.com/{self.app.config['VERSION']}/{self.app.config['PHONE_NUMBER_ID']}/messages"
        headers = {
            "Authorization": "Bearer " + self.app.config['ACCESS_TOKEN'],
            "Content-Type": "application/json",
        }
        data = {
            "messaging_product": "whatsapp",
            "to": self.RECIPIENT_WAID,
            "type": "template",
            "template": {"name": "hello_world", "language": {"code": "en_US"}},
        }
        response = requests.post(url, headers=headers, json=data)
        return response
    
    def get_text_message_input(self, text):
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.RECIPIENT_WAID,
                "type": "text",
                "text": {"preview_url": False, "body": text},
            }
        )
    
    def send_message(self, text):
        data = self.get_text_message_input(text)

        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.app.config['ACCESS_TOKEN']}",
        }

        url = f"https://graph.facebook.com/{self.app.config['VERSION']}/{self.app.config['PHONE_NUMBER_ID']}/messages"

        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            print("Status:", response.status_code)
            print("Content-type:", response.headers["content-type"])
            print("Body:", response.text)
            return response
        else:
            print(response.status_code)
            print(response.text)
            return response