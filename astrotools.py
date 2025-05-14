import swisseph as swe
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from deepseek import *

def natal(date, latitude=55.7558, longitude=37.6176):
    # Устанавливаем дату и время
    text = []
    timezone_offset = 3  # Например, Москва — UTC+3

    # Юлианская дата UTC
    jd = swe.julday(date.year, date.month, date.day, date.hour - timezone_offset + date.minute / 60.0)


    # Устанавливаем географическое положение
    swe.set_topo(longitude, latitude, 0)  # долгота, широта, высота (0 — уровень моря)


    # Список планет
    planet_names = {
        "Солнце": swe.SUN,
        "Луна": swe.MOON,
        "Меркурий": swe.MERCURY,
        "Венера": swe.VENUS,
        "Марс": swe.MARS,
        "Юпитер": swe.JUPITER,
        "Сатурн": swe.SATURN,
        "Уран": swe.URANUS,
        "Нептун": swe.NEPTUNE,
        "Плутон": swe.PLUTO,
    }

    # Знаки зодиака
    zodiac_signs = [
        "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
        "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"
    ]

    zodiac_icon = {
        "Овен": "♈",
        "Телец": "♉",
        "Близнецы": "♊",
        "Рак": "♋",
        "Лев": "♌",
        "Дева": "♍",
        "Весы": "♎",
        "Скорпион": "♏",
        "Стрелец": "♐",
        "Козерог": "♑",
        "Водолей": "♒",
        "Рыбы": "♓"
    }


    planet_icons = {
    'Солнце': '☉',
    'Меркурий': '☿',
    'Луна': '☾',
    'Венера': '♀',
    'Марс': '♂',
    'Юпитер': '♃',
    'Уран': '♅',
    'Нептун': '♆',
    'Сатурн': '♄',
    'Плутон': '♇'}

    # Получаем данные по домам (Placidus используется по умолчанию)
    houses, asc_mc = swe.houses(jd, latitude, longitude, b'P')
    # 'P' — система Плацидус

    print("=== Планеты ===")
    text.append('=== Планеты ===\n')
    planets = []
    for name, planet in planet_names.items():
        position, _ = swe.calc_ut(jd, planet)
        lon = position[0]
        sign_index = int(lon // 30)
        sign_name = zodiac_signs[sign_index]
        degree = lon % 30
        planets.append((name, degree, sign_index))
        print(f"{name}: {degree:.2f}° {sign_name}")
        text.append(f"{name}: {degree:.2f}° {sign_name}" + '\n')

    print("\n=== Дома гороскопа ===")
    text.append('=== Дома гороскопа ===\n')
    home_degrees = []
    for i, cusp in enumerate(houses, start=1):
        sign_index = int(cusp // 30)
        degree = cusp % 30
        home_degrees.append(degree)
        print(f"Дом {i}: {degree:.2f}° {zodiac_signs[sign_index]}")
        text.append(f"Дом {i}: {degree:.2f}° {zodiac_signs[sign_index]}" + '\n')

    print("\n=== Точки ASC/MC ===")
    text.append("=== Точки ASC/MC ===\n")
    asc, mc = asc_mc[0], asc_mc[1]
    asc_sign = zodiac_signs[int(asc // 30)]
    mc_sign = zodiac_signs[int(mc // 30)]
    print(f"Асцендент: {asc % 30:.2f}° {asc_sign}")
    text.append(f"Асцендент: {asc % 30:.2f}° {asc_sign}" + '\n')
    print(f"Midheaven (MC): {mc % 30:.2f}° {mc_sign}")
    text.append(f"Midheaven (MC): {mc % 30:.2f}° {mc_sign}" + '\n')

    #___________________________________________________________
    home_edges = sorted([angle for angle in home_degrees])

    # Допустим, что дома идут друг за другом, включительно с границей
    # Для визуализации добавим центр (0 градусов)
    # В случае, если границы не начинаются с 0, можно добавить его
    if 0 not in home_edges:
        home_edges = [0.] + home_edges

    # Создадим массив центров домов
    home_centers = []
    for i in range(len(home_edges)):
        start = home_edges[i]
        end = home_edges[(i+1) % len(home_edges)]
        center = (start + end) / 2
        home_centers.append(center)





    # Визуализация
    fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection': 'polar'})

    # Установим вращение так, чтобы 0° было сверху (на север)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(1)  # по часовой

    # Нарисуем круг
    circle = plt.Circle((0,0),1, transform=ax.transData._b, fill=False, edgecolor='black')
    ax.add_artist(circle)

    home_degrees = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    home_edges = sorted([float(angle) for angle in home_degrees])
    home_centers = []
    for i in range(len(home_edges)):
        start = home_edges[i]
        end = home_edges[(i + 1) % len(home_edges)]
        center = start + 22.5
        home_centers.append(center)

    # Отметим дома
    for edge in home_edges:
        angle_rad = np.deg2rad(edge)
        ax.plot([angle_rad, angle_rad], [0.9, 1], color='red', linestyle='--', linewidth=1.5)

    print(home_centers)
    print(home_edges)
    # Отметим центры домов
    for center in home_degrees:
        angle_rad = np.deg2rad(center)
        ax.plot([angle_rad, angle_rad], [0.85, 0.95], color='blue', linewidth=2)

    for c in home_centers:
        # Можно добавить подписи
        angle_rad = np.deg2rad(c)
        ax.text(angle_rad, 1.1, f'{list(zodiac_icon.values())[home_centers.index(c)]}', fontsize=8, ha='center')

    # Отметим планеты
    for name, degree, sign_index in planets:
        angle_rad = np.deg2rad(degree + home_degrees[sign_index])
        ax.plot(angle_rad, 0.7, 'o', label=name)
        ax.text(angle_rad, 0.7, planet_icons[name], fontsize=14, ha='center')
        ax.text(angle_rad, 0.60, name, fontsize=8, ha='center')

    angle_rad = np.deg2rad(asc % 30 + home_degrees[zodiac_signs.index(asc_sign)])
    ax.plot([angle_rad, angle_rad], [0, 1.5], color='red', linewidth=2)
    ax.text(angle_rad, 1.25, 'AC', fontsize=14, ha='center')

    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(0, 1.2)

    plt.title('Натальная карта')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.savefig('natal_chart.png')

    text = ''.join(text)

    t2 = ':'.join(text.split('\n'))

    print(':'.join(text.split('\n')))

    aia = chat_stream(f"Выведи характеристику человека по параметрам натальной карты:{t2}")
    return ('natal_chart.png', aia)





