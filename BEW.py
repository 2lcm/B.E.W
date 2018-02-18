import pygame
import sys
import LinkedList
import numpy as np

MAXFPS = 50
SCREEN_SIZE = 800, 600
UNIT_LENGTH = 101  # must be odd numbers
UNIT_RAD2 = (UNIT_LENGTH//2)**2
BULLET_LENGTH = 30

map_img = pygame.image.load("map.png")

unit_img = pygame.image.load("white_unit.png")
unit_img = pygame.transform.scale(unit_img, (UNIT_LENGTH, UNIT_LENGTH))
temp_bullet_img = pygame.image.load("bullet.png")
temp_bullet_img = pygame.transform.scale(temp_bullet_img, (BULLET_LENGTH, BULLET_LENGTH))

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
        ((1332, 1034), (1299, 852)), ((1299, 852), (1088, 889)),((0,0),(1600,0)),((0,0),(0,1200)),((0,1200),(1600,1200)), ((1600,1200),(1600,0))
     ]
# points of figure in map
map_points = \
    [
        (200, 176), (200, 450), (476, 450), (476, 176), (834, 505), (934, 592), (767, 789), (664, 702),
        (282, 658), (282, 1034), (346, 1034), (346, 658), (824, 139), (756, 250), (825, 361), (963, 361),
        (1026, 250), (963, 129), (1224, 411), (1172, 527), (1350, 609), (1402, 492), (1088, 889), (1121, 1073),
        (1332, 1034), (1299, 852)
    ]

# index of points
figures = [((0, 1, 2), (0, 2, 3)), ((4, 5, 6), (4, 6, 7)), ((8, 9, 10), (8, 10, 11)),
           ((12, 13, 14), (14, 15, 16), (16, 17, 12), (12, 14, 16)), ((18, 19, 20), (18, 20, 21)),
           ((22, 23, 24), (22, 24, 25))]


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
        self.AIs = LinkedList.LL()
        tmp = Unit()
        tmp.p = (850,850)
        tmp.img = unit_img
        tmp.img_rot = tmp.img
        self.AIs.insert(tmp)



    def run(self):
        # define local variables
        fps_clk = pygame.time.Clock()
        up_act = False
        down_act = False
        left_act = False
        right_act = False

        # main routine
        while True:
            # set maximum fps
            fps_clk.tick(MAXFPS)

            # local variables
            user = self.units.head.next.val

            now_map = map_img.copy()

            # draw map
            draw_screen([self.gunfire, self.units, self.AIs], now_map)

            # draw screen
            self.screen.fill((0, 0, 0))

            self.screen.blit(now_map, (-user.p[0]+400, -user.p[1]+300))
            pygame.display.update()

            temp_fire = self.gunfire.head.next
            while temp_fire != self.gunfire.tail:
                next_fire = temp_fire.next
                if self.out_of_map(temp_fire.val):
                    if not temp_fire.val.move():
                        self.gunfire.delete(temp_fire)
                else:
                    self.gunfire.delete(temp_fire)
                temp_fire = next_fire
            user_done = False
            first_AIs = False
            temp_unit = self.units.head.next
            temp_unit = self.AIs.head.next
            while True:
                temp_fire = self.gunfire.head.next
                if temp_fire == self.gunfire.tail or temp_unit == self.AIs.tail:
                    break
                while True:
                    if temp_fire == self.gunfire.tail:
                        break
                    temp_next_fire = temp_fire.next
                    if (temp_unit.val.p[0] - temp_fire.val.p[0])**2 + (temp_unit.val.p[1] - temp_fire.val.p[1])**2 < UNIT_RAD2:
                        temp_unit.val.life -=1
                        print('life is :', temp_unit.val.life)
                        self.gunfire.delete(temp_fire)
                    if temp_unit.val.life == 0:
                        self.AIs.delete(temp_unit)
                    if temp_next_fire == self.gunfire.tail:
                        break
                    temp_fire = temp_next_fire
                if temp_unit.next == self.units.tail:
                    user_done = True
                elif temp_unit == self.AIs.head.next:
                    first_AIs = True

                if user_done == False:
                    temp_unit = temp_unit.next
                else:
                    if first_AIs == False:
                        temp_unit = self.AIs.head.next
                    else:
                        temp_unit = temp_unit.next



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

    def out_of_map(self, bullet):
        return 1600 > bullet.p[0] > 0 and 1200 > bullet.p[1] > 0

def collision_clfr(map_info, user_pos):
    unit_rad = UNIT_LENGTH//2
    for temp in map_info:
        tri_side = list(((temp[0][0] - temp[1][0])**2 + (temp[0][1] - temp[1][1])**2, (temp[0][0] - user_pos[0])**2\
                   + (temp[0][1] - user_pos[1])**2, (temp[1][0] - user_pos[0])**2 + (temp[1][1] - user_pos[1])**2))
        if tri_side[1] > tri_side[0] + tri_side[2] or tri_side[2] > tri_side[0] + tri_side[1]:  # 둔각
            if tri_side[1] < unit_rad **2 or tri_side[0] < unit_rad **2:
                return True
        else:  # 예각
            A2 = (-2 * sum([x**2 for x in tri_side]) + sum([y for y in tri_side])**2) / 16
            if 4*A2 < tri_side[0] * unit_rad ** 2:
                return True
    return False


def in_triangular(p1, p2, p3, check_p):
    def magnitude(v):
        return (v[0] ** 2 + v[1] ** 2) ** (1/2)

    def angular(v1, v2):
        try:
            return np.arccos((v1[0] * v2[0] + v1[1] * v2[1]) / (magnitude(v1) * magnitude(v2)))
        except ZeroDivisionError:
            return 0

    ang_sum = 0
    v = [(p[0] - check_p[0], p[1] - check_p[1]) for p in [p1, p2, p3]]
    for i in range(3):
        ang_sum += angular(v[i], v[(i+1) % 3])
    return np.pi * 350/180 < ang_sum < np.pi * 370/180


def in_figures(fig, p):
    for figure in fig:
        for tri in figure:
            if in_triangular(map_points[tri[0]], map_points[tri[1]], map_points[tri[2]], p):
                return True
    return False




# bullet class
class M_gun(object):
    def __init__(self):
        self.p = (0, 0)
        self.img = temp_bullet_img
        self.img_rot = self.img
        self.direct = 0

    # return True, if move successfully. If not, return False
    def move(self):
        self.p = int(self.p[0] + np.cos(np.deg2rad(self.direct))*50), int(self.p[1] - np.sin(np.deg2rad(self.direct))*50)
        if in_figures(figures, self.p):
            return False
        return True


# wandering unit including user unit
class Unit(object):
    def __init__(self):
        self.p = [0, 0]
        self.img = None
        self.img_rot = None
        self.direct = 0  # deg
        self.life = 10

    # return True, if move successfully. If not, return False
    def move(self, d):
        temp = self.p[0] + d[0], self.p[1] + d[1]
        if collision_clfr(map_lines, temp) == False:
            self.p = temp


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