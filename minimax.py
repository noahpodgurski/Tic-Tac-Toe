# We'll use the time module to measure the time of evaluating
# game tree in every move. It's a nice way to show the
# distinction between the basic Minimax and Minimax with
# alpha-beta pruning :)
import time, random
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()  # init font
WIN_WIDTH = 900
WIN_HEIGHT = 900
NUM_COLS = 7
NUM_ROWS = 6
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BLUE = (87,155,252)
RADIUS = 50
MARGIN = 50
class Game:
    def __init__(self):
        self.initialize_game()
        self.window = Rect(MARGIN/2, MARGIN/2, WIN_WIDTH-MARGIN, WIN_HEIGHT-MARGIN)
        self.outline = Rect(MARGIN-5, MARGIN-5, WIN_WIDTH+10-MARGIN*2, WIN_HEIGHT+10-MARGIN*2)
        self.frame = Rect(MARGIN, MARGIN, WIN_WIDTH-MARGIN*2, WIN_HEIGHT-MARGIN*2)
        self.positions = [
            [(0, 0), (300, 0), (600, 0)],
            [(0, 300), (300, 300), (600, 300)],
            [(0, 600), (300, 600), (600, 600)]
        ]
        self.x = pygame.image.load("x.png")
        self.o = pygame.image.load("o.png")
        self.player = random.choice(["O", "X"])
        if self.player == "O":
            self.CPU = "X"
        else:
            self.CPU = "O"

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break
        pygame.draw.rect(win, WHITE, self.window)
        # pygame.draw.rect(win, BLACK, self.outline)
        # pygame.draw.rect(win, WHITE, self.frame)
        pygame.draw.line(win, BLACK, (300,0), (300,900), 10) # |
        pygame.draw.line(win, BLACK, (600,0), (600,900), 10) #    |
        pygame.draw.line(win, BLACK, (0,300), (900,300), 10) # _
        pygame.draw.line(win, BLACK, (0,600), (900,600), 10) #    _

        for i, row in enumerate(self.current_state):
            for j, state in enumerate(row):
                if state == "X":
                    win.blit(self.x, self.positions[i][j])
                elif state == "O":
                    win.blit(self.o, self.positions[i][j])

        #draw win lines
        print(self.winType, self.winIndex)
        if self.winType == "v":
            pygame.draw.line(win, RED, (150+(self.winIndex*300), 150), (150+(self.winIndex*300), 850), 10)
        elif self.winType == "h":            
            pygame.draw.line(win, RED, (150, 150+(self.winIndex*300)), (850, 150+(self.winIndex*300)), 10)
        elif self.winType == "d" and self.winIndex == 1:
            pygame.draw.line(win, RED, (0,0), (900,900), 10)
        elif self.winType == "d" and self.winIndex == 2:
            pygame.draw.line(win, RED, (0,900), (900,0), 10)
        win.blit(win, (0, 0))
        pygame.display.update()


    def getCoords(self, pos):
        for i in range(0, 10, 3):
            for j in range(0, 10, 3):
                if pos[0] < i*100 and pos[1] < j*100:
                    return ((j//3)-1, (i//3)-1)

    def initialize_game(self):
        self.current_state = [['.','.','.'],
                              ['.','.','.'],
                              ['.','.','.']]

        # Player X always plays first
        self.player_turn = 'X'
        self.winType = None
        self.winIndex = None

    def draw_board(self):
        win.fill((255,255,255))

        # generations

        self.draw()
        #######################
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # Determines if the made move is a legal move
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if self.current_state[0][i] != '.' and self.current_state[0][i] == self.current_state[1][i] == self.current_state[2][i]:
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'

        # Main diagonal win
        if (self.current_state[0][0] != '.' and
            self.current_state[0][0] == self.current_state[1][1] and
            self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # Second diagonal win
        if (self.current_state[0][2] != '.' and
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'

    def setWin(self):
        # Vertical win
        for i in range(0, 3):
            if self.current_state[0][i] != '.' and self.current_state[0][i] == self.current_state[1][i] == self.current_state[2][i]:
                self.winType = "v"
                self.winIndex = i

        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X'] or self.current_state[i] == ['O', 'O', 'O']):
                self.winType = "h"
                self.winIndex = i

        # Main diagonal win
        if (self.current_state[0][0] != '.' and
            self.current_state[0][0] == self.current_state[1][1] and
            self.current_state[0][0] == self.current_state[2][2]):
            self.winType = "d"
            self.winIndex = 1

        # Second diagonal win
        if (self.current_state[0][2] != '.' and
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0]):
            self.winType = "d"
            self.winIndex = 2

    # Player 'O' is max, in this case AI
    def max(self):

        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        px = None
        py = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    # On the empty field player 'O' makes a move and calls Min
                    # That's one branch of the game tree.
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min()
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    # Setting back the field to empty
                    self.current_state[i][j] = '.'
        return (maxv, px, py)

    # Player 'X' is min, in this case human
    def min(self):

        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                        break
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max()
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

        return (minv, qx, qy)

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta):

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()
            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            # If it's player's turn
            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min()
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    # px = int(input('Insert the X coordinate: '))
                    # py = int(input('Insert the Y coordinate: '))
                    (px, py) = (qx, qy)

                    (qx, qy) = (px, py)

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's AI's turn
            else:
                (m, px, py) = self.max()
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'



    def play_alpha_beta(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")               

                self.initialize_game()
                return

            if self.player_turn == 'X':
                while True:

                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    # px = int(input('Insert the X coordinate: '))
                    # py = int(input('Insert the Y coordinate: '))
                    (px, py) = (qx, qy)

                    qx = px
                    qy = py

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            else:
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'

    def play_against_AI(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                #set winType winIndex
                print('WAFFLES')
                # for row in self.current_state:
                #     if row == ["X", "X", "X"]:
                self.setWin()
                self.draw()
                return

            
            if self.player_turn == self.player:
                print("my turn!")
                move = True
                while move:
                    run = True
                    while run: #get click and check if valid
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                                break
                            elif event.type == pygame.MOUSEBUTTONUP:
                                pos = pygame.mouse.get_pos()
                                (px, py) = self.getCoords(pos)
                                run = False
                    if self.is_valid(px, py):
                        print("valid!")
                        self.current_state[px][py] = self.player
                        self.player_turn = self.CPU
                        move = False
                        run = False
            else:
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.current_state[px][py] = self.CPU
                self.player_turn = self.player
                print(px, py)


def main():
    g = Game()
    g.play_against_AI()
    # g.play()
    # g.play_alpha_beta()
    for i in range(100):
        g.draw()

if __name__ == "__main__":
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    while True:
        main()
