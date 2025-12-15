import pygame
import json
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class SceneManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.base_path = os.path.dirname(os.path.dirname(json_path))

        def load_font(size):
            user_font = os.path.join(self.base_path, 'assets', 'ui', 'font.ttf')
            if os.path.exists(user_font): return pygame.font.Font(user_font, size)

            win_font = "C:/Windows/Fonts/malgun.ttf"
            if os.path.exists(win_font): return pygame.font.Font(win_font, size)

            try:
                return pygame.font.SysFont("malgungothic", size)
            except:
                return pygame.font.Font(None, size)

        self.font = load_font(40)
        self.name_font = load_font(45)

        self.bg_cache = {}
        self.char_cache = {}
        self.next_arrow_img = self.load_ui_image("next_arrow.png", (50, 50))
        self.arrow_rect = pygame.Rect(1800, 760, 50, 50)

        self.scenes = self.load_scenes(json_path)
        if not self.scenes:
            self.scenes = {"ERROR": {"text": ["데이터 로드 실패"], "next_scene": None}}

        self.current_scene_id = list(self.scenes.keys())[0]
        self.current_scene = self.scenes[self.current_scene_id]
        self.dialogue_index = 0
        self.current_bgm = None
        self.play_scene_bgm()

    def load_scenes(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def load_ui_image(self, filename, size=None):
        try:
            path = os.path.join(self.base_path, 'assets', 'ui', filename)
            img = pygame.image.load(path).convert_alpha()
            if size: img = pygame.transform.scale(img, size)
            return img
        except:
            return None

    def get_image(self, cache, folder, filename, size=None):
        if not filename: return None
        if filename in cache: return cache[filename]
        try:
            path = os.path.join(self.base_path, 'assets', folder, filename)
            img = pygame.image.load(path).convert_alpha()
            if size: img = pygame.transform.scale(img, size)
            cache[filename] = img
            return img
        except:
            return None

    def play_scene_bgm(self):
        if not self.current_scene: return
        bgm_file = self.current_scene.get("bgm")
        if bgm_file and bgm_file != self.current_bgm:
            try:
                bgm_path = os.path.join(self.base_path, 'assets', 'sounds', bgm_file)
                pygame.mixer.music.load(bgm_path)
                pygame.mixer.music.play(-1)
                self.current_bgm = bgm_file
            except:
                pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.arrow_rect.collidepoint(event.pos):
                return self.next_text()
        return None

    def next_text(self):
        if not self.current_scene: return None
        dialogues = self.current_scene.get("text", [])
        if self.dialogue_index < len(dialogues) - 1:
            self.dialogue_index += 1
            return "NEXT_DIALOGUE"
        else:
            next_id = self.current_scene.get("next_scene")
            if next_id == "COMBAT_MODE" or next_id == "START_BATTLE":
                return "START_BATTLE"
            elif next_id in self.scenes:
                self.current_scene_id = next_id
                self.current_scene = self.scenes[next_id]
                self.dialogue_index = 0
                self.play_scene_bgm()
                return "SCENE_CHANGED"
            else:
                return "GAME_END"

    def update(self):
        pass

    def draw(self, screen):
        if self.current_scene:
            bg_name = self.current_scene.get("background")
            bg_img = self.get_image(self.bg_cache, "backgrounds", bg_name, (SCREEN_WIDTH, SCREEN_HEIGHT))
            if bg_img:
                screen.blit(bg_img, (0, 0))
            else:
                screen.fill((30, 30, 30))

            char_name = self.current_scene.get("character")
            if char_name:
                char_img = self.get_image(self.char_cache, "characters", char_name)
                if char_img:
                    target_h = 950 if "professor" in char_name else 800
                    ratio = target_h / char_img.get_height()
                    new_w = int(char_img.get_width() * ratio)
                    char_img = pygame.transform.scale(char_img, (new_w, target_h))

                    if "book" in char_name:
                        screen.blit(char_img, ((SCREEN_WIDTH - new_w) // 2, (SCREEN_HEIGHT - target_h) // 2))
                    else:
                        margin = 50 if "professor" in char_name else 100
                        screen.blit(char_img, (SCREEN_WIDTH - new_w - margin, SCREEN_HEIGHT - target_h))

        dialog_rect = pygame.Rect(50, 750, 1820, 300)
        s = pygame.Surface((dialog_rect.width, dialog_rect.height))
        s.set_alpha(200)  # 투명도 복구
        s.fill((0, 0, 0))
        screen.blit(s, (dialog_rect.x, dialog_rect.y))
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect, 3)

        if self.current_scene:
            dialogues = self.current_scene.get("text", [])
            if dialogues and self.dialogue_index < len(dialogues):
                text_content = dialogues[self.dialogue_index]
                speaker = ""
                content = text_content
                if ":" in text_content:
                    speaker, content = text_content.split(":", 1)

                if speaker:
                    speaker_surf = self.name_font.render(speaker, True, (255, 255, 0))
                    screen.blit(speaker_surf, (80, 780))

                # [색상 복구] 다시 흰색으로 설정
                content_surf = self.font.render(content.strip(), True, (255, 255, 255))
                screen.blit(content_surf, (80, 850))

        if self.next_arrow_img:
            screen.blit(self.next_arrow_img, self.arrow_rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.arrow_rect)