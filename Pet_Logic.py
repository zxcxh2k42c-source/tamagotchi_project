import time
import random
from datetime import datetime


# -----------------------------
# ЕДА
# -----------------------------
class Food:
    def __init__(self, name, nutrition, pet_type):
        self.name = name
        self.nutrition = nutrition  # сколько восстанавливает голода
        self.pet_type = pet_type    # для кого подходит


class Fish(Food):
    def __init__(self):
        super().__init__("Fish", 33, "cat")


class Bone(Food):
    def __init__(self):
        super().__init__("Bone", 33, "dog")


class Bamboo(Food):
    def __init__(self):
        super().__init__("Bamboo", 33, "panda")


# -----------------------------
# ПИТОМЕЦ
# -----------------------------
class Pet:
    def __init__(self):
        self.type = random.choice(["cat", "dog", "panda"])

        self.hunger = 100
        self.energy = 100
        self.happiness = 100
        self.cleanliness = 100

        self.coins = 0

        self.last_update = time.time()
        self.sleep_start_time = None

        self.actions_counter = 0 # для еды + игры
        self.is_dirty = False

        self.birth_date = datetime.now().date()
        self.last_birthday_reward = None

    # -------------------------
    # ОБНОВЛЕНИЕ СОСТОЯНИЯ
    # -------------------------
    def update(self):
        current_time = time.time()
        hours_passed = int((current_time - self.last_update) // 3600)

        if hours_passed > 0:
            for _ in range(hours_passed):
                self.hunger = max(0, self.hunger - 10)

                if self.is_dirty:
                    self.happiness = max(0, self.happiness - 20)
                else:
                    self.happiness = max(0, self.happiness - 10)

            self.last_update += hours_passed * 3600
        self.check_birthday()
    # -------------------------
    # КОРМЛЕНИЕ
    # -------------------------
    def feed(self, food: Food):
        if food.pet_type != self.type:
            print("Питомец не ест эту еду")
            return

        self.hunger = min(100, self.hunger + food.nutrition)
        self.actions_counter += 1
        self.check_dirty()

    # -------------------------
    # ИГРА (счастье)
    # -------------------------
    def play(self):
        self.happiness = min(100, self.happiness + 100)

        self.actions_counter += 1
        self.check_dirty()

    # -------------------------
    # ЗЕЛЬЕ ЭНЕРГИИ
    # -------------------------
    def use_energy_potion(self):
        self.energy = 100

    # -------------------------
    # ГРЯЗЬ
    # -------------------------
    def check_dirty(self):
        if self.actions_counter >= 3:  # 2 игры + 1 еда
            self.is_dirty = True
            self.cleanliness = 0

    def clean_pet(self):
        self.cleanliness = 100
        self.is_dirty = False
        self.actions_counter = 0
    # -------------------------
    # СОН
    # -------------------------
    def sleep(self):
        if self.sleep_start_time is None:
            self.sleep_start_time = time.time()

    def wake_up(self):
        if self.sleep_start_time is None:
            return

        sleep_duration = time.time() - self.sleep_start_time

        energy_per_second = 100 / 7200

        gained_energy = sleep_duration * energy_per_second

        self.energy = min(100, self.energy + gained_energy)

        self.sleep_start_time = None
    # -------------------------
    # СОСТОЯНИЕ
    # -------------------------
    def get_state(self):
        return {
            "type": self.type,
            "hunger": self.hunger,
            "energy": self.energy,
            "happiness": self.happiness,
            "cleanliness": self.cleanliness
        }
    # -------------------------
    # ДЕНЬ РОЖДЕНИЯ
    # -------------------------
    def check_birthday(self):
        today = datetime.now().date()

        if today == self.birth_date:
            if self.last_birthday_reward != today:
                self.coins += 30
                self.last_birthday_reward = today


# -----------------------------
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# -----------------------------
if __name__ == "__main__":
    pet = Pet()
    print("Ваш питомец:", pet.type)

    # имитация игры
    pet.update()

    food = {
        "cat": Fish(),
        "dog": Bone(),
        "panda": Bamboo()
    }

    pet.feed(food[pet.type])
    pet.play()

    pet.sleep()
    time.sleep(2)  # тест, не 2 часа
    pet.wake_up()

    print(pet.get_state())
