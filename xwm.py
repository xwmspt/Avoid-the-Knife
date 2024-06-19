import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GirlRem Game")

# Загрузка изображений
background_image = pygame.image.load("backround.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_over_image = pygame.image.load("game-over.jpg")
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

win_image = pygame.image.load("thumb.jpg")
win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

girl_image = pygame.image.load("girlRem.png")
girl_image = pygame.transform.scale(girl_image, (60, 50))

knife_image = pygame.image.load("knife.png")
knife_image = pygame.transform.scale(knife_image, (40, 40))  # Увеличиваем размер кинжалов

# Загрузка музыки
menu_music = "menu.mp3"
game_music = "Little-girl.mp3"

# Класс для кинжалов
class Knife(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = knife_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = 0
        self.speed = random.randint(10, 15)  # Увеличиваем диапазон скорости

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()  # Удаляем кинжал из группы, если он достиг нижней границы
            global score
            score += 100

# Создание группы спрайтов для кинжалов
knife_group = pygame.sprite.Group()

# Создание спрайта для персонажа
class Girl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = girl_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.rect.y = SCREEN_HEIGHT - self.image.get_height()
        self.speed = 5

    def update(self):
        # Перемещение персонажа по X (по горизонтали)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

# Инициализация спрайта персонажа
girl_sprite = Girl()

# Константы прыжка
GRAVITY = 0.5
JUMP_HEIGHT = 15  # Увеличиваем высоту прыжка
MAX_JUMP = 2  # Максимальное количество прыжков подряд

# Переменные для прыжка
jumping = False
jump_count = 0

# Счетчик очков
score = 0

# Флаги состояния игры
game_over = False
game_won = False
game_start = True  # Добавляем флаг для начального экрана

# Включаем музыку меню при запуске
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)  # Начинаем проигрывание музыки в цикле

def restart_game():
    global score, game_over, game_won
    score = 0
    game_over = False
    game_won = False
    girl_sprite.rect.x = SCREEN_WIDTH // 2 - girl_sprite.image.get_width() // 2
    girl_sprite.rect.y = SCREEN_HEIGHT - girl_sprite.image.get_height()
    knife_group.empty()  # Очищаем группу кинжалов
    pygame.mixer.music.load(game_music)  # Загружаем игровую музыку
    pygame.mixer.music.play(-1)  # Начинаем проигрывание музыки в цикле

def draw_start_screen():
    screen.fill(BLUE)
    font = pygame.font.Font(None, 60)
    title_text = font.render("GirlRem Game", True, RED)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2, 150, 50))
    start_text = font.render("Start", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
    screen.blit(start_text, start_rect)

    pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100, 150, 50))
    exit_text = font.render("Exit", True, WHITE)
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 125))
    screen.blit(exit_text, exit_rect)

# Основной цикл игры
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_start:
                if SCREEN_WIDTH // 2 - 75 <= pygame.mouse.get_pos()[0] <= SCREEN_WIDTH // 2 + 75:
                    if SCREEN_HEIGHT // 2 <= pygame.mouse.get_pos()[1] <= SCREEN_HEIGHT // 2 + 50:
                        game_start = False  # Начинаем игру
                        pygame.mixer.music.load(game_music)  # Загружаем игровую музыку
                        pygame.mixer.music.play(-1)  # Начинаем проигрывание музыки в цикле
                    elif SCREEN_HEIGHT // 2 + 100 <= pygame.mouse.get_pos()[1] <= SCREEN_HEIGHT // 2 + 150:
                        running = False  # Выход из игры
            elif game_over or game_won:
                if SCREEN_WIDTH // 2 - 50 <= pygame.mouse.get_pos()[0] <= SCREEN_WIDTH // 2 + 50 \
                        and SCREEN_HEIGHT // 2 + 150 <= pygame.mouse.get_pos()[1] <= SCREEN_HEIGHT // 2 + 200:
                    restart_game()

    if game_start:
        draw_start_screen()
    else:
        if not game_over and not game_won:
            # Обработка нажатий клавиш
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                girl_sprite.rect.x -= girl_sprite.speed
            if keys[pygame.K_RIGHT]:
                girl_sprite.rect.x += girl_sprite.speed
            if keys[pygame.K_SPACE] and not jumping:
                jumping = True
                jump_count = MAX_JUMP

            # Добавление новых кинжалов
            if random.randint(1, 100) < 3:  # Вероятность появления нового кинжала
                num_knives = random.randint(1, 3)  # Добавляем от 1 до 3 кинжалов
                for _ in range(num_knives):
                    new_knife = Knife()
                    knife_group.add(new_knife)

            # Обновление положения кинжалов и проверка столкновений
            knife_group.update()
            if pygame.sprite.spritecollide(girl_sprite, knife_group, False):
                game_over = True

            # Проверка на выигрыш
            if score >= 5000:
                game_won = True

            # Отрисовка
            screen.blit(background_image, (0, 0))  # Отображаем фон

            # Отображаем все кинжалы
            knife_group.draw(screen)

            # Отображаем персонажа
            screen.blit(girl_image, girl_sprite.rect)

            # Отображение счетчика очков
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            # Отображаем экран проигрыша или выигрыша
            if game_over:
                screen.blit(game_over_image, (0, 0))
                pygame.mixer.music.stop()  # Останавливаем музыку при проигрыше
            elif game_won:
                screen.blit(win_image, (0, 0))
                pygame.mixer.music.stop()  # Останавливаем музыку при выигрыше

            # Отображаем кнопку перезапуска
            pygame.draw.rect(screen, RED, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 150, 100, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Restart", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175))
            screen.blit(text, text_rect)

    pygame.display.flip()

    # Ограничение FPS
    clock.tick(FPS)

# Завершение работы Pygame
pygame.quit()
sys.exit()
