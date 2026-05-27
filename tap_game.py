import pygame
import random


class TapGame:
    def __init__(self, screen, pet, ui):
        self.screen = screen
        self.pet = pet
        self.ui = ui
        self.targets = []
        self.tap_score = 0
        self.game_start_time = 0
        self.last_spawn = pygame.time.get_ticks()
        self.exit_tap_rect = pygame.Rect(700, 20, 80, 50)

        # ЗАГРУЗКА ПРЕДМЕТОВ ДЛЯ РАЗНЫХ ЖИВОТНЫХ (с размерами)
        self.items = {
            "cat": self.load_item("images/items/fish.png", (30, 70)),
            "dog": self.load_item("images/items/bone.png", (70, 30)),
            "panda": self.load_item("images/items/bamboo.png", (30, 70))
        }

        # РАЗМЕРЫ ДЛЯ ОБЛАСТИ КЛИКА (под каждый предмет)
        self.item_sizes = {
            "cat": (30, 70),
            "dog": (70, 30),
            "panda": (30, 70)
        }

        # текущий предмет (будет меняться в зависимости от питомца)
        self.current_item = self.items.get(self.pet.pet_type, self.items["cat"])
        self.current_size = self.item_sizes.get(self.pet.pet_type, (30, 70))

    def load_item(self, path, size):
        try:
            img = pygame.image.load(path)
            return pygame.transform.scale(img, size)
        except:
            print(f"Не найдена картинка: {path}, использую рыбу")
            img = pygame.image.load("images/items/fish.png")
            return pygame.transform.scale(img, size)

    def start(self):
        # обновляем предмет и размер при старте
        self.current_item = self.items.get(self.pet.pet_type, self.items["cat"])
        self.current_size = self.item_sizes.get(self.pet.pet_type, (30, 70))
        self.targets.clear()
        self.tap_score = 0
        self.game_start_time = pygame.time.get_ticks()
        self.last_spawn = pygame.time.get_ticks()
        print(f"Игра запущена! Ловите {self.get_item_name()}!")

    def get_item_name(self):
        names = {
            "cat": "рыбку",
            "dog": "косточку",
            "panda": "бамбук"
        }
        return names.get(self.pet.pet_type, "предмет")

    def handle_click(self, mouse_pos):
        if self.exit_tap_rect.collidepoint(mouse_pos):
            return "exit"

        for target in self.targets[:]:
            # ИСПОЛЬЗУЕМ ТЕКУЩИЙ РАЗМЕР ПРЕДМЕТА
            width, height = self.current_size
            target_rect = pygame.Rect(target["x"], target["y"], width, height)
            if target_rect.collidepoint(mouse_pos):
                self.targets.remove(target)
                self.tap_score += 1
                # +2 счастья за пойманный предмет
                self.pet.happiness = min(100, self.pet.happiness + 2)
                print(f"Поймал {self.get_item_name()}! Счастьице: {self.pet.happiness}")
        return None

    def update(self, current_time):
        if current_time - self.last_spawn > 1000:
            new_target = {
                "x": random.randint(50, 700),
                "y": random.randint(100, 500)
            }
            self.targets.append(new_target)
            self.last_spawn = current_time

        if current_time - self.game_start_time > 15000:
            # бонусное счастье за игру
            bonus_happiness = min(30, self.tap_score // 2)
            self.pet.happiness = min(100, self.pet.happiness + bonus_happiness)
            self.pet.add_coins(self.tap_score)
            print(
                f"Игра окончена! Поймано {self.tap_score} {self.get_item_name()}! +{bonus_happiness} счастья, +{self.tap_score} монет")
            return "exit"
        return None

    def draw(self, current_time):
        self.screen.fill((50, 50, 80))

        for target in self.targets:
            self.screen.blit(self.current_item, (target["x"], target["y"]))

        # название предмета на экране
        item_text = self.ui.font.render(f"Лови {self.get_item_name()}!", True, (255, 200, 100))
        self.screen.blit(item_text, (20, 20))

        score_text = self.ui.font.render(f"Счёт: {self.tap_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 60))

        time_left = max(0, 15 - (current_time - self.game_start_time) // 1000)
        timer_text = self.ui.font.render(f"Время: {time_left}с", True, (255, 255, 255))
        self.screen.blit(timer_text, (20, 100))

        coin_text = self.ui.font.render(f"Монеток: {self.pet.coins}", True, (255, 215, 0))
        self.screen.blit(coin_text, (20, 140))

        happy_text = self.ui.font.render(f"Счастье: {self.pet.happiness}", True, (255, 200, 200))
        self.screen.blit(happy_text, (20, 180))

        pygame.draw.rect(self.screen, (200, 50, 50), self.exit_tap_rect)
        exit_text = self.ui.font.render("Выход", True, (255, 255, 255))
        self.screen.blit(exit_text, (705, 35))
