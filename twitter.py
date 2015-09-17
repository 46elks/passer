from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qs
import os
import json

class Twitter:
    client_key = None
    client_secret = None
    oauth_token = None
    oauth_token_secret = None

    def __init__(self):
        if 'PASSER_TWITTER_KEY' in os.environ:
            self.client_key = os.environ['PASSER_TWITTER_KEY']
        if 'PASSER_TWITTER_SECRET' in os.environ:
            self.client_secret = os.environ['PASSER_TWITTER_SECRET']

    def make_session(self, data={}):
        if self.client_key and self.client_secret:
            if self.oauth_token:
                data['resource_owner_key'] = self.oauth_token
                if self.oauth_token_secret:
                    data['resource_owner_secret'] = self.oauth_token_secret
            return OAuth1Session(self.client_key,
                                 client_secret=self.client_secret,
                                 **data)
        else:
            return None

    def twitter_request_helper(self, target, data={}, request_type='POST'):
        twitbase = 'https://api.twitter.com'
        session = self.make_session(data=data)
        if not session:
            return {}
        url = '%s/%s' % (twitbase, target)
        if request_type == 'POST':
            result = session.post(url)
        elif request_type == 'GET':
            result = session.get(url)
        return result.text

    def get_request_token(self):
        result = parse_qs(self.twitter_request_helper('/oauth/request_token',
                {'callback_uri': 'oob'}))
        if ('oauth_callback_confirmed' in result and
            'true' in result['oauth_callback_confirmed']):
            self.oauth_token = result['oauth_token'][0]
            self.oauth_token_secret = result['oauth_token_secret'][0]
        else:
            return False
        return True

    def get_user_auth_url(self):
        if not self.oauth_token:
            if not self.get_request_token():
                return False
        login_url = 'https://api.twitter.com/oauth/authenticate?oauth_token=%s'
        login_url = login_url % self.oauth_token
        return login_url

    def confirm_pin(self, pin):
        result = parse_qs(self.twitter_request_helper('/oauth/access_token',
                 data={'verifier': pin}))
        self.oauth_token = result['oauth_token'][0]
        self.oauth_token_secret = result['oauth_token_secret'][0]

    def verify_credentials(self):
        return self.twitter_request_helper(
              '/1.1/account/verify_credentials.json',
              request_type='GET')

    def post_tweet(self, content):
        tweet = {
                    'status': content
                }
        tweet = json.dumps(tweet)
        return self.twitter_request_helper(
                '/1.1/statuses/update',
                data=tweet
                )

