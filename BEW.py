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

# points of figure in map
file_points = open("points.txt", "r")
map_points = []
n = int(file_points.readline())
for i in range(n):
    line = file_points.readline()
    map_points.append((int(line.split()[0]), int(line.split()[1])))
file_points.close()

# lines of figure in map
# rectangle, rectangle, rectangle, hexagon, rectangle, rectangle
file_lines = open("lines.txt", "r")
map_lines = []
n = int(file_lines.readline())
for i in range(n):
    line = file_lines.readline()
    a = map_points[int(line.split()[0])]
    b = map_points[int(line.split()[1])]
    map_lines.append((a, b))
map_lines += [((0, 0), (1600, 0)), ((1600, 0), (1600, 1200)), ((1600, 1200), (0, 1200)), ((0, 1200), (0, 0))]
file_lines.close()

# figures in map made with triangles
file_figures = open("figures.txt", "r")
figures = []
n = int(file_figures.readline())
for i in range(n):
    line = file_figures.readline().split()
    tmp1 = []
    for j in range(len(line)//3):
        tmp2 = []
        for k in range(3):
            a = int(line[3 * j + k])
            tmp2.append(map_points[a])
        tmp1.append(tmp2)
    figures.append(tmp1)
file_figures.close()


class BEW(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(10, 25)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.Team1 = LinkedList.LL()
        self.Team2 = LinkedList.LL()
        self.gunfire1 = LinkedList.LL()
        self.gunfire2 = LinkedList.LL()
        tmp = Unit()
        tmp.p = (600, 600)
        tmp.img = unit_img
        tmp.img_rot = tmp.img
        self.Team1.insert(tmp)
        tmp = Unit()
        tmp.p = (850, 850)
        tmp.img = unit_img
        tmp.img_rot = tmp.img
        self.Team2.insert(tmp)

    def run(self):
        # define local variables
        fps_clk = pygame.time.Clock()
        user = self.Team1.head.next.val
        ai = self.Team2.head.next.val

        # main routine
        while True:
            # set maximum fps
            fps_clk.tick(MAXFPS)

            # draw map
            now_map = map_img.copy()
            draw_screen([self.gunfire1, self.gunfire2, self.Team1, self.Team2], now_map)

            # draw screen
            self.screen.fill((0, 0, 0))
            self.screen.blit(now_map, (-user.p[0]+400, -user.p[1]+300))
            pygame.display.update()

            # handle bullets
            temp_fire = self.gunfire1.head.next
            while temp_fire != self.gunfire1.tail:
                next_fire = temp_fire.next
                if self.out_of_map(temp_fire.val):
                    if not temp_fire.val.move():
                        self.gunfire1.delete(temp_fire)
                else:
                    self.gunfire1.delete(temp_fire)
                temp_fire = next_fire

            temp_fire = self.gunfire2.head.next
            while temp_fire != self.gunfire2.tail:
                next_fire = temp_fire.next
                if self.out_of_map(temp_fire.val):
                    if not temp_fire.val.move():
                        self.gunfire2.delete(temp_fire)
                else:
                    self.gunfire2.delete(temp_fire)
                temp_fire = next_fire

            # handle team1 bullets
            temp_unit = self.Team2.head.next
            while temp_unit != self.Team2.tail:
                cur_unit = temp_unit.val
                temp_fire = self.gunfire1.head.next
                while temp_fire != self.gunfire1.tail:
                    if (cur_unit.p[0] - temp_fire.val.p[0])**2 + (cur_unit.p[1] - temp_fire.val.p[1])**2 < UNIT_RAD2:
                        cur_unit.life -= 1
                        print('life is :', cur_unit.life)
                        temp_fire = temp_fire.next
                        self.gunfire1.delete(temp_fire.prev)
                    else:
                        temp_fire = temp_fire.next
                temp_unit = temp_unit.next
                if cur_unit.life <= 0:
                    self.Team2.delete(temp_unit.prev)

            # handle team2 bullets
            temp_unit = self.Team1.head.next
            while temp_unit != self.Team1.tail:
                cur_unit = temp_unit.val
                temp_fire = self.gunfire2.head.next
                while temp_fire != self.gunfire2.tail:
                    if (cur_unit.p[0] - temp_fire.val.p[0]) ** 2 + (
                            cur_unit.p[1] - temp_fire.val.p[1]) ** 2 < UNIT_RAD2:
                        cur_unit.life -= 1
                        print('life is :', cur_unit.life)
                        temp_fire = temp_fire.next
                        self.gunfire2.delete(temp_fire.prev)
                    else:
                        temp_fire = temp_fire.next
                temp_unit = temp_unit.next
                if cur_unit.life <= 0:
                    self.Team1.delete(temp_unit.prev)

            # handle events and user unit
            for event in pygame.event.get():
                # when click x button on window
                if event.type == pygame.QUIT:
                    sys.exit()
                # when press the keyboard
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        user.act[0] = True
                    if event.key == pygame.K_s:
                        user.act[1] = True
                    if event.key == pygame.K_a:
                        user.act[2] = True
                    if event.key == pygame.K_d:
                        user.act[3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        user.act[0] = False
                    if event.key == pygame.K_s:
                        user.act[1] = False
                    if event.key == pygame.K_a:
                        user.act[2] = False
                    if event.key == pygame.K_d:
                        user.act[3] = False

            # update user attribute
            user.atk = pygame.mouse.get_pressed()[0]
            user.look = (user.p[0] - 400 + pygame.mouse.get_pos()[0], user.p[1] - 300 + pygame.mouse.get_pos()[1])

            # update AI attributes
            ai.atk = True
            ai.look = user.p
            ai.act[0] = ai.p[1] > user.p[1]
            ai.act[1] = ai.p[1] < user.p[1]
            ai.act[2] = ai.p[0] > user.p[0]
            ai.act[3] = ai.p[0] < user.p[0]

            # move, change direct, attacks
            cur_node = self.Team1.head.next
            while cur_node != self.Team1.tail:
                cur_node.val.update()
                if cur_node.val.atk:
                    new_shot = M_gun()
                    new_shot.p = cur_node.val.p
                    new_shot.direct = cur_node.val.direct
                    self.gunfire1.insert(new_shot)
                cur_node = cur_node.next

            cur_node = self.Team2.head.next
            while cur_node != self.Team2.tail:
                cur_node.val.update()
                if cur_node.val.atk:
                    new_shot = M_gun()
                    new_shot.p = cur_node.val.p
                    new_shot.direct = cur_node.val.direct
                    self.gunfire2.insert(new_shot)
                cur_node = cur_node.next

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


# check whether given point is in the triangle made by three points
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


# check given points are in that figure
def in_figures(fig, p):
    for figure in fig:
        for tri in figure:
            if in_triangular(tri[0], tri[1], tri[2], p):
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
        self.look = [0, 0]
        self.act = [False, False, False, False]  # up, down, left, right
        self.atk = False

    def move(self):
        d = ((0, -2), (0, 2), (-2, 0), (2, 0))
        for b in enumerate(self.act):
            if b[1]:
                temp = self.p[0] + d[b[0]][0], self.p[1] + d[b[0]][1]
                if not collision_clfr(map_lines, temp):
                    self.p = temp

    # make user unit look toward the particular position
    def update(self):
        self.move()
        xy = np.subtract(np.array(self.look), np.array(self.p))
        if xy[0] == 0:
            if xy[1] / abs(xy[1]) == 1:
                self.direct = -90
            else:
                self.direct = 90
        else:
            self.direct = 0 - np.rad2deg(np.arctan(xy[1] / xy[0]))
            if xy[0] < 0:
                self.direct += 180


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