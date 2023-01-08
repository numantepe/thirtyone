import pygame
import common

pygame.init()


class Widow:
    def __init__(self, cards):
        self.cards = cards
        self.left = self.cards
        self.right = [self.cards.pop(0)]
        common.PAIRS[common.WIDOW_LEFT_HASH] = self.left[0]
        common.PAIRS[common.WIDOW_LEFT_HASH].rect = common.WIDOW_LEFT

        common.PAIRS[common.WIDOW_RIGHT_HASH] = self.right[0]
        common.PAIRS[common.WIDOW_RIGHT_HASH].flip_image()
        common.PAIRS[common.WIDOW_RIGHT_HASH].rect = common.WIDOW_RIGHT

    def addCard(self, card):
        self.right.insert(0, card)
        if self.right[0].image == self.right[0].back:
            self.right[0].flip_image()
        common.ALLCARDS.remove((common.PAIRS[common.WIDOW_RIGHT_HASH],))
        common.PAIRS[common.WIDOW_RIGHT_HASH] = self.right[0]
        common.PAIRS[common.WIDOW_RIGHT_HASH].rect = common.WIDOW_RIGHT
        common.ALLCARDS.add((common.PAIRS[common.WIDOW_RIGHT_HASH], ))

    def removeCard(self, rect):
        if common.TURN == common.HUMAN:
            common.PAIRS[tuple(rect)].change_grabbed()
        if rect == common.WIDOW_LEFT:
            del self.left[0]
            common.PAIRS[common.WIDOW_LEFT_HASH] = self.left[0]
            common.PAIRS[common.WIDOW_LEFT_HASH].rect = common.WIDOW_LEFT
            common.ALLCARDS.add((common.PAIRS[common.WIDOW_LEFT_HASH],))
        else:
            del self.right[0]
            try:
                if self.right[0].image == self.right[0].back:
                        self.right[0].flip_image()
            except:
                pass

            if len(self.right) != 0:
                common.PAIRS[common.WIDOW_RIGHT_HASH] = self.right[0]
                common.PAIRS[common.WIDOW_RIGHT_HASH].rect = common.WIDOW_RIGHT

                common.ALLCARDS.add((common.PAIRS[common.WIDOW_RIGHT_HASH],))
            else:
                common.PAIRS[common.WIDOW_RIGHT_HASH] = None
