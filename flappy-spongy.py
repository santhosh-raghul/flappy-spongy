import pygame,sys,random,threading
from time import sleep
from timeit import default_timer as timer
from data import *

def floor_pos():
	global floor_x_pos,bg_x_pos,game_running,stop_threads,delay
	while True:
		if game_running:
			floor_x_pos-=1
			bg_x_pos-=1
			if bg_x_pos<=-1828:
				bg_x_pos=-626
			if floor_x_pos<=-1242:
				floor_x_pos=-333
		if stop_threads:
			break
		sleep(delay)

def stopwatch():
	global game_time,start_time
	while True:
		game_time=timer()-start_time
		if stop_timer:
			break
		sleep(0.1)

def create_obstacles():
	global obstacle_list
	while True:
		obstacle_height=random.choice(obstacle_heights)
		bottom=obstacle_surface.get_rect(midtop=(700,obstacle_height))
		top=obstacle_surface.get_rect(midbottom=(700,obstacle_height-obstacle_gap))
		obstacle_list.extend((bottom,top))
		if stop_threads:
			break
		sleep(obst_freq)

def spongebob_animation():
	global spongebob_surface,spongebob_rect,spongebob_index
	while True:
		if spongebob_index<3:
			spongebob_index+=1
		else:
			spongebob_index=0
		spongebob_surface=spongebob_frames[spongebob_index]
		spongebob_rect=spongebob_surface.get_rect(center=(100,spongebob_rect.centery))
		if stop_threads:
			break
		sleep(0.15)

def draw_background():
	screen.blit(bg_surface,(bg_x_pos,0))
	screen.blit(bg_surface,(bg_x_pos+1202,0))

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,550))
	screen.blit(floor_surface,(floor_x_pos+909,550))

def move_obstacles(obstacles):
	for obstacle in obstacles:
		obstacle.centerx-=obstacle_speed
	return obstacles

def draw_obstacles(obstacles):
	obstacle_surface_upside_down=pygame.transform.flip(obstacle_surface,False,True)
	for obstacle in obstacles:
		if obstacle.bottom>1024:
			screen.blit(obstacle_surface,obstacle)
		else:
			screen.blit(obstacle_surface_upside_down,obstacle)

def check_collison(obstacles):
	for obstacle in obstacles:
		if obstacle.colliderect(spongebob_rect.inflate(-40,-40)):
			return False
	if spongebob_rect.top<=-100 or spongebob_rect.bottom>=900:
		return False
	return True

def rotate_spongebob(spongebob):
	return pygame.transform.rotozoom(spongebob,-3*spongebob_movement,1)

def display_text(display_text,rectangle_center,font_size=''):

	text_color=(13, 59, 76)
	if font_size == 'big':
		text_surface = score_font.render(display_text,True,text_color)
	else:
		text_surface = game_font.render(display_text,True,text_color)

	text_rect = text_surface.get_rect(center=rectangle_center)
	screen.blit(text_surface,text_rect)

def score_display(state,time=''):

	if state == 'game_mode':
		display_text(str(score),(288,100),"big")
		display_text(str(round(game_time,3)),(510,30))

	elif state == 'game_over':
		display_text(f'Score: {int(score)}',(288,100))
		display_text(f'High score: {int(high_score)}',(288,850))
		display_text(time,(288,475))


def obstacle_score_check():
	global score, can_score 
	if obstacle_list:
		for obstacle in obstacle_list:
			if 95 < obstacle.centerx < 105 and can_score:
				score += 1
				can_score = False
			if obstacle.centerx < 0:
				can_score = True

def update_highscore():
	f=open("data.py","r")
	lines=f.readlines()
	f.close()
	for i in range(len(lines)):
		if lines[i].startswith("high_score="):
			lines[i]="high_score=%d\t\t\t\t# high score\n"%(high_score)
			break
	f=open("data.py","w")
	f.writelines(lines)
	f.close()

def quit_game():
	global stop_threads
	stop_threads=True
	for thread in thread_list:
		thread.join()
	update_highscore()
	pygame.quit()
	sys.exit()

pygame.init() # pygame initiation
pygame.display.set_caption('FlaPpY sPoNgy') # pygame title
screen=pygame.display.set_mode((576,1024)) # setting window size
clock=pygame.time.Clock()

spongebob_movement=0        
floor_x_pos=0
bg_x_pos=0
game_time=0
score=0
game_running=False #flag to check if game is running
can_score=True #control variable in obstacle_score_check init to True
delay=1/frame_rate


# loading fonts 
game_font=pygame.font.Font(font_file,font_size)
score_font=pygame.font.Font(font_file,score_font_size)
# loading the background image 
bg_surface=pygame.transform.scale2x(pygame.image.load(bg_image).convert())
# loading the floor image 
floor_surface=pygame.image.load(floor_image).convert_alpha()

spongebob_frames=[] # contains the list of frames of the character to display to create animation
spongebob_scale=0.42
# pygame.image.load(image_file) will load the image file
# .convert_alpha() method will convert the image to a format which is easier for
# the pygame library to work with, while retaining the transparency of the png image
# pygame.transform.rotozoom(image,rotation_angle,scale_factor) will rotate and scale the given image
# finally the returned image is appended to the spongebob_frames list
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_0).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_1).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_2).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_3).convert_alpha(),0,spongebob_scale))
spongebob_index=1 # index of normal spongebob image
spongebob_surface=spongebob_frames[spongebob_index]
spongebob_rect=spongebob_surface.get_rect(center=start_position) # place the image at start position

# To spawn obstacles chosen at random from obstacle_image given in the data.py 
obstacle_surface=pygame.image.load(obstacle_image).convert_alpha()
obstacle_list=[]

stop_threads=False # variable to check for stopping the threads
thread_list=[]
# creating 3 threads for the functions specified 
thread_list.append(threading.Thread(target=floor_pos))
thread_list.append(threading.Thread(target=create_obstacles))
thread_list.append(threading.Thread(target=spongebob_animation))

start_time=timer() # start time
# thread for timer
timer_thread=threading.Thread(target=stopwatch)

for thread in thread_list:
	thread.start()

first_screen=True # this is the first screen after the program was just executed

while first_screen:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # if the user presses the cross button in the game window
			quit_game() # calling quit_game() function
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: # when the user taps the space bar button
				game_running=True # set the game_running control variable to True
				stop_timer=False # initialise stop_timer to be false for the timer thread
				score=0 # initialize score to zero 
				obstacle_list.clear() # clear the previously created obstacles 
				spongebob_movement=-jump_height # decrease y cordinate of the character to make it jump (y increases downwards) 
				start_time=timer() # set the game starting time
				timer_thread=threading.Thread(target=stopwatch) # create the timer thread
				timer_thread.start() # start the timer thread
				first_screen=False # the displayed screen is no longer the first screen
			elif event.key == pygame.K_ESCAPE:# quit game when esc button is pressed
				quit_game()

	# display the background, character, floor and message for the user, in the first screen
	draw_background() 
	spongebob_surface=spongebob_frames[1]
	screen.blit(spongebob_surface,spongebob_rect)
	score_display('game_over',"PRESS SPACE TO START")
	draw_floor()
	
	pygame.display.update()
	clock.tick(frame_rate)


# this loop is for succesive games after the first game 
# this code has comments for the parts not present in the first game
# for the uncommented parts please refer the corresponding lines in the 
# above first screen loop

while True: # for successive games

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit_game()
		if event.type == pygame.KEYDOWN and game_running:
			if event.key == pygame.K_SPACE:
				spongebob_movement=-jump_height
			elif event.key == pygame.K_ESCAPE:
				quit_game()
		if event.type == pygame.KEYDOWN and not game_running:
			if event.key == pygame.K_SPACE:
				game_running=True
				stop_timer=False
				score=0
				obstacle_list.clear()
				spongebob_movement=-jump_height
				start_time=timer()
				timer_thread=threading.Thread(target=stopwatch)
				timer_thread.start()
			elif event.key == pygame.K_ESCAPE:
				quit_game()

	# this happens 'frame_rate' number of times every second
		
	draw_background()

	if game_running: # if still game on
		game_running=check_collison(obstacle_list) # checking for collision
		obstacle_list=move_obstacles(obstacle_list) # move obstacle and draw them
		draw_obstacles(obstacle_list)
		spongebob_movement+=gravity # make spongebob move down due to gravity(moves down)
		rotated_spongebob=rotate_spongebob(spongebob_surface) # rotate spongebob according to motion
		spongebob_rect.centery+=spongebob_movement # change the image postion according to motion
		screen.blit(rotated_spongebob,spongebob_rect) # print the character on screen
		obstacle_score_check() # score update
		score_display('game_mode') # display
	else: # game ove
		high_score = max(score,high_score) # update highscore
		spongebob_rect.center=start_position # move the character to the start position
		spongebob_index=1 # normal spongebob image
		spongebob_surface=spongebob_frames[spongebob_index]
		screen.blit(spongebob_surface,spongebob_rect) # display character
		if(timer_thread.is_alive()): # stop timer thread if its active
			stop_timer=True
			timer_thread.join()
		score_display('game_over',"Time: "+str(round(game_time,3))) # display score and time

	draw_floor() # drawing floor

	pygame.display.update()
	clock.tick(frame_rate)