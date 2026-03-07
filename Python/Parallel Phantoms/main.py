import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet import text, media, graphics, shapes, font
import os
import random
import copy

window = None
width = 0
height = 0

bgm_player = None
bgm_loaded = False

showStartScreen = True
startScreenAlpha = 255.0
startScreenHoldTimer = 0
startScreenTransitionAlpha = 0.0
startScreenTransitionTimer = 0

page = 0
level = 1
selectedLevel = 1
previewParalleled = False
Paralleled = False
mapLoaded = False

dimensionTransitionAlpha = 0.0
dimensionTransitionTimer = 0
transitionBlocked = False

playerX = 0.0
playerY = 0.0
last_playerX = 0.0
last_playerY = 0.0
playerState = 0
speedX = 0.0
speedY = 0.0
accelerationX = 0.0
a = -1.6

CollideX = 10
CollideY = 30

leftPressed = False
rightPressed = False

stars = []
totalStars = 300
starsCreatedPerBatch = 20
frameInterval = 5
lastStarCreationFrame = 0
starTimer = 0

Levels = []
Levels_Parallel = []
Obstacles = []
Obstacles_Parallel = []

clock = pyglet.clock.Clock()
targetFPS = 30
frameCount = 0

main_batch = graphics.Batch()
ui_batch = graphics.Batch()

ui_labels = []
frame_shapes = []

TITLE_FONT_NAME = 'title'
NORMAL_FONT_NAME = 'normal'

class Star:
    def __init__(self, x, y, batch=None):
        self.x = x
        self.y = y
        self.alpha = 0.0
        self.visible = True
        self.shape = shapes.Rectangle(x, y, 2, 2, color=(255, 255, 255), batch=batch)
        self.shape.opacity = 0
    
    def update_alpha(self, alpha):
        self.alpha = alpha
        self.shape.opacity = int(alpha)
    
    def set_visible(self, visible):
        self.visible = visible
        self.shape.opacity = int(self.alpha) if visible else 0
    
    def delete(self):
        self.shape.delete()

def loadMaps():
    global mapLoaded, Levels, Levels_Parallel
    
    mapLoaded = True
    Levels = []
    Levels_Parallel = []
    
    level1 = [
        [250, 80, 300, 0],
        [400, 300, 420, 0],
        [530, 300, 550, 0],
        [650, 170, 700, 0],
        [50, 15],
        [950, 15]
    ]
    Levels.append(level1)
    
    level1_parallel = [
        [330, 350, 350, 0],
        [450, 120, 500, 0],
        [600, 300, 620, 0],
        [50, 15],
        [950, 850]
    ]
    Levels_Parallel.append(level1_parallel)
    
    level2 = [
        [300, 170, 400, 0],
        [700, 370, 800, 0],
        [50, 15],
        [850, 15]
    ]
    Levels.append(level2)
    
    level2_parallel = [
        [120, 50, 200, 0],
        [500, 290, 600, 0],
        [50, 15],
        [850, 850]
    ]
    Levels_Parallel.append(level2_parallel)
    
    level3 = [
        [70, 40, 100, 30],
        [270, 240, 300, 230],
        [470, 440, 500, 430],
        [50, 15],
        [800, 515]
    ]
    Levels.append(level3)
    
    level3_parallel = [
        [170, 140, 200, 130],
        [370, 340, 400, 330],
        [570, 540, 600, 530],
        [50, 15],
        [585, 545]
    ]
    Levels_Parallel.append(level3_parallel)
    
    level4 = [
        [100, 100, 150, 0],
        [150, 200, 200, 0],
        [200, 300, 250, 0],
        [250, 400, 300, 0],
        [300, 500, 350, 0],
        [350, 600, 400, 0],
        [400, 650, 450, 0],
        [50, 15],
        [800, 515]
    ]
    Levels.append(level4)
    
    level4_parallel = [
        [620, 200, 650, 190],
        [50, 15],
        [630, 210]
    ]
    Levels_Parallel.append(level4_parallel)
    
    level5 = [
        [100, 100, 130, 0],
        [200, 200, 230, 0],
        [300, 300, 330, 0],
        [400, 350, 430, 0],
        [480, 800, 500, 0],
        [560, 800, 580, 0],
        [600, 600, 630, 0],
        [700, 650, 730, 0],
        [50, 15],
        [720, 675]
    ]
    Levels.append(level5)
    
    level5_parallel = [
        [350, 800, 370, 0],
        [400, 320, 430, 0],
        [500, 420, 530, 0],
        [600, 520, 630, 0],
        [650, 800, 670, 0],
        [50, 15],
        [800, 800]
    ]
    Levels_Parallel.append(level5_parallel)

def readData():
    global level
    try:
        if os.path.exists("PP_level.data"):
            with open("PP_level.data", "rb") as f:
                level = int.from_bytes(f.read(1), 'little')
        else:
            level = 1
    except Exception as e:
        print(f"Read error: {e}")
        level = 1

def saveData():
    global level
    try:
        with open("PP_level.data", "wb") as f:
            f.write(level.to_bytes(1, 'little'))
    except Exception as e:
        print(f"Save error: {e}")

def isCollide(playerLeft, playerRight, playerTop, playerBottom,
              obstacleLeft, obstacleRight, obstacleTop, obstacleBottom):
    if playerRight <= obstacleLeft or obstacleRight <= playerLeft:
        return False
    if playerTop <= obstacleBottom or obstacleTop <= playerBottom:
        return False
    return True

def checkCollisionAtPosition(x, y):
    global playerX, playerY, Paralleled, Obstacles, Obstacles_Parallel
    
    BoxLeftX = x - CollideX / 2
    BoxRightX = x + CollideX / 2
    BoxUpY = y + CollideY / 2
    BoxDownY = y - CollideY / 2
    
    currentObstacles = Obstacles_Parallel if Paralleled else Obstacles
    
    for i in range(len(currentObstacles) - 2):
        obs = currentObstacles[i]
        if len(obs) < 4:
            continue
        ObsLeftX = obs[0]
        ObsRightX = obs[2]
        ObsUpY = obs[1]
        ObsDownY = obs[3]
        
        if isCollide(BoxLeftX, BoxRightX, BoxUpY, BoxDownY,
                     ObsLeftX, ObsRightX, ObsUpY, ObsDownY):
            return True
    return False

def checkCollisionBelowAfterFall():
    return checkCollisionAtPosition(playerX, playerY - 2)

def clear_frame_shapes():
    global frame_shapes
    for shape in frame_shapes:
        shape.delete()
    frame_shapes = []

def clear_ui_labels():
    global ui_labels
    for label in ui_labels:
        label.delete()
    ui_labels = []

def drawRect(x, y, w, h, r, g, b, alpha=255, batch=None):
    target_batch = batch if batch else main_batch
    rect = shapes.Rectangle(x, y, w, h, color=(int(r), int(g), int(b)), batch=target_batch)
    rect.opacity = int(alpha)
    frame_shapes.append(rect)
    return rect

def drawEllipse(x, y, w, h, r, g, b, alpha=255, batch=None):
    target_batch = batch if batch else main_batch
    circle = shapes.Circle(x, y, w / 2, color=(int(r), int(g), int(b)), batch=target_batch)
    circle.opacity = int(alpha)
    frame_shapes.append(circle)
    return circle

def drawLine(x1, y1, x2, y2, r, g, b, alpha=255, weight=2, batch=None):
    target_batch = batch if batch else main_batch
    line = shapes.Line(x1, y1, x2, y2, thickness=weight, color=(int(r), int(g), int(b)), batch=target_batch)
    line.opacity = int(alpha)
    frame_shapes.append(line)
    return line

def drawTriangle(x1, y1, x2, y2, x3, y3, r, g, b, alpha=255, batch=None):
    target_batch = batch if batch else main_batch
    try:
        triangle = shapes.Polygon(x1, y1, x2, y2, x3, y3, color=(int(r), int(g), int(b)), batch=target_batch)
        triangle.opacity = int(alpha)
        frame_shapes.append(triangle)
        return triangle
    except Exception as e:
        drawLine(x1, y1, x2, y2, r, g, b, alpha, weight=2, batch=target_batch)
        drawLine(x2, y2, x3, y3, r, g, b, alpha, weight=2, batch=target_batch)
        drawLine(x3, y3, x1, y1, r, g, b, alpha, weight=2, batch=target_batch)
        return None

def drawText(text_str, x, y, size=48, r=255, g=255, b=255, alpha=255, center=False, batch=None, font_type='normal'):
    try:
        target_batch = batch if batch else ui_batch
        
        if font_type == 'title':
            font_name = TITLE_FONT_NAME
        elif font_type == 'normal':
            font_name = NORMAL_FONT_NAME
        else:
            font_name = 'Arial'
        
        if not font.have_font(font_name):
            print(f"⚠ Font '{font_name}' not available, falling back to Arial")
            font_name = 'Arial'
        
        label = text.Label(
            text_str,
            font_name=font_name,
            font_size=size,
            x=x,
            y=y,
            anchor_x='center' if center else 'left',
            anchor_y='center',
            color=(int(r), int(g), int(b), int(alpha)),
            batch=target_batch
        )
        ui_labels.append(label)
        return label
    except Exception as e:
        print(f"Text render error: {e}")
        return None

def logo(CentreX, CentreY):
    # 绘制实心正方体
    # 上表面
    top_face = shapes.Polygon((CentreX, CentreY + 70), (CentreX + 80, CentreY + 25), (CentreX, CentreY - 20), (CentreX - 80, CentreY + 25),
                 color=(255, 255, 255), batch=main_batch)
    frame_shapes.append(top_face)
    # 左表面
    left_face = shapes.Polygon((CentreX, CentreY - 20), (CentreX - 80, CentreY + 25), (CentreX - 80, CentreY - 75), (CentreX, CentreY - 120),
                 color=(200, 200, 200), batch=main_batch)
    frame_shapes.append(left_face)
    # 右表面
    right_face = shapes.Polygon((CentreX, CentreY - 20), (CentreX + 80, CentreY + 25), (CentreX + 80, CentreY - 75), (CentreX, CentreY - 120),
                 color=(180, 180, 180), batch=main_batch)
    frame_shapes.append(right_face)

def rendMap():
    global Paralleled, Obstacles, Obstacles_Parallel, width, height
    
    if Paralleled:
        drawRect(0, 0, width, height, 0, 0, 0, 255)
        obstacleColor = (255, 255, 255)
    else:
        drawRect(0, 0, width, height, 255, 255, 255, 255)
        obstacleColor = (0, 0, 0)
    
    currentObstacles = Obstacles_Parallel if Paralleled else Obstacles
    
    for i in range(len(currentObstacles) - 2):
        p = currentObstacles[i]
        if len(p) < 4:
            continue

        x1, y1 = p[0], p[1]
        x2, y2 = p[0], p[3]
        x3, y3 = p[2], p[3]
        x4, y4 = p[2], p[1]
        
        try:
            obstacleFill = shapes.Polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                          color=obstacleColor, batch=main_batch)
            obstacleFill.opacity = 255
            frame_shapes.append(obstacleFill)
        except Exception as e:
            rectWidth = abs(x3 - x1)
            rectHeight = abs(y1 - y3)
            rectX = min(x1, x3)
            rectY = min(y1, y3)
            drawRect(rectX, rectY, rectWidth, rectHeight, 
                    obstacleColor[0], obstacleColor[1], obstacleColor[2], 255)
        
        drawLine(x1, y1, x2, y2, obstacleColor[0], obstacleColor[1], obstacleColor[2], 255, 2)
        drawLine(x2, y2, x3, y3, obstacleColor[0], obstacleColor[1], obstacleColor[2], 255, 2)
        drawLine(x3, y3, x4, y4, obstacleColor[0], obstacleColor[1], obstacleColor[2], 255, 2)
        drawLine(x4, y4, x1, y1, obstacleColor[0], obstacleColor[1], obstacleColor[2], 255, 2)
    
    startPos = currentObstacles[-2]
    drawRect(startPos[0] - 10, startPos[1] - 10, 20, 20, 0, 255, 0, 255)
    
    endPos = currentObstacles[-1]
    drawRect(endPos[0] - 10, endPos[1] - 10, 20, 20, 255, 0, 0, 255)

def renderLevelPreview(levelIndex, parallelMode):
    global width, height, Levels, Levels_Parallel
    
    currentObstacles = Levels_Parallel[levelIndex - 1] if parallelMode else Levels[levelIndex - 1]
    scale = min((width * 0.4) / 1000, (height * 0.4) / 300)
    
    if parallelMode:
        drawRect(width / 2 - 500 * scale, height / 2 - 150 * scale, 
                 1000 * scale, 300 * scale, 0, 0, 0, 255)
        lineColor = 255
    else:
        drawRect(width / 2 - 500 * scale, height / 2 - 150 * scale, 
                 1000 * scale, 300 * scale, 255, 255, 255, 255)
        lineColor = 0
    
    for i in range(len(currentObstacles) - 2):
        p = currentObstacles[i]
        if len(p) < 4:
            continue
        
        x1 = (p[0] - 500) * scale + width / 2
        y1 = (p[1] - 150) * scale + height / 2
        x2 = (p[0] - 500) * scale + width / 2
        y2 = (p[3] - 150) * scale + height / 2
        x3 = (p[2] - 500) * scale + width / 2
        y3 = (p[3] - 150) * scale + height / 2
        x4 = (p[2] - 500) * scale + width / 2
        y4 = (p[1] - 150) * scale + height / 2
        
        try:
            obstacleFill = shapes.Polygon(x1, y1, x2, y2, x3, y3, x4, y4, 
                                          color=(lineColor, lineColor, lineColor), batch=main_batch)
            obstacleFill.opacity = 255
            frame_shapes.append(obstacleFill)
        except Exception as e:
            rectWidth = abs(x3 - x1)
            rectHeight = abs(y1 - y3)
            rectX = min(x1, x3)
            rectY = min(y1, y3)
            drawRect(rectX, rectY, rectWidth, rectHeight, lineColor, lineColor, lineColor, 255)
        
        drawLine(x1, y1, x2, y2, lineColor, lineColor, lineColor, 255, 2)
        drawLine(x2, y2, x3, y3, lineColor, lineColor, lineColor, 255, 2)
        drawLine(x3, y3, x4, y4, lineColor, lineColor, lineColor, 255, 2)
        drawLine(x4, y4, x1, y1, lineColor, lineColor, lineColor, 255, 2)
    
    startPos = currentObstacles[-2]
    drawRect((startPos[0] - 510) * scale + width / 2, 
             (startPos[1] - 140) * scale + height / 2, 
             20 * scale, 20 * scale, 0, 255, 0, 255)
    
    endPos = currentObstacles[-1]
    drawRect((endPos[0] - 510) * scale + width / 2, 
             (endPos[1] - 140) * scale + height / 2, 
             20 * scale, 20 * scale, 255, 0, 0, 255)

def drawArrow(isLeft, enabled, isWhite):
    global width, height
    
    alpha = 128 if enabled else 64
    r, g, b = (255, 255, 255) if isWhite else (128, 128, 128)
    
    if isLeft:
        drawTriangle(70, height/2 - 20, 70, height/2 + 20, 30, height/2, r, g, b, alpha)
    else:
        drawTriangle(width - 70, height/2 - 20, width - 70, height/2 + 20, width - 30, height/2, r, g, b, alpha)

def player(CentreX, CentreY, state):
    global Paralleled
    
    r, g, b = (255, 255, 255) if Paralleled else (0, 0, 0)
    
    if state == 1:
        drawEllipse(CentreX, CentreY + 10, 10, 10, r, g, b, 255)
        drawLine(CentreX, CentreY + 5, CentreX, CentreY - 15, r, g, b, 255, 2)
    
    elif state == 2:
        drawEllipse(CentreX, CentreY + 10, 10, 10, r, g, b, 255)
        drawLine(CentreX, CentreY + 5, CentreX, CentreY - 5, r, g, b, 255, 2)
        drawLine(CentreX, CentreY - 5, CentreX - 5, CentreY - 15, r, g, b, 255, 2)
        drawLine(CentreX, CentreY - 5, CentreX + 5, CentreY - 15, r, g, b, 255, 2)
        drawLine(CentreX, CentreY, CentreX - 3, CentreY - 3, r, g, b, 255, 2)
        drawLine(CentreX, CentreY, CentreX + 3, CentreY - 3, r, g, b, 255, 2)
    
    elif state == 3:
        drawEllipse(CentreX, CentreY + 10, 10, 10, r, g, b, 255)
        drawLine(CentreX, CentreY + 5, CentreX, CentreY - 5, r, g, b, 255, 2)
        drawLine(CentreX, CentreY - 5, CentreX - 5, CentreY - 12, r, g, b, 255, 2)
        drawLine(CentreX, CentreY - 5, CentreX - 2, CentreY - 15, r, g, b, 255, 2)
        drawLine(CentreX, CentreY, CentreX - 3, CentreY + 3, r, g, b, 255, 2)
        drawLine(CentreX, CentreY, CentreX + 3, CentreY + 3, r, g, b, 255, 2)

def update(dt):
    global frameCount, starTimer, stars, lastStarCreationFrame
    global showStartScreen, startScreenAlpha, startScreenHoldTimer
    global startScreenTransitionAlpha, startScreenTransitionTimer, Paralleled
    global page, playerX, playerY, playerState, speedX, speedY, accelerationX
    global dimensionTransitionAlpha, dimensionTransitionTimer, transitionBlocked
    global leftPressed, rightPressed, Obstacles, Obstacles_Parallel, mapLoaded
    global level, selectedLevel, previewParalleled, last_playerX, last_playerY
    
    frameCount += 1
    
    if showStartScreen:
        for star in stars:
            star.set_visible(True)
        
        starTimer += 1
        if starTimer >= frameInterval and len(stars) < totalStars:
            remainingStars = totalStars - len(stars)
            starsToAdd = min(starsCreatedPerBatch, remainingStars)
            for i in range(starsToAdd):
                stars.append(Star(random.uniform(0, width), random.uniform(0, height), batch=main_batch))
            starTimer = 0
        
        for star in stars:
            if star.alpha < 255:
                star.update_alpha(min(star.alpha + 13, 255))
        
        if startScreenAlpha > 0:
            startScreenAlpha -= 255.0 / 60
            if startScreenAlpha <= 0:
                startScreenAlpha = 0
        
        if startScreenAlpha <= 0:
            if startScreenHoldTimer == 0:
                startScreenHoldTimer = 30
            else:
                startScreenHoldTimer -= 1
                if startScreenHoldTimer <= 0:
                    showStartScreen = False
                    page = 1
                    for star in stars:
                        star.set_visible(False)
    
    elif page == 1:
        for star in stars:
            star.set_visible(False)
        
        if startScreenTransitionTimer > 0:
            startScreenTransitionTimer -= 1
            if startScreenTransitionTimer >= 10:
                startScreenTransitionAlpha = 128
            else:
                startScreenTransitionAlpha = 128 * startScreenTransitionTimer / 10
        
        if frameCount % 60 == 0 and startScreenTransitionTimer <= 0:
            Paralleled = not Paralleled
            startScreenTransitionAlpha = 128
            startScreenTransitionTimer = 10
    
    elif page == 2:
        for star in stars:
            star.set_visible(False)
        
        if not mapLoaded:
            loadMaps()
        if level == 0:
            readData()
        if level < 1 or level > len(Levels):
            level = 1
        Obstacles = copy.deepcopy(Levels[level - 1])
        Obstacles_Parallel = copy.deepcopy(Levels_Parallel[level - 1])
        Paralleled = False
        startPos = Obstacles[-2]
        playerX = float(startPos[0])
        playerY = float(startPos[1])
        page = 4
        playerState = 1
        selectedLevel = level
    
    elif page == 3:
        for star in stars:
            star.set_visible(False)
        
        if not mapLoaded or len(Obstacles) == 0:
            loadMaps()
            Obstacles = copy.deepcopy(Levels[level - 1])
            Obstacles_Parallel = copy.deepcopy(Levels_Parallel[level - 1])
        
        if dimensionTransitionTimer > 0:
            dimensionTransitionTimer -= 1
            if transitionBlocked:
                dimensionTransitionAlpha = 77 * dimensionTransitionTimer / 10
            else:
                dimensionTransitionAlpha = 128 * dimensionTransitionTimer / 10
        
        speedX *= 0.9
        
        if leftPressed and not rightPressed:
            accelerationX = -0.8
        elif rightPressed and not leftPressed:
            accelerationX = 0.8
        else:
            accelerationX = 0
        
        speedX += accelerationX
        maxSpeed = 8.0
        speedX = max(-maxSpeed, min(maxSpeed, speedX))
        
        newX = playerX + speedX
        if not checkCollisionAtPosition(newX, playerY):
            playerX = newX
        elif speedX != 0:
            speedX = 0
        
        if playerState == 3:
            speedY += a
        
        newY = playerY + speedY
        if not checkCollisionAtPosition(playerX, newY):
            playerY = newY
            if abs(speedY) > 0.5:
                playerState = 3
        elif playerY > newY:
            prevY = playerY
            playerY = newY
            
            if checkCollisionAtPosition(playerX, playerY):
                playerY = prevY
                for offset in range(1, 6):
                    if not checkCollisionAtPosition(playerX, playerY - offset):
                        playerY -= offset
                        break
                
                if not checkCollisionAtPosition(playerX, playerY):
                    speedY = 0
                    if checkCollisionBelowAfterFall():
                        playerState = 1 if speedX == 0 else 2
                    else:
                        playerState = 3
                else:
                    playerY = prevY
                    playerState = 3
            else:
                speedY = 0
                playerState = 1 if speedX == 0 else 2
        
        if playerState != 3 and not checkCollisionAtPosition(playerX, playerY - 1):
            if -0.5 < speedY < 0.5 and speedY <= 0:
                playerState = 3
        
        if speedX != 0 and playerState != 3:
            playerState = 2
        elif speedX == 0 and playerState != 3:
            playerState = 1
        
        playerX = max(5, min(width - 5, playerX))
        if playerX <= 5 or playerX >= width - 5:
            speedX = 0
        
        if playerY <= 15:
            playerY = 15
            speedY = 0
            playerState = 1 if speedX == 0 else 2
        if playerY > height - 15:
            playerY = height - 15
            speedY = 0
        
        last_playerX = playerX
        last_playerY = playerY
    
    elif page == 4:
        for star in stars:
            star.set_visible(False)

def on_draw():
    global page, Paralleled, stars, startScreenAlpha, startScreenTransitionAlpha
    global dimensionTransitionAlpha, selectedLevel, previewParalleled
    
    window.clear()
    
    clear_frame_shapes()
    clear_ui_labels()
    
    if showStartScreen:
        drawRect(0, 0, width, height, 0, 0, 0, 255)
        logo(width / 2, height / 2)
        drawText("Stellar Cube Studio", width / 2, height / 2 - 200, 50, 255, 255, 255, 255, center=True, font_type='normal')
        if startScreenAlpha > 0:
            drawRect(0, 0, width, height, 0, 0, 0, int(startScreenAlpha))
    
    elif page == 1:
        if Paralleled:
            drawRect(0, 0, width, height, 0, 0, 0, 255)
            drawText("Parallel Phantoms", width / 2, height / 2 + 180, 100, 255, 255, 255, 255, 
                    center=True, font_type='title')
            drawText("Press Enter or I to start.", width / 2, height / 2 - 200, 45, 255, 255, 255, 255, center=True, font_type='normal')
        else:
            drawRect(0, 0, width, height, 255, 255, 255, 255)
            drawText("Parallel Phantoms", width / 2, height / 2 + 180, 100, 0, 0, 0, 255, 
                    center=True, font_type='title')
            drawText("Press Enter or I to start.", width / 2, height / 2 - 200, 45, 0, 0, 0, 255, center=True, font_type='normal')
        
        if startScreenTransitionTimer > 0:
            drawRect(0, 0, width, height, 255, 255, 255, int(startScreenTransitionAlpha))
    
    elif page == 2:
        drawRect(0, 0, width, height, 255, 255, 255, 255)
        drawText("Loading...", width / 2, height / 2, 100, 0, 0, 0, 255, center=True, font_type='normal')
    
    elif page == 3:
        rendMap()
        if dimensionTransitionTimer > 0:
            if transitionBlocked:
                drawRect(0, 0, width, height, 255, 0, 0, int(dimensionTransitionAlpha))
            else:
                drawRect(0, 0, width, height, 255, 255, 255, int(dimensionTransitionAlpha))
        
        player(playerX, playerY, playerState)
    
    elif page == 4:
        if previewParalleled:
            drawRect(0, 0, width, height, 0, 0, 0, 255)
        else:
            drawRect(0, 0, width, height, 255, 255, 255, 255)
        
        drawText("Select Level", width / 2, height - 70, 65, 128, 128, 128, 255, 
                center=True, font_type='title')
        
        renderLevelPreview(selectedLevel, previewParalleled)
        
        textColor = (255, 255, 255, 220) if previewParalleled else (0, 0, 0, 220)
        drawText(f"Level {selectedLevel}", width / 2, 120, 75, textColor[0], textColor[1], textColor[2], textColor[3], center=True, font_type='normal')
        
        drawText("Press A/D to switch levels, Q to toggle preview, Enter to play", 
                width / 2, 40, 30, 128, 128, 128, 180, center=True, font_type='normal')
        
        drawArrow(True, selectedLevel > 1, previewParalleled)
        drawArrow(False, selectedLevel < len(Levels), previewParalleled)
    
    main_batch.draw()
    ui_batch.draw()

def on_key_press(symbol, modifiers):
    global showStartScreen, startScreenAlpha, page, Paralleled
    global selectedLevel, previewParalleled, level, Obstacles, Obstacles_Parallel
    global playerX, playerY, speedX, speedY, playerState
    global leftPressed, rightPressed, dimensionTransitionAlpha, dimensionTransitionTimer
    global transitionBlocked
    
    if showStartScreen:
        if symbol == key.ENTER or symbol == key.I:
            showStartScreen = False
            page = 1
            for star in stars:
                star.set_visible(False)
        elif symbol == key.ESCAPE:
            window.close()
        return
    
    elif page == 1:
        if symbol == key.ENTER or symbol == key.I:
            page = 2
        elif symbol == key.ESCAPE:
            window.close()
    
    elif page == 4:
        if symbol == key.A:
            if selectedLevel > 1:
                selectedLevel -= 1
        elif symbol == key.D:
            if selectedLevel < len(Levels):
                selectedLevel += 1
        elif symbol == key.Q or symbol == key.K:
            previewParalleled = not previewParalleled
        elif symbol == key.ENTER or symbol == key.I:
            if not mapLoaded:
                loadMaps()
            page = 3
            level = selectedLevel
            Obstacles = copy.deepcopy(Levels[level - 1])
            Obstacles_Parallel = copy.deepcopy(Levels_Parallel[level - 1])
            Paralleled = False
            startPos = Obstacles[-2]
            playerX = float(startPos[0])
            playerY = float(startPos[1])
            speedX = 0
            speedY = 0
            playerState = 1
        elif symbol == key.BACKSPACE:
            page = 1
    
    elif page == 3:
        if playerState != 3 and (symbol == key.W):
            playerState = 3
            speedY = 22
        if symbol == key.D:
            rightPressed = True
        if symbol == key.A:
            leftPressed = True
        if symbol == key.Q or symbol == key.K:
            targetDimension = not Paralleled
            targetObstacles = Obstacles_Parallel if targetDimension else Obstacles
            
            wouldCollide = False
            BoxLeftX = playerX - CollideX / 2
            BoxRightX = playerX + CollideX / 2
            BoxUpY = playerY + CollideY / 2
            BoxDownY = playerY - CollideY / 2
            
            for obs in targetObstacles[:-2]:
                if len(obs) < 4:
                    continue
                if isCollide(BoxLeftX, BoxRightX, BoxUpY, BoxDownY,
                           obs[0], obs[2], obs[1], obs[3]):
                    wouldCollide = True
                    break
            
            if wouldCollide:
                transitionBlocked = True
                dimensionTransitionAlpha = 77
                dimensionTransitionTimer = 10
            else:
                transitionBlocked = False
                dimensionTransitionAlpha = 128
                dimensionTransitionTimer = 10
                Paralleled = targetDimension
        
        if symbol == key.I:
            endPos = Obstacles[-1]
            if (abs(playerX - endPos[0]) <= 15 and abs(playerY - endPos[1]) <= 15):
                page = 2
                level += 1
                saveData()
            
            endPosP = Obstacles_Parallel[-1]
            if (abs(playerX - endPosP[0]) <= 15 and abs(playerY - endPosP[1]) <= 15):
                page = 2
                level += 1
                saveData()
        
        if symbol == key.BACKSPACE:
            page = 1

def on_key_release(symbol, modifiers):
    global leftPressed, rightPressed
    
    if symbol == key.D:
        rightPressed = False
    if symbol == key.A:
        leftPressed = False

def init_audio():
    global bgm_player, bgm_loaded
    
    try:
        if os.path.exists("background.mp3"):
            source = media.load("background.mp3")
            bgm_player = media.Player()
            bgm_player.queue(source)
            bgm_player.loop = True
            bgm_player.play()
            bgm_loaded = True
            print("Audio loaded successfully")
        else:
            print("background.mp3 not found, audio disabled")
    except Exception as e:
        print(f"Audio error: {e}")


def load_custom_fonts():
    global TITLE_FONT_NAME, NORMAL_FONT_NAME
    
    font_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_loaded = 0
    
    title_ttf = os.path.join(font_dir, "Title.ttf")
    if os.path.exists(title_ttf):
        try:
            font.add_file(title_ttf)
            possible_names = ['Title', 'HFIntimate']
            for name in possible_names:
                if font.have_font(name):
                    TITLE_FONT_NAME = name
                    print(f"✓ Title font loaded: {title_ttf} (name: {name})")
                    fonts_loaded += 1
                    break
            else:
                TITLE_FONT_NAME = 'Title'
                print(f"⚠ Title font file loaded but name uncertain: {title_ttf}")
                fonts_loaded += 1
        except Exception as e:
            print(f"✗ Title font load error: {e}")
            TITLE_FONT_NAME = 'Arial'
    else:
        print(f"⚠ Title.ttf not found, using system font")
        TITLE_FONT_NAME = 'Arial'
    
    normal_ttf = os.path.join(font_dir, "Normal.ttf")
    if os.path.exists(normal_ttf):
        try:
            font.add_file(normal_ttf)
            possible_names = ['Normal', 'HFSmoothie']
            for name in possible_names:
                if font.have_font(name):
                    NORMAL_FONT_NAME = name
                    print(f"✓ Normal font loaded: {normal_ttf} (name: {name})")
                    fonts_loaded += 1
                    break
            else:
                NORMAL_FONT_NAME = 'Normal'
                print(f"⚠ Normal font file loaded but name uncertain: {normal_ttf}")
                fonts_loaded += 1
        except Exception as e:
            print(f"✗ Normal font load error: {e}")
            NORMAL_FONT_NAME = 'Arial'
    else:
        print(f"⚠ Normal.ttf not found, using system font")
        NORMAL_FONT_NAME = 'Arial'
    
    chinese_fonts = ['Microsoft YaHei', 'SimHei', 'DengXian', 'KaiTi', 'Songti SC', 'PingFang SC']
    for cn_font in chinese_fonts:
        if font.have_font(cn_font):
            if NORMAL_FONT_NAME == 'Arial':
                NORMAL_FONT_NAME = cn_font
                print(f"✓ Using system Chinese font: {cn_font}")
            break
    
    print(f"\nTotal fonts loaded: {fonts_loaded}/2")
    print(f"TITLE_FONT_NAME: {TITLE_FONT_NAME}")
    print(f"NORMAL_FONT_NAME: {NORMAL_FONT_NAME}")

def setup():
    global window, width, height, stars, page
    
    config = Config(
        double_buffer=True,
        sample_buffers=1, 
        samples=4, 
        depth_size=24,
        alpha_size=8 
    )
    try:
        window = pyglet.window.Window(fullscreen=True, config=config)
    except:
        config = Config(double_buffer=True)
        window = pyglet.window.Window(fullscreen=True, config=config)
    
    width = window.width
    height = window.height
    
    print(f"Window size: {width}x{height}")
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_LINE_SMOOTH)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    pyglet.clock.schedule_once(lambda dt: load_custom_fonts(), 0.1)
    
    for i in range(min(starsCreatedPerBatch, totalStars)):
        stars.append(Star(random.uniform(0, width), random.uniform(0, height), batch=main_batch))
    
    init_audio()

    window.push_handlers(on_draw, on_key_press, on_key_release)
    
    pyglet.clock.schedule_interval(update, 1.0 / targetFPS)
    
    page = 0

if __name__ == "__main__":
    print("Parallel Phantoms - Python Version (pyglet 2.0)")
    print("=" * 40)
    
    setup()
    pyglet.app.run()
