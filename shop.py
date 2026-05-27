import pygame


class Shop:
    def __init__(self, screen, pet, ui, shop_bg):  # добавили shop_bg
        self.screen = screen
        self.pet = pet
        self.ui = ui
        self.shop_bg = shop_bg  # сохраняем
        self.message = ""
        self.message_timer = 0

        # товары
        self.hat_item = self.load_item("images/items/hat.png", (100, 100))
        self.glasses_item = self.load_item("images/items/glasses.png", (100, 60))
        self.potion_item = self.load_item("images/items/energetic.png", (60, 100))  # зелье

        # области для покупки
        self.hat_shop_rect = pygame.Rect(290, 353, 100, 100)
        self.glasses_shop_rect = pygame.Rect(390, 383, 100, 60)
        self.potion_shop_rect = pygame.Rect(500, 353, 60, 100)  # зелье

    def load_item(self, path, size):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    def handle_click(self, mouse_pos):
        current_time = pygame.time.get_ticks()

        # ШЛЯПА
        if self.hat_shop_rect.collidepoint(mouse_pos) and not self.pet.hat_owned:
            if self.pet.coins >= 50:
                self.pet.hat_owned = True
                self.pet.coins -= 50
                self.message = "Купили шляпу!"
            else:
                self.message = "Не хватает монет! Нужно 50"
            self.message_timer = current_time

        # ОЧКИ
        if self.glasses_shop_rect.collidepoint(mouse_pos) and not self.pet.glasses_owned:
            if self.pet.coins >= 30:
                self.pet.glasses_owned = True
                self.pet.coins -= 30
                self.message = "Купили очки!"
            else:
                self.message = "Не хватает монет! Нужно 30"
            self.message_timer = current_time

        # ЗЕЛЬЕ (отдельный блок, не внутри очков!)
        if self.potion_shop_rect.collidepoint(mouse_pos):
            print(f"Попытка купить зелье. Монет: {self.pet.coins}")
            if self.pet.coins >= 105:
                self.pet.coins -= 105
                if self.pet.sleeping:
                    self.pet.sleeping = False
                    self.pet.energy = min(100, self.pet.energy + 30)
                    self.message = "Использовали зелье бодрости! Питомец проснулся!"
                else:
                    self.pet.energy = min(100, self.pet.energy + 30)
                    self.message = "Использовали зелье! Энергия +30!"
                print("Зелье куплено!")
            else:
                self.message = f"Не хватает монет! Нужно 105 (у вас {self.pet.coins})"
                print(f"Не хватает на зелье. Нужно 105, есть {self.pet.coins}")
            self.message_timer = current_time

        # закрытие магазина
        if self.ui.close_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self, current_time):
        self.screen.blit(self.shop_bg, (0, 0))

        # товары
        self.screen.blit(self.hat_item, (290, 353))
        self.screen.blit(self.glasses_item, (390, 383))
        self.screen.blit(self.potion_item, (500, 353))  # зелье

        # цены
        price_text = self.ui.font.render("50", True, (255, 215, 0))
        self.screen.blit(price_text, (325, 460))
        price_text2 = self.ui.font.render("30", True, (255, 215, 0))
        self.screen.blit(price_text2, (427, 450))
        price_text3 = self.ui.font.render("105", True, (255, 215, 0))  # цена зелья
        self.screen.blit(price_text3, (520, 460))

        # сообщение
        if self.message and current_time - self.message_timer < 2000:
            msg_text = self.ui.font.render(self.message, True, (255, 255, 255))
            msg_bg = pygame.Rect(200, 500, 400, 50)
            pygame.draw.rect(self.screen, (0, 0, 0), msg_bg)
            pygame.draw.rect(self.screen, (255, 255, 255), msg_bg, 2)
            self.screen.blit(msg_text, (220, 515))

        # кнопка закрытия
        pygame.draw.rect(self.screen, (200, 50, 50), self.ui.close_rect)
        close_text = self.ui.font.render("X", True, (255, 255, 255))
        self.screen.blit(close_text, (728, 48))
