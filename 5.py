import pygame
import requests
import os

lon = "37.530887"
lat = "55.703118"

map_file = "map.png"
search = ""


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color((0, 0, 0))
        self.text = text
        self.font = pygame.font.Font("data/corbell.ttf", 15)
        self.text_render = self.font.render(text, True, pygame.Color(0, 0, 0))
        self.active = False

    def handle_event(self, event):
        global search
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color((232, 70, 37)) if self.active else pygame.Color((0, 0, 0))
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    search = self.text
                    self.color = pygame.Color((0, 0, 255))
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_render = self.font.render(self.text, True, pygame.Color(0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), self.rect)
        screen.blit(self.text_render, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


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
        exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


paint_map()
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
input_box = InputBox(50, 50, 400, 20)
pygame.draw.rect(screen, pygame.Color(232, 70, 37), (460, 50, 100, 20))
font = pygame.font.Font("data/corbell.ttf", 15)
text = font.render("Найти", True, pygame.Color(0, 0, 0))
screen.blit(text, (487, 52))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paint_map(left=True)
            elif event.key == pygame.K_RIGHT:
                paint_map(right=True)
            elif event.key == pygame.K_DOWN:
                paint_map(down=True)
            elif event.key == pygame.K_UP:
                paint_map(up=True)
        input_box.handle_event(event)
    screen.blit(pygame.image.load(map_file), (0, 0))
    input_box.draw(screen)
    pygame.draw.rect(screen, pygame.Color(232, 70, 37), (460, 50, 100, 20))
    font = pygame.font.Font("data/corbell.ttf", 15)
    text = font.render("Найти", True, pygame.Color(0, 0, 0))
    screen.blit(text, (487, 52))
    pygame.display.flip()

