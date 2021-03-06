import pygame
import requests
import os

window_size = width, height = (600, 450)

longitude = 37.530887
latitude = 55.703118
zoom = 13
style = "map"
placemarks = []

map_file = "map.png"
search_request = ""


def make_a_button(x, y, w, h, t_x, t_y, text='', color=pygame.Color(232, 70, 37)):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font("data/corbell.ttf", 15)
    text = font.render(text, True, pygame.Color(0, 0, 0))
    screen.blit(text, (t_x, t_y))

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color((0, 0, 0))
        self.text = text
        self.font = pygame.font.Font("data/corbell.ttf", 15)
        self.text_render = self.font.render(text, True, pygame.Color(0, 0, 0))
        self.active = False

    def handle_event(self, event):
        global search_request
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color((232, 70, 37)) if self.active else pygame.Color((0, 0, 0))
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                search_request = self.text
                self.text_render = self.font.render(self.text, True, pygame.Color(0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), self.rect)
        screen.blit(self.text_render, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def get_map(z, lon, lat, style, placemarks):
    global map_file
    if not placemarks:
        params = {
            "ll": ",".join(map(str, [lon, lat])),
            "z": z,
            "l": style,
        }
    else:
        params = {
            "ll": ",".join(map(str, [lon, lat])),
            "z": z,
            "l": style,
            "pt": '~'.join(placemarks)
        }
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params)
    if not response:
        print("???????????? ???????????????????? ??????????????:")
        print(api_server)
        print("Http ????????????:", response.status_code, "(", response.reason, ")")
        exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


get_map(zoom, longitude, latitude, style, placemarks)
pygame.init()
pygame.display.set_caption("???????????? ?????????? lite")
screen = pygame.display.set_mode(window_size)
screen.blit(pygame.image.load(map_file), (0, 0))
input_box = InputBox(50, 50, 400, 20)
make_a_button(460, 50, 100, 20, 487, 52, "??????????")

start_button = pygame.draw.rect(screen, (0, 0, 240), (10, height - 60, 50, 50))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if zoom <= 18:
                    zoom += 1
            elif event.key == pygame.K_PAGEDOWN:
                if zoom >= 2:
                    zoom -= 1
            if event.key == pygame.K_LEFT:
                longitude -= 0.05
            elif event.key == pygame.K_RIGHT:
                longitude += 0.05
            elif event.key == pygame.K_DOWN:
                latitude -= 0.02
            elif event.key == pygame.K_UP:
                latitude += 0.02
            get_map(zoom, longitude, latitude, style, placemarks)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] in range(10, 60) and event.pos[1] in range(height - 35, height - 10):
                style = 'map'
            elif event.pos[0] in range(70, 130) and event.pos[1] in range(height - 35, height - 10):
                style = 'sat'
            elif event.pos[0] in range(140, 200) and event.pos[1] in range(height - 35, height - 10):
                style = 'sat,skl'
            get_map(zoom, longitude, latitude, style, placemarks)
        if (event.type == pygame.MOUSEBUTTONDOWN
            and event.pos[0] in range(460, 561)
            and event.pos[1] in range(50, 71)) \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": search_request,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            longitude, latitude = toponym["Point"]["pos"].split()
            placemarks.append(','.join([longitude, latitude, 'ya_ru']))
            longitude, latitude = float(longitude), float(latitude)
            get_map(zoom, longitude, latitude, style, placemarks)

        input_box.handle_event(event)
    screen.blit(pygame.image.load(map_file), (0, 0))
    input_box.draw(screen)
    make_a_button(460, 50, 100, 20, 487, 52, "??????????")
    make_a_button(10, height - 35, 50, 25, 15, height - 30, "??????????")
    make_a_button(70, height - 35, 60, 25, 75, height - 30, "??????????????")
    make_a_button(140, height - 35, 60, 25, 145, height - 30, "????????????")

    pygame.display.flip()
