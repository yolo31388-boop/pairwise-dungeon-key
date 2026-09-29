"""副本开门任务与钥匙系统"""
from dataclasses import dataclass, field

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
        self.npc_dialogue: dict[tuple, int] = {}  # (npc_id, player) -> 对话状态
        self.quest_progress: dict[tuple, int] = {}  # (qid, player) -> 进度
        self.kill_counts: dict[tuple, int] = {}  # (player, dungeon) -> 击杀次数
        self.branches: dict[str, str] = {}  # player -> 已选分支
        self.base_drop_rate = 0.3
        self.max_drop_kills = 10  # 超过次数后不再掉钥匙

    def get_key_drop_rate(self, player: str, dungeon: str) -> float:
        # 概率掉落，且有次数限制：超过上限后不再掉落
        kills = self.kill_counts.get((player, dungeon), 0)
        if kills >= self.max_drop_kills:
            return 0.0
        return self.base_drop_rate

    def save_progress(self, qid: str, player: str, progress: int):
        # 保存任务进度，掉线后可恢复
        self.quest_progress[(qid, player)] = progress
        state = self.quests.get(qid)
        if state is not None and state.player == player:
            state.progress = progress

    def get_quest_branch(self, player: str, choice: str) -> str:
        # 任务链分支：不同选择进入不同分支，给不同钥匙
        branch_map = {
            "fight": "fight_branch",
            "negotiate": "negotiate_branch",
            "stealth": "stealth_branch",
        }
        branch = branch_map.get(choice, f"{choice}_branch")
        self.branches[player] = branch
        return branch

    def is_key_tradable(self, key_type: str) -> bool:
        # 钥匙绑定角色，不可交易
        return False

    def meets_level_req(self, player_level: int, dungeon_level: int) -> bool:
        # 等级要求：玩家等级需达到副本等级
        return player_level >= dungeon_level

    def use_key(self, player: str, key_type: str) -> bool:
        # 使用后消耗一把钥匙
        count = self.keys.get(player, 0)
        if count <= 0:
            return False
        self.keys[player] = count - 1
        return True

    def get_npc_reward(self, npc_id: str, player: str) -> dict:
        # 对话状态机：0=未接 1=进行中 2=已完成；完成后不再给奖励
        state = self.npc_dialogue.get((npc_id, player), 0)
        if state >= 2:
            return {}
        self.npc_dialogue[(npc_id, player)] = 2
        return {"gold": 100, "exp": 50}
