import pygame
from pygame.locals import *
import common
pygame.init()


class HumanPlayer:
    def __init__(self, screen, c1, c2, c3):
        self.screen = screen
        self.is_takenFromWidow = False
        self.control = 0
        self.control2 = False
        self.control3 = False

        self.accessible = (common.HUMAN_FIRST, common.HUMAN_SECOND, common.HUMAN_THIRD,
                           common.WIDOW_LEFT, common.WIDOW_RIGHT)
        common.PAIRS[common.HUMAN_FIRST_HASH] = c1
        common.PAIRS[common.HUMAN_FIRST_HASH].flip_image()
        common.PAIRS[common.HUMAN_FIRST_HASH].rect = common.HUMAN_FIRST

        common.PAIRS[common.HUMAN_SECOND_HASH] = c2
        common.PAIRS[common.HUMAN_SECOND_HASH].flip_image()
        common.PAIRS[common.HUMAN_SECOND_HASH].rect = common.HUMAN_SECOND

        common.PAIRS[common.HUMAN_THIRD_HASH] = c3
        common.PAIRS[common.HUMAN_THIRD_HASH].flip_image()
        common.PAIRS[common.HUMAN_THIRD_HASH].rect = common.HUMAN_THIRD

        self.grabbed_card = None
        self.total = sum([common.PAIRS[tuple(rect)].value for rect in self.accessible[:3]])

        self.fist_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("img/fist.jpeg"), (60, 84)), -90)

        self.fist_rect = pygame.Rect(520, 400, 60, 84)

    def changeTurn(self):
        self.control = 0
        self.control2 = False
        self.control3 = False
        common.TURN = common.COMPUTER
        self.is_takenFromWidow = False

    def hitTable(self):
        common.TABLEHIT = (True, self)
        common.CHANGEROUND = True
        if self.total > common.COMPUTER_PLAYER.total:
            common.HUMANCHIPS += 1
            common.COMPUTERCHIPS -= 1
        else:
            common.HUMANCHIPS -= 1
            common.COMPUTERCHIPS += 1
        for rect in common.COMPUTER_PLAYER.accessible[:3]:
            if common.PAIRS[tuple(rect)].image == common.PAIRS[tuple(rect)].back:
                common.PAIRS[tuple(rect)].flip_image()

    def release_and_grab(self, rect):
        def r_a_g1(self,  rect):
            common.PAIRS[tuple(rect)].change_grabbed()
            self.grabbed_card = common.PAIRS[tuple(rect)]
            common.PAIRS[tuple(rect)] = None

        def r_a_g2(self, rect):
            self.grabbed_card.change_grabbed(rect)
            common.PAIRS[tuple(rect)] = self.grabbed_card
            self.grabbed_card = None

        def r_a_g3(self, rect):
            common.PAIRS[tuple(rect)].change_grabbed()
            self.grabbed_card.change_grabbed(rect)
            common.PAIRS[tuple(rect)], self.grabbed_card = self.grabbed_card, common.PAIRS[tuple(rect)]

        if common.TURN == common.HUMAN:
            if not self.is_takenFromWidow and rect == common.WIDOW_LEFT and self.grabbed_card is None:
                self.is_takenFromWidow = True
                self.control += 1

                self.grabbed_card = common.PAIRS[tuple(rect)]
                common.WIDOW.removeCard(rect)

                #r_a_g1(self, rect)
                self.grabbed_card.flip_image()

            if rect == common.WIDOW_RIGHT:
                self.control += 1

            if rect != common.WIDOW_LEFT:
                if self.grabbed_card is None:
                    if rect == common.WIDOW_RIGHT:
                        self.grabbed_card = common.PAIRS[tuple(rect)]
                        common.WIDOW.removeCard(rect)
                        self.control2 = True
                    else:
                        r_a_g1(self, rect)
                        self.control2 = False
                elif common.PAIRS[tuple(rect)] is None:
                    if self.control == 2:
                        self.control += 1
                        self.grabbed_card.change_grabbed(rect)
                        common.WIDOW.addCard(self.grabbed_card)
                        self.grabbed_card = None
                        self.changeTurn()
                    else:
                        r_a_g2(self, rect)

                else:
                    if self.control == 2:
                        # r_a_g2(self, rect)
                        if not self.control2:
                            self.grabbed_card.change_grabbed(rect)
                            common.WIDOW.addCard(self.grabbed_card)
                            self.grabbed_card = None
                            self.changeTurn()
                    else:
                        r_a_g3(self, rect)
                        self.control2 = False

            if self.control == 2:
                self.changeTurn()

    def getRect(self):
        x, y = pygame.mouse.get_pos()
        for rect in self.accessible:
            if rect.top <= y <= rect.bottom and rect.left <= x <= rect.right:
                return rect
        return None

    def getEvents(self, event):
        if event.type == MOUSEBUTTONDOWN:
            rect = self.getRect()
            if rect is not None:
                self.release_and_grab(rect)

        if event.type == KEYDOWN:
            if event.key == K_h:
                self.hitTable()
                self.changeTurn()

    def update(self):
        if self.control3 is False:
            try:
                self.total = sum([common.PAIRS[tuple(rect)].value for rect in self.accessible[:3]])
                if self.total == 31:
                    self.hitTable()
                    self.changeTurn()
                elif self.total > 31:
                    common.TABLEHIT = (None, common.COMPUTER_PLAYER)
                    self.changeTurn()
                    common.CHANGEROUND = True
                    common.HUMANCHIPS -= 1
                    common.COMPUTERCHIPS += 1
            except:
                pass
            self.control3 = True