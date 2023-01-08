import pygame, random
import common

pygame.init()


class ComputerPlayer:
    def __init__(self, screen, c1, c2, c3):
        self.screen = screen
        self.accessible = (common.COMPUTER_FIRST, common.COMPUTER_SECOND,
                           common.COMPUTER_THIRD, common.WIDOW_LEFT, common.WIDOW_RIGHT)
        common.PAIRS[common.COMPUTER_FIRST_HASH] = c1
        common.PAIRS[common.COMPUTER_FIRST_HASH].rect = common.COMPUTER_FIRST

        common.PAIRS[common.COMPUTER_SECOND_HASH] = c2
        common.PAIRS[common.COMPUTER_SECOND_HASH].rect = common.COMPUTER_SECOND

        common.PAIRS[common.COMPUTER_THIRD_HASH] = c3
        common.PAIRS[common.COMPUTER_THIRD_HASH].rect = common.COMPUTER_THIRD


        self.total = sum([common.PAIRS[tuple(rect)].value for rect in self.accessible[:3]])

        self.fist_image = pygame.transform.rotate(pygame.transform.flip(
            pygame.transform.scale(pygame.image.load("img/fist.jpeg"), (60, 84)), True, True), -90)
        self.fist_rect = pygame.Rect(200, 121, 60, 84)
        self.control = False

    def changeTurn(self):
        common.TURN = common.HUMAN
        self.control = False

    def hitTable(self):
        common.TABLEHIT = (True, self)
        common.CHANGEROUND = True
        if self.total > common.HUMAN_PLAYER.total:
            common.HUMANCHIPS -= 1
            common.COMPUTERCHIPS += 1
        else:
            common.HUMANCHIPS += 1
            common.COMPUTERCHIPS -= 1
        for rect in self.accessible[:3]:
            if common.PAIRS[tuple(rect)].image == common.PAIRS[tuple(rect)].back:
                common.PAIRS[tuple(rect)].flip_image()

    def play(self):
        values = [common.PAIRS[tuple(rect)].value for rect in self.accessible[:3]]
        smallest_index = values.index(min(values))
        widow_right_value = common.PAIRS[tuple(self.accessible[-1])].value
        if 7 <= widow_right_value and values[smallest_index] <= widow_right_value:
            if sum(values) - values[smallest_index] + widow_right_value <= 31:
                temp = common.PAIRS[tuple(self.accessible[smallest_index])].copy()
                temp.flip_image()
                common.PAIRS[tuple(self.accessible[smallest_index])] = common.WIDOW.right[0]
                common.PAIRS[tuple(self.accessible[smallest_index])].rect = self.accessible[smallest_index]
                common.PAIRS[tuple(self.accessible[smallest_index])].flip_image()
                common.WIDOW.addCard(temp)

        elif 7 <= widow_right_value:
            if random.choice([True, True, False]):
                common.PAIRS[tuple(self.accessible[smallest_index])].flip_image()
                common.WIDOW.addCard(common.PAIRS[tuple(self.accessible[smallest_index])])
                common.PAIRS[tuple(self.accessible[smallest_index])] = common.WIDOW.right.pop(1)
                common.PAIRS[tuple(self.accessible[smallest_index])].rect = self.accessible[smallest_index]
                common.PAIRS[tuple(self.accessible[smallest_index])].flip_image()
            else:
                widow_left_value = common.PAIRS[tuple(self.accessible[-2])].value
                if sum(values) - values(smallest_index) + widow_left_value <= 31:
                    temp = common.PAIRS[tuple(self.accessible[smallest_index])].copy()
                    temp.flip_image()

                    common.PAIRS[tuple(self.accessible[smallest_index])] = common.WIDOW.left[0]
                    common.PAIRS[tuple(self.accessible[smallest_index])].rect = self.accessible[smallest_index]
                    common.WIDOW.removeCard(self.accessible[-2])
                    common.WIDOW.addCard(temp)

                else:
                    common.PAIRS[tuple(self.accessible[-2])].flip_image()
                    common.WIDOW.addCard(common.PAIRS[tuple(self.accessible[-2])])
                    common.WIDOW.removeCard(self.accessible[-2])

        elif 29 < self.total:
            self.hitTable()

        elif 25 < self.total and random.choice([True, True, False]):
            self.hitTable()


        else:
            widow_left_value = common.PAIRS[tuple(self.accessible[-2])].value
            if sum(values) - values[smallest_index] + widow_left_value <= 31:
                temp = common.PAIRS[tuple(self.accessible[smallest_index])].copy()
                temp.flip_image()

                common.PAIRS[tuple(self.accessible[smallest_index])] = common.WIDOW.left[0]
                common.PAIRS[tuple(self.accessible[smallest_index])].rect = self.accessible[smallest_index]
                common.WIDOW.removeCard(self.accessible[-2])
                common.WIDOW.addCard(temp)

            else:
                common.PAIRS[tuple(self.accessible[-2])].flip_image()
                common.WIDOW.addCard(common.PAIRS[tuple(self.accessible[-2])])
                common.WIDOW.removeCard(self.accessible[-2])

        self.changeTurn()

    def update(self):
        if self.control is False:
            try:
                self.total = sum([common.PAIRS[tuple(rect)].value for rect in self.accessible[:3]])
                if self.total == 31:
                    self.hitTable()
                    self.changeTurn()
                elif self.total > 31:
                    common.TABLEHIT = (None, common.HUMAN_PLAYER)
                    self.changeTurn()
                    common.CHANGEROUND = True
                    common.HUMANCHIPS += 1
                    common.COMPUTERCHIPS -= 1
            except:
                pass
            self.control = True