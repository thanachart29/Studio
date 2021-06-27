from turtle import color
import xlsxwriter
import pygame
import math

class button:
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.Font('angsana.ttc',26)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True       
       
        return False


class ball:
    def __init__(self, x, y , color ):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 2
        self.setheigh = 0
        self.setwidth = 0.1
        self.pichigh = 55
        self.picwidth = 421

    def moving(self,rad,screen):
        a = 0 
        time = 0 
        v = math.sqrt((-g*((self.setwidth)**2))/(2*((math.cos(rad))**2)*(-self.setheigh-(self.setwidth* (math.tan(rad)) ) ) ) )
        self.velo = v
        instant_y = self.y - ( self.setheigh * 250 )
        render_x = self.x
        while a != 1:
            distance_x = ( v * (math.cos(rad)) * time ) *250
            distance_y = ( (v * (math.sin(rad)) * time) + (-0.5 * g * ((time) ** 2)) ) *250
            render_y = instant_y - distance_y
            pygame.draw.circle(screen, (0, 0, 0), (render_x ,render_y), self.radius)
            pygame.display.update()
            time += 0.0015
            render_x = distance_x + self.x
            if render_y > (self.y + 1 ) :
                a += 1

        
        output_velo = 'v : ' + str(round(v,5)) + '  m/s'
        self.text_output_velo = font.render(output_velo , True , (255,255,255))

    def ballenergy(self,mass,k,rad):
        self.DeltaX = ( ( -2 * mass * g * math.sin(rad) ) + math.sqrt( ( ( 2 * mass * g * math.sin(rad) ) ** 2 ) + 4 * k * mass * (self.velo**2) ) ) / ( 2 * k )
        # self.k = ( ((2*mass*g*x*(math.sin(rad))) - (mass*(self.velo**2))) / (-(x**2)) )
        displacement_spring = 'x : ' + str(round(self.DeltaX,5)) + '  m'
        self.text_displacement_spring = font.render(displacement_spring , True , (255,255,255))

    def SetSy(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.setheigh < 2.3 :
                    self.setheigh += 0.1
                    self.pichigh += 25
            elif event.key == pygame.K_DOWN:
                if self.setheigh > 0 :
                    self.setheigh -= 0.1
                    self.pichigh -= 25
    
    def SetSx(self):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.setwidth > 0.1:
                        self.setwidth -= 0.1
                        self.picwidth -= 25
                elif event.key == pygame.K_RIGHT:
                    if self.setwidth < 3:
                        self.setwidth += 0.1    
                        self.picwidth += 25

    def render(self,screen):
        screen.blit(SetSyPic,(380,heighscreen-self.pichigh))
        screen.blit(SetSxPic,(self.picwidth,heighscreen-40))
    

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = clrblue3
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def Boxevent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = clrblue2 if self.active else clrblue3
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box
        width = max(18, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


pygame.init()
g = 9.80665
widthscreen = 1280
heighscreen = 720
screen = pygame.display.set_mode((widthscreen,heighscreen))
pygame.display.set_caption('Spring Launcher Simulation')
icon = pygame.image.load('Launcher.PNG')
pygame.display.set_icon(icon)

background3 = pygame.image.load('BG3.PNG')
background4 = pygame.image.load('BG4.PNG')
SetSyPic = pygame.image.load('SetSy.PNG')
SetSxPic = pygame.image.load('SetSx.PNG')

clrblue3 = pygame.Color('lightskyblue3')
clrblue2 = pygame.Color('dodgerblue2')

clock = pygame.time.Clock()
FPS = 1200

font = pygame.font.Font('Helvetica.ttf',20)

outputfile = xlsxwriter.Workbook('output.xlsx')
output = outputfile.add_worksheet()
output_Sx = []
output_Sy = []
output_deg = []
output_mass = []
output_k = []
output_v = []
output_deltaX = []

output_list = [output_Sx,output_Sy,output_deg,output_mass,output_k,output_v,output_deltaX]


########## CLASS BUTTON ##########
clearbutton = button((0,255,0),150,440,60,25,'CLEAR')

########## CLASS INPUTBOX ##########
input_deg = InputBox(170, 282, 50, 28)
input_mass = InputBox(170, 332, 50, 28)
input_k = InputBox(170, 382, 50, 28)
input_boxes = [input_deg,input_mass,input_k]

########## CLASS ball ##########
balling = ball(403 ,(heighscreen-55),(255, 255, 255))

########## FONT RENDER ##########
degree = font.render('Degrees',True , (255,255,255))
degunit = font.render('Deg',True,(255,255,255))
mass = font.render('Mass',True,(255,255,255))
massunit = font.render('Kg',True,(255,255,255))
constat_spring = font.render('K spring',True,(255,255,255))
constat_spring_unit = font.render('N/m',True,(255,255,255))
error = font.render('Please input your number',True , (255,0,0))
ready = font.render('Ready to start',True , (0,255,0))


def check_float(a):
    try:
        float(a)
        return True
    except ValueError:
        return False


def clearing():
    screen.blit(background4,(0,0))
    screen.blit(background3,(0,0))
    for box in input_boxes:
        box.text = ''
        box.txt_surface = font.render(box.text, True, box.color)
    pygame.display.update()


def rewindow():
    screen.blit(background3,(0,0))
    screen.blit(degree,(75,285))
    screen.blit(degunit,(240,285))
    screen.blit(mass,(75,335))
    screen.blit(massunit,(240,335))
    screen.blit(constat_spring,(75,385))
    screen.blit(constat_spring_unit,(240,385))
    clearbutton.draw(screen,(0,0,0))


def saveoutput():
    column = 0
    output.write("A1","Sx")
    output.write("B1","Sy")
    output.write("C1","Degrees")
    output.write("D1","Mass")
    output.write("E1","Spring Constant")
    output.write("F1","Velocity")
    output.write("G1","Delta X")
    for i in output_list:
        for j in range(len(i)):
            output.write( (j+1) ,column , i[j])
        column += 1

########## GAME LOOP ##########
screen.blit(background4,(0,0))
running = True 
rdy = False
shooting = False

while running :
    clock.tick(FPS)
    rewindow()

    if (check_float(input_mass.text) == True and check_float(input_k.text) == True and check_float(input_deg.text) == True):
            energy_mass = float(input_mass.text)
            displacement_spring = float(input_k.text)
            deg = float(input_deg.text)
            raddeg = math.radians(deg)
            screen.blit(ready,(88,693))
            rdy = True
    else:
            screen.blit(error,(88,693))
            rdy = False


    for event in pygame.event.get() :
        pos = pygame.mouse.get_pos()
        balling.SetSy()
        balling.SetSx()
        if event.type == pygame.QUIT : 
            running = False
            outputfile.close()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clearbutton.isOver(pos):
                clearing()
        if event.type == pygame.MOUSEMOTION:
            if clearbutton.isOver(pos):
                clearbutton.color = (255,0,0)
            else:
                clearbutton.color = (0,255,0)

        for i in input_boxes:
            i.Boxevent(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if rdy == True :
                    balling.moving(raddeg,screen)
                    balling.ballenergy(energy_mass,displacement_spring,raddeg)
                    output_Sx.append(str(balling.setwidth))
                    output_Sy.append(str(balling.setheigh))
                    output_deg.append(input_deg.text)
                    output_mass.append(input_mass.text)
                    output_k.append(input_k.text)
                    output_v.append(str(balling.velo))
                    output_deltaX.append(str(balling.DeltaX))
                    saveoutput()
                    shooting = True
                    
    if shooting == True :
        screen.blit(balling.text_output_velo,(115,560))
        screen.blit(balling.text_displacement_spring,(115,610))

    balling.render(screen)
    for box in input_boxes:
        box.update()

    for box in input_boxes:
        box.draw(screen)

    pygame.display.update()


