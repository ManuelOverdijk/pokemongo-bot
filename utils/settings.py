STEP_SIZE_METERS = 2
STEP_SIZE_POLAR = 0.000009 * STEP_SIZE_METERS  # roughly equal to 1 meter, in degrees lat/long

LOGIN_USER_AGENT = 'Niantic App'

PTC_LOGIN_URL = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
PTC_OAUTH_URL = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'
PTC_CLIENT_SECRET = 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR'
PTC_CLIENT_ID = 'mobile-app_pokemon-go'
PTC_CLIENT_REDIRECT_URI = 'https://www.nianticlabs.com/pokemongo/error'
PTC_TOKEN_MARKER = 'sso.pokemon.com'

API_USER_AGENT = 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ONEPLUS A3003 Build/MMB29M)'
API_INITIAL_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
API_OWN_URL = 'https://{0}/rpc'

MAX_POKEMON = 250
MAX_ITEMS = 350

## Set to True in order to activate human-like walking behaviour
PARANOID_MODE = False
