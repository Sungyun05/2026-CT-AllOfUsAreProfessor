import pygame
import os
import math

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Player(pygame.sprite.Sprite):
    def __init__(self, game_state):
        super().__init__()
        self.game_state = game_state

        # 1. 캐릭터 이미지 로드
        try:
            image_path = os.path.join("assets", "characters", "player.png")
            self.original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (80, 100))
        except:
            self.image = pygame.Surface((40, 60))
            self.image.fill((0, 0, 255))

        # 2. [추가됨] 총알 이미지 미리 로드
        try:
            bullet_path = os.path.join("assets", "items", "bullet.png")
            self.bullet_image = pygame.image.load(bullet_path).convert_alpha()
            # 총알 크기 조절 (너무 크면 줄이세요)
            self.bullet_image = pygame.transform.scale(self.bullet_image, (30, 30))
        except:
            self.bullet_image = None  # 이미지가 없으면 None

        # 3. 효과음 로드
        try:
            sound_path = os.path.join("assets", "sounds", "shoot.mp3")
            self.shoot_sound = pygame.mixer.Sound(sound_path)
            self.shoot_sound.set_volume(0.3)
        except:
            self.shoot_sound = None

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 50
        self.speed = 8
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

        self.bullet_group.update()

    def shoot(self, target_pos):
        # 총알 생성 시 이미지도 같이 넘겨줌
        bullet = Bullet(self.rect.centerx, self.rect.centery, target_pos, self.bullet_image)
        self.bullet_group.add(bullet)
        if self.shoot_sound: self.shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos, image=None):
        super().__init__()

        # 1. 각도 계산 (마우스 방향)
        tx, ty = target_pos
        dx = tx - x
        dy = ty - y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        # 2. 이미지 설정 및 회전
        if image:
            self.original_image = image
            # 이미지를 각도에 맞춰 회전 (Pygame 회전은 반시계 방향이라 -부호 붙임)
            # 기본 이미지가 위(Up)를 보고 있다고 가정하고 -90도 추가 보정
            self.image = pygame.transform.rotate(self.original_image, -angle_deg - 90)
        else:
            # 이미지가 없으면 노란 네모
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20

        # 3. 이동 속도 계산
        self.vx = self.speed * math.cos(angle_rad)
        self.vy = self.speed * math.sin(angle_rad)
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self):
        self.pos_x += self.vx
        self.pos_y += self.vy
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
                self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()