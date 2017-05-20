import config
from ._LivestreamSource import LivestreamSource


class Twitch(LivestreamSource):
    def __init__(self):
        account = config.readJson('accounts.json')
        settings = config.readJson('settings.json')

        parameters = []
        request_headers = {}

        if 'api_key' in account and 'twitch' in account['api_key']:
            request_headers = {'Client-ID': account['api_key']['twitch']}

        if 'games' in settings['sidebar']['livestreams']:
            games = self.convertGames(settings['sidebar']['livestreams']['games'])['Twitch']
            # NOTE: This doesn't work! Twitch API is dumb and won't accept arrays, so this is temporary!
            parameters += ['game=' + game for game in games]
            parameters += ['limit=' + str(settings['sidebar']['livestreams']['max_shown'] * 2)]

        # Turn parameters list into a stringified URL parameter chain
        # e.g. &game=CSGO&limit=5&channel=Jpon9,RedditGlobalOffensive,vooCSGO
        parameters = '?' + '&'.join(parameters) if len(parameters) > 0 else ''

        # Variables to be used in the rest of the object, mainly inherited funcs
        self.name = 'Twitch'
        self.api_url = 'https://api.twitch.tv/kraken/streams/' + parameters
        self.streams_field = 'streams'
        self.request_headers = request_headers

    def convertStream(self, stream):
        # Twitch API sometimes doesn't have the channel status. I dunno why.
        if 'status' not in stream['channel']:
            return None
        return {
            'streamer': stream['channel']['display_name'],
            'title': self.prepareTitle(stream['channel']['status']),
            'url': stream['channel']['url'],
            'viewers_raw': int(stream['viewers']),
            'viewers': '{:,}'.format(int(stream['viewers'])),
            'thumbnail': stream['preview']['template'].replace('{width}', '45').replace('{height}', '30'),
            'language': stream['channel']['language']
        }
