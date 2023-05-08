#Stuff
level = list()
runBefore = False
savedX = 0
savedY = 0
charX = 0
charY = 0
enemySavedX = 0
enemySavedY = 0
pointsNeeded = 0
whatLevel = 1
switchesOn = True
hasEnemy = False
points = 0

#Colours
red         = (200,  40,   0)
water       = (  0,  50, 200)
ice         = (175, 206, 209)
black       = (  0,   0,   0)
white       = (255, 255, 255)
grey        = (150, 150, 150)
groundDark  = (102,  64,  10)
groundLight = (135,  90,  16)
line        = (122, 144, 219)
lineDark    = ( 81,  94, 143)
wallLight   = (107,  29,  21)
wallDark    = ( 61,  17,  13)
backGround  = ( 22,  10,  87)
text        = (222, 218, 205)

# Inventory
player_items = {"red key": "assets/redKey.png",
         "toy box": "assets/toyBox.png",
         "socks": "assets/socks.png",
         "blue key": "assets/blueKey.png",
         "green key": "assets/greenKey.png",
         "flashlight": "assets/flashlight.png",
         }