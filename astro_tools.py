import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import get_sun, solar_system_ephemeris, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime

def natal_chart(birth_date, birth_time, birth_location):
    # Установка времени рождения
    birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    birth_time = Time(birth_datetime)

    # Установка места рождения
    loc = EarthLocation(lat=birth_location[0], lon=birth_location[1])

    # Получение координат Солнца для времени рождения
    with solar_system_ephemeris.set('builtin'):
        sun = get_sun(birth_time)

    # Конвертация в AltAz
    altaz = sun.transform_to(AltAz(obstime=birth_time, location=loc))

    # Построение натальной карты
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

    # Конфигурация осей
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Пример - нарисуем только Солнце
    phi = np.radians(altaz.az.deg)
    r = 90 - altaz.alt.deg  # радиус соответствует высоте
    ax.plot(phi, r, marker='o', linestyle='None', color='gold', label='Солнце')

    # Добавление других планет (по желанию)

    ax.set_title(f'Натальная карта для {birth_datetime}', va='bottom')
    ax.legend(loc='upper right')
    # plt.show()
    plt.savefig('natal_chart.png')
    '''
    # Возвращаем текстовое описание
    text_description = f"Дата рождения: {birth_date}n"
    f"Время рождения: {birth_time}n"
    f"Место рождения: {birth_location}n"
    f"Положение Солнца: Азимут {altaz.az.deg:.2f}°, Высота {altaz.alt.deg:.2f}°"
    '''


    return 'natal_chart.png'