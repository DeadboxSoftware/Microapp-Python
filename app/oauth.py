from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config('.env')
oauth = OAuth(config)
discord = oauth.register(
    name='discord',
    client_id=config('DISCORD_CLIENT_ID'),
    client_secret=config('DISCORD_CLIENT_SECRET'),
    authorize_url='https://discord.com/api/oauth2/authorize',
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_params=None,
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=config('DISCORD_REDIRECT_URI'),
    client_kwargs={'scope': 'identify email'},
    jwks_uri='https://discord.com/.well-known/jwks.json'
)