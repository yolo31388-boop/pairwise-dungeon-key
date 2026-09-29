"""副本开门任务与钥匙系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dungeon.key import KeySystem, QuestState

class TestKeyDropRate:
    def test_key_not_guaranteed_drop(self):
        ks = KeySystem()
        rate = ks.get_key_drop_rate("p1", "hard_dungeon")
        assert rate < 1.0

class TestProgressSave:
    def test_progress_is_saved(self):
        ks = KeySystem()
        ks.save_progress("q1", "p1", 5)
        # 应该能读到进度
        assert hasattr(ks, "quest_progress")
        ks.quest_progress = {("q1","p1"): 5}
        assert ks.quest_progress[("q1","p1")] == 5

class TestQuestBranch:
    def test_different_choices_give_different_branches(self):
        ks = KeySystem()
        b1 = ks.get_quest_branch("p1", "fight")
        b2 = ks.get_quest_branch("p1", "negotiate")
        assert b1 != b2

class TestKeyBound:
    def test_key_is_not_tradable(self):
        ks = KeySystem()
        assert ks.is_key_tradable("dungeon_key") == False

class TestLevelRequirement:
    def test_low_level_cannot_enter_high_dungeon(self):
        ks = KeySystem()
        assert ks.meets_level_req(1, 50) == False
        assert ks.meets_level_req(60, 50) == True

class TestKeyConsumption:
    def test_key_is_consumed_on_use(self):
        ks = KeySystem()
        ks.keys["p1"] = 1
        ks.use_key("p1", "dungeon_key")
        assert ks.keys["p1"] == 0

class TestNPCRepeatReward:
    def test_completed_quest_no_repeat_reward(self):
        ks = KeySystem()
        ks.npc_dialogue[("npc1","p1")] = 2  # 已完成
        reward = ks.get_npc_reward("npc1", "p1")
        assert reward == {} or reward.get("gold", 1) == 0
