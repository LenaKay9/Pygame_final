import pygame.gfxdraw
import time
import random
from label import *

pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("add/sound.mp3")
screen = pygame.display.set_mode((775, 350))
clock = pygame.time.Clock()
buttons = pygame.sprite.Group()

questions = [
    ["What year did the Titanic sink?", ["1912", "1923", "1890", "2024"]],
    ["What is the world’s smallest bird?", ["Bee Hummingbird", "Whale Pigeon", "Tree Swallow", "Ruby-crowned Kinglet"]],
    ["What is the rarest blood type in humans?", ["-AB", "-A", "-O", "-B"]],
    ["What is the lifespan of a dragonfly?", ["24 Hours", "48 Hours", "6 Months", "1 Year"]],
    ["How many hearts does an Octopus Have?", ["Three", "Eight", "One", "Four"]],
    ["What is the capital city of Mongolia?", ["Ulaanbaatar", "Ulaanbaataa", "Ulaanbatar", "Ulaanbaat"]],
]

class Button(pygame.sprite.Sprite):

    def __init__(self, position, text, size,
                 colors="white on purple",
                 hover_colors="purple on pink",
                 style="button1",
                 borderc=(255, 102, 255),
                 command=lambda: print("No command activated for this button")):

        super().__init__()
        global num

        self.text = text
        self.command = command
        # colors
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        # hover_colors
        self.hover_colors = hover_colors
        self.style = style
        self.borderc = borderc  # style2
        # font
        self.font = pygame.font.SysFont("times new roman", size)
        self.render(self.text)
        self.x, self.y, self.w, self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)
        self.position = position
        self.pressed = 1
        buttons.add(self)

    def render(self, text):
        self.text_render = self.font.render(text, 1, self.fg)
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == "button1":
            self.draw_button1()
        elif self.style == "button2":
            self.draw_button2()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button1(self):
        color = (150, 150, 150)
        color2 = (50, 50, 50)
        pygame.draw.line(screen, color, self.position,
                         (self.x + self.w, self.y), 5)
        pygame.draw.line(screen, color, (self.x, self.y - 2),
                         (self.x, self.y + self.h), 5)
        pygame.draw.line(screen, color2, (self.x, self.y + self.h),
                         (self.x + self.w, self.y + self.h), 5)
        pygame.draw.line(screen, color2, (self.x + self.w, self.y + self.h),
                         [self.x + self.w, self.y], 5)
        pygame.draw.rect(screen, self.bg, self.rect)

    def draw_button2(self):
        pygame.draw.rect(screen, self.bg, (self.x - 50, self.y, 500, self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 500, self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colors = self.hover_colors
        else:
            self.colors = self.original_colors

    def hover(self):
        # is the mouse over the button
        self.check_collision()

    def click(self):
        # checks if you click on the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1

def on_right():
    check_score("right")

def on_false():
    check_score()

def check_score(answered="wrong"):
    global qnum, points

    hit.play()
    if qnum < len(questions):
        print(qnum, len(questions))
        if answered == "right":
            time.sleep(.1)  # avoid adding more point when pressed too much
            points += 1
        qnum += 1
        score.change_text(str(points))
        title.change_text(questions[qnum - 1][0], color="purple")
        num_question.change_text(str(qnum))
        show_question(qnum)


    elif qnum == len(questions):
        print(qnum, len(questions))
        if answered == "right":
            kill()
            time.sleep(.1)
            points += 1
        score.change_text("You won " + str(points) +" points!")
    time.sleep(.5)

def show_question(qnum):
    kill()
    # position of the buttons
    pos = [100, 150, 200, 250]
    # randomized, so that the right one is not always top
    random.shuffle(pos)

    # buttons
    Button((50, pos[0]), questions[qnum - 1][1][0], 36, "purple on white",
           hover_colors="purple on pink", style="button2", borderc=(255, 255, 0),
           command=on_right)
    Button((50, pos[1]), questions[qnum - 1][1][1], 36, "purple on white",
           hover_colors="purple on pink", style="button2", borderc=(255, 255, 0),
           command=on_false)
    Button((50, pos[2]), questions[qnum - 1][1][2], 36, "purple on white",
           hover_colors="purple on pink", style="button2", borderc=(255, 255, 0),
           command=on_false)
    Button((50, pos[3]), questions[qnum - 1][1][3], 36, "purple on white",
           hover_colors="purple on pink", style="button2", borderc=(255, 255, 0),
           command=on_false)

def kill():
    for _ in buttons:
        _.kill()

qnum = 1
points = 0
# label
num_question = Label(screen, str(qnum), 0, 0)
score = Label(screen, "Points!", 50, 300)
title = Label(screen, questions[qnum - 1][0], 10, 10, 45, color="purple")



def start_again():
    pass


def loop():
    global game_on

    show_question(qnum)

    while True:
        pygame_icon = pygame.image.load('add/logo.png')
        pygame.display.set_icon(pygame_icon)
        screen.fill((246, 191, 239))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
        buttons.update()
        buttons.draw(screen)
        show_labels()
        clock.tick(60)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game_on = 1
    loop()