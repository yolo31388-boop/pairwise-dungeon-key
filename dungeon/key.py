"""副本开门任务与钥匙系统 - 含7个bug"""
from dataclasses import dataclass, field

@dataclass
class QuestState:
    qid: str
    player: str
    progress: int = 0  # bug2: 不保存
    completed: bool = False

class KeySystem:
    def __init__(self):
        self.quests: dict[str, QuestState] = {}
        self.keys: dict[str, int] = {}  # player -> key count
        self.npc_dialogue: dict[str, int] = {}  # bug7: 无状态

    def get_key_drop_rate(self, player: str, dungeon: str) -> float:
        # bug1: 必掉
        return 1.0

    def save_progress(self, qid: str, player: str, progress: int):
        # bug2: 不保存
        pass

    def get_quest_branch(self, player: str, choice: str) -> str:
        # bug3: 无分支
        return "main"

    def is_key_tradable(self, key_type: str) -> bool:
        # bug4: 可交易
        return True

    def meets_level_req(self, player_level: int, dungeon_level: int) -> bool:
        # bug5: 无等级要求
        return True

    def use_key(self, player: str, key_type: str) -> bool:
        # bug6: 不消耗
        return True

    def get_npc_reward(self, npc_id: str, player: str) -> dict:
        # bug7: 重复给奖励
        return {"gold": 100, "exp": 50}
