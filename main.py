"""
ZE : Zombies Escape

Game Controls :
            right arrow : move forward
            left arrow  : move backward
            up arrow    : enter gate
            down arrow  : leave gate
            q key       : quit

Cheat Codes :
            k key       : make player invincible
            p key       : level up
            o key       : level down

Developed By :
            Idea and Debugging   : Yaman Kumar Sahu
            Code and Soundtracks : Amitesh Patra
            Graphics and sprites : Manas Banjare
            Documentation        : Rishabh Biswal
"""
import pygame
from pygame.locals import *
import random

import level_data


# Game initialized
pygame.init()
zombies = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


# Game Variables
screen_width = 1200
screen_height = 800
run = True
tile_size = 50
fps = 60
level = 1
max_levels = 5
gate_coordinates = []
draw_rect = False
teleport = False
death = 1
death1 = 1
bg = [ 1, 2, 3, 4, 5]
random.shuffle(bg)
over_time = 0
exit_err_p = False
respawn_err = 0

# Game classes
class World():
    def __init__(self, world_map):
        self.tile_list = []
        floor_img = pygame.image.load( "images/floor/floor_3.jpg")
        wall_img = pygame.image.load( "images/floor/floor_3.jpg")

        row_count = 0
        for row in world_map:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale( floor_img, ( tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = ( img, img_rect)
                    self.tile_list.append( tile)
                elif tile == 2:
                    img = pygame.transform.scale( wall_img, ( tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = ( img, img_rect)
                    self.tile_list.append( tile)
                elif tile in [ 3, 4, 5]:
                    zombie = Zombie( col_count * tile_size + tile_size, row_count * tile_size - 36, tile)
                    zombies.add( zombie)
                col_count += 1
            row_count += 1

    def draw( self):
        for tile in self.tile_list:
            screen.blit( tile[0], tile[1])
            if draw_rect:
                pygame.draw.rect( screen, ( 255, 255, 255), tile[1], 2)

class Zombie( pygame.sprite.Sprite):
    def __init__( self, x, y, type):
        pygame.sprite.Sprite.__init__( self)
        self.spawnZombie( x, y, type)
    
    def spawnZombie( self, x, y, type):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.type = type
        if type == 3:
            for num in range( 8):
                img_right = pygame.image.load( f"images/zombie/zom_1/zombie_{num}.png")
                img_right = pygame.transform.scale( img_right, ( 65, 95))
                img_left = pygame.transform.flip( img_right, True, False)
                self.images_right.append( img_right)
                self.images_left.append( img_left)
            self.image = self.images_right[ self.index]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.speed = 10
            self.walk_cooldown = 10
            self.rect.x = x
            self.direction = random.choice( [1, -1])
        elif type == 4:
            for num in range( 5):
                img_right = pygame.image.load( f"images/zombie/zom_2/zombie_{num}.png")
                img_right = pygame.transform.scale( img_right, ( 85, 85))
                img_left = pygame.transform.flip( img_right, True, False)
                self.images_right.append( img_right)
                self.images_left.append( img_left)
            self.image = self.images_right[ self.index]
            dummy_image = pygame.image.load( f"images/zombie/zom_2/zombie_{num}.png")
            dummy_image = pygame.transform.scale( img_right, ( 65, 75))
            self.rect = dummy_image.get_rect()
            self.rect.y = y + 5
            self.speed = 20
            self.walk_cooldown = 10
            self.rect.x = x
            self.direction = random.choice( [1, -1])
        if type == 5:
            for num in range( 1, 11):
                img_right = pygame.image.load( f"images/zombie/zom_3/000{num}.png")
                img_right = pygame.transform.scale( img_right, ( 105, 135))
                img_left = pygame.transform.flip( img_right, True, False)
                self.images_left.append( img_right)
                self.images_right.append( img_left)
            self.image = self.images_right[ self.index]
            self.rect = self.image.get_rect()
            self.rect.y = y - 35
            self.speed = 8
            self.walk_cooldown = 15
            self.rect.x = x
            self.teleport_wait = 0
            self.max_wait = random.choice( [ 200, 400, 600])
            self.direction = random.choice( [1, -1])
    
    def checkEdges( self):
        screen_rect = screen.get_rect()  
        if self.direction == 1:
            if self.rect.right >= screen_rect.right - tile_size:
                self.direction *= -1
        if self.direction == -1:
            if self.rect.left <= tile_size:
                self.direction *= -1

    def update( self):
        walk_cooldown = self.walk_cooldown
        self.checkEdges()
        if self.direction == 1:
            self.rect.x += float( random.randint( 1, self.speed) * self.direction) / 6
        elif self.direction == -1:
            self.rect.x += float( random.randint( 1, self.speed) * self.direction) / 6 + 1
        self.counter += 1
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len( self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[ self.index]
            if self.direction == -1:
                self.image = self.images_left[ self.index]
        if self.type == 5:
            self.teleport_wait += 1
            if self.teleport_wait >= self.max_wait:
                new_pos = random.choice( gate_coordinates)
                self.rect.x = new_pos[0]
                self.rect.y = new_pos[1]
                self.teleport_wait = 0
                self.max_wait = random.choice( [ 200, 400, 600])
        if draw_rect:
            pygame.draw.rect( screen, ( 255, 255, 255), self.rect, 2)

class Player():
    def __init__( self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.speed = 3
        for num in range( 7):
            img_right = pygame.image.load( f"images/player/player_{num}.png")
            img_right = pygame.transform.scale( img_right, ( 45, 85))
            img_left = pygame.transform.flip( img_right, True, False)
            self.images_right.append( img_right.subsurface( img_right.get_rect().x, img_right.get_rect().y,
                    img_right.get_width(), img_right.get_height() - 5))
            self.images_left.append( img_left)
        self.dead_image = pygame.image.load( "images/player/death.png")
        self.image = self.images_right[ self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temp_pos = [0, 0]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 0
        self.inside = False
        self.game_over = 0
        self.death_float = 0

    def update( self):
        dx = 0
        dy = 0
        walk_cooldown = 20
        key = pygame.key.get_pressed()

        if self.game_over == 0:
            if key[ pygame.K_LEFT]:
                dx -= self.speed
                self.counter += 3
                self.direction = -1
            if key[ pygame.K_RIGHT]:
                dx += self.speed
                self.counter += 3
                self.direction = 1
            if not key[ pygame.K_LEFT] and not key[ pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[ self.index]
                elif self.direction == -1:
                    self.image = self.images_left[ self.index]
            
            if key[ pygame.K_DOWN] and self.inside:
                self.rect.x, self.rect.y = self.temp_pos[0], self.temp_pos[1]
                self.inside = False

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len( self.images_right):
                    self.index = 1
                if self.direction == 1:
                    self.image = self.images_right[ self.index]
                elif self.direction == -1:
                    self.image = self.images_left[ self.index]
            
            for tile in world.tile_list:
                if tile[1].colliderect( self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect( self.rect.x, self.rect.y, self.width, self.height):
                    dy = tile[1].top - self.rect.bottom
            
            if pygame.sprite.spritecollide( self, zombies, False) and death == 1 and death1 == 1 :
                self.game_over = -1
            
            if pygame.sprite.spritecollide( self, exit_group, False):
                self.game_over = 1

            self.rect.x += dx
            self.rect.y += dy
        elif self.game_over == -1:
            self.image = self.dead_image
            if self.death_float < 20:
                self.rect.y -= 5
                self.death_float += 1

        screen.blit( self.image, self.rect)
        if draw_rect:
            pygame.draw.rect( screen, ( 255, 255, 255), self.rect, 2)

    def teleport( self):
        if self.game_over == 0:
            key = pygame.key.get_pressed()
            
            if key[ pygame.K_UP] and not self.inside:
                for gate in gates.gate_list:
                    if gate[1].colliderect( self.rect):
                        if gate[2] == -1:
                            self.temp_pos[0] = gate[1].x + tile_size / 2
                            self.temp_pos[1] = gate[1].bottom
                            self.rect.x, self.rect.y = 10000, 10000
                            self.inside = True
                        elif gate[2] > 0:
                            for teleport_gate in gates.teleport_gates:
                                if teleport_gate[2] == gate[2] and teleport_gate[3] != gate[3]:
                                    self.rect.x = teleport_gate[1].x + tile_size / 2
                                    self.rect.y =teleport_gate[1].bottom
        elif self.game_over == -1:
            self.image = self.dead_image
            if self.death_float < 20:
                self.rect.y -= 5
                self.death_float += 1
        
        screen.blit( self.image, self.rect)
        if draw_rect:
            pygame.draw.rect( screen, ( 255, 255, 255), self.rect, 2)
    
    def reset( self, x, y):
        self.images_right = []
        self.images_right = []
        self.index = 0
        self.counter = 0
        for num in range( 7):
            img_right = pygame.image.load( f"images/player/player_{num}.png")
            img_right = pygame.transform.scale( img_right, ( 45, 85))
            img_left = pygame.transform.flip( img_right, True, False)
            self.images_right.append( img_right.subsurface( img_right.get_rect().x, img_right.get_rect().y,
                    img_right.get_width(), img_right.get_height() - 5))
            self.images_left.append( img_left)
        self.dead_image = pygame.image.load( "images/player/death.png")
        self.image = self.images_right[ self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temp_pos = [0, 0]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = 0
        self.inside = False
        self.game_over = 0
        self.death_float = 0


class Gate():
    def __init__( self, gate_map):
        self.gate_list = []
        self.teleport_gates = []
        gate_img_1 = pygame.image.load( "images/door/door_1.png")
        gate_img_2 = pygame.image.load( "images/door/door_2.png")
        gate_img_3 = pygame.image.load( "images/door/door_3.png")
        gate_img_4 = pygame.image.load( "images/door/door_4.png")

        gate_id = 0
        row_count = 0
        for row in gate_map:
            col_count = 0
            for gate in row:
                if gate == -2:
                    img = pygame.transform.scale( gate_img_4, ( tile_size * 2, tile_size * 2 + 20))
                    img_rect = img.get_rect()
                    img_rect.x = 2 * tile_size + col_count * img_rect.width + col_count * tile_size
                    img_rect.y = row_count * tile_size + 3 * tile_size * row_count + tile_size - 20
                    gate = ( img, img_rect, gate, gate_id)
                    self.gate_list.append( gate)
                    gate_id += 1
                    gate_coordinates.append( ( img_rect.x, img_rect.y))
                elif gate == -1:
                    img = pygame.transform.scale( gate_img_1, ( tile_size * 2, tile_size * 2 + 20))
                    img_rect = img.get_rect()
                    img_rect.x = 2 * tile_size + col_count * img_rect.width + col_count * tile_size
                    img_rect.y = row_count * tile_size + 3 * tile_size * row_count + tile_size - 20
                    gate = ( img, img_rect, gate, gate_id)
                    self.gate_list.append( gate)
                    gate_id += 1
                    gate_coordinates.append( ( img_rect.x, img_rect.y))
                elif gate == 0:
                    x = 2 * tile_size + col_count * img_rect.width + col_count * tile_size
                    y = row_count * tile_size + 3 * tile_size * row_count + tile_size - 20
                    exit_gate = Exit( x, y)
                    exit_group.add( exit_gate)
                    gate_id += 1
                    gate_coordinates.append( ( img_rect.x, img_rect.y))
                else:
                    img = pygame.transform.scale( gate_img_2, ( tile_size * 2, tile_size * 2 + 20))
                    img_rect = img.get_rect()
                    img_rect.x = 2 * tile_size + col_count * img_rect.width + col_count * tile_size
                    img_rect.y = row_count * tile_size + 3 * tile_size * row_count + tile_size - 20
                    gate = ( img, img_rect, gate, gate_id)
                    self.gate_list.append( gate)
                    self.teleport_gates.append( gate)
                    gate_coordinates.append( ( img_rect.x, img_rect.y))
                col_count += 1
            row_count += 1
    
    def draw( self):
        for gate in self.gate_list:
            screen.blit( gate[0], gate[1])
            if draw_rect:
                pygame.draw.rect( screen, ( 255, 255, 255), gate[1], 2)

class Exit( pygame.sprite.Sprite):
    def __init__( self, x, y):
        pygame.sprite.Sprite.__init__( self)
        img = pygame.image.load( "images/door/door_3.png")
        self.image = pygame.transform.scale( img, ( tile_size * 2, tile_size * 2 + 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

# Game Functions
def drawGrid():
    for line in range( 0, 60):
        pygame.draw.line(screen, ( 255, 255, 255), ( 0, line * tile_size), ( screen_width, line * tile_size))
        pygame.draw.line(screen, ( 255, 255, 255), ( line * tile_size, 0), ( line * tile_size, screen_width))
    for line in range( 0, 10):
        pygame.draw.line(screen, ( 0, 0, 0), ( 0, line * tile_size * 4), ( screen_width, line * tile_size * 4), 5)
        pygame.draw.line(screen, ( 0, 0, 0), ( line * tile_size * 4, 0), ( line * tile_size * 4, screen_width), 5)

def resetLevel( level):
    bg_num = level - 1
    bg_l = pygame.image.load( f"images/background/bg_l{bg[bg_num]}.jpg")
    player.reset( tile_size, screen_height - 75)
    zombies.empty()
    exit_group.empty()
    world = World( level_data.world_maps[ level - 1])
    gates = Gate( level_data.gate_maps[ level - 1])
    return world, gates, bg_l

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False
                elif event.key == K_q:
                    pygame.quit()
                    return True
        
        first_screen = pygame.image.load(f"images\menu\PAUSE.png")
        screen.blit(first_screen,(0,0))
        pygame.display.update()
        clock.tick(5)
        
def start():

    started = True

    while started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  False
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    started = False
                elif event.key == K_q:
                    pygame.quit()
                    return  False
        
        first_screen = pygame.image.load(f"images\menu\START.png")
        screen.blit(first_screen,(-100,100))
        pygame.display.update()
        clock.tick(5)
    return True

def gameOver():

    over = True

    while over:
        
        first_screen = pygame.image.load(f"images\menu\GAMEOVER.png")
        screen.blit(first_screen,(0,0))
        pygame.display.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                over_err =  True
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    over = False
                    over_err =  False
                    respawn_err = 0
                
                elif event.key == K_q:
                    pygame.quit()
                    over_err =  True
                    

        clock.tick(5)
    if over_err:
        return False
    else:
        return True, respawn_err


def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 256):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)

# Misc
screen = pygame.display.set_mode(( screen_width, screen_height))
pygame.display.set_caption( "Zombies Escape")
bg_l = pygame.image.load( f"images/background/bg_l{bg[0]}.jpg")
clock = pygame.time.Clock()

# Game objects
player = Player( tile_size, screen_height - 75)
world = World( level_data.world_maps[ level - 1])
gates = Gate( level_data.gate_maps[ level - 1])

run = start()

# Game Loop


while run:
    clock.tick( fps)
    if respawn_err == 0 :
        death = 0
    elif respawn_err == 1 :
        death = 1
    if player.game_over == 1:
        level += 1
        if level <= max_levels:
            fade(screen_width,screen_height)
            world, gates, bg_l = resetLevel( level)
            game_over = 0
        else:
            pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                respawn_err = 1
            if event.key == pygame.K_RIGHT:
                respawn_err = 1
            if event.key == pygame.K_k:
                death1 = (death1 + 1) % 2
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_UP:
                if teleport == False:
                    player.teleport()
                    teleport = True
                if teleport:
                    teleport = False 
            if event.key == pygame.K_p:
                level += 1
                if level <= max_levels:
                    world, gates, bg_l = resetLevel( level)
                    game_over = 0
                else:
                    level = 5
            if event.key == pygame.K_o:
                level -= 1
                if level >= 1:
                    world, gates, bg_l = resetLevel( level)
                    game_over = 0
                else:
                    level = 1
            if event.key == pygame.K_ESCAPE:
                exit_err_p = pause()
    if exit_err_p:
        break
    
    if player.game_over == 0:
        pygame.mouse.set_visible( False) 
    elif player.game_over == -1:
        pygame.mouse.set_visible( True)
        if over_time >= fps and  gameOver() :
            level = 1 
            player.reset(tile_size, screen_height - 75)
            over_time = 0
            respawn_err = 0
        elif over_time >= fps and not gameOver():
            break    
        over_time += 1
    screen.blit( bg_l, ( 0, 0))
    world.draw()
    gates.draw()
    exit_group.draw( screen)
    if player.game_over == 0:
        zombies.update()
    zombies.draw( screen)
    player.update()
    if draw_rect:
        drawGrid()
    pygame.display.update()

# Game quitting
pygame.quit()
