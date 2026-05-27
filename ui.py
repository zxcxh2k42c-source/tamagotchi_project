import pygame


class UI:
    def draw_sleep_warning(self):
        """отображение, что питомец хочет спать"""
        sleep_text = self.font.render("Хочет спать!", True, (150, 150, 255))
        self.screen.blit(sleep_text, (400, 130))

    def draw_pet_name(self, pet):
        """отображение имени животного"""
        pet_name = pet.get_pet_name()
        name_text = self.font.render(pet_name, True, (255, 255, 255))
        self.screen.blit(name_text, (370, 240))

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.font_big = pygame.font.SysFont(None, 50)

        # загрузка кнопок
        self.feed_button = self.load_button("images/buttons/feed.png")
        self.play_button = self.load_button("images/buttons/play.png")
        self.sleep_button = self.load_button("images/buttons/sleep.png")
        self.wash_button = self.load_button("images/buttons/wash.png")
        self.shop_button = self.load_button("images/buttons/shop.png")
        self.toilet_button = self.load_button("images/buttons/toilet.png")

        # области кнопок
        self.feed_rect = pygame.Rect(30, 500, 90, 90)
        self.play_rect = pygame.Rect(140, 500, 90, 90)
        self.sleep_rect = pygame.Rect(270, 500, 90, 90)
        self.wash_rect = pygame.Rect(400, 500, 90, 90)
        self.toilet_rect = pygame.Rect(530, 500, 90, 90)
        self.shop_rect = pygame.Rect(660, 500, 90, 90)
        self.close_rect = pygame.Rect(700, 30, 70, 50)

    def load_button(self, path, size=(90, 90)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    def draw_bar(self, x, y, value, color):
        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, 200, 25))
        pygame.draw.rect(self.screen, color, (x, y, value * 2, 25))

    def draw_stats(self, pet):
        # полоски
        self.draw_bar(30, 30, pet.hunger, (244, 209, 149))
        self.draw_bar(30, 70, pet.energy, (148, 244, 203))
        self.draw_bar(30, 110, pet.happiness, (214, 118, 118))
        self.draw_bar(30, 150, pet.cleanliness, (150, 220, 255))

        # подписи
        texts = ["Голод", "Энергия", "Счастьице", "Чистота"]
        y_positions = [25, 65, 105, 145]
        for text, y in zip(texts, y_positions):
            rendered = self.font.render(text, True, (255, 255, 224))
            self.screen.blit(rendered, (240, y))

    def draw_buttons(self):
        self.screen.blit(self.feed_button, (30, 500))
        self.screen.blit(self.play_button, (140, 500))
        self.screen.blit(self.sleep_button, (270, 500))
        self.screen.blit(self.wash_button, (400, 500))
        self.screen.blit(self.toilet_button, (530, 500))
        self.screen.blit(self.shop_button, (660, 500))

    def draw_coins(self, coins):
        coin_text = self.font.render(f"Монеток: {coins}", True, (255, 215, 0))
        self.screen.blit(coin_text, (620, 20))

    def draw_toilet_warning(self):
        toilet_text = self.font.render("Хочет в туалет!", True, (255, 100, 100))
        self.screen.blit(toilet_text, (400, 100))

    def draw_sleep_mode(self, current_time, pet):
        """отображение режима сна с текущим питомцем"""
        self.screen.fill((0, 0, 0))
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # используем спящую версию ТЕКУЩЕГО питомца
        self.screen.blit(pet.sleepy_pet, (290, 275))

        sleep_text = self.font_big.render("Питомец спит...", True, (255, 255, 255))
        self.screen.blit(sleep_text, (280, 150))

        time_left = max(0, (pet.sleep_duration - (current_time - pet.sleep_start)) // 1000)
        timer_text = self.font.render(f"Проснётся через: {time_left} сек", True, (255, 255, 255))
        self.screen.blit(timer_text, (280, 220))
