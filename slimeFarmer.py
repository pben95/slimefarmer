import copy, random, math, pygame
colors = [pygame.image.load("assets/redSlime.jpg"),pygame.image.load("assets/blueSlime.jpg"),pygame.image.load("assets/yellowSlime.jpg"),
          pygame.image.load("assets/pinkSlime.jpg"),pygame.image.load("assets/purpleSlime.jpg"),pygame.image.load("assets/cyanSlime.jpg"),
          pygame.image.load("assets/orangeSlime.jpg"),pygame.image.load("assets/greySlime.jpg"),pygame.image.load("assets/greenSlime.jpg")]
farmbg = pygame.image.load("assets/farmbg.png")
natureBattle = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24],
                    [2, 4, 5, 7], [3, 4, 9, 10], [7, 8, 13, 14], [11, 12, 17, 18], [15, 16, 21, 22], [18, 20, 21, 23]]
natures = ["Cool", "Hardy", "Lonely", "Brave", "Adamant", "Careful", "Bold", "Docile", "Impish", "Lazy", "Timid",
           "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Quirky", "Rash", "Calm", "Gentle", "Sassy", "Naughty", "Bashful"]  #24
def natureCheck(s1, s2):
    multi = 1
    for j, i in enumerate(natureBattle):
        if s1 in i and s2 in i:
            if j <= 6:
                multi += 1
            if j > 6:
                multi -= 1
    if multi == 0:
        multi = 0.5
    print(multi)
    return multi

def nta(inp):  #0 is number to alpha, 1 is alpha to number
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    if isinstance(inp, str):
        for j, i in enumerate(alphabet):
            if inp == i:
                return int(len(alphabet[0:j]))
    elif isinstance(inp, int):
        return alphabet[inp-1]



def randomGene():
    gene = ""
    gene += str(random.randint(0,1))
    gene += nta(random.randint(1,24))
    for _ in range(0,4):
        gene += str(random.randint(0,1))
        gene += str(random.randint(1,9))
    return gene



class Player:
    def __init__(self):
        #self.name = name
        self.level = 0
        self.exp = 0
        self.money = 1200
        self.inv = []  #max 220
        self.jelly = [0, 0, 0] #  Red, Blue, Yellow
        self.farm = Farm("Farm")
        self.turn = 0
        self.itemSelected = None
        self.slimeSelected = None

class Slime:
    def __init__(self, name, gene):
        self.name = name
        self.gene = gene
        self.food = "Steak"
        self.outputAmt = 1
        self.lvl = 0
        self.exp = 0
        self.natureNum = nta(self.gene[1])
        self.nature = natures[self.natureNum]
        self.color = int(self.gene[3])
        self.health = int(self.gene[5])
        self.attack = int(self.gene[7])
        self.speed = int(self.gene[9])
        self.health = self.health * 10
        self.hp = self.health
        self.img = colors[self.color-1]
        self.rect = pygame.Rect(0,0,60,60)
        self.hover = False
    def feed(self, input):
        if input.name == self.food:
            self.XP(50)
        else:
            self.XP(20)
        player.inv.remove(input)
    def XP(self, amount):
        self.exp += amount
        if self.exp >= 100:
            self.exp -= 100
            self.lvl += 1
            self.outputAmt += 1
            self.attack += 1
            self.speed += 1
            self.hp += 10
            self.health += 10
    def mate(self, geneM, geneF):
        geneC = ""
        for i in range(0, 10, 2):
            num = None
            if i == 0:
                maleNum = nta(geneM[i + 1])
                femaleNum = nta(geneF[i + 1])
            else:
                maleNum = int(geneM[i + 1])
                femaleNum = int(geneF[i + 1])
            if (geneM[i] == "0" and geneF[i] == "0") or (geneM[i] == "1" and geneF[i] == "1"):
                geneC += geneM[i]
                randnum = random.randint(0,10)
                if randnum < 4:
                    geneC += geneM[i + 1]
                elif randnum > 6:
                    geneC += geneF[i + 1]
                else:
                    num = (maleNum * 0.75) + 2 * femaleNum
            elif geneM[i] == "0" and geneF[i] == "1":
                geneC += str(random.randint(0,1))
                if random.randint(0,4) == 0:
                    num = ( maleNum * 0.5) + .75 * femaleNum
                else:
                    geneC += geneM[i + 1]
            elif geneM[i] == "1" and geneF[i] == "0":
                geneC += str(random.randint(0,1))
                if random.randint(0,4) == 0:
                    num = .75 * maleNum + (femaleNum * 0.5)
                else:
                    geneC += geneF[i + 1]
            if num != None:
                num = int(math.floor(num))
                if num <= 0:
                    num = 1
                if i > 0 and num > 9:
                    num = 9
                elif i == 0 and num > 25:
                    num = 25
                if i == 0:
                    if random.randint(0, 50) == 0:
                        num = random.randint(1, 25)
                    num = nta(num)
                elif i > 0:
                    if random.randint(0, 50) == 0:
                        num = random.randint(1, 9)
                geneC += str(num)
        print(geneC)
        if len(player.farm.slimes) < 9:
            player.farm.slimes.append(Slime("Slime", geneC))
    def buy(self):
        if player.money >= 100 and len(player.farm.slimes) < 9:
            player.money -= 100
            player.farm.slimes.append(Slime("Slime", randomGene()))

class Farm:
    def __init__(self, name):
        self.name = name
        self.level = 0
        self.exp = 0
        self.slimes = [Slime("Slime","1a11111111"),Slime("Slime","1b12111111")]

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.hover = False
    def buy(self):
        if player.money >= self.price:
            player.money -= self.price
            player.inv.append(copy.copy(self))
    def sell(self):
        player.money += int(self.price * 0.75)
        player.inv.remove(self)
    def use(self):
        pass

enemySlime = Slime("Enemy", randomGene())

class Scene:
    def __init__(self, num, input):
        self.num = num
        self.input = input
        self.active = False
    def gui(self):
        global buttons, labels, lines
        if renderScene.num == 0 or renderScene.num == 3:
            screen.blit(farmbg, (0, 39))
        buttons = [
            screen.fill((20, 20, 150), pygame.Rect(0, 525, 200, 75)),  # left
            screen.fill((20, 20, 150), pygame.Rect(200, 525, 200, 75)),  # mid
            screen.fill((20, 20, 150), pygame.Rect(400, 525, 200, 75)),  # right
            screen.fill((255, 255, 255), pygame.Rect(0, 0, 600, 40))  # top
        ]
        labels = [
            screen.blit(pygame.font.Font(None, 36).render("Farm", False, (255, 255, 255)),
                        (buttons[0].x + 67, buttons[0].y + 30)),
            screen.blit(pygame.font.Font(None, 36).render("Inventory", False, (255, 255, 255)),
                        (buttons[1].x + 45, buttons[1].y + 30)),
            screen.blit(pygame.font.Font(None, 36).render("Market", False, (255, 255, 255)),
                        (buttons[2].x + 61, buttons[2].y + 30))
        ]
        lines = [
            pygame.draw.line(screen, (0, 0, 0), (195, 525), (195, 600), 5),
            pygame.draw.line(screen, (0, 0, 0), (395, 525), (395, 600), 5),
            pygame.draw.line(screen, (0, 0, 0), (0, 525), (600, 525), 5),
            pygame.draw.line(screen, (0, 0, 0), (0, 40), (600, 40), 5)
        ]
        screen.blit(pygame.font.Font(None, 24).render(
            "Level: " + str(player.level) + " [" + str(player.exp) + "/100], Money: " + str(player.money), False,
            (0, 0, 0), (255, 255, 255)), (0, 0))
        if player.slimeSelected != None:
            screen.blit(pygame.font.Font(None, 24).render(player.slimeSelected.gene, False,(0, 0, 0), (255, 255, 255)), (300,0))
    def render(self):
        self.gui()
        if self.num == 0:
            slimePos = [[75, 125], [275, 125], [475, 125], [75, 250], [275, 250], [475, 250], [75, 375], [275, 375], [475, 375]]
            for j, i in enumerate(player.farm.slimes):
                i.rect.x, i.rect.y = slimePos[j]
                screen.blit(i.img, (i.rect.x, i.rect.y))
                screen.blit(pygame.font.Font(None, 24).render(i.gene + " : " + str(i.lvl) + " [" + str(i.exp) + "/100]",
                                                              False,(0, 0, 0), (255, 255, 255)), (i.rect.x - 70, i.rect.y + 60))
                screen.blit(pygame.font.Font(None, 24).render(i.nature + " H:" + str(i.hp) + "/" + str(i.health) + " A:" + str(i.attack) + " S:" + str(i.speed),
                                                              False,(0,0,0), (255,255,255)), (i.rect.x - 70 , i.rect. y + 80))
            screen.blit(pygame.font.Font(None, 24).render("Farm", False, (0, 0, 0), (255, 255, 255)), (0, 17))
        elif self.num == 1:
            xCount = 0
            for j, i in enumerate(player.inv):
                xCount += 1
                if j % 9 == 0:
                    xCount = 0
                i.rect.x, i.rect.y = (xCount * 60), (4 + math.floor(j / 9)) * 20
                if i.hover == True:
                    screen.blit(pygame.font.Font(None, 24).render(i.name, False, (255, 255, 255), (0, 0, 0)),(i.rect.x, i.rect.y))
                else:
                    screen.blit(pygame.font.Font(None, 24).render(i.name, False, (0, 0, 0), (255, 255, 255)),(i.rect.x, i.rect.y))
            screen.blit(pygame.font.Font(None, 24).render("Inventory", False, (0, 0, 0), (255, 255, 255)), (0, 17))
        elif self.num == 2:
            xCount = 0
            global marketList
            marketList = [Slime("Slime", randomGene()), Item("Steak",10)]
            for j, i in enumerate(marketList):
                xCount += 1
                if j % 9 == 0:
                    xCount = 0
                i.rect.x, i.rect.y = i.rect.x, i.rect.y = 8 + (xCount * 66), (4 + math.floor(j / 9)) * 20
                screen.blit(pygame.font.Font(None, 24).render(i.name, False, (255, 255, 255), (0, 0, 0)),(i.rect.x, i.rect.y))
            screen.blit(pygame.font.Font(None, 24).render("Market", False, (0, 0, 0), (255, 255, 255)), (0, 17))
        elif self.num == 3:
            self.input.rect.x,self.input.rect.y = [40,400]
            screen.blit(self.input.img, self.input.rect)
            screen.blit(pygame.font.Font(None, 24).render(
                self.input.nature + " H:" + str(self.input.hp) + "/" + str(self.input.health) + "A:" + str(self.input.attack) + " S:" + str(self.input.speed),
                False, (0, 0, 0),(255, 255, 255)), (10, 460))
            pygame.draw.line(screen, (255, 0, 0), (10, 480), (160, 480), 5)
            pygame.draw.line(screen, (0, 255, 0), (10, 480), (10+(self.input.hp/self.input.health)*150, 480), 5)
            enemySlime.rect.x,enemySlime.rect.y = [470,140]
            screen.blit(enemySlime.img, enemySlime.rect)
            screen.blit(pygame.font.Font(None, 24).render(
                enemySlime.nature + " H:" + str(enemySlime.hp) + "/" + str(enemySlime.health) + " A:" + str(enemySlime.attack) + " S:" + str(enemySlime.speed),
                False, (0, 0, 0),(255, 255, 255)), (420, 200))
            pygame.draw.line(screen, (255, 0, 0), (420, 220), (570, 220), 5)
            pygame.draw.line(screen, (0, 255, 0), (420, 220), (420 + (enemySlime.hp/enemySlime.health)*150, 220), 5)
            screen.blit(pygame.font.Font(None, 24).render("Battle", False, (0, 0, 0), (255, 255, 255)), (0, 17))

player = Player()
pygame.init()
screen = pygame.display.set_mode((600, 600))
done = False
sceneList = [  #Scene reference
    Scene(0, player.farm.slimes),  #Farm
    Scene(1, player.inv),  #Inventory
    Scene(2, player.inv),  #Market
    Scene(3, player.slimeSelected)  #Battle
]
renderScene = sceneList[0]

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #pygame.time.set_timer(pygame.MOUSEBUTTONDOWN,500)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons[0].collidepoint(pygame.mouse.get_pos()):
                renderScene = sceneList[0]
            elif buttons[1].collidepoint(pygame.mouse.get_pos()):
                renderScene = sceneList[1]
            elif buttons[2].collidepoint(pygame.mouse.get_pos()):
                renderScene = sceneList[2]
            else:
                if renderScene.num == 0:
                    for i in player.farm.slimes:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            if player.itemSelected != None:
                                i.feed(player.itemSelected)
                                player.itemSelected = None
                                if len(player.inv) > 0:
                                    renderScene = sceneList[1]
                            if player.slimeSelected != None and len(player.farm.slimes) > 1:
                                i.mate(player.slimeSelected.gene,i.gene)
                                player.slimeSelected = None
                            elif player.slimeSelected == None:
                                player.slimeSelected = i
                elif renderScene.num == 1:
                    for i in player.inv:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            player.itemSelected = i
                            renderScene = sceneList[0]
                elif renderScene.num == 2:
                    for i in marketList:
                        if i.rect.collidepoint(pygame.mouse.get_pos()):
                            i.buy()
                elif renderScene.num == 3:
                    if player.slimeSelected.rect.collidepoint(pygame.mouse.get_pos()):
                        enemySlime.hp -= int(math.ceil(.5*(player.slimeSelected.attack)) * natureCheck(enemySlime.natureNum, player.slimeSelected.natureNum))
                        player.slimeSelected.hp -= int(math.ceil(.5*(enemySlime.attack)) * (1/natureCheck(enemySlime.natureNum, player.slimeSelected.natureNum)))
                        if player.slimeSelected.hp <= 0:
                            player.farm.slimes.remove(player.slimeSelected)
                            player.slimeSelected = None
                            renderScene = sceneList[0]
                        else:
                            if enemySlime.hp <= 0:
                                enemySlime.hp = 0
                                player.slimeSelected.hp = player.slimeSelected.health
                                player.money += 100
                                player.slimeSelected.XP(10)
                                player.slimeSelected = None
                                renderScene = sceneList[0]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if renderScene.num == 0:
                for i in player.farm.slimes:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        player.money += 100 + i.exp + (100 * i.lvl)
                        player.farm.slimes.remove(i)
                        break
                player.slimeSelected = None
            elif renderScene.num == 1:
                for i in player.inv:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        i.sell()
                        break
        elif event.type == pygame.MOUSEMOTION:
            if renderScene.num == 0 or renderScene.num == 1:
                for i in renderScene.input:
                    i.hover = i.rect.collidepoint(pygame.mouse.get_pos())

    screen.fill((0,0,0))
    renderScene.render()
    pygame.display.flip()