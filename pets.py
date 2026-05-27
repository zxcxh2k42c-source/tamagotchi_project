import pygame
import random
import os


class Pet:
    def __init__(self, screen):
        self.screen = screen

        # Проверяем какие животные реально есть в папке
        available_pets = []
        for pet in ["cat", "dog", "panda"]:
            if os.path.exists(f"images/pets/{pet}.png"):
                available_pets.append(pet)
                print(f"Доступен: {pet}")
            else:
                print(f"НЕ доступен: {pet} - нет файла images/pets/{pet}.png")

        if not available_pets:
            available_pets = ["cat"]
            print("Нет доступных животных, использую кота")

        self.pet_type = random.choice(available_pets)
        print(f"Выбрано животное: {self.pet_type}")

        # КООРДИНАТЫ ДЛЯ АКСЕССУАРОВ В ЗАВИСИМОСТИ ОТ ЖИВОТНОГО
        self.accessory_positions = {
            "cat": {
                "hat": (330, 180),
                "glasses": (340, 332)
            },
            "dog": {
                "hat": (330, 175),  # подберите свои координаты
                "glasses": (340, 330)  # подберите свои координаты
            },
            "panda": {
                "hat": (330, 185),  # подберите свои координаты
                "glasses": (340, 335)  # подберите свои координаты
            }
        }

        # статы
        self.hunger = 80
        self.energy = 60
        self.happiness = 90
        self.cleanliness = 100
        self.coins = 0
        self.needs_toilet = False

        # таймеры
        self.last_toilet_time = pygame.time.get_ticks()
        self.last_cleanliness_update = pygame.time.get_ticks()
        self.last_sleep_need_time = pygame.time.get_ticks()

        # ЗАГРУЗКА ВСЕХ СОСТОЯНИЙ ДЛЯ ВЫБРАННОГО ЖИВОТНОГО
        self.normal_pet = self.load_pet(f"images/pets/{self.pet_type}.png")
        self.sad_pet = self.load_pet(f"images/pets/sad_{self.pet_type}.png")
        self.sleepy_pet = self.load_pet(f"images/pets/sleepy_{self.pet_type}.png")
        self.sad_sleepy_pet = self.load_pet(f"images/pets/sad_sleepy_{self.pet_type}.png")
        self.dirty_pet = self.load_pet(f"images/pets/dirty_{self.pet_type}.png")

        self.current_pet = self.normal_pet

        # аксессуары
        self.hat_owned = False
        self.glasses_owned = False
        self.hat_image = self.load_image("images/on_items/on_hat.png", (140, 170))
        self.glasses_image = self.load_image("images/on_items/on_glasses.png", (150, 70))

        # РЕЖИМ СНА
        self.sleeping = False
        self.sleep_start = 0
        self.sleep_duration = 60000

        # ПОТРЕБНОСТЬ ВО СНЕ
        self.needs_sleep = False

    def load_pet(self, path, size=(220, 270)):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    def load_image(self, path, size):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    def get_pet_name(self):
        names = {
            "cat": "Котик",
            "dog": "Собачка",
            "panda": "Панда"
        }
        return names.get(self.pet_type, "Питомец")

    def update_stats(self):
        current_time = pygame.time.get_ticks()

        self.hunger = max(0, self.hunger - 5)
        self.energy = max(0, self.energy - 3)
        self.happiness = max(0, self.happiness - 5)

        # потребность во сне
        if current_time - self.last_sleep_need_time > 45000:
            if self.energy < 70:
                self.needs_sleep = True
            self.last_sleep_need_time = current_time

        # туалет
        if current_time - self.last_toilet_time > 60000:
            self.needs_toilet = True
            self.last_toilet_time = current_time

        # чистота
        if current_time - self.last_cleanliness_update > 5000:
            if self.needs_toilet:
                self.cleanliness = max(0, self.cleanliness - 10)
            else:
                self.cleanliness = max(0, self.cleanliness - 3)
            self.last_cleanliness_update = current_time

        self.update_appearance()

    def start_sleep(self):
        print(f"start_sleep вызван. energy={self.energy}")
        if self.energy < 100:
            self.sleeping = True
            self.sleep_start = pygame.time.get_ticks()
            self.needs_sleep = False
            print(f"Питомец уснул! sleep_start={self.sleep_start}")
            return True
        else:
            print("Питомец не хочет спать, энергия полная")
            return False

    def update_sleep(self, current_time):
        if self.sleeping:
            if current_time - self.sleep_start >= self.sleep_duration:
                self.sleeping = False
                self.energy = 100
                print("Питомец проснулся!")
                return True
        return False

    def wake_up(self):
        self.sleeping = False
        self.energy = min(100, self.energy + 30)
        print("Питомец проснулся от зелья!")

    def update_appearance(self):
        if self.cleanliness < 30:
            self.current_pet = self.dirty_pet
        elif self.happiness < 50 and self.energy < 35:
            self.current_pet = self.sad_sleepy_pet
        elif self.energy < 35:
            self.current_pet = self.sleepy_pet
        elif self.happiness < 50:
            self.current_pet = self.sad_pet
        else:
            self.current_pet = self.normal_pet

    def feed(self):
        self.hunger = min(100, self.hunger + 10)

    def play(self):
        self.happiness = min(100, self.happiness + 10)

    def wash(self):
        self.cleanliness = min(100, self.cleanliness + 20)
        self.needs_toilet = False

    def add_coins(self, amount):
        self.coins += amount

    def draw(self):
        self.screen.blit(self.current_pet, (290, 275))

        if self.pet_type == "cat":
            hat_x, hat_y = 330, 180
            glasses_x, glasses_y = 340, 332
        elif self.pet_type == "dog":
            hat_x, hat_y = 330, 175
            glasses_x, glasses_y = 320, 335
        elif self.pet_type == "panda":
            hat_x, hat_y = 330, 185
            glasses_x, glasses_y = 323, 342  # подберите свои цифры для панды
        else:
            hat_x, hat_y = 330, 180
            glasses_x, glasses_y = 340, 332

        if self.hat_owned:
            self.screen.blit(self.hat_image, (hat_x, hat_y))
        if self.glasses_owned:
            self.screen.blit(self.glasses_image, (glasses_x, glasses_y))
