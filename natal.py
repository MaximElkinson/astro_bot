import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import get_body, solar_system_ephemeris, EarthLocation, AltAz
from astropy.time import Time
from datetime import datetime

def calculate_houses(birth_time, location):
    # Простой расчет домов по системе Плацидуса
    houses = []
    for i in range(12):
        house_angle = (i * 30)  # 360° / 12 домов
        houses.append(house_angle)
    return houses

def natal_chart(birth_date, birth_time, birth_location):
    # Установка времени рождения
    birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    birth_time = Time(birth_datetime)

    # Установка места рождения
    loc = EarthLocation(lat=birth_location[0], lon=birth_location[1], height=0)

    # Получение координат планет для времени рождения
    with solar_system_ephemeris.set('builtin'):
        bodies = solar_system_ephemeris.bodies
        planets = {}
        for body in bodies:
            if body in ['earth', 'earth-moon-barycenter']:  # Исключаем Землю
                continue
            planets[body] = get_body(body, birth_time)
        
    # Конвертация в AltAz
    altaz_planets = {}
    for body, planet in planets.items():
        altaz_planets[body] = planet.transform_to(AltAz(obstime=birth_time, location=loc))
    
    # Расчет домов
    houses = calculate_houses(birth_time, loc)

    # Построение натальной карты
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    # Конфигурация осей
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    # Цвета для планет
    planet_colors = {
        "sun": "gold",
        "moon": "silver",
        "mercury": "brown",
        "venus": "khaki",
        "mars": "tomato",
        "jupiter": "sandybrown",
        "saturn": "goldenrod",
        "uranus": "lightblue",
        "neptune": "royalblue"
    }
    
    # Рисуем планеты и добавляем подписи
    for body, altaz in altaz_planets.items():
        phi = np.radians(altaz.az.deg)
        r = 90 - altaz.alt.deg  # радиус соответствует высоте
        ax.plot(phi, r, marker='o', linestyle='None', color=planet_colors.get(body, "black"))
        
        # Добавляем подпись справа от планеты
        ax.text(phi, r + 5, body.capitalize(), horizontalalignment='left', fontsize=10, color="black")

    # Рисуем дома и добавляем подписи
    for i, house in enumerate(houses):
        house_angle = np.radians(house - 90)  # Поворачиваем на 90 градусов
        ax.plot([house_angle, house_angle], [0, 150], color='darkblue', linestyle='-', linewidth=1)  # Линии выходят за пределы круга
        
        # Добавляем подписи для асцендента и десцента
        if i == 0:  # Асцендент (1 дом)
            ax.text(house_angle, 155, 'ASC', horizontalalignment='center', fontsize=12, color='black')
        elif i == 6:  # Десцент (7 дом)
            ax.text(house_angle, 155, 'DSC', horizontalalignment='center', fontsize=12, color='black')
        else:
            # Против часовой стрелки: 1 дом - 12 дом
            house_number = 12 - i if i > 0 else 1
            ax.text(house_angle, 155, str(house_number), horizontalalignment='center', fontsize=12, color='black')

    ax.set_title(f'Натальная карта для {birth_datetime}', va='bottom')
    plt.savefig('natal_chart.png')

    return 'natal_chart.png'

# Пример использования
natal_chart('2005-01-01', '12:00', (40.7128, -74.0060))  # Замените на ваши данные
