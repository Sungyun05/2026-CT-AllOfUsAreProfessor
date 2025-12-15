import pygame
import random
import os
import math

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, target_player):
        super().__init__()
        self.target = target_player
        self.enemy_type = enemy_type

        # 기본 설정 (일반 좀비)
        self.hp = 30
        self.speed = 3
        img_name = "zombie.png"
        size = (60, 80)
        self.detect_radius = 600

        # [최종 보스] 교수님
        if self.enemy_type == "BOSS":
            self.hp = 200
            self.max_hp = 200
            self.speed = 2
            img_name = "professor_boss.png"
            size = (300, 400)
            self.detect_radius = 3000
            self.last_shot_time = pygame.time.get_ticks()
            self.shot_delay = 5000

        # [추가됨] 준보스: 대학원생 좀비
        elif self.enemy_type == "SUB_BOSS":
            self.hp = 100  # 체력 100 (일반보다 튼튼함)
            self.max_hp = 100
            self.speed = 5  # 속도 5 (분노로 인해 매우 빠름!)
            img_name = "graduate_zombie.png"
            size = (120, 160)  # 일반 좀비보다 2배 큼
            self.detect_radius = 1500  # 감지 범위 넓음

        # 이미지 로드
        try:
            image_path = os.path.join("assets", "characters", img_name)
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        except:
            self.image = pygame.Surface(size)
            if self.enemy_type == "BOSS":
                self.image.fill((100, 0, 100))
            elif self.enemy_type == "SUB_BOSS":
                self.image.fill((0, 100, 100))  # 청록색
            else:
                self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()

        # 위치 초기화
        self.rect.x = random.randint(50, SCREEN_WIDTH - size[0] - 50)

        if self.enemy_type in ["BOSS", "SUB_BOSS"]:
            self.rect.y = -450  # 보스급은 위에서 등장
        else:
            self.rect.y = random.randint(-1000, -100)

        self.wander_direction = [0, 0]
        self.wander_timer = 0

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # [보스 움직임]
        if self.enemy_type == "BOSS":
            if self.rect.y < 100:
                self.rect.y += 2
            else:
                if self.rect.centerx < self.target.rect.centerx:
                    self.rect.x += 1
                elif self.rect.centerx > self.target.rect.centerx:
                    self.rect.x -= 1

        # [준보스 & 일반 좀비 움직임]
        else:
            # 화면 밖이면 입장
            if self.rect.y < 0:
                self.rect.y += 5
            else:
                # 추적 모드 (준보스는 무조건 추적)
                if self.enemy_type == "SUB_BOSS" or distance < self.detect_radius:
                    if distance != 0:
                        move_x = (dx / distance) * self.speed
                        move_y = (dy / distance) * self.speed
                        self.rect.x += move_x
                        self.rect.y += move_y
                # 배회 모드 (일반 좀비만)
                else:
                    self.wander_timer += 1
                    if self.wander_timer > 60:
                        self.wander_timer = 0
                        wx = random.choice([-1, 0, 1])
                        wy = random.choice([-1, 0, 1])
                        self.wander_direction = [wx, wy]
                    self.rect.x += self.wander_direction[0] * (self.speed * 0.5)
                    self.rect.y += self.wander_direction[1] * (self.speed * 0.5)

        # 화면 가두기
        if self.rect.y > 0:
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
            if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT
            # 보스급은 위로 못 도망감
            if self.rect.top < 0 and self.enemy_type not in ["BOSS", "SUB_BOSS"]:
                self.rect.top = 0

    def check_shoot(self):
        if self.enemy_type == "BOSS":
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.shot_delay:
                self.last_shot_time = now
                return True
        return False


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((150, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 9
        dx = target_x - x
        dy = target_y - y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0: distance = 1
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
                self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()