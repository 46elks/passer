# passer -- self-hosted sms to tweet

Passer is a proof-of-concept self-hosted SMS to Tweet server.

## Security Notice

**The Passer microapplication is made for demonstrational purposes only and
opens up your Twitter account so that anyone can send tweets from your
account as it doesn't authenticate the incoming SMSes. Please use as a
reference only and do not try to deploy to production.**

## Installation

From zsh or bash starting in the Passer directory

1. Setup a Virtualenv in the Passer directory using `virtualenv -p python3 env`
and activate the virtualenv environment using `. env/bin/activate` then
install the dependencies for Passer with 
`pip install -r requirements.txt`
1. Create a Twitter application on [apps.twitter.com](https://apps.twitter.com/)
and extract your Twitter consumer key and and consumer secret from the
_Keys and Access Tokens_ tab and export 
your Twitter API keys to the environment using
`export PASSER_TWITTER_KEY=<consumer key>` and
`export PASSER_TWITTER_SECRET=<consumer secret>`
1. Log in/create an account on 46elks [46elks](https://www.46elks.com/) and
extract your API username and secret from the 46elks dashboard
and export your 46elks API keys to the environment using
`export PASSER_ELKS_KEY=<api username>` and
`export PASSER_ELKS_SECRET=<api secret>`
1. Update the `authorized_numbers` array in `server.py` so that you can use your
number
1. Start Passer using `python server.py`
1. Go to `<url>/authorize` to authorize your twitter account
and then to `<url>/authorize/<key>` to finish the authorization
1. Buy a 46elks virtual number and set it's SMS URL to `<url>/incoming_sms`

It is also made to be useful with Heroku :)

