import pygame, sys
from pygame.locals import *
from pygame import Vector2
from PhysicsEngine import Two_Body_System as TBS

class App:

    def __init__(self):
        pygame.init()

        self.WIN_SIZE = [1080, 600]
        self.screen = pygame.display.set_mode(self.WIN_SIZE)
        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.system = TBS(self.screen, 2, 5, Vector2(-100, 0), Vector2(100, 0), Vector2(1, 1), Vector2(0, 0))

    def run(self):
        paused = False
        running = True
        while running:

            t = pygame.time.get_ticks() / 1000  ## Elapsed time in seconds
            dt = self.clock.get_time() / 1000  ## Delta time (time since last call) in seconds


            self.screen.fill((35, 35, 40))

            ## Check Inpot
            for event in pygame.event.get():
                #print(event)

                if event.type == QUIT:
                    running = False
                    sys.exit()

                if event.type == KEYDOWN:

                    paused =  not  paused
                    if paused :
                        print("Paused")
                        pygame.time.delay(10000)


            self.system.update(t, dt)

            pygame.display.update()
            self.clock.tick(self.FPS)


def main():
    app = App()
    app.run()



if __name__ == '__main__':
    main()