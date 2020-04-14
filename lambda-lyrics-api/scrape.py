import json
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse

start = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"
end = "<!-- MxM banner -->"
baseurl = "https://www.azlyrics.com"

from make_response import make_response


def scrape(event, context):
    """
    Event of type
        {
            "path": "/lyrics/artist/song.html"
        }
    """
    body = urlparse.parse_qs(event.get('body'))
    path = body.get('path', None)[0]

    if path == None or "lyrics" not in path:
        return make_response(400, event)

    r = requests.get(baseurl + path)
    if r.status_code != 200:
        return make_response(400, 'bad path {}'.format(path))


    s = r.text
    a, b = s.find(start), s.find(end)
    lyric_part = s[a+len(start):b]

    soup = BeautifulSoup(lyric_part, 'html.parser')
    lyrics = soup.get_text().strip()

    return make_response(200, {
            "lyrics": lyrics
        })

if __name__ == "__main__":
    from pprint import pprint
    event = {
        'body': "path=%2Flyrics%2Fgreenday%2Famericanidiot.html"
    }
    pprint(json.loads(scrape(event, None).get('body')))

