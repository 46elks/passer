from flask import Flask, request
from twitter import Twitter
import json

app = Flask(__name__)
twitter_session = None
twitter_authorized = False
authorized_numbers = []

@app.route('/')
def index():
    return ''

@app.route('/incoming_sms', methods=['POST'])
def incoming_sms():
    incoming = request.get_json()
    print(incoming)

@app.route('/blergh')
def blergh():
    return 'BLEEERGH!'

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

if __name__ == '__main__':
    twitter_session = Twitter()
    print('Starting server...')
    app.run()
