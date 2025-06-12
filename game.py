import pygame
from characters import MainCharacter, CatEnemy
from inventory_module import Inventory
from settings import *


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.characters = pygame.sprite.Group()
        self.enemies = []
        self.inventory = Inventory()
        self.points = 0
        self.won = False
        self.dead = False
        self.started = False
        self.paused = False
        self.time_difference = 0
        self.calculated_time = 0
        self.now = 0

        self.main_character = MainCharacter()
        self.main_character.rect.x = 50 + (6 * 50)
        self.main_character.rect.y = 100 + (6 * 50)
        self.characters.add(self.main_character)
        self.enemies.append(CatEnemy())

    def reset(self):
        self.inventory = Inventory()
        self.points = 0
        self.dead = False
        self.started = False
        self.won = False
        self.paused = False
        self.time_difference = 0

    def draw_character(self):
        self.characters.draw(self.screen)
        pygame.display.update()

    def update(self):
        # Example update placeholder for game loop
        self.draw_character()
        # Additional update logic would go here
