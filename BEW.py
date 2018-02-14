import pygame
import sys
import LinkedList
import numpy as np

MAXFPS = 50
SCREEN_SIZE = 800, 600
UNIT_LENGTH = 101  # must be odd numbers
BULLET_LENGTH = 30

map_img = pygame.image.load("map.png")

unit_img = pygame.image.load("unit.png")
unit_img = pygame.transform.scale(unit_img, (UNIT_LENGTH, UNIT_LENGTH))
temp_bullet_img = pygame.image.load("bullet.png")
temp_bullet_img = pygame.transform.scale(temp_bullet_img, (BULLET_LENGTH, BULLET_LENGTH))


class BEW(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(10, 25)
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.units = LinkedList.LL()
        self.gunfire = LinkedList.LL()
        tmp = Unit()
        tmp.p = (600, 600)
        tmp.img = unit_img
        tmp.img_rot = tmp.img
        self.units.insert(tmp)

    def run(self):
        # define local variables
        fps_clk = pygame.time.Clock()
        up_act = False
        down_act = False
        left_act = False
        right_act = False
        # lines of figure in map
        # rectangle, rectangle, rectangle, hexagon, rectangle, rectangle
        map_lines = \
            [
                ((200, 176), (200, 450)), ((200, 450), (476, 450)), ((476, 450), (476, 176)), ((476, 176), (200, 176)),
                ((834, 505), (934, 592)), ((934, 592), (767, 789)), ((767, 789), (664, 702)), ((664, 702), (834, 505)),
                ((282, 658), (282, 1034)), ((282, 1034), (346, 1034)), ((346, 1034), (346, 658)),
                ((346, 658), (282, 658)), ((824, 139), (756, 250)), ((756, 250), (825, 361)), ((825, 361), (963, 361)),
                ((963, 361), (1026, 250)), ((1026, 250), (963, 129)), ((963, 129), (824, 139)),
                ((1224, 411), (1172, 527)), ((1172, 527), (1350, 609)), ((1350, 609), (1402, 492)),
                ((1402, 492), (1224, 411)), ((1088, 889), (1121, 1073)), ((1121, 1073), (1332, 1034)),
                ((1332, 1034), (1299, 852)), ((1299, 852), (1088, 889))
             ]
        # points of figure in map
        map_points = \
            [
                (200, 176), (200, 450), (476, 450), (476, 176), (834, 505), (934, 592), (767, 789), (664, 702),
                (282, 658), (282, 1034), (346, 1034), (346, 658), (824, 139), (756, 250), (825, 361), (963, 361),
                (1026, 250), (963, 129), (1224, 411), (1172, 527), (1350, 609), (1402, 492), (1088, 889), (1121, 1073),
                (1332, 1034), (1299, 852)
            ]

        # main routine
        while True:
            # set maximum fps
            fps_clk.tick(MAXFPS)

            # local variables
            user = self.units.head.next.val
            now_map = map_img.copy()

            # draw map
            draw_screen([self.gunfire, self.units], now_map)

            # draw screen
            self.screen.fill((255, 255, 255))

            self.screen.blit(now_map, (-user.p[0]+400, -user.p[1]+300))
            pygame.display.update()

            temp_fire = self.gunfire.head.next
            while temp_fire != self.gunfire.tail:
                next_fire = temp_fire.next
                if self.out_of_map(temp_fire.val):
                    temp_fire.val.move()
                else:
                    self.gunfire.delete(temp_fire)
                temp_fire = next_fire

            # handle events
            for event in pygame.event.get():
                # when click x button on window

                if event.type == pygame.QUIT:
                    sys.exit()
                # when press the keyboard
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        up_act = True
                    if event.key == pygame.K_a:
                        left_act = True
                    if event.key == pygame.K_d:
                        right_act = True
                    if event.key == pygame.K_s:
                        down_act = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        up_act = False
                    if event.key == pygame.K_a:
                        left_act = False
                    if event.key == pygame.K_d:
                        right_act = False
                    if event.key == pygame.K_s:
                        down_act = False

            # move "wasd"
            if up_act:
                user.move((0, -2))
            if down_act:
                user.move((0, 2))
            if left_act:
                user.move((-2, 0))
            if right_act:
                user.move((2, 0))

            if pygame.mouse.get_pressed()[0]:
                new_shot = M_gun()
                new_shot.p = user.p
                new_shot.direct = user.direct
                self.gunfire.insert(new_shot)

            # make user unit look toward mouse position
            xy = np.subtract(np.array(pygame.mouse.get_pos()), np.array((400, 300)))
            if xy[0] == 0:
                if xy[1] / abs(xy[1]) == 1:
                    user.direct = -90
                else:
                    user.direct = 90
            else:
                user.direct = 0 - np.rad2deg(np.arctan(xy[1] / xy[0]))
                if xy[0] < 0:
                    user.direct += 180

            user.arr = pygame.surfarray.array3d(user.img_rot)

            cur = self.gunfire.head.next
            while cur != self.gunfire.tail:
                cur.val.arr = pygame.surfarray.array3d(cur.val.img_rot)
                cur = cur.next

    def out_of_map(self, bullet):
        return 1600 > bullet.p[0] > 0 and 1200 > bullet.p[1] > 0


# check whether the points collide given lines or not
def line_collision(line_list, point_list):
    def line_point(l, p):
        x1, y1 = l[0]
        x2, y2 = l[1]
        x3, y3 = p
        if x1 == x2:
            d = (x3 - x1) ** 2
        else:
            m = (y2 - y1) / (x2 - x1)
            d = ((m * (x3 - x1) + (y1 - y3)) ** 2) / (1 + m**2)
        return d <= 2 and ((x1 <= x3 <= x2) or (x2 <= x3 <= x1)) and ((y1 <= y3 <= y2) or (y2 <= y3 <= y1))

    res = []
    for i in range(len(point_list)):
        res.append(False)
        for j in range(len(line_list)):
            if line_point(line_list[j], point_list[i]):
                res[-1] = True
                break
    return res


# bullet class
class M_gun(object):
    def __init__(self):
        self.p = [0, 0]
        self.img = temp_bullet_img
        self.img_rot = self.img
        self.direct = 0
        self.arr = None

    def move(self):
        self.p = self.p[0] + np.cos(np.deg2rad(self.direct))*50, self.p[1] - np.sin(np.deg2rad(self.direct))*50


# wandering unit including user unit
class Unit(object):
    def __init__(self):
        self.p = [0, 0]
        self.img = None
        self.img_rot = None
        self.direct = 0  # deg
        self.arr = None

    def move(self, d):
        self.p = self.p[0] + d[0], self.p[1] + d[1]


# take pygame.Surface(screen) and list comprised of LinkedList.LL
# draw given Units in LinkedLists on given Surface(screen)
def draw_screen(ls, screen):
    for LL in ls:
        # defensive coding
        if type(LL) != LinkedList.LL or type(screen) != pygame.Surface:
            raise TypeError

        # draw unit image on screen
        cur = LL.head.next
        while cur != LL.tail:
            new_img = pygame.transform.rotate(cur.val.img, cur.val.direct)
            cur.val.img_rot = new_img
            new_p = cur.val.p[0] - int(new_img.get_size()[0] / 2), cur.val.p[1] - int(new_img.get_size()[1] / 2)
            screen.blit(new_img, new_p)
            cur = cur.next


if __name__ == '__main__':
    bew = BEW()
    bew.run()