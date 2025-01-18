from authlib.integrations.flask_client import OAuth
from flask import Flask

# Initialize OAuth
oauth = OAuth()
google = oauth.register(
    'google',
    client_id='84497968223-sq4jgsb2gu8tlgpqavlb8n0gc395ir5v.apps.googleusercontent.com',
    client_secret='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',
    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',

)

# Flask app will initialize OAuth during app setup
def init_oauth(app):
    oauth.init_app(app)