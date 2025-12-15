import pygame
import sys
from game_state import GameState
from battle_system import BattleSystem

# --- 설정 ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60


def run_battle_test():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("전투 시스템 테스트 모드")
    clock = pygame.time.Clock()

    # 1. 필수 시스템 초기화
    game_state = GameState()
    battle_system = BattleSystem()

    # 2. 전투 강제 시작
    battle_system.start_battle(game_state)

    running = True
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 전투 시스템에 키 입력 전달
            battle_system.handle_event(event)

        # 업데이트
        result = battle_system.update()

        # 결과 확인
        if result == "BATTLE_WON":
            print("승리! 테스트 종료")
            running = False
        elif result == "GAME_OVER":
            print("패배! 테스트 종료")
            running = False

        # 그리기
        battle_system.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_battle_test()