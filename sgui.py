# Implementation of classic arcade game Pong

import simpleguitk as simplegui
# Implementation of classic arcade game Pong
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
UP = True
DOWN = False
class Ball:
    pos = [WIDTH / 2, HEIGHT / 2]
    vel = [0,0]
class Paddle:
    def __init__(self,pos,size):
        self.paddle_pos = [[pos,240],[size,240],[size,160],[pos,160]]
        self.score = 0
        self.paddle_vel = [[0,0],[0,0],[0,0],[0,0]]
    def up(self):
        for i in range(len(self.paddle_vel)):
            self.paddle_vel[i][1] -= 4
        
    def down(self):
        for i in range(len(self.paddle_vel)):
            self.paddle_vel[i][1] += 4
        
    def default(self):
        for i in range(len(self.paddle_vel)):
            self.paddle_vel[i][1] = 0
    def move(self):
        self.paddle_pos[0][1] += self.paddle_vel[0][1]
        self.paddle_pos[1][1] += self.paddle_vel[1][1]
        self.paddle_pos[2][1] += self.paddle_vel[2][1]
        self.paddle_pos[3][1] += self.paddle_vel[3][1]
        
paddle1 = Paddle(0,8)
paddle2 = Paddle(600,592)
ball = Ball()
dir_rand = True
# initialize ball.pos and ball.vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    # these are vectors stored as lists
    ball.pos =[WIDTH / 2, HEIGHT / 2]
    print 
    if direction == RIGHT:
        ball.vel[0] = -(random.randrange(120, 240))/60
        ball.vel[1] = -(random.randrange(60, 180))/60
    elif direction == LEFT:
        ball.vel[0] = random.randrange(120, 240)/60
        ball.vel[1] = -(random.randrange(60, 180))/60
        
def ran_choice():
    global dir_rand
    dir_rand = random.choice([True,False])
    
# define event handlers
def new_game():
    # these are numbers
    global dir_rand  # these are ints
    ran_choice()
    spawn_ball(dir_rand)
    paddle1.score = 0
    paddle2.score = 0

def keydown(key):
    if key == simplegui.KEY_MAP["s"]:
        paddle1.down()
    elif key == simplegui.KEY_MAP["w"]:
        paddle1.up()
    if key == simplegui.KEY_MAP["up"]:
        paddle2.up()
    elif key == simplegui.KEY_MAP["down"]:
        paddle2.down()
        
    
def keyup(key):
    if key == simplegui.KEY_MAP["s"]:
        paddle1.default()
    elif key == simplegui.KEY_MAP["w"]:
        paddle1.default()
    if key == simplegui.KEY_MAP["up"]:
        paddle2.default()
    elif key == simplegui.KEY_MAP["down"]:
        paddle2.default()
   
    
def draw(canvas):
    global dir_rand
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball.pos[0] += ball.vel[0]
    ball.pos[1] += ball.vel[1]
       
    if ball.pos[1] <= 20 or ball.pos[1] >= HEIGHT-20:
        ball.vel[1] = -ball.vel[1]
    elif ball.pos[0] <= 20:
        paddle2.score += 1
        ran_choice()
        spawn_ball(dir_rand)
    elif ball.pos[0] >= WIDTH-20:
        paddle1.score += 1
        ran_choice()
        spawn_ball(dir_rand)
    # draw ball
    canvas.draw_circle(ball.pos, 20, 2,"Green" ,"White")
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1.paddle_pos[2][1] + paddle1.paddle_vel[2][1]) >= 0 and (paddle1.paddle_pos[2][1] + paddle1.paddle_vel[2][1]) <= 320: 
        paddle1.move()
       
    if (paddle2.paddle_pos[2][1] + paddle2.paddle_vel[2][1]) >= 0 and (paddle2.paddle_pos[2][1] + paddle2.paddle_vel[2][1]) <= 320:
        paddle2.move()
    # draw paddles
    canvas.draw_polygon(paddle1.paddle_pos,2,"Yellow","Blue")
    canvas.draw_polygon(paddle2.paddle_pos,2,"Blue","Yellow")
    # determine whether paddle and ball collide
    if ((ball.pos[0] <= paddle1.paddle_pos[1][0]+20) and (ball.pos[1] >= paddle1.paddle_pos[2][1] and ball.pos[1] <= paddle1.paddle_pos[1][1])) or ((ball.pos[0] >= paddle2.paddle_pos[1][0]-20) and (ball.pos[1] >= paddle2.paddle_pos[2][1] and ball.pos[1] <= paddle2.paddle_pos[1][1])):
        ball.vel[0] = -(ball.vel[0]*1.1) 
    # draw scores
    canvas.draw_text(str(paddle1.score),[150,50], 50, "Blue")
    canvas.draw_text(str(paddle2.score),[425,50], 50, "Yellow")   

        

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button_new_game = frame.add_button("New game", new_game) 


# start frame

frame.start()
