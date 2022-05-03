import pygame
import requests
import os

longitude = 37.530887
latitude = 55.703118

map_file = "map.png"
search_request = ""


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
            self.active = not self.active if self.rect.collidepoint(
                event.pos) else False
            self.color = pygame.Color(
                (232, 70, 37)) if self.active else pygame.Color((0, 0, 0))
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            search_request = self.text
            self.text_render = self.font.render(
                self.text, True, pygame.Color(0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), self.rect)
        screen.blit(self.text_render, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def get_map(lon, lat, pin=False):
    global map_file
    params = {
        "ll": ",".join(map(str, [lon, lat])),
        "spn": ",".join(["0.04", "0.04"]),
        "l": "map"
    }
    if pin:
        params["pt"] = f"{','.join(map(str, [lon, lat]))},pm2rdm"
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


get_map(longitude, latitude)
pygame.init()
pygame.display.set_caption("Яндекс карты lite")
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
input_box = InputBox(50, 50, 400, 20)
pygame.draw.rect(screen, pygame.Color(232, 70, 37), (460, 50, 100, 20))
font = pygame.font.Font("data/corbell.ttf", 15)
text = font.render("Найти", True, pygame.Color(0, 0, 0))
screen.blit(text, (487, 52))
pygame.draw.rect(screen, pygame.Color(204, 188, 188), (570, 50, 20, 20))
pygame.draw.line(screen, pygame.Color(0, 0, 0), (575, 55), (585, 65), 3)
pygame.draw.line(screen, pygame.Color(0, 0, 0), (575, 65), (585, 55), 3)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(map_file)
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                longitude -= 0.05
            elif event.key == pygame.K_RIGHT:
                longitude += 0.05
            elif event.key == pygame.K_DOWN:
                latitude -= 0.02
            elif event.key == pygame.K_UP:
                latitude += 0.02
            get_map(longitude, latitude)
        if (event.type == pygame.MOUSEBUTTONDOWN
            and event.pos[0] in range(460, 561)
            and event.pos[1] in range(50, 71)) \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": search_request,
                "format": "json"}
            response = requests.get(
                geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            longitude, latitude = map(float, toponym["Point"]["pos"].split())
            input_box.text = toponym["metaDataProperty"]["GeocoderMetaData"]["text"][8:63] + "..."
            input_box.text_render = input_box.font.render(
                toponym["metaDataProperty"]["GeocoderMetaData"]["text"][8:63] + "...", True, pygame.Color(0, 0, 0))
            get_map(longitude, latitude, pin=True)
        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] in range(570, 590) and event.pos[1] in range(50, 70):
            input_box.text = ""
            input_box.text_render = input_box.font.render(
                "", True, pygame.Color(0, 0, 0))
            longitude, latitude = 37.530887, 55.703118
            get_map(longitude, latitude)
        input_box.handle_event(event)
    screen.blit(pygame.image.load(map_file), (0, 0))
    input_box.draw(screen)
    pygame.draw.rect(screen, pygame.Color(232, 70, 37), (460, 50, 100, 20))
    font = pygame.font.Font("data/corbell.ttf", 15)
    text = font.render("Найти", True, pygame.Color(0, 0, 0))
    screen.blit(text, (487, 52))
    pygame.draw.rect(screen, pygame.Color(204, 188, 188), (570, 50, 20, 20))
    pygame.draw.line(screen, pygame.Color(0, 0, 0), (575, 55), (585, 65), 3)
    pygame.draw.line(screen, pygame.Color(0, 0, 0), (575, 65), (585, 55), 3)
    pygame.display.flip()
