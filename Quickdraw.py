# Quickdraw!
# A reaction based game (you shoot faster than your enemy).
# You really FEEL like a COWBOY!!!!!!!!!!!!!
import pygame
import sys
import random 
import os

# Variables - some of these gets documentation and some of these don't because they should be explain themselves.
p1_score = 0
p2_score = 0
p1_quickdraw = False # Just the action boolean.
p2_quickdraw = False
p1_last_press_time = 0
p2_last_press_time = 0
p1_round_winner = False
p2_round_winner = False
p1_winner_displayed = False
p2_winner_displayed = False  
p1_timeout = False
p2_timeout = False 
countdown_timer = 0
random_timer = 0
random_choice = ["P1", "P2"]
random_winner_selection = ""
round_winner_display_duration = 2000  # Display winning screen for 2 seconds (adjust as needed)
round_winner_display_start_time = 0
round_winner_displayed = False
rounds = 0 # The amount they want to go about (for this case we the max will be 5.)
rounder = 1 # So I can force I mean store this thing somewhere. By thing I mean the rounds variable.
game_started = False
clock = pygame.time.Clock()
return_to_main_menu = False

# Initialize Pygame
pygame.init()

# Game states
class GameState:
    MAIN_MENU = 0
    IN_GAME = 1
    GAME_OVER = 2
    GAME_START = 3
    GAME_OPTIONS = 4
    BEFORE_GAME_START = 5
    OPTIONS_MENU = 6

current_state = GameState.MAIN_MENU

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Sprites 

# Load the background's sprite image

# Use this for loading up the file path
current_directory = os.path.dirname(os.path.abspath(__file__))

menu_background_image_path = os.path.join(current_directory, "menu_background.png")
menu_background_image = pygame.image.load(menu_background_image_path)
menu_background_image = pygame.transform.scale(menu_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

options_image_path = os.path.join(current_directory, "settings_background.png")
options_image = pygame.image.load(options_image_path)
options_image = pygame.transform.scale(options_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

before_background_image_path = os.path.join(current_directory, "before_background.png")
before_background_image = pygame.image.load(before_background_image_path)
before_background_image = pygame.transform.scale(before_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# BG Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Actual BGs
background_one_path = os.path.join(current_directory, "background_one.png")
background_one = pygame.image.load(background_one_path)
background_one = pygame.transform.scale(background_one, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_two_path = os.path.join(current_directory, "background_two.png")
background_two = pygame.image.load(background_two_path)
background_two = pygame.transform.scale(background_two, (SCREEN_WIDTH, SCREEN_HEIGHT))

background_three_path = os.path.join(current_directory, "background_three.png")
background_three = pygame.image.load(background_three_path)
background_three = pygame.transform.scale(background_three, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Background colors list
BG_COLORS = [background_one, background_two, background_three]
background_surface = random.choice(BG_COLORS)

gun_icon_path = os.path.join(current_directory, "pixel_gun_icon.png")
gun_icon = pygame.image.load(gun_icon_path)
scaled_width = 100  # Adjust this value to your desired width
scaled_height = 150  # Adjust this value to your desired height
gun_icon = pygame.transform.scale(gun_icon, (scaled_width, scaled_height))

logo_icon_path = os.path.join(current_directory, "logo_sprite.png")
logo_icon = pygame.image.load(logo_icon_path)

# Sound initialization
pygame.mixer.init()
pygame.mixer.set_num_channels(16)  # Set the number of channels to 16 

fire_sound_path = os.path.join(current_directory, "fire_shot_sound.mp3")
fire_sound = pygame.mixer.Sound(fire_sound_path)  

notif_sound_path = os.path.join(current_directory, "notifcation_sound.mp3")
notif_sound = pygame.mixer.Sound(notif_sound_path)  

ealry_shot_path = os.path.join(current_directory, "Early_shot.mp3")
ealry_shot = pygame.mixer.Sound(ealry_shot_path) 

# Load the Arial font
font = pygame.font.Font(pygame.font.match_font('arial'), 42)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quickdraw!")

# The methods & class thing
# This for the menu buttons
class MenuButton:
    def __init__(self, sprite_sheet, x, y, width, height):
        self.sprite_sheet = sprite_sheet
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = "normal"  # Button state (normal, hovered, clicked)

    def update(self, mouse_pos, mouse_clicked):
        if self.x <= mouse_pos[0] <= self.x + self.width and \
           self.y <= mouse_pos[1] <= self.y + self.height:
            if mouse_clicked:
                self.state = "clicked"
            else:
                self.state = "hovered"
        else:
            self.state = "normal"

    def draw(self, screen):
        sprite_rect = pygame.Rect(0, 0, self.width, self.height)
        if self.state == "normal":
            sprite_rect.y = 0
        elif self.state == "hovered":
            sprite_rect.x = self.width
        elif self.state == "clicked":
            sprite_rect.y = self.width * 2
        
        if self is quit_button:
            sprite_rect.y = 110  # Adjust the x position for the options button sprite

        screen.blit(self.sprite_sheet, (self.x, self.y), sprite_rect)

# For the before game basically the how many rounds screen
class BeforGameButton:
    def __init__(self, sprite_sheet, x, y, width, height):
        self.sprite_sheet = sprite_sheet
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = "normal"  # Button state (normal, hovered, clicked)

    def update(self, mouse_pos, mouse_clicked):
        if self.x <= mouse_pos[0] <= self.x + self.width and \
           self.y <= mouse_pos[1] <= self.y + self.height:
            if mouse_clicked:
                self.state = "clicked"
            else:
                self.state = "hovered"
        else:
            self.state = "normal"

    def draw(self, screen):
        sprite_rect = pygame.Rect(0, 0, self.width, self.height)
        if self.state == "normal":
            sprite_rect.y = 0
        elif self.state == "hovered":
            sprite_rect.x = 56
        elif self.state == "clicked":
            sprite_rect.x = 55

        if self is backwards_button:
            sprite_rect.y = 55  # Adjust the x position for the options button sprite
        
        if self is go_back_button:
            sprite_rect.y = 110  # Adjust the x position for the options button sprite

        screen.blit(self.sprite_sheet, (self.x, self.y), sprite_rect)


# Load up the buttons for the menu 
button_sprite_sheet_path = os.path.join(current_directory, "button_atlas.png")
button_sprite_sheet  = pygame.image.load(button_sprite_sheet_path)

button_width = 140
button_height = 50

# Create a button instance - Just so the class is initialized that's why it is here (it may look sloppy). 
play_button = MenuButton(button_sprite_sheet, 335, 350, button_width, button_height)
quit_button = MenuButton(button_sprite_sheet, 335, 400, button_width, button_height)

# Load up the buttons for the menu 
urm_button_sprite_sheet_path = os.path.join(current_directory, "urm_buttons.png")
urm_button_sprite_sheet  = pygame.image.load(urm_button_sprite_sheet_path)

urm_button_width = 60
urm_button_height = 50

# Create a button instance - Just so the class is initialized that's why it is here (it may look sloppy). 
play_button_two = MenuButton(button_sprite_sheet, 320, 450, button_width, button_height)
forwards_button = BeforGameButton(urm_button_sprite_sheet, 300, 350, urm_button_width, urm_button_height)
backwards_button = BeforGameButton(urm_button_sprite_sheet, 360, 350, urm_button_width, urm_button_height)
go_back_button = BeforGameButton(urm_button_sprite_sheet, 420, 350, urm_button_width, urm_button_height)

# Functions like a shot from a gun by turning the screen black and then returns back to normal.
def fire_action():
    fire_sound.play()
    screen.fill(BLACK)
    pygame.display.flip()  # Update the display to show the black screen
    pygame.time.delay(1000)  # Wait for 1 second
    screen.blit(background_surface, (0, 0))
    pygame.display.flip()  # Update the display to show the blue screen

# It does as it told in the title
def reset_quickdraw_bools():
    global p1_quickdraw, p2_quickdraw, p1_round_winner, p2_round_winner, p1_winner_displayed, p2_winner_displayed
    p1_quickdraw = False
    p2_quickdraw = False
    p1_round_winner = False
    p2_round_winner = False
    p1_winner_displayed = False
    p2_winner_displayed = False

def reset_the_game():
    global p1_score, p2_score, rounds
    p1_score = 0
    p2_score = 0
    rounds = 3  # Reset the number of rounds

# Main menu function
def main_menu():
    global game_started, current_state #menu_button_width, menu_button_height
    current_state = GameState.MAIN_MENU
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Get mouse position and clicked status
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Update and draw the button
        play_button.update(mouse_pos, mouse_clicked)
        quit_button.update(mouse_pos, mouse_clicked)

        if mouse_clicked and play_button.state == "clicked":
            pygame.time.delay(600)  # Add a 2-second delay
            game_start_setting() 
            return GameState.BEFORE_GAME_START

        elif mouse_clicked and quit_button.state == "clicked":
            pygame.quit()
            sys.exit()

        # Clear the screen
        screen.fill((0, 0, 0))
        screen.blit(menu_background_image, (0, 0))

        # Draw the buttons
        play_button.draw(screen)
        quit_button.draw(screen)

        screen.blit(logo_icon, (155, 0))

        pygame.display.flip()

# Before the game starts the game will ask for the user to set how much rounds there are. 
def game_start_setting():
    global rounds, rounder, current_state, game_started, return_to_main_menu, background_surface

    waiting_for_key_release = False
    key_press_delay = 200  # Delay in milliseconds
    last_key_press_time = 0
    rounds = 1
    current_state = GameState.BEFORE_GAME_START
    background_surface = random.choice(BG_COLORS)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # Get mouse position and clicked status
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Update and draw the button
        play_button_two.update(mouse_pos, mouse_clicked)
        forwards_button.update(mouse_pos, mouse_clicked)
        backwards_button.update(mouse_pos, mouse_clicked) 
        go_back_button.update(mouse_pos, mouse_clicked)
            
        if mouse_clicked and play_button_two.state == "clicked":
            game_started = True
            current_state = GameState.IN_GAME  # Transition to in-game state
            return

        elif mouse_clicked and forwards_button.state == "clicked":
            current_time = pygame.time.get_ticks()
            if not waiting_for_key_release and current_time - last_key_press_time >= key_press_delay:
                rounds += 1
                if rounds > 5:
                    rounds = 1
                    rounder = rounds
                else:
                    rounder = rounds
                last_key_press_time = current_time
        
        elif mouse_clicked and backwards_button.state == "clicked":
            current_time = pygame.time.get_ticks()
            if not waiting_for_key_release and current_time - last_key_press_time >= key_press_delay:
                rounds -= 1
                if rounds < 1:
                    rounds = 5
                    rounder = rounds
                else:
                    rounder = rounds
                last_key_press_time = current_time

        elif mouse_clicked and go_back_button.state == "clicked":
            pygame.time.delay(670) 
            return_to_main_menu = True

        elif return_to_main_menu:
            break
     
        else:
            waiting_for_key_release = False

        screen.fill((255, 255, 255))
        screen.blit(before_background_image, (0, 0))

        round_text = "Rounds: " + str(rounds)
        round_text_surface = font.render(round_text, True, (0, 0, 0))
        round_text_rect = round_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(round_text_surface, round_text_rect)

        play_button_two.draw(screen)
        forwards_button.draw(screen)
        backwards_button.draw(screen)
        go_back_button.draw(screen)

        pygame.display.flip()
    
# Game loop
running = True
while running:
    if current_state == GameState.MAIN_MENU:
        current_state = main_menu()
        countdown_timer = 0

    elif current_state == GameState.IN_GAME:
        reset_the_game()  # Reset game variables
        reset_quickdraw_bools()  # Reset quickdraw flag
        countdown_timer = 0  # Reset countdown timer for a new game

    elif current_state == GameState.BEFORE_GAME_START:
        current_state = game_start_setting()
        countdown_timer = 0
    
    if return_to_main_menu:
        current_state = GameState.MAIN_MENU
        return_to_main_menu = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # The controls and keyboard stuff
    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Player 1 quickdraw handling
    if keys[pygame.K_f] and not p1_key_pressed:
        p1_quickdraw = True
        p1_key_pressed = True
    
    # Player 2 quickdraw handling
    if keys[pygame.K_j] and not p2_key_pressed:
        p2_quickdraw = True
        p2_key_pressed = True
    
    # Update the key press flags
    if not keys[pygame.K_f]:
        p1_key_pressed = False
    if not keys[pygame.K_j]:
        p2_key_pressed = False
    
    # Fill the background with white
    screen.blit(background_surface, (0, 0))
    
    # Game logic
    # The fire logic 
    if countdown_timer < 100 and not round_winner_displayed and game_started:
        countdown_timer += 1

    # This is for that disqualification.
    if countdown_timer < 100 and not round_winner_displayed:
        if p1_quickdraw and not p2_quickdraw and not p2_timeout and not p1_timeout:
            # Player 1 pressed too early and gets disqualified
            p1_timeout = True
            p2_timeout = False
            ealry_shot.play()

        elif p2_quickdraw and not p1_quickdraw and not p1_timeout and not p2_timeout:
            # Player 2 pressed too early and gets disqualified
            p1_timeout = False
            p2_timeout = True
            ealry_shot.play()

    if countdown_timer >= 100 and random_timer != 130:
        screen.blit(gun_icon, (350, 150))

        if p1_quickdraw and not p1_timeout:
            fire_action()
            p1_score += 1
            countdown_timer = 0 
            random_timer = 0
            p1_round_winner = True
        elif p2_quickdraw and not p2_timeout:
            fire_action()
            p2_score += 1
            countdown_timer = 0 
            random_timer = 0
            p2_round_winner = True
        

    # Pretty much does the same thing as the regular player quickdraw but with a random rng because why not.
    # I thought it would be cool I guess.
    if random_timer < 130 and not round_winner_displayed and game_started:
        random_timer += 1
    
        # Check for the "Failed" condition
        if countdown_timer >= 100 and random_timer >= 130:
            random_winner_selection = random.choice(random_choice)
            # Yeah it acts like the same.
            if random_winner_selection == "P1" and not p1_timeout:
                fire_action()
                p1_score += 1
                countdown_timer = 0 
                random_timer = 0
                p1_round_winner = True
                
            elif p1_timeout:
                fire_action()
                p2_score += 1
                countdown_timer = 0 
                random_timer = 0
                p2_round_winner = True
                
            elif random_winner_selection == "P2" and not p2_timeout:
                fire_action()
                p2_score += 1
                countdown_timer = 0 
                random_timer = 0
                p2_round_winner = True
            elif p2_timeout:
                fire_action()
                p1_score += 1
                countdown_timer = 0 
                random_timer = 0
                p1_round_winner = True
                
    # Winner select text
    if p1_round_winner and not p2_round_winner and not round_winner_displayed:
        winner_text = "Player 1 wins this round!"
        winner_text_surface = font.render(winner_text, True, (0, 0, 0))
        winner_text_rect = winner_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Display the winning screen for a duration
        if not round_winner_displayed:
            round_winner_display_start_time = current_time
            round_winner_displayed = True

    # This here is causing the issue.
    elif p2_round_winner and not p1_round_winner and not round_winner_displayed:
        winner_text = "Player 2 wins this round!"
        winner_text_surface = font.render(winner_text, True, (0, 0, 0))
        winner_text_rect = winner_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        p1_timeout = False
        p2_timeout = False

        # Display the winning screen for a duration
        if not round_winner_displayed:
            round_winner_display_start_time = current_time
            round_winner_displayed = True

    # The Winner selection
    if p1_score == rounder:
        p1_winner_displayed = True
        p2_winner_displayed = False  # Ensure the other winner display flag is False

    elif p2_score == rounder:
        p2_winner_displayed = True
        p1_winner_displayed = False  # Ensure the other winner display flag is False

    # Display logic
    if round_winner_displayed:
        if current_time - round_winner_display_start_time <= round_winner_display_duration:
            screen.blit(background_surface, (0, 0))
            screen.blit(winner_text_surface, winner_text_rect)
            countdown_timer = 0
            p1_timeout = False
            p2_timeout = False
        
        else:
            round_winner_displayed = False
            round_winner_display_start_time = 0
            countdown_timer = 0

    # Check if the overall winner text has been displayed
    if p1_winner_displayed and not p2_winner_displayed:
        winner_text = "Player 1 Wins!"
        winner_text_surface = font.render(winner_text, True, (0, 0, 0))
        winner_text_rect = winner_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_text_surface, winner_text_rect)
        print("P1 Wins")
        pygame.time.delay(2000)  # Display the winner for 2 seconds
        reset_the_game()
        reset_quickdraw_bools()
        # Go back to main after game has ended.
        current_state = GameState.MAIN_MENU  # Go back to the main menu

    elif p2_winner_displayed and not p1_winner_displayed:
        winner_text = "Player 2 Wins!"
        winner_text_surface = font.render(winner_text, True, (0, 0, 0))
        winner_text_rect = winner_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_text_surface, winner_text_rect)
        print("P2 Wins")
        pygame.time.delay(2000)  # Display the winner for 2 seconds
        reset_the_game()
        reset_quickdraw_bools()
        # Go back to main after game has ended.
        current_state = GameState.MAIN_MENU  # Go back to the main menu

    reset_quickdraw_bools()
    
    # Draw

    # Render the text
    text = f"{p1_score}  {p2_score}"
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect)
    
    # Update the display
    pygame.display.flip()

    # Limit frame rate to 60 FPS
    clock.tick(60)
    
# Clean up
pygame.quit()
sys.exit()