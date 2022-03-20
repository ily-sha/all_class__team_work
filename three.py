import os
import sys

import pygame
import requests

lon = "37.530887"
lat = "55.703118"
map_file = "map.png"
z = 6

pygame.init()
size = w, h = 500, 450
screen = pygame.display.set_mode(size)


def paint_map(z):
    global map_file
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z={z}&size={w},{h}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
        
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


paint_map(z)
screen.blit(pygame.image.load(map_file), (0, 0))
running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEUP:
                if z <= 18:
                    z += 1
                    paint_map(z)
            elif i.key == pygame.K_PAGEDOWN:
                if z >= 2:
                    z -= 1
                    paint_map(z)
            if i.key == pygame.K_UP:
                lat = str(float(lat) + 0.02) if z > 7 else str(float(lat) + 0.2)
                paint_map(z)
            elif i.key == pygame.K_DOWN:
                lat = str(float(lat) - 0.02) if z > 7 else str(float(lat) - 0.2)
                paint_map(z)
            elif i.key == pygame.K_RIGHT:
                lon = str(float(lon) + 0.05) if z > 7 else str(float(lon) + 0.5)
                paint_map(z)
            elif i.key == pygame.K_LEFT:
                lon = str(float(lon) - 0.05) if z > 7 else str(float(lon) - 0.5)
                paint_map(z)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)