import pygame 
import time
import random
pygame.font.init()

### Window
WIDTH, HEIGHT = 1024, 1024
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game")

backgrounds = ["b1.png", "b2.png", "b3.png", "b4.png"]
last_BG = random.choice(backgrounds)
BG = pygame.image.load(last_BG)

### Player
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_VEL = 7
player_health = 3

FONT = pygame.font.SysFont("comicsans", 30)

level = 1

### Projectiles

STAR_WIDTH = 20
STAR_HEIGHT = 20

class Star:
    def __init__(self):
        self.x, self.y, self.direction = self.get_initial_position_and_direction()
        self.rect = pygame.Rect(self.x, self.y, STAR_WIDTH, STAR_HEIGHT)
        self.speed = random.randint(2, 4) 
        self.is_active = True # Flag to track if the star is active (on-screen)

    def get_initial_position_and_direction(self):
        # Decide from which edge the star will enter and set its direction
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            return random.randint(0, WIDTH - STAR_WIDTH), -STAR_HEIGHT, (0, 1)
        elif edge == 'bottom':
            return random.randint(0, WIDTH - STAR_WIDTH), HEIGHT, (0, -1)
        elif edge == 'left':
            return -STAR_WIDTH, random.randint(0, HEIGHT - STAR_HEIGHT), (1, 0)
        else:
            return WIDTH, random.randint(0, HEIGHT - STAR_HEIGHT), (-1, 0)

    def update(self, player_rect):
        # Update the star's position
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if self.rect.colliderect(player_rect):
            self.is_active = False
            return True

        # Remove the star if it goes off-screen
        if (self.rect.x < -STAR_WIDTH or self.rect.x > WIDTH + STAR_WIDTH or
            self.rect.y < -STAR_HEIGHT or self.rect.y > HEIGHT + STAR_HEIGHT):
            self.is_active = False

        return False

        

    def draw(self, window):
        pygame.draw.rect(window, (153, 51, 255), self.rect)  # Draw the star as white


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    level_text = FONT.render(f"Level: {level}", 1, (24, 232, 38))
    WIN.blit(level_text, (10, 10))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, (24, 232, 38))
    WIN.blit(time_text, (10, 50))

    health_text = FONT.render(f"Health: ", 1, (24, 232, 38))
    WIN.blit(health_text, (10, 90))
    health = [pygame.Rect(120, 105, 20, 20), pygame.Rect(150, 105, 20, 20), pygame.Rect(180, 105, 20, 20)]
    for i in range(player_health):
        pygame.draw.rect(WIN, "red", health[i])

    for star in stars:
        star.draw(WIN)

    pygame.draw.rect(WIN, (24, 232, 38), player)

    pygame.display.update()

def main():
    run = True
    global player_health
    global level
    global BG
    global last_BG
    player = pygame.Rect(492, HEIGHT - PLAYER_HEIGHT - 30, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []

    while run:
        star_count += clock.tick(165)
        elapsed_time = time.time() - start_time

        # Upon level-up
        if elapsed_time >= 15:
            level += 1
            stars.clear()
            start_time = time.time()
            elapsed_time = 0
            star_add_increment = 2000 - 100 * level
            
            new_BG = random.choice(backgrounds)
            while new_BG == last_BG:
                new_BG = random.choice(backgrounds)

            last_background = new_BG
            BG = pygame.image.load(new_BG)

        if star_count > star_add_increment:
            for _ in range(3 * level):
                stars.append(Star())
            star_add_increment = max(100, 1000 - 150 * level, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
        if keys[pygame.K_d]:
            if player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VEL
        if keys[pygame.K_w]:
            if player.y - PLAYER_VEL >= 0:
                player.y -= PLAYER_VEL
        if keys[pygame.K_s]:
            if player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
                player.y += PLAYER_VEL

        for star in stars[:]:
            if star.update(player):
                player_health -= 1
                stars.clear()
                if player_health <= 0:
                    run = False
                    break
        
        stars = [star for star in stars if star.is_active]

        draw(player, elapsed_time, stars)

             

    pygame.quit()

if __name__ == "__main__":
    main()