import time
import random


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
        super().__init__("Fish", 30, "cat")


class Bone(Food):
    def __init__(self):
        super().__init__("Bone", 30, "dog")


class Bamboo(Food):
    def __init__(self):
        super().__init__("Bamboo", 30, "panda")


# -----------------------------
# ПИТОМЕЦ
# -----------------------------
class Pet:
    def __init__(self):
        self.type = random.choice(["cat", "dog", "panda"])

        # статы (0-100)
        self.hunger = 100
        self.energy = 100
        self.happiness = 100
        self.cleanliness = 100

        self.last_update = time.time()
        self.sleep_start_time = None

    # -------------------------
    # ОБНОВЛЕНИЕ СОСТОЯНИЯ
    # -------------------------
    def update(self):
        current_time = time.time()
        hours_passed = int((current_time - self.last_update) // 3600)

        if hours_passed > 0:
            for _ in range(hours_passed):
                self.hunger = max(0, self.hunger - 10)
                self.happiness = max(0, self.happiness - 10)

            self.last_update += hours_passed * 3600

    # -------------------------
    # КОРМЛЕНИЕ
    # -------------------------
    def feed(self, food: Food):
        if food.pet_type != self.type:
            print("Питомец не ест эту еду")
            return

        self.hunger = min(100, self.hunger + food.nutrition)

    # -------------------------
    # ИГРА (счастье)
    # -------------------------
    def play(self):
        self.happiness = min(100, self.happiness + 100)

    # -------------------------
    # ЗЕЛЬЕ ЭНЕРГИИ
    # -------------------------
    def use_energy_potion(self):
        self.energy = 100

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

        if sleep_duration >= 7200:  # 2 часа
            self.energy = 100

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