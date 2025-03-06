import pygame, sys, random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)#fontfamiy and size
score_font = pygame.font.Font(None, 40)

#colors
GREEN = (150, 250, 100)
DARKGREEN = (40, 55, 25)
RED = (200,0,0)
 

cell_size = 20
num_of_cells = 30

offset = 75

class Food:
    #initialise the object
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
    
    def draw(self):
        food_rect = pygame.Rect(offset + self.position.x*cell_size, offset + self.position.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED , food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, num_of_cells-1)
        y = random.randint(0,num_of_cells-1)
        return Vector2(x,y)
    
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
        

class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.add_segment = False
        
    def draw(self):
        for segment in self.body:
            segment_rect = (offset + segment.x*cell_size, offset + segment.y*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARKGREEN, segment_rect, 0, 4) #border size and corner radius

    def update(self):
        self.body.insert(0, self.body[0]+self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]#remove last element

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = 1
        self.score = 0
        
    def draw(self):
        self.food.draw()
        self.snake.draw()
        
    def update(self):
        if self.state == 1:
            self.snake.update()
            self.atfood()
            self.check_edges()
            self.check_collision_with_body()
        
    def atfood(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score+=1
            
    def check_edges(self):
        if self.snake.body[0].x >= num_of_cells or self.snake.body[0].x < 0:
            self.game_over()
        if self.snake.body[0].y >= num_of_cells or self.snake.body[0].y < 0:
            self.game_over()
            
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = 0
        self.score = 0
        
    def check_collision_with_body(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
             
        
#display surface for objects
screen = pygame.display.set_mode((2*offset + cell_size*num_of_cells, 2*offset + cell_size*num_of_cells))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT #create custom events
pygame.time.set_timer(SNAKE_UPDATE, 150)


while True:
    for event in pygame.event.get():
        
        #check for event happened?
        if event.type == SNAKE_UPDATE:
            game.update()
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if game.state == 0:
                game.state = 1
            
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
                game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0) 
    
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARKGREEN, (offset-5, offset-5, cell_size*num_of_cells+10, cell_size*num_of_cells+10), 5)
    game.draw()  
    
    title_surface = title_font.render("Snake Game", True, DARKGREEN)
    screen.blit(title_surface, (offset-5, 20))
    score_surface = score_font.render(str(game.score), True, DARKGREEN)
    screen.blit(score_surface, (offset + 10 + cell_size*(num_of_cells-1), offset-2*cell_size))
    
    pygame.display.update()
    #tick method takes number for frames per second
    clock.tick(60)
    #set sonstant game speed