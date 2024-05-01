import pygame
from pygame.locals import *
import time
import random

SIZE = 40
button_click = 0

class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.apple_x = SIZE*3
        self.apple_y = SIZE*3
        
    def draw_apple(self):
       # self.parent_screen.fill((110, 110, 5)) # this clears the screen.
        self.parent_screen.blit(self.apple, (self.apple_x,self.apple_y))
        pygame.display.flip()
    
    def move(self):
        self.apple_x = random.randint(0,25)*SIZE
        self.apple_y = random.randint(0,19)*SIZE
        

class Snake:
    def __init__(self, parent_screen, length):
        # we are creating 5 blocks so need 5 x and y.
        self.length = length
        self.parent_screen = parent_screen
        # Loading the image and drawing it in the screen using blit
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_x = [SIZE]*length
        self.block_y = [SIZE]*length
        self.direction = 'down'
    
    def draw_block(self):
        self.parent_screen.fill((110, 110, 5)) # this clears the screen.
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i],self.block_y[i]))
        pygame.display.flip()
    
    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def move_left(self):
        self.direction = 'left'
        
    def move_right(self):
        self.direction = 'right'
    
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]
        if self.direction == 'up':
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            self.block_y[0] += SIZE
        if self.direction == 'left':
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            self.block_x[0] += SIZE
        
        self.draw_block()
        
class Game:
    def __init__(self, x, y):
        pygame.init() # initialize the whole module.
        pygame.mixer.init()
        self.play_background_music()
        # creating a surface
        self.border_x = x
        self.border_y = y
        self.surface = pygame.display.set_mode((self.border_x, self.border_y))
        # to change the color of the window
        self.surface.fill((110, 110, 5))
        # Need to draw snake inside the game class.
        self.snake = Snake(self.surface, 1)
        self.snake.draw_block()
        # Initialize the apple
        self.apple = Apple(self.surface)
        self.apple.draw_apple()

    
    def is_collison(self, x1, y1, x2, y2):
        if x1 >= x2  and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
    
    def restart_game(self):
        # Need to draw snake inside the game class.
        self.snake = Snake(self.surface, 1)
        # Initialize the apple
        self.apple = Apple(self.surface)
        
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw_apple()
        self.display_score()
        pygame.display.flip()
        
        # snake colliding with apple
        if self.is_collison(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y):
            ding_sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(ding_sound)
            self.snake.increase_length()
            self.apple.move()
        
        # snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collison(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                crash_sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(crash_sound)
                raise "Game Over"
        
        # snake colliding with the border
        if (self.snake.block_x[0] < 0 or self.snake.block_x[0] >= self.border_x or self.snake.block_y[0] < 0 or self.snake.block_y[0] >= self.border_y):
            if (button_click == 1):
                crash_sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(crash_sound)
                raise "Game Over"
        
        
    def play_background_music(self):
        pygame.mixer.music.load("resources/crash.mp3")
        pygame.mixer.music.play()
    
    def display_score(self):
        # displaying score at top right corner.
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800,10))
    
    def show_game_over(self):
        self.surface.fill((110,110,5))
        font = pygame.font.SysFont('arial', 30)
        display_score = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(display_score, (200,300))
        play_again = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(play_again, (200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
        
    def run(self):
        running = True
        pause = False
        while running:
            # stop on certain key strokes
            # pygame locals
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    button_click = 1
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                        self.restart_game()
                    if not pause:
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
            time.sleep(0.4)
    

if __name__ == "__main__":
    game = Game(1000,800)
    game.run()

