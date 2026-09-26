import asyncio
import random
import pygame  # noqa: F401 — ΜΗΝ το σβήσεις: το pygbag διαβάζει ΜΟΝΟ αυτό το αρχείο για imports
import time

# ---------------- Ρυθμίσεις ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60

random.seed(time.time_ns())

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Πιάσε το νόμισμα")
    clock = pygame.time.Clock()

    # ΒΗΜΑ 1 — ο παίκτης: ένα ορθογώνιο (x, y, πλάτος, ύψος)
    player = pygame.Rect(380, 280, 40, 40)
    speed = 5

    # ΒΗΜΑ 3 — το νόμισμα: σε τυχαία θέση
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)
    coin_rect = pygame.Rect(coin_x - 15, coin_y - 15, 30, 30)

    # ΒΗΜΑ 4 - το σκόρ
    score = 0
    font = pygame.font.Font(None, 48)

    # ΒΗΜΑ 5 - Ο Εχθρός!!!!!!!!!!!!!!
    enemy = pygame.Rect(100, 450, 50, 50)
    enemy_speed = 3
    enemy_dir = 1

    running = True
    while running:
        # 1) ΓΕΓΟΝΟΤΑ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2) ΛΟΓΙΚΗ
        # ΒΗΜΑ 2 — κίνηση με τα βελάκια
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed
        player.clamp_ip(screen.get_rect())

        # Επαφή παίκτη και νομίσματος
        if player.colliderect(coin_rect):
            score += 1
            coin_x = random.randint(20, WIDTH - 20)
            coin_y = random.randint(20, HEIGHT - 20)
            coin_rect.x = coin_x - 15
            coin_rect.y = coin_y - 15

        enemy.x += enemy_dir * enemy_speed
        if enemy.right >= WIDTH or enemy.left <= 0:
            enemy_dir *= -1

        if player.colliderect(enemy):
            running = False

        # 3) ΖΩΓΡΑΦΙΚΗ
        screen.fill((15, 40, 60))
        pygame.draw.rect(screen, (80, 200, 120), player)
        pygame.draw.circle(screen, (255, 209, 102), (coin_x, coin_y), 15)
        pygame.draw.rect(screen, (255, 100, 100), enemy)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)  # ΜΗΝ το σβήσεις: χωρίς αυτό δεν τρέχει στο web

    pygame.quit()


asyncio.run(main())