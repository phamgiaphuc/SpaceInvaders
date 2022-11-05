import pygame
import sys
import math
import random
from pygame import mixer
from button import Button

pygame.init()

# Create the screen:
# Width = 800; Height = 600
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("resources/background.png")

# Logo
logo = pygame.image.load("resources/logo.png")

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("resources/spaceship.png")
pygame.display.set_icon(icon)

# Sound
mixer.music.load("resources/background.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.35)


# Return the font and size
def get_font(size):
    return pygame.font.Font("resources/font.ttf", size)


# Show the logo
def show_logo():
    screen.blit(logo, (285, 20))


# Play stage
def play():
    # Player
    player = pygame.image.load("resources/spaceship.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Alien
    alienImg = []
    alienX = []
    alienY = []
    alienX_change = []
    alienY_change = []
    num_of_aliens = 6

    for i in range(num_of_aliens):
        alienImg.append(pygame.image.load("resources/alien.png"))
        alienX.append(random.randint(0, 735))
        alienY.append(random.randint(40, 100))
        alienX_change.append(3)
        alienY_change.append(40)

    # Bullet
    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    bulletImg = pygame.image.load("resources/bullet.png")
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 15
    bullet_state = "ready"

    # Score
    score_value = 0
    textX = 625
    testY = 10

    def player_movement(x, y):
        screen.blit(player, (x, y))

    def alien_movement(x, y, i):
        screen.blit(alienImg[i], (x, y))

    def game_over_text():
        over_text = get_font(64).render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (140, 250))

    def fire_bullet(x, y):
        screen.blit(bulletImg, (x + 15, y + 10))
        return "fire"

    def is_collision(x1, y1, x2, y2):
        distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
        if distance < 27:
            return True
        else:
            return False

    def show_score(x, y):
        score = get_font(20).render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    while True:
        # Set the background for the menu stage
        screen.blit(background, (0, 0))
        # Get the position of the user mouse
        play_mouse_position = pygame.mouse.get_pos()

        back_button = Button(image=pygame.image.load("resources/rect.png"), pos=(80, 30),
                             text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        back_button.change_color(play_mouse_position)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(play_mouse_position):
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("resources/laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        bullet_state = fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0

        playerX += playerX_change
        # Checking for the boundaries of spaceship, so it doesn't go out of bounds
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(num_of_aliens):
            # Game Over
            if alienY[i] > 440:
                for j in range(num_of_aliens):
                    alienY[j] = 2000
                game_over_text()
                break

            alienX[i] += alienX_change[i]

            if alienX[i] <= 0:
                alienX_change[i] = 3
                alienY[i] += alienY_change[i]
            elif alienX[i] >= 736:
                alienX_change[i] = -3
                alienY[i] += alienY_change[i]

            alien_movement(alienX[i], alienY[i], i)

            # Collision
            collision = is_collision(alienX[i], alienY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("resources/explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                alienX[i] = random.randint(0, 735)
                alienY[i] = random.randint(40, 100)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player_movement(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()


# Main menu
def main_menu():
    while True:
        # Set the background for the menu stage
        screen.blit(background, (0, 0))
        # Get the position of the user mouse
        menu_mouse_position = pygame.mouse.get_pos()
        # Set the text "MAIN MENU"
        menu_text = get_font(30).render("MAIN MENU", True, "#b68f40")
        menu_rectangle = menu_text.get_rect(center=(410, 250))

        play_button = Button(image=pygame.image.load("resources/rect.png"), pos=(410, 310),
                             text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="Green")
        quit_button = Button(image=pygame.image.load("resources/rect.png"), pos=(410, 370),
                             text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="Green")

        screen.blit(menu_text, menu_rectangle)

        for button in [play_button, quit_button]:
            button.change_color(menu_mouse_position)
            button.update(screen)

        screen.blit(menu_text, menu_rectangle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_position):
                    play()
                if quit_button.check_for_input(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

        show_logo()
        pygame.display.update()


main_menu()
