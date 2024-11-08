import logging
import time

from motors import pwm
from sensors import get_encoders, get_sensors_raw


def forward_first(cell_count: int) -> None:
    """
    Функция движения вперед на заданное количество клеток с улучшенной стабильностью
    """
    # Параметры корректировки
    K_P = 0.5  # Увеличен коэффициент для более агрессивной коррекции
    MAX_CORRECTION = 30.0  # Увеличена максимальная коррекция
    ENCODERONECEIL = 242  # Тики энкодера на одну клетку
    MAXSPEED = 100
    ROTATETIME = 1000

    # Сброс энкодеров перед началом движения
    get_sensors_raw("all")
    time.sleep(0.01)  # Небольшая задержка для стабилизации
    get_encoders()  # Очищаем накопленные значения

    max_speed = float(MAXSPEED)
    total_distance = float(cell_count) * ENCODERONECEIL
    sum_distance = 0.0

    # Параметры движения
    acceleration_dist = total_distance * 0.15  # Уменьшен участок разгона
    deceleration_dist = total_distance * 0.85  # Раньше начинаем торможение
    min_speed = max_speed * 0.4  # Увеличена минимальная скорость

    previous_left = 0
    previous_right = 0

    # Счетчик для определения остановки
    stable_count = 0
    last_sum = 0

    while sum_distance <= total_distance and stable_count < 5:
        sensors = get_encoders()
        left_delta = sensors["left"] - previous_left
        right_delta = sensors["right"] - previous_right

        # Сохраняем текущие значения
        previous_left = sensors["left"]
        previous_right = sensors["right"]

        # Улучшенный расчет пройденного расстояния
        left_dist = float(abs(left_delta))
        right_dist = float(abs(right_delta))
        delta = (left_dist + right_dist) / 2
        sum_distance += delta

        # Проверка на остановку
        if abs(sum_distance - last_sum) < 1:
            stable_count += 1
        else:
            stable_count = 0
        last_sum = sum_distance

        # Расчет текущей скорости
        if sum_distance <= acceleration_dist:
            progress = sum_distance / acceleration_dist
            current_speed = min_speed + (max_speed - min_speed) * progress
        elif sum_distance >= deceleration_dist:
            progress = (total_distance - sum_distance) / (total_distance * 0.15)
            current_speed = max(min_speed * 0.8, min_speed + (max_speed - min_speed) * progress)
        else:
            current_speed = max_speed

        # Улучшенная коррекция движения
        encoder_diff = float(left_delta - right_delta)
        correction = K_P * encoder_diff
        correction = max(-MAX_CORRECTION, min(MAX_CORRECTION, correction))

        # Применяем коррекцию
        left_speed = int(current_speed - correction)
        right_speed = int(current_speed - correction)  # Используем одинаковую коррекцию

        # Ограничение скорости
        left_speed = max(-MAXSPEED, min(MAXSPEED, left_speed))
        right_speed = max(-MAXSPEED, min(MAXSPEED, right_speed))

        # Применяем скорости
        pwm(left_speed, ROTATETIME, right_speed, ROTATETIME)

        # Логирование
        logging.info(f"Position: {sum_distance/ENCODERONECEIL:.2f} cells")
        logging.info(f"Speed: L:{left_speed} R:{right_speed}")
        logging.info(f"Delta: L:{left_delta} R:{right_delta}")

        time.sleep(0.01)

    # Финальная остановка
    pwm(0, ROTATETIME, 0, ROTATETIME)


if __name__ == '__main__':
    FORMAT = "%(funcName)15s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    forward_first(1)