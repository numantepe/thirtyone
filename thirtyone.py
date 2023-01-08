import pygame, random, time
from pygame.locals import *
import common
import computerPlayer, humanPlayer
import widow
import card

pygame.init()

print("""The Pack
The standard 52-card pack is used.

OBJECT OF THE GAME
The goal is to obtain a hand that totals 31 in cards of one suit; or to have a hand at the showdown whose count in one suit is higher than that of any other player.

RANK OF CARDS
A (high), K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2 (low)

CARD VALUES/SCORING
An Ace counts 11 points, face cards count 10 points, and all other cards count their face value.

THE DEAL
The players cut for deal and the lowest card deals, the turn to deal alternates to the left. 
Three cards are dealt face down to each player; then three cards are dealt face up for a "widow."

THE PLAY
Before play begins, all players put an equal amount of chips into a pot. The player on the dealer's left has the first turn. 
On each turn, a player may take one card from the widow and replace it with one card from their hand (face up). 
Players take turns, clockwise around the table, until one player is satisfied that the card values 
they hold will likely beat the other players. A player indicates this by "knocking" on the table. 
All other players then get one more turn to exchange cards. 
Then there is a showdown in which the players reveal their hands and compare values. 
The player with the highest total value of cards of the same suit wins the pot.
If there is a tie for the highest score, the player with the highest-ranking card wins. 

Any time a player holds exactly 31, they may "knock" immediately, and they win the pot. 
If a player knocks before the first round of exchanges have begun, the showdown occurs immediately with no exchange of cards.
After the pot has been won, all the players put in chips for the next hand.
""")

def blitCards():
    for card in common.ALLCARDS.sprites():
        if card != common.HUMAN_PLAYER.grabbed_card:
            screen.blit(card.image, card.rect)
    if common.HUMAN_PLAYER.grabbed_card is not None:
        screen.blit(common.HUMAN_PLAYER.grabbed_card.image, common.HUMAN_PLAYER.grabbed_card.rect)


def changeToAnotherRound():
    global cards

    common.ALLCARDS = pygame.sprite.Group()
    for card in common.CARDS:
        card.image = card.back
        card.rect = card.image.get_rect()
        card.dragging = card.image.get_rect()
        card.grabbed = False
    cards = common.CARDS.copy()
    random.shuffle(cards)

    common.HUMAN_PLAYER = humanPlayer.HumanPlayer(screen, cards.pop(0), cards.pop(1), cards.pop(2))
    common.COMPUTER_PLAYER = computerPlayer.ComputerPlayer(screen, cards.pop(0), cards.pop(0), cards.pop(0))
    common.WIDOW = widow.Widow(cards)

    common.ALLCARDS.add(common.PAIRS.values())
    common.TABLEHIT = (False, None)
    common.CHANGEROUND = False

font = pygame.font.SysFont(None, 25)
def message_to_screen(msg, color, coordinates):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, (coordinates))


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Question3")

clock = pygame.time.Clock()
FPS = 60


common.ALLCARDS = pygame.sprite.Group()
common.CARDS = [card.Card("img/2a.png", 2), card.Card("img/2b.png", 2), card.Card("img/2c.png", 2), card.Card("img/2d.png", 2),
                card.Card("img/3a.png", 3), card.Card("img/3b.png", 3), card.Card("img/3c.png", 3), card.Card("img/3d.png", 3),
                card.Card("img/4a.png", 4), card.Card("img/4b.png", 4), card.Card("img/4c.png", 4), card.Card("img/4d.png", 4),
                card.Card("img/5a.png", 5), card.Card("img/5b.png", 5), card.Card("img/5c.png", 5), card.Card("img/5d.png", 5),
                card.Card("img/6a.png", 6), card.Card("img/6b.png", 6), card.Card("img/6c.png", 6), card.Card("img/6d.png", 6),
                card.Card("img/7a.png", 7), card.Card("img/7b.png", 7), card.Card("img/7c.png", 7), card.Card("img/7d.png", 7),
                card.Card("img/8a.png", 8), card.Card("img/8b.png", 8), card.Card("img/8c.png", 8), card.Card("img/8d.png", 8),
                card.Card("img/9a.png", 9), card.Card("img/9b.png", 9), card.Card("img/9c.png", 9), card.Card("img/9d.png", 9),
                card.Card("img/10a.png", 10), card.Card("img/10b.png", 10), card.Card("img/10c.png", 10), card.Card("img/10d.png", 10),
                card.Card("img/10e.png", 10), card.Card("img/10f.png", 10), card.Card("img/10g.png", 10), card.Card("img/10h.png", 10),
                card.Card("img/10i.png", 10), card.Card("img/10j.png", 10), card.Card("img/10k.png", 10), card.Card("img/10l.png", 10),
                card.Card("img/10m.png", 10), card.Card("img/10n.png", 10), card.Card("img/10o.png", 10), card.Card("img/10p.png", 10),
                card.Card("img/11a.png", 11), card.Card("img/11b.png", 11), card.Card("img/11c.png", 11), card.Card("img/11d.png", 11)]
cards = common.CARDS.copy()
random.shuffle(cards)

common.HUMAN_PLAYER = humanPlayer.HumanPlayer(screen, cards.pop(0), cards.pop(1), cards.pop(2))
common.COMPUTER_PLAYER = computerPlayer.ComputerPlayer(screen, cards.pop(0), cards.pop(0), cards.pop(0))
common.WIDOW = widow.Widow(cards)

common.ALLCARDS.add(common.PAIRS.values())


gamePlay = True
clock.tick(30)
while gamePlay:
    for event in pygame.event.get():
        if event.type == QUIT:
            gamePlay = False
        if event.type == KEYDOWN:
            if event.key == K_n:
                if common.CHANGEROUND:
                    changeToAnotherRound()

        if common.TABLEHIT[0] is not None:
            if not common.TABLEHIT[0] and common.TURN == common.HUMAN:
                common.HUMAN_PLAYER.getEvents(event)
                t0 = time.perf_counter()
            if not common.TABLEHIT[0] and common.TURN == common.COMPUTER and time.perf_counter() - t0 > 1:
                common.COMPUTER_PLAYER.play()

    screen.fill(WHITE)
    if common.HUMANCHIPS == 0:
        message_to_screen("You got all the chips of the computer so you win", BLACK, (200, 300))

    elif common.COMPUTERCHIPS == 0:
        message_to_screen("You lost all your chips so computer wins", BLACK, (200, 300))

    else:
        if common.TABLEHIT[0] is None:
            if common.COMPUTER_PLAYER.total > 31:
                message_to_screen("Computer holds cards whose values add up to more than 31 so,", BLACK, (50, 170))
                message_to_screen("You won this round", BLACK, (50, 200))
                message_to_screen("You have {} chips".format(common.HUMANCHIPS), BLACK, (50, 230))
                message_to_screen("Computer has {} chips".format(common.COMPUTERCHIPS), BLACK, (50, 260))
            else:
                message_to_screen("You hold cards whose values add up to more than 31 so,", BLACK, (50, 170))
                message_to_screen("Computer won this round", BLACK, (50, 200))
                message_to_screen("Computer has {} chips".format(common.COMPUTERCHIPS), BLACK, (50, 230))
                message_to_screen("You have {} chips".format(common.HUMANCHIPS), BLACK, (50, 260))

        elif common.TABLEHIT[0]:
            message_to_screen("The table is knocked", BLACK, (600, 200))
            screen.blit(common.TABLEHIT[1].fist_image, common.TABLEHIT[1].fist_rect)
            if common.HUMAN_PLAYER.total > common.COMPUTER_PLAYER.total:
                message_to_screen("You won this round", BLACK, (50, 200))
                message_to_screen("You have {} chips".format(common.HUMANCHIPS), BLACK, (50, 230))
                message_to_screen("Computer has {} chips".format(common.COMPUTERCHIPS), BLACK, (50, 260))
            else:
                message_to_screen("Computer won this round", BLACK, (50, 200))
                message_to_screen("Computer has {} chips".format(common.COMPUTERCHIPS), BLACK, (50, 230))
                message_to_screen("You have {} chips".format(common.HUMANCHIPS), BLACK, (50, 260))
        else:
            if common.TURN == common.HUMAN:
                message_to_screen("It is your turn", BLACK, (600, 200))
            else:
                message_to_screen("It is computer turn", BLACK, (600, 200))

        message_to_screen("Press n to play a new round, press h to knock the table", BLACK, (10, 10))
        blitCards()
        common.HUMAN_PLAYER.update()
        common.COMPUTER_PLAYER.update()
        common.ALLCARDS.update()

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
quit()
