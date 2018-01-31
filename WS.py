import pygame
import sys


class WS(object):
    def __init__(self):
        pygame.init()
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class Unit(object):
    def __init__(self):
        self.x, self.y = [0, 0]
        raise NotImplementedError


def draw_screen(lss):
    raise NotImplementedError

if __name__ == '__main__':
    ws = WS()
    WS().run()