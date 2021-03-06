from flask import Flask, request
from twitter import Twitter
from elks import Elks
from urllib.parse import parse_qs
import json

app = Flask(__name__)
elks_session = Elks()
twitter_session = Twitter()
twitter_authorized = False
authorized_numbers = ['+46709784966']

@app.route('/')
def index():
    return 'Welcome to Passer, the self-hosted text-to-tweet service!'

@app.route('/incoming_sms', methods=['POST'])
def incoming_sms():
    try:
        if not twitter_authorized:
            return 'Authorize for Twitter'
        incoming = request.form['id'].strip()
        message = elks_session.get_text_by_id(incoming)
        if message and message['from'] in authorized_numbers:
            twitter_session.post_tweet(message['message'])
            return ''
        else:
            return 'Failed posting tweet'
    except:
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
