import pygame
import math
from random import randint
#Wahou 2 dfddddcqdzqdddd
######################### CONST #########################
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (10, 10, 100)
BRIGHT_BLUE = (10, 10, 255)
GREEN = (0, 100, 0)
BRIGHT_GREEN = (0,255,0)
RED = (100, 0, 0)
BRIGHT_RED = (255, 0, 0)
ORANGE = (120, 50, 0)
BRIGHT_ORANGE = (255, 125, 0)

######################### CLASSES #########################
class Tree: 
    def __init__(self, value, index = 0): 
        self.value = value # player 
        self.children = [] # children 
        self.index = index #  index on the board where player play 
        self.point = 0 # min-max algorithm points 
        self.win = 0 # game win (1 or 2 depend of player won) OR neutral game = 0 
     
# Update points (min-max algorithm) of nodes, in avantage to the player (value) in parameter 
    def GivePoint(self, tree, value, deph = 0): 
        if(tree.children != []): 
            # MAX 
            if tree.value != value: 
                max_min = -100 
                for child in tree.children: 
                    point = self.GivePoint(child, value, deph + 1) 
                    if(point > max_min and point != 0): 
                        max_min = point 
            # MIN 
            else: 
                max_min = 100 
                for child in tree.children: 
                    point = self.GivePoint(child, value, deph + 1) 
                    if(point < max_min and point != 0): 
                        max_min = point 
            if (max_min == 100) or (max_min == -100): 
                max_min = 0 
            tree.point = max_min 
            return max_min 
        else: 
            if tree.win == value: 
                tree.point = 10 - deph 
                return 10 - deph 
            elif tree.win == 0: 
                return 0 
            else: 
                tree.point = deph - 10 
                return deph - 10 
      
# From self tree, go index children index in parameter 
    def GoIntoIndex(self, index): 
        for child in self.children: 
            if child.index == index: 
                self.index = child.index 
                self.value = child.value 
                self.point = child.point 
                self.win = child.win 
                self.children = child.children 
                return True 
        return False 
     
# Find best index where player need to play to won the game (IA strategie), find the max "point" of all his children, return array of all if equals 
    def BestIndex(self): 
        max = self.children[0].point 
        index = [self.children[0].index] 
         
        for child in self.children: 
            if child.point > max: 
                max = child.point 
                index = [child.index] 
            elif child.point == max: 
                index.append(child.index) 
        random = index[randint(0, len(index) - 1)] 
        return random 
             
             
class Board: 
    def __init__(self, lenght): 
        self.lenght = lenght 
        self.board = [] 
        for i in range(lenght * lenght): 
            self.board.append(0) 
     
    # Return if index on board is already use or not 
    def BoardPlaceIsFree(self, board, index): 
        if board[index] == 0: 
            return True 
        else: 
            return False 
     
    # Return board after play with value at the index in parameter 
    def Play(self, board, index, value): 
        new_board = [] 
        for case in board: 
            new_board.append(case) 
        new_board[index] = value 
        return new_board 
         
    # Return the n-air tree of the board in parameter 
    def CreateTree(self, tree, board, value = 1, level = None): 
        if level != None and level == 0: 
            return tree 
        if len(tree.children) == 0: 
            for index in range(self.lenght * self.lenght): 
                if(self.BoardPlaceIsFree(board, index)): 
                    tree.children.append(Tree(value,index)) 
                 
        if level != None: 
            level = level - 1 
             
        for index in range(len(tree.children)): 
            if (WinGame(self.Play(board, tree.children[index].index, value), self.lenght) == False): 
                if(value == 1): 
                    tree.children[index] = self.CreateTree(tree.children[index], self.Play(board, tree.children[index].index, value), 2, level) 
                elif(value == 2): 
                    tree.children[index] = self.CreateTree(tree.children[index], self.Play(board, tree.children[index].index, value), 1, level)    
            else: 
                tree.children[index].win = value 
        return tree 
  
        
######################### WIN LOGIC #########################  

def DrawGame(board): # Check if the game end as a draw (i.e. all square filled and no-one won
    draw = True 
    for shape in board.board: 
        if shape == 0: # if one square empty
            draw = False 
            break 
    return draw 
  
def WinGame(board, lenght): #Use to detect the global win 
    if (Win_diagonale(board, lenght) or Win_column(board, lenght) or Win_row(board, lenght)): 
        return True 
    else: 
        return False 
     
def Win_diagonale(board, lenght): #Use to detect the win through a diagonale 
    win = False 
    # Up diagonale 
    if (board[0] != 0): #We check if the first square is taken by a pawn 
        columnIndex = 0 
        rowIndex = 0 
        count = 0 
        for i in range (0,lenght): # We run through the board to detect the other occupied square by the same pawn 
            if (board[0] == board[(lenght * i) + i]): 
                count = count + 1 
  
        if (count == lenght): #If the number of same pawn in the same diagonale is equal to the lenght of the board the player win. (3x3 : 3 pawn to win) 
            win = True 
    #Down diagonale 
    if (win == False): # If we didn't detect the victory beforehand we could check if there are 3 same pawns in the down diagonale 
        if (board[lenght - 1] != 0): 
            columnIndex = 0 
            rowIndex = 0 
            count = 0                                            
            for i in range (0,lenght): 
                if (board[lenght - 1] == board[(lenght * i) + (lenght - 1 - i)]): 
                    count = count + 1 
  
            if (count == lenght): 
                win = True 
     
    return win 
  
def Win_column(board, lenght): #Use to detect the win through a column 
    win = False 
    columnIndex = 0 
    for columnIndex in range (0, lenght): #We run through a specific column to detect a win 
        rowIndex = 0  
        count = 0 
        for rowIndex in range (0, lenght): 
            if (board[(lenght * rowIndex) + (columnIndex)] != 0): #We check if the first square if taken by a pawn 
                if (board[(lenght * rowIndex) + (columnIndex)] == board[(lenght * 0) + (columnIndex)]):# We check if the next square of the column are taken by the same pawn than the first square 
                    count = count + 1 
            if count == (lenght):  #If the number of same pawn in the same column is equal to the lenght of the board the player win. (3x3 : 3 pawn to win) 
                win = True 
                return win 
    return win        
  
def Win_row(board, lenght): #Use to detect the win through a row 
    win = False 
    rowIndex = 0 
    for rowIndex in range (0, lenght): #We run through a specific row to detect a win 
        count = 0 
        columnIndex = 0 
        for columnIndex in range (lenght): 
            if (board[(lenght * rowIndex) + columnIndex] != 0): #We check if the first square if taken by a pawn 
                if (board[(lenght * rowIndex) + columnIndex] == board[(lenght * rowIndex) + 0]):# We check if the next square of the row are taken by the same pawn than the first square 
                    count = count + 1 
  
        if count == lenght: #If the number of same pawn in the same row is equal to the lenght of the board the player win. (3x3 : 3 pawn to win) 
            win = True 
            return win 
    return win  


######################### GRAPHIC #########################
def MouseToSquare(xPosClic, yPosClic):# Convert the X Y pos into the index of the board
    indexSquare = 0
    xIndex = xPosClic // 255
    yIndex = yPosClic // 255
    indexSquare = (yIndex * 3) + xIndex 
    return indexSquare

def ChooseMode(screen):
    screen.fill(BLACK)
    # Text "Choose your opponent"
    font = pygame.font.SysFont('Calibri', 70, True, False)
    textToPrint = "Choose your opponent"
    text = font.render(textToPrint,True,WHITE)
    screen.blit(text, [40, 150])

    pygame.display.flip()# Display screen

    clock = pygame.time.Clock()
    choose = -1
    while choose == -1: # Loop until the player as choose the game mode
        ##Display difficulty buttons with brighting
        mouse = pygame.mouse.get_pos() # Position of the mouse (X, Y)
        # Change color to a bright version when the mouse is on the top of it
        if 370 > mouse[0] > 30 and 700 > mouse[1] > 500:
                pygame.draw.rect(screen, BRIGHT_BLUE,(30,500,340,200))#Bright the color of the square
                pygame.draw.rect(screen, ORANGE,(390,500,340,200))
        elif 700 > mouse[0] > 390 and 700 > mouse[1] > 500:
                pygame.draw.rect(screen, BLUE,(30,500,340,200))
                pygame.draw.rect(screen, BRIGHT_ORANGE,(390,500,340,200))#Bright the color of the square
        else:
            pygame.draw.rect(screen, BLUE,(30,500,340,200))
            pygame.draw.rect(screen, ORANGE,(390,500,340,200))
        # Listen events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # If the player click on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 370 > mouse[0] > 30 and 700 > mouse[1] > 500:
                    vsAI = True
                    choose = 1
                elif 700 > mouse[0] > 390 and 700 > mouse[1] > 500:
                    vsAI = False
                    choose = 0

        #Text of difficulty levels
        fontDiff = pygame.font.SysFont('Lucida Bright', 50, True, False)
        textEasy = fontDiff.render("Computer",True,WHITE)
        screen.blit(textEasy, [73, 570])
        textMedium = fontDiff.render("Player",True,WHITE)
        screen.blit(textMedium, [482, 570])

        pygame.display.flip()
        clock.tick(15)

    pygame.time.wait(200) # Freeze the screen during 200 ms, to let the player see it

    return vsAI

def ChooseDifficulty(screen):
    screen.fill(BLACK)
    #Text "Choose your difficulty"
    font = pygame.font.SysFont('Calibri', 80, True, False)
    textToPrint = "Choose your difficulty"
    text = font.render(textToPrint,True,WHITE)
    screen.blit(text, [10, 150])

    pygame.display.flip()

    clock = pygame.time.Clock()
    difficulty = 0
    while difficulty == 0:
        # Display difficulty buttons with brighting
        mouse = pygame.mouse.get_pos()
        if 244 > mouse[0] > 30 and 700 > mouse[1] > 500:
                pygame.draw.rect(screen, BRIGHT_GREEN,(30,500,214,200))#Bright the color of the square
                pygame.draw.rect(screen, ORANGE,(274,500,214,200))
                pygame.draw.rect(screen, RED,(518,500,214,200))
        elif 488 > mouse[0] > 244 and 700 > mouse[1] > 500:
                pygame.draw.rect(screen, BRIGHT_ORANGE,(274,500,214,200))#Bright the color of the square
                pygame.draw.rect(screen, GREEN,(30,500,214,200))
                pygame.draw.rect(screen, RED,(518,500,214,200))
        elif 732 > mouse[0] > 488 and 700 > mouse[1] > 500:
                pygame.draw.rect(screen, BRIGHT_RED,(518,500,214,200))#Bright the color of the square
                pygame.draw.rect(screen, GREEN,(30,500,214,200))
                pygame.draw.rect(screen, ORANGE,(274,500,214,200))
        else:
            pygame.draw.rect(screen, GREEN,(30,500,214,200))
            pygame.draw.rect(screen, ORANGE,(274,500,214,200))
            pygame.draw.rect(screen, RED,(518,500,214,200))

        # Listen events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # If the player click on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 244 > mouse[0] > 30 and 700 > mouse[1] > 500:
                    difficulty = 1
                elif 488 > mouse[0] > 244 and 700 > mouse[1] > 500:
                    difficulty = 2
                elif 732 > mouse[0] > 488 and 700 > mouse[1] > 500:
                    difficulty = 4


        # Text of difficulty levels
        fontDiff = pygame.font.SysFont('Lucida Bright', 50, True, False)
        textEasy = fontDiff.render("Easy",True,WHITE)
        screen.blit(textEasy, [75, 570])
        textMedium = fontDiff.render("Medium",True,WHITE)
        screen.blit(textMedium, [282, 570])
        textHard = fontDiff.render("Hard",True,WHITE)
        screen.blit(textHard, [565, 570])

        pygame.display.flip()
        clock.tick(15)

    pygame.time.wait(200)
    return difficulty

def DrawLines(screen):
    # Lines of the board
    pygame.draw.line(screen, WHITE, [250, 0], [250, 760], 5)
    pygame.draw.line(screen, WHITE, [505, 0], [505, 760], 5)
    pygame.draw.line(screen, WHITE, [0, 250], [760, 250], 5)
    pygame.draw.line(screen, WHITE, [0, 505], [760, 505], 5)
        
def DrawShape(shapeNum, xPos, yPos, screen):
    # Define Pos for Cross and cirle
    posCircle = [20, 275, 530]
    posCross = [120, 375, 630]

    if shapeNum == 1:# Circle
        xCircle = posCircle[xPos]
        yCircle = posCircle[yPos]
        pygame.draw.ellipse(screen, BRIGHT_BLUE, [xCircle,yCircle,200,200], 10)
        
    elif shapeNum == 2:# Cross
        xCross = posCross[xPos]
        yCross = posCross[yPos]
        pygame.draw.line(screen, BRIGHT_RED, [xCross - 110, yCross - 110], [xCross + 110, yCross + 110], 15)
        pygame.draw.line(screen, BRIGHT_RED, [xCross - 110, yCross + 110], [xCross + 110, yCross - 110], 15)

    pygame.display.flip() # Make it visible on the screen
    

def Display(board, screen): # Display the board on the screen
    screen.fill(BLACK)
    DrawLines(screen)
    for index in range(0,9):
        if (board[index] != 0): # Loop on each square of the board 
            x = index % 3
            y = index / 3
            DrawShape(board[index], x, y, screen) # Display the shape corresponding to the player
    pygame.display.flip() # Make it visible on the screen


def DisplayEnd(PlayerWhoWon, screen, sizeBoard, vsAI):
    screen.fill(BLACK)# Black Background

    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 100, True, False)

    # Text of who won depending on the winner (or not)
    if (PlayerWhoWon == 0):
        textToPrint = "       Draw !"
        TEXT_COLOR = BRIGHT_BLUE
    elif vsAI:
        if (PlayerWhoWon == 1):
            textToPrint = "     You win !"
            TEXT_COLOR = BRIGHT_GREEN
        elif (PlayerWhoWon == 2):
            textToPrint = "       AI win !"
            TEXT_COLOR = BRIGHT_RED
    else:
        textToPrint = " Player " + str(PlayerWhoWon) + " Win !!"
        TEXT_COLOR = BRIGHT_GREEN
    
    text = font.render(textToPrint,True,TEXT_COLOR)
    screen.blit(text, [80, 250]) # Put the text on the screen

    # Text of the replay
    textReplay = "Replay"
    textR = font.render(textReplay,True,BRIGHT_BLUE)
    screen.blit(textR, [200, 500])

    pygame.display.flip() # Make it visible on the screen

    endGame = 0
    while endGame == 0:
        # Display a replay button with brighting when the mouse is on the top of it
        mouse = pygame.mouse.get_pos()
        if 730 > mouse[0] > 30 and 700 > mouse[1] > 500:
            pygame.draw.rect(screen, BRIGHT_GREEN,(30,500,700,200))
        else:
            pygame.draw.rect(screen, GREEN,(30,500,700,200))
        # Text of the replay
        textReplay = "Replay"
        textR = font.render(textReplay,True,BRIGHT_BLUE)
        screen.blit(textR, [230, 550])
        pygame.display.update()

        # Listen events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # If the player click on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 730 > mouse[0] > 30 and 700 > mouse[1] > 500:
                    board = Board(sizeBoard)
                    endGame = -1
                    return endGame
        clock.tick(15)

######################### PLAY LOGIC #########################
def StartRandom(): # Randomize the first player to start
    return randint(1,2)

def SwitchPlayer(player):
    player = (player % 2) + 1# if 1 -> 2; if 2 -> 1
    return player
        
def PlayerPlay(screen, board, tree, player): # When the player play
    played = False
    while not played: # Loop to wait the player to play
        # Listen events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # If the player click on the screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                play_index = MouseToSquare(mouse[0],mouse[1])
                if board.board[play_index] == 0:#Clic only on blanck square
                    board.board = board.Play(board.board, play_index, player)
                    tree.GoIntoIndex(play_index)# Update the tree for the AI
                    played = True
                    return [play_index, tree] 

def AiPlay(screen, board, tree, difficulty): # When the AI play
    tree = board.CreateTree(tree, board.board, 2, difficulty)# Create the tree
    tree.GivePoint(tree, 2)
    best_index = tree.BestIndex() # Find the best index in the tree
    tree.GoIntoIndex(best_index)
    board.board = board.Play(board.board,best_index,2) # Play on the board
    return [best_index, tree]


def EndGame(board, player, sizeBoard):
    if WinGame(board.board, sizeBoard): # Check if the play who played won
        return player # Return the current player, the one whom won
    elif DrawGame(board): # Check if its a draw
        return 0
    else:
        return -1


######################### LOOP #########################
def MainLoop():
    # Init pygame
    pygame.init()
     
    # Set the width and height of the screen 
    size = (760, 760)
    screen = pygame.display.set_mode(size)
    # Set the name of the window
    pygame.display.set_caption("TicTacToe")

    #To close the game
    done = False
     
    # -------- Main Program Loop -----------
    while not done :
        #Init variables
        player = StartRandom()
        play_index = 0
        sizeBoard = 3
        board = Board(sizeBoard)
        tree = Tree(0)
        endGame = -1
        vsAI = False

        # Choose mode
        vsAI = ChooseMode(screen)

        # Choose difficulty
        if vsAI:
            difficulty = ChooseDifficulty(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        
        while endGame == -1:
        # --- Main loop
            #Display Board and Lines
            DrawLines(screen)
            Display(board.board, screen)
            pygame.display.flip()
            
            #Switch player
            player = SwitchPlayer(player)

            # Play of each player / AI
            if player == 1:#Player play
                playerP = PlayerPlay(screen, board, tree, player)
                play_index = playerP[0]
                if vsAI:
                    tree = playerP[1]
            elif (player == 2 and (vsAI == False)):# Other player play
                playerP = PlayerPlay(screen, board, tree, player)
                play_index = playerP[0]
            elif player == 2 and vsAI:# IA play
                pygame.time.wait(500)# Let the time to see the screen
                playerAI = AiPlay(screen, board, tree, difficulty)
                play_index = playerAI[0]
                tree = playerAI[1]
            

            # Display Board
            DrawLines(screen)
            Display(board.board, screen)
            pygame.display.flip()

            # Check the win
            endGame = EndGame(board, player, sizeBoard) #Check if the player win or if its a draw
         
            # --- Limit to 60 frames per second
            clock.tick(60)
         
        #End Game
        pygame.time.wait(1000)#See the screen before the end
        endGame = DisplayEnd(endGame, screen, sizeBoard, vsAI)# Get the choice to replay or not
          
    #Close Game
    pygame.quit()

MainLoop()
