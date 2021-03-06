import copy, random, math, pygame
colors = [pygame.image.load("assets/blueSlime.png"),pygame.image.load("assets/redSlime.png"),pygame.image.load("assets/yellowSlime.png"),  #slime images for each color
          pygame.image.load("assets/orangeSlime.png"),pygame.image.load("assets/greenSlime.png"),pygame.image.load("assets/cyanSlime.png"),
          pygame.image.load("assets/pinkSlime.png"),pygame.image.load("assets/purpleSlime.png"),pygame.image.load("assets/greySlime.png")]
farmbg = pygame.image.load("assets/farmbg.png")
worldmap = pygame.image.load("assets/worldmap.png")
natureBattle = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24],  #rock paper scissors for slime nature damage
                    [2, 4, 5, 7], [3, 4, 9, 10], [7, 8, 13, 14], [11, 12, 17, 18], [15, 16, 21, 22], [18, 20, 21, 23]]
natures = ["Cool", "Hardy", "Lonely", "Brave", "Adamant", "Careful", "Bold", "Docile", "Impish", "Lazy", "Timid", "Hasty",   #slime nature names, from pokemon :)
           "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Quirky", "Rash", "Calm", "Gentle", "Sassy", "Naughty", "Bashful"]  #24
mapPoints = [ pygame.Rect(10,350,150,150),"Island",
              pygame.Rect(350,350,170,150),"Desert",
              pygame.Rect(200,250,150,150),"Plain",
              pygame.Rect(300,70,200,200),"Forest",
              pygame.Rect(80,50,200,200),"Mountain"]

class Player:
    def __init__(self):
        self.money = 100
        self.inv = [Item("Steak", 10)]
        self.itemX = None
        self.slimeX = None
        self.slimes = [Slime("Slime", game.randomGene(3)), Slime("Slime", game.randomGene(3))]
        self.battle = False
        self.map = "Island"
        self.diff = 1

class Game:  #game class, has some game functions in it
    def natureCheck(self, s1, s2):  #checks damage multiplier for slime nature R-P-S
        multi = 1
        for j, i in enumerate(natureBattle):
            if s1 in i and s2 in i:
                if j <= 6:
                    multi += 1
                if j > 6:
                    multi -= 1
        if multi == 0:
            multi = 0.5
        return multi
    def nta(self, inp):  #converts a number to a letter, or letter to number. a-z, 1-26
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        if isinstance(inp, str):
            for j, i in enumerate(alphabet):
                if inp == i:
                    return int(len(alphabet[0:j]))
        elif isinstance(inp, int):
            return alphabet[inp-1]
    def randomGene(self, max = 9):  #makes a random slime gene.
        gene = ""
        gene += str(random.randint(0,1))  #even indexes are dominant 0 and resessive 1
        gene += self.nta(random.randint(1,25))  #converts number to letter to get slime nature
        if max > 1:
            min = max - 2
        else:
            min = 1
        for _ in range(0,4):  #color, health, attack, speed
            gene += str(random.randint(0,1))
            gene += str(random.randint(min,max))
        return gene

class Slime:  #slime class, very useful :)
    def __init__(self, name, gene):
        self.name = name
        self.gene = gene  #currently 10 char long, 5 values, nature color health attack speed. see randomGene()
        self.lvl = 1
        self.exp = 0
        self.natureNum = game.nta(self.gene[1])  #1-25, place in natures list
        self.nature = natures[self.natureNum]  #slime's nature, used in damage rock-paper-scissors
        self.color = int(self.gene[3])  #slime's color, 9 choices
        self.health = int((self.lvl/2) * int(self.gene[5]) * 10) #multiplied by 10 to get hit points, going to change probably
        self.attack = self.lvl * int(self.gene[7])  #damage, probably going to change
        self.speed = self.lvl * int(self.gene[9])  #speed, probably going to change
        self.hp = self.health
        self.img = colors[self.color-1]  #image, based on color
        self.rect = pygame.Rect(0,0,60,60)  #pygame rect for mouse detection
    def XP(self, amount):  #gives EXP to slime, then checks if level up
        self.exp += amount
        if self.exp >= 100:
            self.exp -= 100
            self.lvl += 1
            self.attack = int(self.lvl * int(self.gene[7]))
            self.speed = int(self.lvl * int(self.gene[9]))
            self.health = int((self.lvl/2) * int(self.gene[5]) * 10)
            self.hp = self.health
    def mate(self, geneM, geneF):  #slime mating. even indexes of gene determine dominance or ressiveness
        if player.money >= 100 and geneM.lvl > 0 and geneF.lvl > 0:
            if random.randint(0,1) == 0:
                geneM.lvl -= 1
            else:
                geneF.lvl -= 1
            player.money -= 100
            geneC = ""
            for i in range(0, 10, 2):
                num = None
                if i == 0:  #check if doing nature value since it's letter instead of number
                    maleNum, femaleNum = game.nta(geneM.gene[i + 1]), game.nta(geneF.gene[i + 1])
                else:
                    maleNum, femaleNum = int(geneM.gene[i + 1]), int(geneF.gene[i + 1])
                if (geneM.gene[i] == "0" and geneF.gene[i] == "0") or (geneM.gene[i] == "1" and geneF.gene[i] == "1"):  #if both dom/res
                    geneC += geneM.gene[i]
                    randnum = random.randint(0,10)
                    if randnum < 4:
                        geneC += geneM.gene[i + 1]
                    elif randnum > 6:
                        geneC += geneF.gene[i + 1]
                    else:
                        num = (maleNum * 0.75) + 2 * femaleNum
                elif geneM.gene[i] == "0" and geneF.gene[i] == "1":  #if male dom
                    geneC += str(random.randint(0,1))
                    if random.randint(0,4) == 0:
                        num = ( maleNum * 0.25) + .75 * femaleNum
                    else:
                        geneC += geneM.gene[i + 1]
                elif geneM.gene[i] == "1" and geneF.gene[i] == "0":  #if female dom
                    geneC += str(random.randint(0,1))
                    if random.randint(0,4) == 0:
                        num = .75 * maleNum + (femaleNum * 0.25)
                    else:
                        geneC += geneF.gene[i + 1]
                if num != None:  #if there isn't straight inheritance from a parent, this fixes the edited value
                    num = int(math.floor(num))
                    if num <= 0:
                        num = 1
                    if i > 0 and num > 9:
                        num = 9
                    elif i == 0 and num > 25:
                        num = 25
                    if i == 0:
                        if random.randint(0, 50) == 0:  #mutation!
                            num = random.randint(1, 25)
                        num = game.nta(num)
                    elif i > 0:
                        if random.randint(0, 50) == 0:   #mutation!
                            num = random.randint(2, 6)
                    geneC += str(num)
            if len(player.slimes) < 9:  #adds child to farm if less than 9 slimes
                player.slimes.append(Slime("Slime", geneC))

class Item:  #item's pretty much only food right now
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.rect = pygame.Rect(0, 0, 30, 30)
    def buy(self):  #buys item, clones self info player inv if enough money
        if player.money >= self.price:
            player.money -= self.price
            player.inv.append(copy.copy(self))
    def sell(self):  #sells item, gives back % of value
        player.money += int(self.price * 0.75)
        player.inv.remove(self)
    def use(self, slime):  #uses item
        if self.name == "Steak":
            slime.XP(25)
        player.inv.remove(self)

class Scene:  #handling different scenes (farm, inv, market, battle). want to rework to be less shitty
    def __init__(self, num):
        self.num = num  #scene number for render function
    def gui(self):  #render's GUI firstly and separetely from everything else
        screen.fill((24, 76, 48))
        global buttons, labels, lines
        if renderScene.num == 0 or renderScene.num == 3:  #renders background at farm and battle
            screen.blit(farmbg, (0, 39))
        elif renderScene.num == 4:  #renders worldmap at map
            screen.blit(worldmap, (0, 39))
        buttons = [screen.fill((20, 20, 150), pygame.Rect(0, 525, 200, 75)),  # left
            screen.fill((20, 20, 150), pygame.Rect(200, 525, 200, 75)),  # mid
            screen.fill((20, 20, 150), pygame.Rect(400, 525, 200, 75)),  # right
            screen.fill((255, 255, 255), pygame.Rect(0, 0, 600, 40))]  # top
        labels = [screen.blit(pygame.font.Font(None, 36).render("Farm", False, (255, 255, 255)),  #farm scene label
                        (buttons[0].x + 67, buttons[0].y + 30)),
            screen.blit(pygame.font.Font(None, 36).render("Inventory", False, (255, 255, 255)),  #battle scene label
                        (buttons[1].x + 45, buttons[1].y + 30)),
            screen.blit(pygame.font.Font(None, 36).render("Map", False, (255, 255, 255)),  #market scene label
                        (buttons[2].x + 61, buttons[2].y + 30))]
        lines = [pygame.draw.line(screen, (0, 0, 0), (195, 525), (195, 600), 5),  #left bottom vertical line
            pygame.draw.line(screen, (0, 0, 0), (395, 525), (395, 600), 5),  #right bottom vertical line
            pygame.draw.line(screen, (0, 0, 0), (0, 525), (600, 525), 5),  #bottom horizontal line
            pygame.draw.line(screen, (0, 0, 0), (0, 40), (600, 40), 5)]  #top horizontal line
        if player.itemX != None:
            info = "Money: " + str(player.money) + ", " + player.map + ", " + player.itemX.name
        elif player.itemX == None:
            info = "Money: " + str(player.money) + ", " + player.map
        screen.blit(pygame.font.Font(None, 24).render(info, False,(0, 0, 0), (255, 255, 255)), (0, 0))
        if player.slimeX != None:  #if slime selected, renders it's info
            screen.blit(pygame.font.Font(None, 24).render(player.slimeX.gene, False,(0, 0, 0), (255, 255, 255)), (300,0))
    def render(self):  #render's the GUI then the scene
        self.gui()  #renders the GUI
        if self.num == 0:  #farm
            slimePos = [[75, 125], [275, 125], [475, 125], [75, 250], [275, 250], [475, 250], [75, 375], [275, 375], [475, 375]]
            for j, i in enumerate(player.slimes):
                i.rect.x, i.rect.y = slimePos[j]  #nice formatting for 3x3 slime grid
                screen.blit(i.img, (i.rect.x, i.rect.y))  #slime's image
                screen.blit(pygame.font.Font(None, 24).render(i.gene + " : " + str(i.lvl) + " [" + str(i.exp) + "/100]",  #slime info under name
                                                              False,(0, 0, 0), (255, 255, 255)), (i.rect.x - 70, i.rect.y + 60))
                screen.blit(pygame.font.Font(None, 24).render(i.nature + " H:" + str(i.hp) + "/" + str(i.health) + " A:" + str(i.attack) + " S:" + str(i.speed),  #more info under name
                                                              False,(0,0,0), (255,255,255)), (i.rect.x - 70 , i.rect. y + 80))
            screen.blit(pygame.font.Font(None, 24).render("Farm", False, (0, 0, 0), (255, 255, 255)), (0, 17))  #renders farm label if farm scene
        elif self.num == 1:
            xCount = 0  #inventory, combine with market?
            for j, i in enumerate(player.inv):
                xCount += 1
                if j % 9 == 0:
                    xCount = 0
                i.rect.x, i.rect.y = (xCount * 60), (4 + math.floor(j / 9)) * 20
                screen.blit(pygame.font.Font(None, 24).render(i.name, False, (0, 0, 0), (255, 255, 255)),(i.rect.x, i.rect.y))
            screen.blit(pygame.font.Font(None, 24).render("Inventory", False, (0, 0, 0), (255, 255, 255)), (0, 17))  #renders inventory label if inventory scene
        elif self.num == 2:  #market
            global marketList
            marketList, xCount = [Slime("Slime", game.randomGene()), Item("Steak",10)], 0
            for j, i in enumerate(marketList):  #shows all items in marketlist, generalized and expandable :)
                xCount += 1
                if j % 9 == 0:
                    xCount = 0
                i.rect.x, i.rect.y = 8 + (xCount * 66), (4 + math.floor(j / 9)) * 20
                screen.blit(pygame.font.Font(None, 24).render(i.name, False, (0, 0, 0), (255, 255, 255)),(i.rect.x, i.rect.y))
            screen.blit(pygame.font.Font(None, 24).render("Market", False, (0, 0, 0), (255, 255, 255)), (0, 17))  #renders market label if market scene
        elif self.num == 3:  #battle
            player.slimeX.rect.x,player.slimeX.rect.y = [40,400]  #puts player slime in bottom left
            screen.blit(player.slimeX.img, player.slimeX.rect)  #player slime img
            screen.blit(pygame.font.Font(None, 24).render(  #renders player slime info
                player.slimeX.nature + " H:" + str(player.slimeX.hp) + "/" + str(player.slimeX.health) + "A:" + str(player.slimeX.attack) + " S:" + str(player.slimeX.speed),
                False, (0, 0, 0),(255, 255, 255)), (10, 460))
            pygame.draw.line(screen, (255, 0, 0), (10, 480), (160, 480), 5)  #health bar red
            pygame.draw.line(screen, (0, 255, 0), (10, 480), (10+(player.slimeX.hp/player.slimeX.health)*150, 480), 5)  #health bar green
            enemySlime.rect.x,enemySlime.rect.y = [470,140]  #puts enemy slime in top right
            screen.blit(enemySlime.img, enemySlime.rect)  #enemy slime img
            screen.blit(pygame.font.Font(None, 24).render(  #renders enemy slime info
                enemySlime.nature + " H:" + str(enemySlime.hp) + "/" + str(enemySlime.health) + " A:" + str(enemySlime.attack) + " S:" + str(enemySlime.speed),
                False, (0, 0, 0),(255, 255, 255)), (420, 200))
            pygame.draw.line(screen, (255, 0, 0), (420, 220), (570, 220), 5)  #health bar red
            pygame.draw.line(screen, (0, 255, 0), (420, 220), (420 + (enemySlime.hp/enemySlime.health)*150, 220), 5)  #health bar green
            screen.blit(pygame.font.Font(None, 24).render("Battle", False, (0, 0, 0), (255, 255, 255)), (0, 17))  #renders battle label if battle

game = Game()
player = Player()
pygame.init()
screen = pygame.display.set_mode((600, 600))  #sets window size at 600x600
done = False
enemySlime = Slime("Enemy", game.randomGene(3))
renderScene = Scene(0)  #sets current render scene. 0 farm 1 inv 2 market 3 battle 4 map
while not done:
    if len(player.slimes) == 0:
        done = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #pygame.time.set_timer(pygame.MOUSEBUTTONDOWN,500)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  #left mouse button down
            if buttons[0].collidepoint(pygame.mouse.get_pos()) and not player.battle:  #click left button, go to farm
                renderScene.num = 0
            elif buttons[1].collidepoint(pygame.mouse.get_pos()) and not player.battle:  #click middle button, go to inv
                renderScene.num = 1
            elif buttons[2].collidepoint(pygame.mouse.get_pos()) and not player.battle:  #click right button, go to map
                renderScene.num = 4
            elif buttons[3].collidepoint(pygame.mouse.get_pos()) and not player.battle:
                pass
            else:
                if renderScene.num == 0:  #if farm
                    for i in player.slimes:  #check if click slime
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            if player.itemX != None:  #check if item selected, feed to slime
                                player.itemX.use(i)
                                player.itemX = None
                                if len(player.inv) > 0:  #go back to inv if not empty
                                    renderScene.num = 1
                            if player.slimeX != None and i != player.slimeX:  #if slime selected and there are 2
                                i.mate(player.slimeX,i)  #mate two slimes
                                player.slimeX = None
                            elif player.slimeX == None and player.itemX == None:  #selects slime if none selected
                                player.slimeX = i
                            elif i == player.slimeX and player.itemX == None:
                                enemySlime = Slime("Enemy", game.randomGene(player.diff))
                                player.battle = True
                                renderScene.num = 3
                elif renderScene.num == 1:  #if inventory
                    for i in player.inv:  #selects item, brings to farm scene
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            player.itemX = i
                            renderScene.num = 0
                elif renderScene.num == 2:  #if market
                    for i in marketList:  #selects item in marketList, buys it
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            i.buy()  #every item has own buy function, clones itself if sufficient funds
                elif renderScene.num == 3:  #if battle
                    if player.slimeX.rect.collidepoint(pygame.mouse.get_pos()):  #click your slime to attack and receive damage
                        enemySlime.hp -= int(math.ceil(.5*(player.slimeX.attack)) * game.natureCheck(enemySlime.natureNum, player.slimeX.natureNum))  #enemy damage, natureCheck
                        player.slimeX.hp -= int(math.ceil(.5*(enemySlime.attack)) * (1/game.natureCheck(enemySlime.natureNum, player.slimeX.natureNum)))  #player damage, natureCheck
                        if player.slimeX.hp <= 0:  #if player slime loses all HP, permadeath!
                            player.money -= 100
                            if player.money < 0:
                                player.money = 0
                            player.slimeX.hp = player.slimeX.health
                            player.slimeX = None
                            player.battle = False
                            renderScene.num = 0 #back to farm scene
                        else:
                            if enemySlime.hp <= 0:  #if enemy slime 0 hp, get money and xp
                                enemySlime.hp = 0  #so health bar doesn't go backwards :)
                                player.slimeX.hp = player.slimeX.health  #heals your slime for now
                                player.money += 50
                                player.slimeX.XP(int(math.ceil((enemySlime.attack+enemySlime.speed+(enemySlime.health/10))/3))*10)
                                if random.randint(0,20) == 0:
                                    player.inv.append(Item("Steak", 10))
                                player.slimeX = None
                                player.battle = False
                                renderScene.num = 0  #back to farm
                elif renderScene.num == 4:  #if map
                    for i in range(len(mapPoints)):
                        if not isinstance(mapPoints[i], str) and mapPoints[i].collidepoint(pygame.mouse.get_pos()):
                            player.map = mapPoints[i + 1]
                            player.diff = i + 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  #if right mouse button down
            if renderScene.num == 0:  #if farm
                for i in player.slimes:  #removes slime if right clicked
                    if i.rect.collidepoint(pygame.mouse.get_pos()) and len(player.slimes) > 2:  #need 2 slimes
                        #player.money += 100 + i.exp + (100 * i.lvl) #gives player money based on slime's level/exp
                        player.slimes.remove(i)
                        break
                player.slimeX = None  #deselects slime if right click
                player.itemX = None  #deselects item if right click
            elif renderScene.num == 1:  #if inventory
                for i in player.inv:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):  #sells item in inventory if right clicked
                        i.sell()
                        break
    screen.fill((0,0,0))  #clears screen before render
    renderScene.render()  #renders scene
    pygame.display.flip()  #flips display