import logging
from time import sleep

import config
from config import FWD_WAIT_TIME
from motors import pwm
from sensors import get_encoders, get_sensors, get_sensors_raw


def forward(dist_cells):


    for i in range(dist_cells):
        pwm(100, 300, 100, 300)
        sleep(0.300)
        pwm(-255, 20, -255, 20)


    #
    # if dist_cells > config.FWD_MAX_DIST:
    #     dist1 = dist_cells // config.FWD_MAX_DIST
    #     dist1_times = dist_cells // dist1
    #     dist2 = dist_cells % dist1
    #
    #     for i in range(dist1_times):
    #         forward(dist1)
    #     forward(dist2)


    pass

import time
from typing import Callable

# Константы
MAXSPEED = 100  # Максимальная скорость
ENCODERONECEIL = 237  # Тики энкодера на одну клетку
ROTATETIME = 1000  # Время поворота в мс


def forward_first(cell_count: int,) -> None:
    """
    Функция движения вперед на заданное количество клеток

    Args:
        cell_count: количество клеток для движения
        get_sensors: функция получения данных с сенсоров
        move: функция управления моторами
        logger: функция для логирования (по умолчанию print)
    """
    # Параметры корректировки
    K_P = 0.3  # Пропорциональный коэффициент
    MAX_CORRECTION = 20.0  # Максимальная корректировка мощности

    # Получаем начальные показания сенсоров
    get_sensors_raw("all")
    max_speed = float(MAXSPEED)
    # Делим желаемое расстояние на 3, чтобы компенсировать разницу в масштабе
    total_distance = float(cell_count) * ENCODERONECEIL
    sum_distance = 0.0

    # Параметры движения
    acceleration_dist = total_distance * 0.2  # Участок разгона
    deceleration_dist = total_distance - acceleration_dist  # Начало торможения
    min_speed = max_speed * 0.3
    previous_left = 0
    previous_right = 0

    while sum_distance <= total_distance:
        # Получаем текущие показания энкодеров
        sensors = get_encoders()
        left_delta = sensors["left"] - previous_left
        right_delta = sensors["right"] - previous_right

        # Сохраняем текущие значения для следующей итерации
        previous_left = sensors["left"]
        previous_right = sensors["right"]
        delta = float(abs(left_delta + right_delta)) / 2
        sum_distance += delta

        # Рассчитываем текущую скорость на основе пройденного расстояния
        if sum_distance <= acceleration_dist:
            # Фаза ускорения
            progress = sum_distance / acceleration_dist
            current_speed = min_speed + (max_speed - min_speed) * progress
        elif sum_distance >= deceleration_dist:
            # Фаза торможения
            progress = (total_distance - sum_distance) / (total_distance - deceleration_dist)
            current_speed = min_speed + (max_speed - min_speed) * progress
            if total_distance - sum_distance < 0.1 * ENCODERONECEIL:
                current_speed = min_speed / 2
        else:
            # Фаза крейсерской скорости
            current_speed = max_speed

        # Корректируем скорость если есть отклонение от желаемой
        encoder_diff = float(left_delta - right_delta)
        correction = K_P * encoder_diff

        # Ограничиваем максимальную корректировку
        correction = max(-MAX_CORRECTION, min(MAX_CORRECTION, correction))

        # Применяем корректировку к левому и правому мотору
        left_speed = int(current_speed - correction)
        right_speed = int(current_speed + correction)

        # Убеждаемся, что скорости не превышают допустимые значения
        left_speed = max(-MAXSPEED, min(MAXSPEED, left_speed))
        right_speed = max(-MAXSPEED, min(MAXSPEED, right_speed))

        pwm(left_speed, ROTATETIME, right_speed, ROTATETIME)

        # Логирование
        logging.info(f"Position: {sum_distance/ENCODERONECEIL:.2f} cells")
        logging.info(f"Speed: L:{left_speed} R:{right_speed}")
        # logging.info(f"Encoders: L:{sensors.encoders.left} R:{sensors.encoders.right}")

        time.sleep(0.01)  # 10 миллисекунд

    # Финальная корректировка
    # if sum_distance > total_distance:
    #     correction = -(sum_distance - total_distance) * 0.8
    #     pwm(int(correction), ROTATETIME,int(correction), ROTATETIME)
    #     time.sleep(0.1)  # 100 миллисекунд

if __name__ == '__main__':
    FORMAT = "%(funcName)15s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    forward_first(1)