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
			if bg_x_pos<=-576:
				bg_x_pos=0
			if floor_x_pos<=-576:
				floor_x_pos=0
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
	screen.blit(bg_surface,(bg_x_pos+576,0))

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos+576,900))

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
		if obstacle.colliderect(spongebob_rect.inflate(-20,-20)):
			return False
	if spongebob_rect.top<=-100 or spongebob_rect.bottom>=900:
		return False
	return True

def rotate_spongebob(spongebob):
	return pygame.transform.rotozoom(spongebob,-3*spongebob_movement,1)

def score_display(state,time=''):

	if state == 'game_mode':

		score_surface = score_font.render(str(score),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
		
		time_surface = game_font.render(str(round(game_time,3)),True,(255,255,255))
		time_rect = time_surface.get_rect(top=20,right=556)
		screen.blit(time_surface,time_rect)

	if state == 'game_over':

		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)
		
		time_surface = game_font.render(time,True,(255,255,255))
		time_rect = time_surface.get_rect(center=(288,475))
		screen.blit(time_surface,time_rect)

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

pygame.init()
screen=pygame.display.set_mode((576,1024))
clock=pygame.time.Clock()

spongebob_movement=0        
floor_x_pos=0
bg_x_pos=0
game_time=0
score=0
game_running=False
can_score=True
delay=1/frame_rate

game_font=pygame.font.Font(font_file,font_size)
score_font=pygame.font.Font(font_file,score_font_size)

bg_surface=pygame.transform.scale2x(pygame.image.load(bg_image).convert())
floor_surface=pygame.transform.scale2x(pygame.image.load(floor_image).convert())

# spongebob_surface=pygame.transform.scale2x(pygame.image.load(spongebob_mid_image).convert_alpha())
# spongebob_rect=spongebob_surface.get_rect(center=start_position)

spongebob_frames=[]
spongebob_scale=0.36
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_0).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_1).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_2).convert_alpha(),0,spongebob_scale))
spongebob_frames.append(pygame.transform.rotozoom(pygame.image.load(spongebob_3).convert_alpha(),0,spongebob_scale))
spongebob_index=1
spongebob_surface=spongebob_frames[spongebob_index]
spongebob_rect=spongebob_surface.get_rect(center=start_position)

obstacle_surface=pygame.transform.scale2x(pygame.image.load(obstacle_image).convert())
obstacle_list=[]

stop_threads=False
thread_list=[]
thread_list.append(threading.Thread(target=floor_pos))
thread_list.append(threading.Thread(target=create_obstacles))
thread_list.append(threading.Thread(target=spongebob_animation))
start_time=timer()
timer_thread=threading.Thread(target=stopwatch)

for thread in thread_list:
	thread.start()

first_screen=True

while first_screen:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit_game()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				game_running=True
				stop_timer=False
				score=0
				start_time=timer()
				obstacle_list.clear()
				spongebob_movement=-jump_height
				start_time=timer()
				timer_thread=threading.Thread(target=stopwatch)
				timer_thread.start()
				first_screen=False
			elif event.key == pygame.K_ESCAPE:
				quit_game()

	draw_background()
	spongebob_surface=spongebob_frames[1]
	screen.blit(spongebob_surface,spongebob_rect)
	score_display('game_over',"PRESS SPACE TO START")
	draw_floor()
	
	pygame.display.update()
	clock.tick(frame_rate)

while True:

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
				start_time=timer()
				obstacle_list.clear()
				spongebob_movement=-jump_height
				start_time=timer()
				timer_thread=threading.Thread(target=stopwatch)
				timer_thread.start()
			elif event.key == pygame.K_ESCAPE:
				quit_game()

	draw_background()

	if game_running:
		game_running=check_collison(obstacle_list)
		obstacle_list=move_obstacles(obstacle_list)
		draw_obstacles(obstacle_list)
		spongebob_movement+=gravity
		rotated_spongebob=rotate_spongebob(spongebob_surface)
		spongebob_rect.centery+=spongebob_movement
		screen.blit(rotated_spongebob,spongebob_rect)
		obstacle_score_check()
		score_display('game_mode')
	else:
		high_score = max(score,high_score)
		spongebob_rect.center=start_position
		spongebob_index=1
		spongebob_surface=spongebob_frames[spongebob_index]
		screen.blit(spongebob_surface,spongebob_rect)
		if(timer_thread.is_alive()):
			stop_timer=True
			timer_thread.join()
		score_display('game_over',"time: "+str(round(game_time,3)))

	draw_floor()

	pygame.display.update()
	clock.tick(frame_rate)