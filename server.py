from flask import Flask, request
from twitter import Twitter
from elks import Elks
import json

app = Flask(__name__)
elks_session = Elks()
twitter_session = Twitter()
twitter_authorized = False
authorized_numbers = []

@app.route('/')
def index():
    return 'Welcome to Passer, the self-hosted text-to-tweet service!'

@app.route('/incoming_sms', methods=['POST'])
def incoming_sms():
    incoming = json.loads(request.data.decode('utf-8'))
    message = elks_session.get_text_by_id(incoming['id'])
    if message:
        return message['message']
    else:
        return 'Failed posting tweet'

@app.route('/authorize')
def authorize_twitter():
    global twitter_session
    twitter_confirm_url = twitter_session.get_user_auth_url()
    if not twitter_confirm_url:
        return 'Could not initialize Twitter session'
    return 'Authorize Passer on\n%s' % twitter_confirm_url

@app.route('/authorize/<pin>')
def authorize_pin(pin):
    twitter_session.confirm_pin(pin)
    twitter_user = json.loads(twitter_session.verify_credentials())
    if 'screen_name' in twitter_user:
        twitter_authorized = True
        return 'Authorized as %s' % twitter_user['screen_name']
    else:
        return 'Could not authorize'

@app.route('/whoami')
def whoami():
    twitter_user = json.loads(twitter_session.verify_credentials())
    return 'Authorized as %s' % twitter_user['screen_name']

if __name__ == '__main__':
    print('Starting server...')
    app.debug = True
    app.run()
