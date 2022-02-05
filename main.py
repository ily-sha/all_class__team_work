import os
import sys

import pygame
import requests

lon = "37.530887"
lat = "55.703118"


map_file = "map.png"
def paint_map(left=False, right=False, up=False, down=False):
    global map_file, lat, lon
    if left:
        lon = str(float(lon) - 0.05)
    elif right:
        lon = str(float(lon) + 0.05)
    elif up:
        lat = str(float(lat) + 0.02)
    elif down:
        lat = str(float(lat) - 0.02)

    params = {"ll": ",".join([lon, lat]), "spn": ",".join(["0.04", "0.04"]), "l": "map"}
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


paint_map()
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                paint_map(left=True)
            elif i.key == pygame.K_RIGHT:
                paint_map(right=True)
            elif i.key == pygame.K_DOWN:
                paint_map(down=True)
            elif i.key == pygame.K_UP:
                paint_map(up=True)
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)