import pygame

class Inventory:
    def __init__(self):
        self.redKey = False
        self.blueKey = False
        self.greenKey = False
        self.rainbowKey = False
        self.waterBoot = False
        self.iceSkate = False
        self.socks = False
        self.flashlight = False
        self.invNum = 0
        self.allInvent = []
        self.inventPics = []
        self.picIndex = []
        self.set_images()

    def set_images(self):
        images = [
            "assets/red_key.png",
            "assets/toy_box.png",
            "assets/socks.png",
            "assets/blue_key.png",
            "assets/green_key.png",
            "assets/socks.png",
            "assets/flashlight.png",
        ]
        for path in images:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            self.inventPics.append(image)

    def add_item(self, item, index):
        self.allInvent.append(item)
        self.picIndex.append(index)

    def remove_item(self, item, index):
        if item in self.allInvent:
            self.allInvent.remove(item)
        if index in self.picIndex:
            self.picIndex.remove(index)

    def get_item(self, index):
        return self.allInvent[index]

    def return_invent_len(self):
        return len(self.allInvent)

    def return_pic(self, pic_position):
        return self.inventPics[self.picIndex[pic_position]]

    # Key/item methods
    def get_red_key(self):
        self.redKey = True
        self.add_item("redKey", 0)

    def lose_red_key(self):
        self.remove_item("redKey", 0)
        if self.allInvent.count("redKey") == 0:
            self.redKey = False

    def return_red_key(self):
        return self.redKey

    def get_blue_key(self):
        self.blueKey = True
        self.add_item("blueKey", 3)

    def lose_blue_key(self):
        self.remove_item("blueKey", 3)
        if self.allInvent.count("blueKey") == 0:
            self.blueKey = False

    def return_blue_key(self):
        return self.blueKey

    def get_green_key(self):
        self.greenKey = True
        self.add_item("greenKey", 4)

    def lose_green_key(self):
        self.remove_item("greenKey", 4)
        if self.allInvent.count("greenKey") == 0:
            self.greenKey = False

    def return_green_key(self):
        return self.greenKey

    def return_water_boot(self):
        return self.waterBoot

    def get_water_boot(self):
        self.waterBoot = True
        self.add_item("waterBoot", 1)

    def lose_water_boot(self):
        self.waterBoot = False
        self.remove_item("waterBoot", 1)

    def get_socks(self):
        self.socks = True
        self.add_item("socks", 5)

    def lose_socks(self):
        self.socks = False
        self.remove_item("socks", 5)

    def return_socks(self):
        return self.socks

    def get_flashlight(self):
        self.flashlight = True
        self.add_item("flashlight", 6)

    def lose_flashlight(self):
        self.flashlight = False
        self.remove_item("flashlight", 6)

    def return_flashlight(self):
        return self.flashlight

    def get_ice_skate(self):
        self.iceSkate = True
        self.add_item("iceSkate", 2)

    def lose_ice_skate(self):
        self.iceSkate = False
        self.remove_item("iceSkate", 2)

    def return_ice_skate(self):
        return self.iceSkate
