import pygame
import random
import os
from player import Player
from enemy import Enemy, EnemyBullet

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (148, 0, 211)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class BattleSystem:
    def __init__(self):
        self.game_state = None
        self.player = None
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.is_battle_active = False
        self.font = pygame.font.Font(None, 40)
        self.font_boss = pygame.font.Font(None, 60)

        self.battle_type = "NORMAL"
        self.battle_bg = None
        self.wave_count = 0
        self.max_waves = 0
        self.enemies_per_wave = 0

    def start_battle(self, game_state, battle_type="NORMAL", bg_image_name=None):
        self.game_state = game_state
        self.is_battle_active = True
        self.battle_type = battle_type

        # 배경 로드
        if bg_image_name:
            try:
                bg_path = os.path.join("assets", "backgrounds", bg_image_name)
                img = pygame.image.load(bg_path).convert()
                self.battle_bg = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.battle_bg = None
        else:
            self.battle_bg = None

        self.all_sprites.empty()
        self.enemies.empty()
        self.enemy_bullets.empty()

        self.player = Player(game_state)
        self.all_sprites.add(self.player)

        # [전투 타입별 설정]
        if self.battle_type == "BOSS":
            print("⚠️ 최종 보스전!")
            boss = Enemy("BOSS", self.player)
            self.all_sprites.add(boss)
            self.enemies.add(boss)

        elif self.battle_type == "SUB_BOSS_BATTLE":
            print("⚠️ 준보스전 시작!")
            self.wave_count = 1
            self.max_waves = 2
            self.enemies_per_wave = 15  # 1웨이브 잡몹 수
            self.spawn_wave()

        else:  # NORMAL
            self.wave_count = 1
            self.max_waves = 2
            self.enemies_per_wave = 25
            self.spawn_wave()
            print(f"⚔️ 일반 전투 시작!")

    def spawn_wave(self):
        # [준보스전 웨이브 로직]
        if self.battle_type == "SUB_BOSS_BATTLE":
            if self.wave_count == 1:
                for _ in range(self.enemies_per_wave):
                    enemy = Enemy("NORMAL", self.player)
                    self.all_sprites.add(enemy)
                    self.enemies.add(enemy)
            elif self.wave_count == 2:
                print("😱 대학원생 좀비 등장!")
                sub_boss = Enemy("SUB_BOSS", self.player)
                self.all_sprites.add(sub_boss)
                self.enemies.add(sub_boss)

        # [일반 전투 웨이브 로직]
        else:
            for _ in range(self.enemies_per_wave):
                enemy = Enemy("NORMAL", self.player)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def handle_event(self, event):
        # 마우스 발사
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.player.shoot(event.pos)

        # --- [추가됨] 마스터 키 (치트키 K) ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                print("⚡ 마스터 키 발동! (즉시 승리)")
                self.enemies.empty()  # 모든 적 제거
                self.wave_count = self.max_waves  # 마지막 웨이브로 설정 (다음 웨이브 스킵)
                # 즉시 승리 조건을 만족시키기 위해 상태 강제 변경은 update()에서 처리됨

        return None

    def update(self):
        if not self.is_battle_active: return None

        self.all_sprites.update()
        self.enemy_bullets.update()

        for enemy in self.enemies:
            if enemy.check_shoot():
                bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom,
                                     self.player.rect.centerx, self.player.rect.centery)
                self.all_sprites.add(bullet)
                self.enemy_bullets.add(bullet)

        hits = pygame.sprite.groupcollide(self.player.bullet_group, self.enemies, True, False)
        for bullet, hit_enemies in hits.items():
            for enemy in hit_enemies:
                enemy.hp -= 10
                if enemy.hp <= 0: enemy.kill()

        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits: self.game_state.update_health(-1)

        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for bullet in hits: self.game_state.update_health(-20)

        # [승리 조건 체크]
        if len(self.enemies) == 0:
            if self.battle_type == "BOSS":
                self.is_battle_active = False
                return "BATTLE_WON"

            # 웨이브가 남았으면 다음 웨이브 진행
            elif self.wave_count < self.max_waves:
                self.wave_count += 1
                self.spawn_wave()

            # 모든 웨이브 클리어
            else:
                self.is_battle_active = False
                return "BATTLE_WON"

        if self.game_state.player_hp <= 0:
            self.is_battle_active = False
            return "GAME_OVER"

        return None

    def draw(self, screen):
        if self.battle_bg:
            screen.blit(self.battle_bg, (0, 0))
        else:
            screen.fill((20, 0, 0))

        self.all_sprites.draw(screen)
        self.player.bullet_group.draw(screen)
        self.enemy_bullets.draw(screen)
        self.draw_ui(screen)

    def draw_ui(self, screen):
        pygame.draw.rect(screen, RED, (30, 30, 300, 30))
        hp_percent = self.game_state.player_hp / self.game_state.max_hp
        pygame.draw.rect(screen, GREEN, (30, 30, int(300 * hp_percent), 30))
        pygame.draw.rect(screen, WHITE, (30, 30, 300, 30), 3)
        hp_text = self.font.render(f"HP: {self.game_state.player_hp}", True, WHITE)
        screen.blit(hp_text, (340, 30))

        # [보스 체력바]
        if self.battle_type == "BOSS" and len(self.enemies) > 0:
            self.draw_boss_bar(screen, self.enemies.sprites()[0], "PROFESSOR (BOSS)", PURPLE)

        # [준보스 체력바 (2웨이브일 때만)]
        elif self.battle_type == "SUB_BOSS_BATTLE" and self.wave_count == 2 and len(self.enemies) > 0:
            self.draw_boss_bar(screen, self.enemies.sprites()[0], "GRADUATE STUDENT (SUB-BOSS)", ORANGE)

        # [웨이브 정보]
        else:
            info_text = f"WAVE {self.wave_count}/{self.max_waves} - Left: {len(self.enemies)}"
            text_surf = self.font.render(info_text, True, WHITE)
            screen.blit(text_surf, (30, 80))

    def draw_boss_bar(self, screen, enemy, name, color):
        bar_width = 1000
        bar_height = 40
        bar_x = (1920 - bar_width) // 2
        bar_y = 50
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        hp_percent = enemy.hp / enemy.max_hp
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * hp_percent), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 4)
        name_surf = self.font_boss.render(name, True, RED)
        name_rect = name_surf.get_rect(center=(1920 // 2, bar_y - 30))
        screen.blit(name_surf, name_rect)