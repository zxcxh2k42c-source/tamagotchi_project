import pygame
import random


class CleaningGame:
    def __init__(self, screen, pet, ui):
        self.screen = screen
        self.pet = pet
        self.ui = ui
        self.bubbles = []
        self.cleaning_start = 0
        self.last_bubble_spawn = pygame.time.get_ticks()

        # Убираем загрузку dirty_pet отсюда - будем использовать pet.dirty_pet

    def start(self):
        self.bubbles.clear()
        self.cleaning_start = pygame.time.get_ticks()
        self.last_bubble_spawn = pygame.time.get_ticks()

    def handle_click(self, mouse_pos):
        for bubble in self.bubbles[:]:
            bubble_rect = pygame.Rect(bubble["x"] - 30, bubble["y"] - 30, 60, 60)
            if bubble_rect.collidepoint(mouse_pos):
                self.bubbles.remove(bubble)
                self.pet.cleanliness = min(100, self.pet.cleanliness + 10)
                print(f"Чистота: {self.pet.cleanliness}")
        return None

    def update(self, current_time):
        if current_time - self.last_bubble_spawn > 700:
            new_bubble = {
                "x": random.randint(50, 700),
                "y": random.randint(100, 500)
            }
            self.bubbles.append(new_bubble)
            self.last_bubble_spawn = current_time

        if current_time - self.cleaning_start > 10000:
            self.pet.cleanliness = min(100, self.pet.cleanliness + 20)
            self.pet.needs_toilet = False
            print("Мойка окончена!")
            return "exit"
        return None

    def draw(self, current_time):
        self.screen.fill((100, 150, 200))  # голубой фон воды

        # Рисуем ГРЯЗНОГО питомца (используем pet.dirty_pet)
        self.screen.blit(self.pet.dirty_pet, (290, 275))

        # Рисуем пузырьки
        for bubble in self.bubbles:
            pygame.draw.circle(self.screen, (200, 230, 255), (bubble["x"], bubble["y"]), 30)

        # Таймер
        time_left = max(0, 10 - (current_time - self.cleaning_start) // 1000)
        timer_text = self.ui.font.render(f"Время: {time_left}с", True, (255, 255, 255))
        self.screen.blit(timer_text, (20, 20))

        # Шкала чистоты
        self.ui.draw_bar(30, 150, self.pet.cleanliness, (150, 220, 255))
        clean_text = self.ui.font.render("Чистота", True, (255, 255, 255))
        self.screen.blit(clean_text, (240, 145))
