import pygame
import sys
import os

from game_state import GameState
from scene_manager import SceneManager
from battle_system import BattleSystem

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
CAPTION = "지금 우리 교수님은"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scene_json_path = os.path.join(self.current_dir, 'script', 'scenes.json')

        try:
            logo_path = os.path.join(self.current_dir, 'assets', 'ui', 'logo.png')
            pygame.display.set_icon(pygame.image.load(logo_path))
        except:
            pass

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        # [이미지 로드]
        self.title_bg = self.load_image_ui('title_bg.png')
        self.gameover_bg = self.load_image_ui('gameover_bg.png')
        self.how_to_play_bg = self.load_image_ui('how_to_play.png')
        self.prologue_bg = self.load_image_ui('prologue.png')
        self.intro_bg = self.load_image_ui('intro.png')  # [추가됨] 인트로(경고문 등) 이미지

        self.item_images = {}
        self.load_item_image("열쇠", "key.png")
        self.load_item_image("해독제", "antidote.png")
        self.load_item_image("연구일지", "book.png")
        self.load_item_image("총", "gun.png")

        self.play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150, 300, 80)
        self.exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 250, 300, 80)
        self.resume_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 80)
        self.main_menu_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 300, 80)
        self.return_main_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 200, 300, 80)

        def load_font(size):
            user_font = os.path.join(self.current_dir, 'assets', 'ui', 'font.ttf')
            if os.path.exists(user_font): return pygame.font.Font(user_font, size)

            win_font = "C:/Windows/Fonts/malgun.ttf"
            if os.path.exists(win_font): return pygame.font.Font(win_font, size)

            try:
                return pygame.font.SysFont("malgungothic", size)
            except:
                return pygame.font.Font(None, size)

        self.font_button = load_font(40)
        self.font_pause = load_font(80)
        self.font_gameover = load_font(150)
        self.font_guide = load_font(50)
        self.font_item = load_font(20)

        self.init_game_system()
        self.mode = "MENU"
        self.previous_mode = None
        self.play_menu_music()

    def load_image_ui(self, filename):
        try:
            path = os.path.join(self.current_dir, 'assets', 'ui', filename)
            img = pygame.image.load(path).convert()
            return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            return None

    def load_item_image(self, item_name, filename):
        try:
            path = os.path.join(self.current_dir, 'assets', 'items', filename)
            img = pygame.image.load(path).convert_alpha()
            self.item_images[item_name] = pygame.transform.scale(img, (64, 64))
        except:
            self.item_images[item_name] = None

    def play_menu_music(self):
        try:
            bgm_path = os.path.join(self.current_dir, 'assets', 'sounds', 'menu_bgm.mp3')
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
        except:
            pass

    def stop_music(self):
        pygame.mixer.music.stop()

    def init_game_system(self):
        self.game_state = GameState()
        self.scene_manager = SceneManager(self.scene_json_path)
        self.battle_system = BattleSystem()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # --- [1] 메인 메뉴 ---
            if self.mode == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.init_game_system()
                        # [변경됨] 게임 시작 -> INTRO 화면으로 이동
                        self.mode = "INTRO"
                    elif self.exit_button_rect.collidepoint(event.pos):
                        self.running = False

            # --- [1.5] (추가됨) 인트로 화면 ---
            elif self.mode == "INTRO":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # 클릭하면 게임 방법 화면으로 이동
                        self.mode = "HOW_TO_PLAY"

            # --- [2] 게임 방법 ---
            elif self.mode == "HOW_TO_PLAY":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mode = "PROLOGUE"

            # --- [3] 프롤로그 ---
            elif self.mode == "PROLOGUE":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.stop_music()
                        self.mode = "STORY"
                        self.check_scene_item()

            elif self.mode == "PAUSE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.mode = self.previous_mode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button_rect.collidepoint(event.pos):
                        self.mode = self.previous_mode
                    elif self.main_menu_button_rect.collidepoint(event.pos):
                        self.mode = "MENU"
                        self.play_menu_music()
            elif self.mode == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_main_button_rect.collidepoint(event.pos):
                        self.mode = "MENU"
                        self.play_menu_music()
            elif self.mode in ["STORY", "BATTLE"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.previous_mode = self.mode
                    self.mode = "PAUSE"
                    return
                if self.mode == "STORY":
                    action = self.scene_manager.handle_event(event)
                    self.process_story_action(action)
                elif self.mode == "BATTLE":
                    action = self.battle_system.handle_event(event)
                    if action: self.process_battle_action(action)

    def update(self):
        if self.mode in ["MENU", "PAUSE", "GAME_OVER", "HOW_TO_PLAY", "PROLOGUE", "INTRO"]:
            pass
        elif self.mode == "STORY":
            self.scene_manager.update()
        elif self.mode == "BATTLE":
            action = self.battle_system.update()
            if action: self.process_battle_action(action)

    def check_scene_item(self):
        if not self.scene_manager.current_scene: return
        item_name = self.scene_manager.current_scene.get("item_reward")
        if item_name and item_name not in self.game_state.inventory:
            self.game_state.add_item(item_name)

    def process_story_action(self, action):
        if action == "START_BATTLE":
            print("⚔️ 전투 개시! 모드를 변경합니다.")
            self.mode = "BATTLE"

            current_bg_name = None
            if self.scene_manager.current_scene:
                current_bg_name = self.scene_manager.current_scene.get("background")

            current_scene_id = self.scene_manager.current_scene_id

            if current_scene_id == "FUTURELAB_02":
                self.play_bgm("boss_bgm.mp3")
                self.battle_system.start_battle(self.game_state, battle_type="BOSS", bg_image_name=current_bg_name)
            elif current_scene_id == "CONHALL_BACK_02":
                self.play_bgm("battle_bgm.mp3")
                self.battle_system.start_battle(self.game_state, battle_type="SUB_BOSS_BATTLE",
                                                bg_image_name=current_bg_name)
            else:
                self.play_bgm("battle_bgm.mp3")
                self.battle_system.start_battle(self.game_state, battle_type="NORMAL", bg_image_name=current_bg_name)

        elif action == "SCENE_CHANGED":
            self.check_scene_item()
        elif action == "GAME_END":
            self.mode = "MENU"
            self.play_menu_music()

    def play_bgm(self, filename):
        try:
            bgm_path = os.path.join(self.current_dir, 'assets', 'sounds', filename)
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
        except:
            pass

    def process_battle_action(self, action):
        if action == "BATTLE_WON":
            self.mode = "STORY"
            current = self.scene_manager.current_scene_id

            # [수정됨] 전투 승리 후 이동할 다음 씬을 정확하게 지정
            if current == "HILL_01":
                next_scene = "CONHALL_BACK_01"  # 헐떡고개 전투 승리 -> 컨홀 뒷편(대화)
            elif current == "CONHALL_BACK_01":
                next_scene = "CONHALL_BACK_02"  # 컨홀 일반 좀비 승리 -> 대학원생 만남
            elif current == "CONHALL_BACK_02":
                next_scene = "FUTURELAB_01"  # 대학원생 승리 -> 미래관 복도
            elif current == "FUTURELAB_01":
                next_scene = "FUTURELAB_02"  # 미래관 복도 전투 승리 -> 연구실 앞
            elif current == "FUTURELAB_02":
                next_scene = "FUTURELAB_RESULT_01"  # 보스전 승리 -> 엔딩
            else:
                next_scene = "DORM_01"  # 예외 시 처음으로

            # 다음 씬 로드
            if next_scene in self.scene_manager.scenes:
                self.scene_manager.current_scene_id = next_scene
                self.scene_manager.current_scene = self.scene_manager.scenes[next_scene]
                self.scene_manager.dialogue_index = 0
                self.check_scene_item()  # 아이템 있는지 확인
            else:
                print(f"⚠️ 이동할 씬을 찾을 수 없음: {next_scene}")

        elif action == "GAME_OVER":
            if self.game_state.player_hp <= 0:
                self.mode = "GAME_OVER"
            else:
                self.mode = "STORY"

    def draw_button(self, rect, text, hover_color=(200, 200, 200), default_color=WHITE):
        mouse_pos = pygame.mouse.get_pos()
        color = hover_color if rect.collidepoint(mouse_pos) else default_color
        pygame.draw.rect(self.screen, color, rect, border_radius=20)
        pygame.draw.rect(self.screen, BLACK, rect, 5, border_radius=20)
        text_surf = self.font_button.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_text_centered(self, text, y_offset=0, color=WHITE):
        text_surf = self.font_guide.render(text, True, color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(text_surf, text_rect)

    def draw_inventory(self):
        start_x = SCREEN_WIDTH - 80
        start_y = 20
        gap = 80
        for i, item_name in enumerate(self.game_state.inventory):
            img = self.item_images.get(item_name)
            if img:
                x_pos = start_x - (i * gap)
                self.screen.blit(img, (x_pos, start_y))
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(x_pos, start_y, 64, 64).collidepoint(mouse_pos):
                    name_surf = self.font_item.render(item_name, True, WHITE)
                    self.screen.blit(name_surf, (x_pos, start_y + 70))

    def draw(self):
        if self.mode != "PAUSE": self.screen.fill(BLACK)
        if self.mode == "MENU":
            if self.title_bg:
                self.screen.blit(self.title_bg, (0, 0))
            else:
                self.screen.fill((50, 50, 100))
            self.draw_button(self.play_button_rect, "게임 시작")
            self.draw_button(self.exit_button_rect, "게임 종료")

        # [추가됨] 인트로 화면 (게임 방법 전 단계)
        elif self.mode == "INTRO":
            if self.intro_bg:
                self.screen.blit(self.intro_bg, (0, 0))
            else:
                self.screen.fill(BLACK)
                self.draw_text_centered("INTRO", -50)
                self.draw_text_centered("- 화면 클릭 -", 100, GRAY)

        elif self.mode == "HOW_TO_PLAY":
            if self.how_to_play_bg:
                self.screen.blit(self.how_to_play_bg, (0, 0))
            else:
                self.screen.fill(BLACK)

            self.draw_text_centered("1. 아무도 믿지말고 모두 죽일 것.", -50)
            self.draw_text_centered("2. 1번을 꼭 기억할 것.", 50)
            self.draw_text_centered("- 화면을 클릭하면 넘어갑니다 -", 200, GRAY)

        elif self.mode == "PROLOGUE":
            if self.prologue_bg:
                self.screen.blit(self.prologue_bg, (0, 0))
            else:
                self.screen.fill(BLACK)

        elif self.mode == "STORY":
            self.scene_manager.draw(self.screen)
            self.draw_inventory()
        elif self.mode == "BATTLE":
            self.battle_system.draw(self.screen)
            self.draw_inventory()
        elif self.mode == "PAUSE":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            pause_text = self.font_pause.render("일시정지", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(pause_text, text_rect)
            self.draw_button(self.resume_button_rect, "계속 하기")
            self.draw_button(self.main_menu_button_rect, "메인으로")
        elif self.mode == "GAME_OVER":
            if self.gameover_bg:
                self.screen.blit(self.gameover_bg, (0, 0))
            else:
                self.screen.fill(BLACK)
                gameover_text = self.font_gameover.render("GAME OVER", True, RED)
                text_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
                self.screen.blit(gameover_text, text_rect)
            self.draw_button(self.return_main_button_rect, "메인으로")
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()