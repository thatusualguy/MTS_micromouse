import requests

from MouseCommand import MouseCommands
from shared import real_baseUrl, real_robotId

if __name__ == "__main__":
    left = 120
    right = 120
    left_time = 500
    right_time = 500
    data = {"id":real_robotId, "l": int(left), "r":int(right), "l_rime":left_time, "r_rime":right_time}
    url = real_baseUrl + '/' + "motor"
    print(requests.put(url, json = data).text)