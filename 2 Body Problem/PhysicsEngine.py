import pygame
from pygame import Vector2
import math

GRAVITY = 1

class Two_Body_System:

    def __init__(self,screen, mass1, mass2, pos1=Vector2(0, 0), pos2=Vector2(0,0), init_vel1= Vector2(0, 0), init_vel2= Vector2(0, 0)):
        self.screen = screen
        self.screen_dim = self.screen.get_size()
        self.offset = Vector2(self.screen_dim[0]/2, self.screen_dim[1]/2 )

        ## Mass 1
        self.mass1 = mass1
        self.m1_col = (225, 10, 100)
        self.m1_pos = pos1
        self.m1_vel = init_vel1

        ## Mass 2
        self.mass2 = mass2
        self.m2_col = (112, 90, 210)

        self.m2_pos = pos2
        self.m2_vel = init_vel2

        self.m1_accel_field = self.calculate_m1_accel_field()


    def linear_grad(self, start, fin=[255, 255, 255], n=5):
        grad_list = []

        for i in range(1, n):
            curr = []

            for j in range(0, 3):
                c = start[j] + ((float(i) / (n - 1)) * (fin[j] - start[j]))
                curr.append(c)

            grad_list.append(curr)

        return grad_list

    def get_m1_accel(self, m1_pos, m2_pos):

        direction = m2_pos.__sub__(m1_pos)
        dir_mag = direction.magnitude()

        if dir_mag == 0:
            unit_dir = Vector2(0, 0)
        else:
            unit_dir = direction.__mul__(1/(3*dir_mag ** 2))

        return unit_dir.__mul__(self.mass2 * GRAVITY)

    def calculate_m1_accel_field(self):
        field = []

        for y in range(-self.screen_dim[1]//2, self.screen_dim[1]//2, 50):
            field.append([])
            for x in range(-self.screen_dim[0]//2, self.screen_dim[0]//2, 50):

                field.append(self.get_m1_accel( Vector2(x, y), self.m2_pos ))

        return field

    def get_m2_accel(self, m1_pos, m2_pos):
        direction = m1_pos.__sub__(m2_pos)
        dir_mag = direction.magnitude()

        if dir_mag == 0:
            unit_dir = Vector2(0, 0)
        else:
            unit_dir = direction.__mul__(1 / (dir_mag ** 2))

        return unit_dir.__mul__(self.mass1 * GRAVITY)


    def show_field(self, field):

        for y in range(-self.screen_dim[1]//2, self.screen_dim[1]//2, 10):

            for x in range(-self.screen_dim[0]//2, self.screen_dim[0]//2, 10):
                if Vector2(x, y).__sub__(self.m1_pos).magnitude() > 20 and Vector2(x, y).__sub__(self.m2_pos).magnitude() > 20:
                    start = Vector2(x, y).__add__(self.offset)
                    tmp = self.get_m1_accel(Vector2(x, y), self.m2_pos).__add__(self.get_m1_accel(Vector2(x, y), self.m1_pos)).__mul__(20)
                    end_pos = start.__add__(tmp)

                    # pygame.draw.circle(self.screen, (255, 255, 255), start, 2)
                    # pygame.draw.circle(self.screen, (255,0, 0), end_pos, 1)
                    pygame.draw.line(self.screen, (90, 90, 95), start, end_pos)

    def update(self, t , dt):
        self.m1_vel = self.m1_vel.__add__(self.get_m1_accel(self.m1_pos, self.m2_pos).__mul__(1))
        self.m1_pos = self.m1_pos.__add__(self.m1_vel.__mul__(1))

        self.m2_vel = self.m2_vel.__add__(self.get_m2_accel(self.m1_pos, self.m2_pos).__mul__(1))
        self.m2_pos = self.m2_pos.__add__(self.m2_vel)

        #self.m2_pos = Vector2(900 * math.cos(0.1 * t) * dt, 900 * math.sin(0.1 * t) * dt)
        self.show_field(self.m1_accel_field)
        pygame.draw.circle(self.screen, self.m1_col, self.m1_pos.__add__(self.offset), 5)
        pygame.draw.circle(self.screen, self.m2_col, self.m2_pos.__add__(self.offset), 5)