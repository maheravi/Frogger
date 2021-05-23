import pygame
import random
import time

pygame.init()


class Object:
    def __init__(self):
        self.direction = random.choice(['ltr', 'rtl'])
        if self.direction == 'ltr':
            self.x = -50
        elif self.direction == 'rtl':
            self.x = game.width + 50

    def move(self):
        if self.direction == 'ltr':
            self.x += self.speed
        elif self.direction == 'rtl':
            self.x -= self.speed

    def show(self):
        game.display.blit(self.image, [self.x, self.y])

    def intersects(self, other):
        left = self.x
        top = self.y
        right = self.x + self.w
        bottom = self.y + self.h

        other_left = other.x
        other_top = other.y
        other_right = other.x + other.w
        other_bottom = other.y + other.h

        return not (left >= other_right or right <= other_left or top >= other_bottom or bottom <= other_top)


class Car(Object):
    def __init__(self):
        super().__init__()
        self.w = 50
        self.h = 32
        self.no = random.choice([8, 9, 10, 11])
        self.speed = 3
        if self.direction == 'ltr':
            self.no = random.choice([8, 10])
            self.image = pygame.transform.scale(pygame.image.load('Car2.png'), (self.w, self.h))
            self.y = self.no * game.grid
        elif self.direction == 'rtl':
            self.no = random.choice([9, 11])
            self.image = pygame.transform.scale(pygame.image.load('Car1.png'), (self.w, self.h))
            self.y = self.no * game.grid


class Wood(Object):
    def __init__(self):
        super().__init__()
        self.w = 50
        self.h = 32
        self.speed = 2
        self.no = random.choice([2, 3, 4, 5])
        if self.direction == 'ltr':
            self.no = random.choice([2, 4])
            self.image = pygame.transform.scale(pygame.image.load('wood.png'), (self.w, self.h))
            self.y = self.no * game.grid
        elif self.direction == 'rtl':
            self.no = random.choice([3, 5])
            self.image = pygame.transform.scale(pygame.image.load('wood.png'), (self.w, self.h))
            self.y = self.no * game.grid


class Frog:
    def __init__(self):
        self.x = 6 * game.grid
        self.y = game.height - 32
        self.w = 32
        self.h = 32
        self.image = pygame.image.load('Frog.png')
        self.score = 0
        self.remaining = 5
        self.gu = pygame.transform.scale(self.image, (self.w, self.h))
        self.rect = self.gu.get_rect()

    def show(self):
        game.display.blit(self.gu, (self.x, self.y))

    def reset(self):
        self.x = 6 * game.grid
        self.y = game.height - 32
        self.remaining -= 1

    def new(self):
        self.x = 6 * game.grid
        self.y = game.height - 32
        self.remaining = 5
        self.score = 0


class Game:
    def __init__(self):
        self.width = 416
        self.height = 416
        self.grid = 32
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.lanes = []
        pygame.display.set_caption('Frogger')

    def play(self):
        pygame.mouse.set_visible(False)
        font = pygame.font.SysFont('comicsansms', 16)
        my_frog = Frog()
        cars = []
        woods = []
        received_frogs = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        my_frog.y -= 32
                    elif event.key == pygame.K_DOWN:
                        my_frog.y += 32

            self.display.fill((0, 0, 0))
            self.lanes.append(pygame.draw.rect(self.display, (50, 192, 122), pygame.Rect(0, 416 - 32, 416, 32)))
            self.lanes.append(pygame.draw.rect(self.display, (50, 192, 122), pygame.Rect(0, 32, 416, 32)))
            self.lanes.append(pygame.draw.rect(self.display, (50, 192, 122), pygame.Rect(0, 224, 416, 32)))
            self.lanes.append(pygame.draw.rect(self.display, (50, 192, 122), pygame.Rect(0, 192, 416, 32)))
            self.lanes.append(pygame.draw.rect(self.display, (195, 195, 195), pygame.Rect(0, 256, 416, 128)))
            self.lanes.append(pygame.draw.rect(self.display, (153, 217, 234), pygame.Rect(0, 64, 416, 128)))

            for frog in received_frogs:
                frog.show()

            if random.random() < 0.04:
                cars.append(Car())

            if random.random() < 0.05:
                woods.append(Wood())

            for car in cars:
                car.show()
                car.move()

            for wood in woods:
                wood.show()
                wood.move()

            my_frog.show()

            if any(car.intersects(my_frog) for car in cars):
                my_frog.score = 0
                my_frog.reset()
            if game.grid < my_frog.y < 6 * game.grid:
                if not any(wood.intersects(my_frog) for wood in woods):
                    my_frog.reset()
                for wood in woods:
                    if wood.intersects(my_frog):
                        if wood.direction == 'ltr':
                            my_frog.x += wood.speed
                        elif wood.direction == 'rtl':
                            my_frog.x -= wood.speed

            if 0 > my_frog.x or my_frog.x > game.width:
                my_frog.reset()

            if my_frog.remaining == 0:
                if len(received_frogs) == 5:
                    score_font = font.render("Completed!", True, (255, 0, 0))
                    font_pos = score_font.get_rect(center=(game.width * 0.5, 16))
                    self.display.blit(score_font, font_pos)
                    pygame.display.update()
                    time.sleep(4)
                    my_frog.new()
                elif len(received_frogs) < 5:
                    score_font = font.render("You lose", True, (255, 0, 0))
                    font_pos = score_font.get_rect(center=(game.width * 0.5, 16))
                    self.display.blit(score_font, font_pos)
                    pygame.display.update()
                    time.sleep(4)
                    my_frog.new()

            if my_frog.y <= game.grid:
                received_frogs.append(my_frog)
                score_font = font.render("Great!", True, (255, 0, 0))
                font_pos = score_font.get_rect(center=(game.width / 2, 16))
                self.display.blit(score_font, font_pos)
                pygame.display.update()
                time.sleep(4)
                my_frog.reset()

            score_font = font.render("Remaining Frogs: " + str(my_frog.remaining), True, (255, 0, 0))
            font_pos = score_font.get_rect(center=(game.width * 0.5, 16))
            self.display.blit(score_font, font_pos)

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    game.play()
