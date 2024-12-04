# Este arquivo contem a classe responsavel por obter respostas do facebook
#
#
#

from flask import request, jsonify
import hashlib
import hmac


class Ear:
    def __init__(self, app):
        self.app = app
        self.webhook_status = False
        self.data = None
        self.set_routes()

    def verify_signature(self, request):
        received_signature = request.headers.get('x-hub-signature-256')
        if not received_signature:
            return False

        payload = request.get_data()
        expected_signature = 'sha256=' + hmac.new(
            key=self.app.config['APP_SECRET'].encode(),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(received_signature, expected_signature)
    
    def set_routes(self):
        @self.app.route('/webhook', methods=['GET', 'POST'])
        def webhook():
            if request.method == 'GET':
                # Facebook webhook verification
                mode = request.args.get('hub.mode')
                token = request.args.get('hub.verify_token')
                challenge = request.args.get('hub.challenge')

                if mode and token:
                    if mode == 'subscribe' and token == self.app.config['VERIFICATION_TOKEN']:
                        self.webhook_status = True
                        return challenge, 200
                    else:
                        return 'Verification token mismatch', 403

            if request.method == 'POST':
                # Verify the request signature
                if not self.verify_signature(request):
                    status = "Invalid signature"
                    return jsonify({'status': 'error', 'message': 'Invalid signature'}), 403

                self.data = request.json 
                
                return jsonify({'status': 'success'}), 200