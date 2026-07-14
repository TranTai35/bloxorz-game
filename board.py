import json
import math
from dataclasses import dataclass

from block import Block, Orientation


@dataclass(frozen=True)
class TransitionResult:
    block: Block
    bridge_states: tuple
    activated_switches: tuple
    valid: bool


class Board:
    """Level data and deterministic Bloxorz transition rules."""

    SPECIAL_GRID_TILES = {
        "F": "fragile",
        "S": "soft",
        "H": "heavy",
        "X": "split",
    }

    def __init__(self, filename):
        with open(filename, "r", encoding="utf-8") as level_file:
            data = json.load(level_file)

        self.grid = [list(row) for row in data["grid"]]
        if not self.grid or not self.grid[0]:
            raise ValueError("Level phải có ít nhất một ô")
        if any(len(row) != len(self.grid[0]) for row in self.grid):
            raise ValueError("Tất cả các hàng trong grid phải có cùng độ dài")

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = tuple(data["start"])
        self.goal = tuple(data["goal"])

        self.bridges = self._parse_bridges(data.get("bridges", {}))
        self.bridge_at = {}
        for bridge_id, bridge in self.bridges.items():
            for cell in bridge["cells"]:
                if cell in self.bridge_at:
                    raise ValueError(f"Ô {cell} thuộc nhiều bridge")
                self.bridge_at[cell] = bridge_id

        self.switches = self._parse_switches(data.get("switches", []))
        self.switch_at = {switch["position"]: switch for switch in self.switches}
        self.fragile_cells = {
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.grid[row][col] == "F"
        }
        self.fragile_cells.update(
            tuple(cell) for cell in data.get("fragile", [])
        )

        self.initial_bridge_states = tuple(
            sorted(
                (bridge_id, bridge["initial_open"])
                for bridge_id, bridge in self.bridges.items()
            )
        )

        for name, cell in (("start", self.start), ("goal", self.goal)):
            if not self.is_inside(*cell):
                raise ValueError(f"{name} nằm ngoài grid: {cell}")
        if not self.is_floor(*self.start, self.initial_bridge_states):
            raise ValueError("Ô bắt đầu phải là ô sàn hợp lệ")

    def _parse_bridges(self, raw_bridges):
        if isinstance(raw_bridges, dict):
            entries = [dict(config, id=bridge_id) for bridge_id, config in raw_bridges.items()]
        elif isinstance(raw_bridges, list):
            entries = raw_bridges
        else:
            raise ValueError("bridges phải là object hoặc list")

        parsed = {}
        for index, entry in enumerate(entries):
            bridge_id = str(entry.get("id", f"bridge_{index + 1}"))
            cells = tuple(tuple(cell) for cell in entry.get("cells", []))
            if not cells:
                raise ValueError(f"Bridge {bridge_id} chưa có cells")
            parsed[bridge_id] = {
                "cells": cells,
                "initial_open": bool(entry.get("initial_open", entry.get("open", False))),
            }
        return parsed

    def _parse_switches(self, raw_switches):
        parsed = []
        valid_types = {"soft", "heavy", "split"}
        valid_actions = {"toggle", "open", "close"}

        for index, entry in enumerate(raw_switches):
            switch_type = str(entry.get("type", "soft")).lower()
            if switch_type not in valid_types:
                raise ValueError(f"Loại switch không hợp lệ: {switch_type}")

            action = str(entry.get("action", "toggle")).lower()
            if entry.get("behavior") == "permanent":
                action = "open" if entry.get("state", "open") == "open" else "close"
            if action not in valid_actions:
                raise ValueError(f"Hành vi switch không hợp lệ: {action}")

            switch_id = str(entry.get("id", f"switch_{index + 1}"))
            position = tuple(entry["position"])
            bridge_ids = tuple(str(item) for item in entry.get("bridges", []))
            unknown = [item for item in bridge_ids if item not in self.bridges]
            if unknown:
                raise ValueError(f"Switch {switch_id} tham chiếu bridge không tồn tại: {unknown}")

            targets = entry.get("targets")
            if targets is not None:
                if len(targets) != 2:
                    raise ValueError(f"Split switch {switch_id} cần đúng hai targets")
                targets = tuple(tuple(cell) for cell in targets)

            parsed.append(
                {
                    "id": switch_id,
                    "position": position,
                    "type": switch_type,
                    "bridges": bridge_ids,
                    "action": action,
                    "targets": targets,
                }
            )
        return parsed

    def is_inside(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def normalize_bridge_states(self, bridge_states=None):
        if bridge_states is None:
            return self.initial_bridge_states
        if isinstance(bridge_states, dict):
            state_dict = bridge_states
        else:
            state_dict = dict(bridge_states)
        return tuple(
            sorted(
                (bridge_id, bool(state_dict.get(bridge_id, bridge["initial_open"])))
                for bridge_id, bridge in self.bridges.items()
            )
        )

    def bridge_state_dict(self, bridge_states=None):
        return dict(self.normalize_bridge_states(bridge_states))

    def is_bridge(self, row, col):
        return (row, col) in self.bridge_at

    def is_fragile(self, row, col):
        return (row, col) in self.fragile_cells

    def get_switch(self, row, col):
        return self.switch_at.get((row, col))

    def tile_type(self, row, col):
        cell = (row, col)
        if cell == self.goal:
            return "goal"
        if cell in self.bridge_at:
            return "bridge"
        if cell in self.switch_at:
            return self.switch_at[cell]["type"]
        if cell in self.fragile_cells:
            return "fragile"
        if self.is_inside(row, col):
            symbol = self.grid[row][col]
            if symbol == "#":
                return "void"
            return self.SPECIAL_GRID_TILES.get(symbol, "floor")
        return "void"

    def is_floor(self, row, col, bridge_states=None):
        if not self.is_inside(row, col):
            return False

        cell = (row, col)
        if cell in self.bridge_at:
            bridge_id = self.bridge_at[cell]
            return self.bridge_state_dict(bridge_states).get(bridge_id, False)

        if cell in self.switch_at or cell in self.fragile_cells:
            return True
        if cell in (self.start, self.goal):
            return True
        return self.grid[row][col] != "#"

    def is_void(self, row, col, bridge_states=None):
        return not self.is_floor(row, col, bridge_states)

    def is_goal(self, row, col):
        return (row, col) == self.goal

    def is_valid_block(self, block, bridge_states=None):
        cells = block.get_cells()
        if any(not self.is_floor(row, col, bridge_states) for row, col in cells):
            return False

        if block.orientation == Orientation.STANDING and self.is_fragile(*block.pos1):
            return False
        return True

    def is_win(self, block):
        return block.orientation == Orientation.STANDING and block.pos1 == self.goal

    def available_actions(self, block):
        actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        if block.is_split:
            actions.append("SWITCH")
        return actions

    def _pressed_switch_ids(self, block):
        pressed = set()
        occupied = set(block.get_cells())
        for switch in self.switches:
            switch_type = switch["type"]
            position = switch["position"]
            if switch_type == "soft" and position in occupied:
                pressed.add(switch["id"])
            elif (
                switch_type in {"heavy", "split"}
                and block.orientation == Orientation.STANDING
                and block.pos1 == position
            ):
                pressed.add(switch["id"])
        return pressed

    def _apply_switches(self, old_block, new_block, bridge_states):
        states = self.bridge_state_dict(bridge_states)
        newly_pressed = self._pressed_switch_ids(new_block) - self._pressed_switch_ids(old_block)
        activated = []

        for switch in self.switches:
            if switch["id"] not in newly_pressed:
                continue
            activated.append(switch["id"])
            for bridge_id in switch["bridges"]:
                if switch["action"] == "toggle":
                    states[bridge_id] = not states[bridge_id]
                elif switch["action"] == "open":
                    states[bridge_id] = True
                else:
                    states[bridge_id] = False

            if switch["type"] == "split" and switch["targets"] is not None:
                new_block = Block.split(*switch["targets"])

        return new_block, self.normalize_bridge_states(states), tuple(activated)

    def transition(self, block, bridge_states, action):
        states = self.normalize_bridge_states(bridge_states)
        new_block = block.copy()
        new_block.move(action)

        # A block must first be able to land before its switches can be pressed.
        if not self.is_valid_block(new_block, states):
            return TransitionResult(new_block, states, (), False)

        new_block, new_states, activated = self._apply_switches(block, new_block, states)
        valid = self.is_valid_block(new_block, new_states)
        return TransitionResult(new_block, new_states, activated, valid)

    def get_action_cost(self, result, action):
        """Non-uniform cost used by UCS and A*.

        A roll costs 1, landing on fragile tiles adds 1, activating a switch
        adds 0.25, and changing the active split cube costs 0.5.
        """
        if action == "SWITCH":
            return 0.5
        cost = 1.0
        if any(self.is_fragile(*cell) for cell in result.block.get_cells()):
            cost += 1.0
        cost += 0.25 * len(result.activated_switches)
        return cost

    def heuristic(self, block):
        """Admissible relaxed distance for A* under ``get_action_cost``."""
        distance = min(
            abs(row - self.goal[0]) + abs(col - self.goal[1])
            for row, col in block.get_cells()
        )
        lower_bound = math.ceil(distance / 2)
        if block.orientation != Orientation.STANDING:
            lower_bound = max(lower_bound, 1)
        return float(lower_bound)

    def estimated_state_count(self):
        floor_cells = sum(
            1
            for row in range(self.rows)
            for col in range(self.cols)
            if (
                self.grid[row][col] != "#"
                or (row, col) in self.bridge_at
                or (row, col) in self.switch_at
                or (row, col) in self.fragile_cells
                or (row, col) in (self.start, self.goal)
            )
        )
        bridge_configurations = 2 ** len(self.bridges)
        return max(1, floor_cells * floor_cells * 2 * bridge_configurations)

    def print_board(self):
        for row in self.grid:
            print(" ".join(row))
