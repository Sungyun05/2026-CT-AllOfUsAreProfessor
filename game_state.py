class GameState:
    """
    주인공의 체력, 인벤토리, 진행도 등 게임의 모든 상태를 저장하고 관리합니다.
    """

    def __init__(self):
        # 1. 플레이어 체력
        self.player_hp = 100
        self.max_hp = 100

        # 2. 인벤토리 (아이템 이름을 담을 리스트)
        self.inventory = []

        # 3. 스토리 플래그 (특정 사건 발생 여부)
        self.flags = {}

    def update_health(self, amount):
        """체력을 변경합니다. (양수: 회복, 음수: 피해)"""
        self.player_hp += amount
        # 체력은 0보다 작을 수 없고, 최대 체력보다 클 수 없음
        self.player_hp = max(0, min(self.player_hp, self.max_hp))

    def add_item(self, item_name):
        """
        [추가된 기능] 아이템을 인벤토리에 추가합니다.
        """
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            print(f"🎒 인벤토리 추가됨: {item_name}")

    def has_item(self, item_name):
        """특정 아이템을 가지고 있는지 확인합니다."""
        return item_name in self.inventory

    def get_player_stats(self):
        """전투 시 공격력 등을 계산해서 반환"""
        # 총이 있으면 공격력이 세짐
        attack_power = 10
        if "총" in self.inventory:
            attack_power = 30

        return {"ATTACK": attack_power, "DEFENSE": 0}