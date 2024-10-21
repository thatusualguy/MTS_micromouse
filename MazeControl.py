import requests

from shared import baseUrl, token


class MazeControl(object):
    _base = "maze"

    @staticmethod
    def restart():
        url = baseUrl + MazeControl._base + '/' + "restart" + '?token=' + token
        print("restart")
        requests.post(url).json()
