"""副本开门任务与钥匙系统"""
from dataclasses import dataclass, field

# NPC对话状态机: 0=未开始, 1=进行中, 2=已完成
NPC_STATE_NOT_STARTED = 0
NPC_STATE_IN_PROGRESS = 1
NPC_STATE_COMPLETED = 2

# 任务分支 -> 奖励钥匙
QUEST_BRANCHES = {
    "fight": ("branch_fight", "war_key"),
    "negotiate": ("branch_negotiate", "diplomat_key"),
}

# 副本 -> (钥匙掉率, 每玩家掉落次数上限, 等级要求, 装等要求)
DUNGEON_RULES = {
    "hard_dungeon": (0.3, 3, 50, 200),
}
DEFAULT_DUNGEON_RULE = (0.2, 3, 1, 0)


@dataclass
class QuestState:
    qid: str
    player: str
    progress: int = 0
    completed: bool = False

class KeySystem:
    def __init__(self):
        self.quests: dict[str, QuestState] = {}
        self.keys: dict[str, int] = {}  # player -> key count
        self.npc_dialogue: dict[tuple[str, str], int] = {}
        self.quest_progress: dict[tuple[str, str], int] = {}
        self.drop_counts: dict[tuple[str, str], int] = {}
        self.player_branch: dict[str, str] = {}

    def get_key_drop_rate(self, player: str, dungeon: str) -> float:
        rate, max_drops, _, _ = DUNGEON_RULES.get(dungeon, DEFAULT_DUNGEON_RULE)
        if self.drop_counts.get((player, dungeon), 0) >= max_drops:
            return 0.0
        return rate

    def record_key_drop(self, player: str, dungeon: str):
        key = (player, dungeon)
        self.drop_counts[key] = self.drop_counts.get(key, 0) + 1

    def save_progress(self, qid: str, player: str, progress: int):
        self.quest_progress[(qid, player)] = progress
        state = self.quests.get(qid)
        if state is None:
            state = QuestState(qid=qid, player=player)
            self.quests[qid] = state
        state.progress = progress

    def load_progress(self, qid: str, player: str) -> int:
        return self.quest_progress.get((qid, player), 0)

    def get_quest_branch(self, player: str, choice: str) -> str:
        branch, _ = QUEST_BRANCHES.get(choice, ("branch_main", "common_key"))
        self.player_branch[player] = branch
        return branch

    def get_branch_key(self, player: str, choice: str) -> str:
        _, key_type = QUEST_BRANCHES.get(choice, ("branch_main", "common_key"))
        return key_type

    def is_key_tradable(self, key_type: str) -> bool:
        return False

    def meets_level_req(self, player_level: int, dungeon_level: int,
                        player_gear: int = 0, gear_req: int = 0) -> bool:
        return player_level >= dungeon_level and player_gear >= gear_req

    def use_key(self, player: str, key_type: str) -> bool:
        if self.keys.get(player, 0) <= 0:
            return False
        self.keys[player] -= 1
        return True

    def get_npc_reward(self, npc_id: str, player: str) -> dict:
        state = self.npc_dialogue.get((npc_id, player), NPC_STATE_NOT_STARTED)
        if state >= NPC_STATE_COMPLETED:
            return {}
        self.npc_dialogue[(npc_id, player)] = NPC_STATE_COMPLETED
        return {"gold": 100, "exp": 50}
