from worlds.splasher.test.__init import SplasherTest
from worlds.splasher.utils import SplasherUtils

class TestRegions(SplasherTest):
    options = {
        "include_keys": 2,
        "checkpoint_sanity": 2
    }

    def test_all_state_can_reach_everything(self):
        pass

    def test_fill(self):
        pass

    def test(self):
        state = self.multiworld.state
        p = self.player

        # for item in self.multiworld.get_items():
        #     print(f"{item.name} : {item.classification}")

        self.assertTrue(state.can_reach_region(SplasherUtils.origin, p))
        self.assertFalse(state.can_reach_region("Potatoes Ink", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Area 0", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Area 1", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 2 juridiction", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 1 juridiction", p))

        self.collect(self.get_item_by_name("Potatoes Ink : Entrance Key"))
        self.assertTrue(state.can_reach_region("Potatoes Ink", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Area 0", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Area 1", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 2 juridiction", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 1 juridiction", p))

        self.collect(self.get_item_by_name("Progressive Water"))
        self.assertTrue(state.can_reach_region("Potatoes Ink : Area 0", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Area 1", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 2 juridiction", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 1 juridiction", p))

        self.collect(self.get_item_by_name("Progressive Water"))
        self.assertTrue(state.can_reach_region("Potatoes Ink : Area 1", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 2 juridiction", p))
        self.assertFalse(state.can_reach_region("Potatoes Ink : Checkpoint 1 juridiction", p))

        self.collect(self.get_item_by_name("Potatoes Ink - Checkpoint 2"))
        self.assertTrue(state.can_reach_region("Potatoes Ink : Checkpoint 2 juridiction", p))
        self.assertTrue(state.can_reach_region("Potatoes Ink : Checkpoint 1 juridiction", p))