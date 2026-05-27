import pygame
import sys
import random
from ui import UI
from pets import Pet
from shop import Shop
from tap_game import TapGame
from cleaning_game import CleaningGame

pygame.init()

# размеры окна
WIDTH = 800
HEIGHT = 600

# создание базового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tamagotchi")

# загрузка фона
background = pygame.image.load("images/backgrounds/home.png")
background = pygame.transform.scale(background, (800, 600))
shop_bg = pygame.image.load("images/backgrounds/market.png")
shop_bg = pygame.transform.scale(shop_bg, (800, 600))

# создание объектов
ui = UI(screen)
pet = Pet(screen)
shop = Shop(screen, pet, ui, shop_bg)
tap_game = TapGame(screen, pet, ui)
cleaning_game = CleaningGame(screen, pet, ui)

# переменные состояния
game_mode = "main"  # main, tap_game, cleaning_game, shop
shop_open = False
last_update = pygame.time.get_ticks()

# игровой цикл
running = True
while running:
    current_time = pygame.time.get_ticks()

    # обновление сна (проверка проснулся ли)
    pet.update_sleep(current_time)

    # таймеры для статов
    if not pet.sleeping and game_mode == "main":
        if current_time - last_update > 5000:
            pet.update_stats()
            last_update = current_time

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if game_mode == "tap_game":
                result = tap_game.handle_click(mouse_pos)
                if result == "exit":
                    game_mode = "main"

            elif game_mode == "cleaning_game":
                result = cleaning_game.handle_click(mouse_pos)
                if result == "exit":
                    game_mode = "main"

            elif shop_open:
                if shop.handle_click(mouse_pos):
                    shop_open = False

            elif game_mode == "main":
                # кнопка кормления
                if ui.feed_rect.collidepoint(mouse_pos):
                    pet.feed()
                    print("Feed")

                # кнопка игры (тапалка) - с проверкой на сон
                if ui.play_rect.collidepoint(mouse_pos):
                    if not pet.needs_sleep and not pet.sleeping:
                        game_mode = "tap_game"
                        tap_game.start()
                        print("Игра запущена!")
                    else:
                        print("Питомец хочет спать! Сначала уложите его спать или купите зелье!")

                # кнопка сна
                if ui.sleep_rect.collidepoint(mouse_pos):
                    if pet.start_sleep():
                        print("Питомец уснул!")
                    else:
                        print("Питомец не хочет спать, у него полная энергия!")

                # кнопка мытья
                if ui.wash_rect.collidepoint(mouse_pos):
                    game_mode = "cleaning_game"
                    cleaning_game.start()
                    print("Мыться!")

                # кнопка магазина
                if ui.shop_rect.collidepoint(mouse_pos):
                    shop_open = True
                    print("Shop")

                # кнопка туалета
                if ui.toilet_rect.collidepoint(mouse_pos):
                    pet.needs_toilet = False
                    print("Спасибочки!")

    # отрисовка

    if pet.sleeping:
        ui.draw_sleep_mode(current_time, pet)

    elif game_mode == "tap_game":
        result = tap_game.update(current_time)
        if result == "exit":
            game_mode = "main"
        tap_game.draw(current_time)

    elif game_mode == "cleaning_game":
        result = cleaning_game.update(current_time)
        if result == "exit":
            game_mode = "main"
        cleaning_game.draw(current_time)

    elif shop_open:
        shop.draw(current_time)

    else:
        screen.blit(background, (0, 0))
        pet.draw()
        ui.draw_stats(pet)
        ui.draw_buttons()

        if pet.needs_toilet:
            ui.draw_toilet_warning()

        if pet.needs_sleep and not pet.sleeping:
            ui.draw_sleep_warning()

        ui.draw_coins(pet.coins)

    pygame.display.flip()

pygame.quit()
sys.exit()
