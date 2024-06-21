import pygame 
import board
import math

# ------------------ CONSTANTS -------------------- #
FPS = 60
WIDTH, HEIGHT = 700, 775
COLLIDE_LILLY = pygame.USEREVENT + 1
COLLIDE_OUCH = pygame.USEREVENT + 2

# ------------------ GAMEPLAY ---------------------- #
def main():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frogger")

    clock = pygame.time.Clock()
    b = board.Board(WIN)
    b.init_moveables()
    run = True 

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:
                    b.player.move('l')
                elif event.key == pygame.K_RIGHT:
                    b.player.move('r')
                elif event.key == pygame.K_UP:
                    b.player.move('u')
                elif event.key == pygame.K_DOWN:
                    b.player.move('d')

            if event.type == COLLIDE_OUCH:
                b.player.has_died()
                pygame.time.delay(500)
                if b.player.get_lives() == 0:
                    # player has died
                    run = False 
                    break
                else:
                    b.player.reset()

            if event.type == COLLIDE_LILLY:
                pygame.time.delay(500)
                b.player.inc_lives()
                b.player.reset()
                for road in b.enemies:
                    for e in road:
                        e.speed_up()
                for lane in b.logs:
                    for l in lane:
                        l.speed_up()

                if len(b.occupied_pads) == 5:
                    run = False
                    print("Congrats! You won!")
                    break 
                
        if run:
            # movement and positioning
            b.draw_board()
            b.move_moveables()
            for road in b.enemies:
                for enemy in road:
                    enemy.update()
            for road in b.logs:
                for log in road:
                    log.update()

            b.player.update()

            # check for player/log collision & move player
            on_log = False
            for lane in b.logs:
                for log in lane:
                    if log.log.colliderect(b.player.player):
                        on_log = True
                        b.player.player.x += math.cos(log.dir)*log.VEL

            # checking for enemy/player collision
            for road in b.enemies:
                for enemy in road:
                    if enemy.enemy.colliderect(b.player.player):
                        pygame.event.post(pygame.event.Event(COLLIDE_OUCH))

            # checking for collision with lilly pads
            for oc in b.occupied_pads:
                if b.player.player.colliderect(oc):
                    pygame.event.post(pygame.event.Event(COLLIDE_OUCH))
            for l in range(len(b.pads)):
                if b.player.player.colliderect(b.pads[l]):
                    # place an image of the frog on the lilly pad 
                    b.occupied_pads.append(b.pads[l])
                    pygame.event.post(pygame.event.Event(COLLIDE_LILLY))   

            # checking for collision with hedge 
            check = True
            for h in range(len(b.top_hedge)):
                if b.player.player.colliderect(b.top_hedge[h]) and check:
                    check = False
                    pygame.event.post(pygame.event.Event(COLLIDE_OUCH))    

            # detect collision with open water 
            check = True
            for lane in b.water:
                for w in lane:
                    if w.colliderect(b.player.player) and not on_log and check:
                        check = False
                        pygame.event.post(pygame.event.Event(COLLIDE_OUCH))
                        

            pygame.display.update()
        
    pygame.quit()


# ------------------ RUNNING ---------------------- #
if __name__ == "__main__":
    main()

