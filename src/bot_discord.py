from bs4 import BeautifulSoup
import config
import json
import requests


def simplified():
    infos = dict(sorted(
        json.loads(formatted()).items(),
        key = lambda user: user[1]['rate'],
        reverse=True
    ))
    msg   = []

    for user in infos.keys():
        info = infos[user]
        msg += [ f"{user:11s} : {info['tier']:9s} ({info['percentage']:02d}%) {info['solved']:3d}" ]

    return '\n'.join(msg)


def formatted():
    with open("res/users.json", "r") as f: users = json.load(f)

    msg = {}
    for m in users['ADMINs'] + users['MEMBERs']:
        info    = {}
        url     = f'{config.URL_API}?boj={m}'
        text    = requests.get(url).text

        soup                = BeautifulSoup(text, 'html.parser')
        info['tier']        = soup.select_one('svg > text.tier-text').get_text()
        info['rate']        = int(soup.select_one('svg > g:nth-child(6) > text.rate.value').get_text().replace(',', ''))
        info['solved']      = int(soup.select_one('svg > g:nth-child(7) > text.solved.value').get_text())
        info['class']       = soup.select_one('svg > g:nth-child(8) > text.class.value').get_text()
        info['percentage']  = int(soup.select_one('svg > text.percentage').get_text()[ : -1 ])
        msg[m] = info

    return json.dumps(msg, indent=4)


def run():
    return simplified()


if __name__ == "__main__":
    print(run())
