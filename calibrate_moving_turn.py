import requests

from shared import real_robotId, real_baseUrl


def move(l_pwm, l_time, r_pwm, r_time):
    data = {"id":real_robotId, "l": int(l_pwm), "r":int(r_pwm), "l_time":int(l_time), "r_time":int(r_time)}
    url = real_baseUrl + '/' + "motor"
    print(data)
    requests.put(url, json = data)

if __name__ == '__main__':

    print("Начало")

    while True:
        time = int(input("Time. 500?"))
        l_pwm, r_pwm = map(int, input("Мощность L R. 255 120?").strip().split())
        move(l_pwm, 500, r_pwm, 500)


