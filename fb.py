import pygame,sys,random,threading
from data import *

def draw_floor():
	global floor_x_pos
	floor_x_pos-=1
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos+576,900))
	if floor_x_pos<=-576:
		floor_x_pos=0

def draw_background():
	screen.blit(bg_surface,(floor_x_pos,0))
	screen.blit(bg_surface,(floor_x_pos+576,0))

def create_obstacle():
	obstacle_height=random.choice(obstacle_heights)
	bottom=obstacle_surface.get_rect(midtop=(700,obstacle_height))
	top=obstacle_surface.get_rect(midbottom=(700,obstacle_height-obstacle_gap))
	return bottom,top

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
		if spongebob_rect.colliderect(obstacle):
			return False
	if spongebob_rect.top<=-100 or spongebob_rect.bottom>=900:
		return False
	return True

def rotate_spongebob(spongebob):
	return pygame.transform.rotozoom(spongebob,-3*spongebob_movement,1)

def spongebob_animation():
	new_spongebob=spongebob_frames[spongebob_index]
	new_spongebob_rect=new_spongebob.get_rect(center=(100,spongebob_rect.centery))
	return new_spongebob,new_spongebob_rect

pygame.init()
screen=pygame.display.set_mode((576,1024))
clock=pygame.time.Clock()
game_running=False
floor_x_pos=0

bg_surface=pygame.transform.scale2x(pygame.image.load(bg_image).convert())

floor_surface=pygame.transform.scale2x(pygame.image.load(floor_image).convert())

# spongebob_surface=pygame.transform.scale2x(pygame.image.load(spongebob_mid_image).convert_alpha())
# spongebob_rect=spongebob_surface.get_rect(center=start_position)

spongebob_down=pygame.transform.scale2x(pygame.image.load(spongebob_down_image).convert_alpha())
spongebob_mid=pygame.transform.scale2x(pygame.image.load(spongebob_mid_image).convert_alpha())
spongebob_up=pygame.transform.scale2x(pygame.image.load(spongebob_up_image).convert_alpha())
spongebob_frames=[spongebob_down,spongebob_mid,spongebob_up]
spongebob_index=1
spongebob_surface=spongebob_frames[spongebob_index]
spongebob_rect=spongebob_surface.get_rect(center=start_position)

obstacle_surface=pygame.transform.scale2x(pygame.image.load(obstacle_image).convert())
obstacle_list=[]
SPAWNOBSTACLE=pygame.USEREVENT
pygame.time.set_timer(SPAWNOBSTACLE,obst_freq)
SPONGEBOBANIMATION=pygame.USEREVENT+1
pygame.time.set_timer(SPONGEBOBANIMATION,200)


while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and game_running:
			if event.key == pygame.K_SPACE:
				spongebob_movement=-jump_height
		if event.type == pygame.KEYDOWN and not game_running:
			if event.key == pygame.K_SPACE:
				game_running=True
				obstacle_list.clear()
				spongebob_movement=-jump_height
		if event.type == SPAWNOBSTACLE:
			obstacle_list.extend(create_obstacle())
		if event.type == SPONGEBOBANIMATION and game_running:
			if spongebob_index<2:
				spongebob_index+=1
			else:
				spongebob_index=0
			spongebob_surface,spongebob_rect=spongebob_animation()

	# screen.blit(bg_surface,(0,0))
	draw_background()

	if game_running:
		spongebob_movement+=gravity
		rotated_spongebob=rotate_spongebob(spongebob_surface)
		spongebob_rect.centery+=spongebob_movement
		screen.blit(rotated_spongebob,spongebob_rect)
		game_running=check_collison(obstacle_list)
		obstacle_list=move_obstacles(obstacle_list)
		draw_obstacles(obstacle_list)
		draw_floor()
	else:
		screen.blit(bg_surface,(floor_x_pos,0))
		screen.blit(bg_surface,(floor_x_pos+576,0))
		screen.blit(floor_surface,(floor_x_pos,900))
		screen.blit(floor_surface,(floor_x_pos+576,900))
		spongebob_rect.center=start_position
		spongebob_index=1
		spongebob_surface=spongebob_frames[spongebob_index]
		screen.blit(spongebob_surface,spongebob_rect)

	pygame.display.update()
	clock.tick(120)