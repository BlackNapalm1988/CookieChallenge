import pygame

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.boardX = 0
        self.boardY = 0
        character_image = pygame.image.load("assets/temp_character.png")
        self.image = pygame.transform.scale(character_image, (50, 50)).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, centre):
        self.rect.center = centre

class CatEnemy:
    def __init__(self):
        character_image = pygame.image.load("assets/enemy_one.png")
        self.image = pygame.transform.scale(character_image, (50, 50)).convert_alpha()
        self.set_xy(0, 0)
        self.set_direction(1)
        self.drawing = False
        self.positionX = 0
        self.positionY = 0
        self.change = False
        self.boardX = 0
        self.boardY = 0

    def set_board_position(self, x, y):
        self.boardX = x
        self.boardY = y

    def set_xy(self, x, y):
        self.positionX = x
        self.positionY = y

    def set_direction(self, direction):
        self.direction = direction

    def set_drawing(self, drawing):
        self.drawing = drawing

    def get_image(self):
        return self.image

    def get_drawing(self):
        return self.drawing

    def get_direction(self):
        return self.direction

    def change_direction(self, change):
        self.change = change

    def get_change(self):
        return self.change

    def get_position_x(self):
        return self.positionX

    def get_position_y(self):
        return self.positionY

    def get_board_x(self):
        return self.boardX

    def get_board_y(self):
        return self.boardY
