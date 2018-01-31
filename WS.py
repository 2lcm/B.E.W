import pygame
import sys


class WS:
    def __init__(self):
        pygame.init()
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


if __name__ == '__main__':
    ws = WS()
    WS().run()