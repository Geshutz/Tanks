import pygame
import sys
import os
import tkinter as tk
from tkinter import ttk

# Инициализация Pygame
pygame.init()

# Инициализация звукового микшера
pygame.mixer.init()

# Размеры окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle City")

# Указание абсолютного пути к файлам
base_path = r'C:\Users\STATION\Desktop\TANK'

try:
    # Загрузка текстуры уровня
    sand_texture_path = os.path.join(base_path, 'sand_texture.png')
    sand_texture = pygame.image.load(sand_texture_path).convert()
    print("Текстура уровня загружена успешно")
except pygame.error as e:
    print(f"Ошибка загрузки sand_texture.png: {e}")
    sys.exit()

try:
    # Загрузка иконки танка
    tank_icon_path = os.path.join(base_path, 'tank_icon.png')
    tank_icon = pygame.image.load(tank_icon_path).convert_alpha()
except pygame.error as e:
    print(f"Ошибка загрузки tank_icon.png: {e}")
    sys.exit()

try:
    # Загрузка иконки пули
    bullet_icon_path = os.path.join(base_path, 'bullet_icon.png')
    bullet_icon = pygame.image.load(bullet_icon_path).convert_alpha()
    bullet_icon = pygame.transform.scale(bullet_icon, (9, 9))  # Изменение размера иконки пули
except pygame.error as e:
    print(f"Ошибка загрузки bullet_icon.png: {e}")
    sys.exit()

try:
    # Загрузка звука выстрела
    shoot_sound_path = os.path.join(base_path, 'shoot_sound.wav')
    shoot_sound = pygame.mixer.Sound(shoot_sound_path)
except pygame.error as e:
    print(f"Ошибка загрузки shoot_sound.wav: {e}")
    sys.exit()

# Основные цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Частота кадров
clock = pygame.time.Clock()

# Функция для создания окна с ползунком скорости танка
def create_speed_slider():
    root = tk.Tk()
    root.title("Tank Speed Controller")
    root.geometry("300x100")

    def on_speed_change(event):
        global tank_speed
        tank_speed = speed_var.get()

    speed_var = tk.IntVar(value=5)
    speed_slider = ttk.Scale(root, from_=3, to_=7, orient='horizontal', variable=speed_var)
    speed_slider.pack(pady=20)
    speed_slider.bind("<Motion>", on_speed_change)

    tk.Label(root, text="Adjust Tank Speed:").pack(pady=5)
    root.update()
    return root

tank_speed = 5
speed_window = create_speed_slider()

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = tank_icon
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = tank_speed
        self.direction = 'UP'

    def update(self):
        self.speed = tank_speed  # Обновление скорости в соответствии с текущим значением ползунка
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rect.y -= self.speed
            self.direction = 'UP'
        elif keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.rect.y += self.speed
            self.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.rect.x += self.speed
            self.direction = 'RIGHT'

        # Удержание танка внутри границ окна
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # Поворот танка
        self.rotate()

    def rotate(self):
        if self.direction == 'UP':
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == 'DOWN':
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == 'LEFT':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.original_image, -90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        print(f"Shooting in direction: {self.direction}")
        try:
            shoot_sound.play()  # Воспроизведение звука выстрела перед созданием пули
            if self.direction == 'UP':
                bullet = Bullet(self.rect.centerx, self.rect.top, self.direction)
            elif self.direction == 'DOWN':
                bullet = Bullet(self.rect.centerx, self.rect.bottom, self.direction)
            elif self.direction == 'LEFT':
                bullet = Bullet(self.rect.left, self.rect.centery, self.direction)
            elif self.direction == 'RIGHT':
                bullet = Bullet(self.rect.right, self.rect.centery, self.direction)
            all_sprites.add(bullet)
            bullets.add(bullet)
            print("Bullet created successfully")
        except Exception as e:
            print(f"Error creating bullet: {e}")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.original_image = bullet_icon
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction
        print(f"Bullet initialized at ({x}, {y}) heading {direction}")

        # Поворот пули в зависимости от направления
        if self.direction == 'UP':
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == 'DOWN':
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == 'LEFT':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == 'RIGHT':
            self.image = pygame.transform.rotate(self.original_image, -90)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed

        # Удаляем пулю, если она выходит за границы экрана
        if self.rect.y < 0 or self.rect.y > screen_height or self.rect.x < 0 or self.rect.x > screen_width:
            self.kill()

# Создаем объект танка
player = Tank(screen_width // 2, screen_height // 2)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites.add(player)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # Отрисовка
    screen.fill(WHITE)
    screen.blit(sand_texture, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Обновление окна слайдера
    speed_window.update()