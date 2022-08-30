import random
import pygame
import sys
import pathfinder
import time
from decisiontree import DecisionTree
from imagerecognizer import ImageRecognizer
from objects import Grass
from objects import Mine
from objects import Rock
from objects import Puddle


MARGIN = 20  # marginesy - odległość kraty od końca okna
SQUARE_HEIGHT = 35
SQUARE_WIDTH = 35
CENTER_DIST = 38  # odległość pomiędzy środkami kwadratów
BOARDCOLS = 15 # liczba kolumn planszy
BOARDROWS = BOARDCOLS  # liczba wierszy planszy
WINDOW_HEIGHT = BOARDCOLS * CENTER_DIST + (2 * MARGIN)
WINDOW_WIDTH = BOARDROWS * CENTER_DIST + (2 * MARGIN)


class Field:  # obiekt clasy field jest pojedynczym polem planszy
    def __init__(self, coordinates, color, fieldty):
        Board.fields.append(self)
        self.rect = pygame.Rect(coordinates[0], coordinates[1], SQUARE_WIDTH, SQUARE_HEIGHT)
        self.color = color
        self.type = fieldty
        self.object = self.assign_object()
        self.deley_value = self.object.deley
        self.redisp = True

    def assign_object(self):
        if self.type == 'T':
            object = Grass(self.rect.center[0],self.rect.center[1], SQUARE_WIDTH, SQUARE_HEIGHT)
            return object
        if self.type == 'P':
            object = Puddle(self.rect.center[0],self.rect.center[1],SQUARE_WIDTH, SQUARE_HEIGHT)
            return object
        if self.type == 'R':
            object = Rock(self.rect.center[0],self.rect.center[1],SQUARE_WIDTH, SQUARE_HEIGHT)
            return object
        if self.type == 'B':
            object = Mine(self.rect.center[0],self.rect.center[1],SQUARE_WIDTH, SQUARE_HEIGHT)
            return object



class Board:
    fields = []  # tablica obiektów klasy filed, czyli po prostu tablica pól planszy gotowych do wizualizacji
    bombs = 0
    def __init__(self):
        self.margin = MARGIN
        self.square_high = SQUARE_HEIGHT
        self.square_width = SQUARE_WIDTH
        self.center_dist = CENTER_DIST
        self.window_height = WINDOW_HEIGHT
        self.window_widhth = WINDOW_WIDTH
        self.boardcols = BOARDCOLS  # liczba kolumn planszy
        self.boardrows = BOARDROWS  # liczba wierszy planszy
        self.board = [[0 for i in range(self.boardcols)] for j in range(self.boardrows)]
        self.firstwinner = True

        pygame.display.set_caption("Saper")
        self.game_display = pygame.display.set_mode((self.window_height, self.window_widhth))  # wielkość okna adaptująca się do wielkości planszy
        self.load_board()
        self.first_ground = self.board[0].index('T')
        self.show_board()
        self.init_board()
        #self.bombfield = pathfinder.find_bomb(self.fields, self.first_ground)
        self.genetic = pathfinder.Genetic(self.fields, self.first_ground)
        self.bombfield = self.genetic.genetic_path.fields_order[0]
        #print(self.bombfield)
        self.pathf = pathfinder.Pathfind(self.fields, self.bombfield, self.first_ground)
        self.ir = ImageRecognizer()
        self.dt = DecisionTree()

    def load_board(self):  # funkcja tworząca tablicę opisującą planszę
        for i in range(self.boardrows):
            for j in range(self.boardcols):
                chance = random.randint(1,100)  # prawdopodobieństwo że dane pole będzie terenem (T), przeszkodą (O) lub bombą (B)
                if chance >= 1 and chance < 80:
                    self.board[i][j] = 'T'
                if chance >= 80 and chance < 95:
                    chance = random.randint(1,2)
                    if chance == 1:
                        self.board[i][j] = 'R'
                    if chance == 2:
                        self.board[i][j] = 'P'

                if chance >= 95 and chance <= 100:
                    self.board[i][j] = 'B'
                    self.bombs += 1

    def show_board(self):  # funkcja pomocnicza wypisująca tablicę opisującą planszę
        for i in range(self.boardrows):
            for j in range(self.boardcols):
                print(self.board[i][j], end=' ')
            print("")
        print("")
        print("bomby:",self.bombs)

    def init_board(self):  # funkcja inicjująca planszę
        x = self.margin
        y = self.margin
        for i in range(self.boardrows):
            for j in range(self.boardcols):
                if self.board[i][j] == 'T':
                    Field((x, y), (0, 128,0), 'T')  # tworzony jest obiekt clasy field zawierający współżędne oraz kolor danego pola planszy
                if self.board[i][j] == 'R':
                    Field((x, y), (255, 255, 0), 'R')
                if self.board[i][j] == 'P':
                    Field((x, y), (255, 255, 0), 'P')
                if self.board[i][j] == 'B':
                    Field((x, y), (165, 42, 42), 'B')

                x += self.center_dist
            y += self.center_dist
            x = self.margin

    def objects_display(self,i):
        objecttype = self.fields[i].object
        self.game_display.blit(objecttype.image_scaled, objecttype.rect)

    def board_events(self, agent):

        for event in pygame.event.get():
            self.agent_field_update(agent)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # klawisz esc zamyka program
                sys.exit(0)

            #if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and agent.pos_field+1 < len(self.fields):
             #   if self.fields[agent.pos_field+1].object.walkable == 0:
              #      self.fields[agent.pos_field].redisp = True
               #     agent.move(self.window_height, self.margin, self.center_dist, "RIGHT", 1)

            #if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and agent.pos_field-1 >= 0:
             #   if self.fields[agent.pos_field - 1].object.walkable == 0:
              #      self.fields[agent.pos_field].redisp = True
               #     agent.move(self.window_height, self.margin, self.center_dist, "LEFT", -1)

            #if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and agent.pos_field+BOARDROWS < len(self.fields):
             #   if self.fields[agent.pos_field + BOARDROWS].object.walkable == 0:
              #      self.fields[agent.pos_field].redisp = True
               #     agent.move(self.window_height, self.margin, self.center_dist, "DOWN", BOARDROWS)

            #if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and agent.pos_field-BOARDROWS >= 0:
             #   if self.fields[agent.pos_field - BOARDROWS].object.walkable == 0:
              #      self.fields[agent.pos_field].redisp = True
               #     agent.move(self.window_height,self.margin,self.center_dist,"UP", -BOARDROWS)


    def agent_field_update(self,agent):
        agent.cooldown = 100
        if self.fields[agent.pos_field].type == 'B' and self.fields[agent.pos_field].object.defused == False:
            if self.ir.recognize(self.fields[agent.pos_field].object.itr) == "stones":
                print("to kamień!")
                self.fields[agent.pos_field].object.its_rock(SQUARE_WIDTH, SQUARE_HEIGHT)
                self.fields[agent.pos_field].redisp = True
                self.bombs -= 1
            else:
                print("to bomba!")
                wtd = self.dt.make_decision(((self.bombs*100)//(BOARDCOLS**2))+1, self.fields[agent.pos_field].object.time, self.fields[agent.pos_field].object.reach)
                if wtd == "Defuse":
                    self.fields[agent.pos_field].object.defuse(SQUARE_WIDTH, SQUARE_HEIGHT)
                    self.fields[agent.pos_field].redisp = True
                if wtd == "Move away":
                    self.fields[agent.pos_field].object.move_away(SQUARE_WIDTH, SQUARE_HEIGHT)
                    self.fields[agent.pos_field].redisp = True
                self.bombs -= 1
        if self.bombs > 0 and agent.pos_field == self.bombfield:
            #self.bombfield = pathfinder.find_bomb(self.fields, agent.pos_field)
            #print(self.bombfield)
            self.genetic.genetic_path.fields_order.remove(self.genetic.genetic_path.fields_order[0])
            self.bombfield = self.genetic.genetic_path.fields_order[0]
            print("next bombfield is: ", self.bombfield)
            self.pathf = pathfinder.Pathfind(self.fields, self.bombfield, agent.pos_field)



    def automove_agent(self,agent):
        self.agent_field_update(agent)
        if len(self.pathf.way) > 0:
            wayfield = self.pathf.way[0]
            self.pathf.way.remove(wayfield)
            if agent.pos_field - BOARDCOLS == wayfield:
                self.fields[agent.pos_field].redisp = True
                agent.move(self.window_height, self.margin, self.center_dist, "UP", -BOARDCOLS)

            if agent.pos_field + BOARDCOLS == wayfield:
                self.fields[agent.pos_field].redisp = True
                agent.move(self.window_height, self.margin, self.center_dist, "DOWN", BOARDCOLS)

            if agent.pos_field - 1 == wayfield:
                self.fields[agent.pos_field].redisp = True
                agent.move(self.window_height, self.margin, self.center_dist, "LEFT", -1)

            if agent.pos_field + 1 == wayfield:
                self.fields[agent.pos_field].redisp = True
                agent.move(self.window_height, self.margin, self.center_dist, "RIGHT", 1)






    def full_board_display(self,first):  # funkcja pomocnicza wywołująca program, w celu wizualizacji planszy możną ją wywołać
        if self.bombs <= 0 and self.firstwinner == True:
            print("wszystkie miny rozbrojone!")
            self.firstwinner = False

        if first == True:
            self.game_display.fill((0, 0, 0))
        i=0
        for square in self.fields:
            if square.redisp == True:
                pygame.draw.rect(self.game_display, square.color, square.rect)
                self.objects_display(i)
                square.redisp = False
            i=i+1