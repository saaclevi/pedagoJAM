# Arquivo: services/state_tracker.py
import time

class StateTracker:
    def __init__(self):
        self._store = {} 
        self.SESSION_TTL = 1800 

    def _init_default_state(self):
        return {
            "active_class_id": None,
            "interaction_stage": None,
            "temp_data": {},
            "last_interaction": time.time()
        }

    def get_state(self, user_id):
        user_state = self._store.get(user_id)
        if not user_state or (time.time() - user_state["last_interaction"] > self.SESSION_TTL):
            user_state = self._init_default_state()
            self._store[user_id] = user_state
        return user_state

    def update_slot(self, user_id, key, value):
        state = self.get_state(user_id)
        state[key] = value
        state["last_interaction"] = time.time()
        self._store[user_id] = state

    def set_stage(self, user_id, stage_name):
        self.update_slot(user_id, "interaction_stage", stage_name)

    def clear_flow(self, user_id):
        state = self.get_state(user_id)
        state["interaction_stage"] = None
        state["temp_data"] = {}
        state["last_interaction"] = time.time()
        self._store[user_id] = state    