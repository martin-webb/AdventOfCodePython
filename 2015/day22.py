from collections import deque
from dataclasses import dataclass
from pathlib import Path
from time import time

YEAR = 2015
DAY = 22
NAME = "Wizard Simulator 20XX"


@dataclass
class Player:
    hp: int
    armor: int
    mana: int
    mana_spent: int
    shield: int
    recharge: int

    def copy(self) -> "Player":
        return Player(
            self.hp,
            self.armor,
            self.mana,
            self.mana_spent,
            self.shield,
            self.recharge
        )


@dataclass
class Boss:
    hp: int
    damage: int
    poison: int

    def copy(self) -> "Boss":
        return Boss(self.hp, self.damage, self.poison)


@dataclass
class Game:
    player: Player
    boss: Boss
    is_hard: bool

    def copy(self) -> "Game":
        return Game(
            player=self.player.copy(),
            boss=self.boss.copy(),
            is_hard=self.is_hard
        )


@dataclass(frozen=True)
class Spell:
    name: str
    cost: int


SPELLS = [
    Spell("Magic Missile", 53),
    Spell("Drain", 73),
    Spell("Shield", 113),
    Spell("Poison", 173),
    Spell("Recharge", 229)
]


def parse_input(input: str) -> tuple[int, int]:
    for line in input.strip().split("\n"):
        parts = line.split(":")
        if parts[0] == "Hit Points":
            hp = int(parts[1])
        elif parts[0] == "Damage":
            damage = int(parts[1])

    return hp, damage


def can_cast(spell: Spell, game: Game) -> bool:
    if spell.name == "Magic Missile":
        return (spell.cost <= game.player.mana)
    elif spell.name == "Drain":
        return (spell.cost <= game.player.mana)
    elif spell.name == "Shield":
        return (spell.cost <= game.player.mana) and (game.player.shield == 0)
    elif spell.name == "Poison":
        return (spell.cost <= game.player.mana) and (game.boss.poison == 0)
    elif spell.name == "Recharge":
        return (spell.cost <= game.player.mana) and (game.player.recharge == 0)
    else:
        assert False, "Should not get here"


def cast_spell(spell: Spell, game: Game) -> None:
    if spell.name == "Magic Missile":
        game.boss.hp -= 4
    elif spell.name == "Drain":
        game.player.hp += 2
        game.boss.hp -= 2
    elif spell.name == "Shield":
        game.player.shield = 6
    elif spell.name == "Poison":
        game.boss.poison = 6
    elif spell.name == "Recharge":
        game.player.recharge = 5

    game.player.mana -= spell.cost
    game.player.mana_spent += spell.cost


def apply_effects(game: Game) -> None:
    player_hp_loss = 1 if game.is_hard else 0

    # Pre-tick value used for these as they apply per tick
    player_mana_recharged = 101 if game.player.recharge > 0 else 0
    boss_hp_loss = 3 if game.boss.poison > 0 else 0

    # Post-tick value used for armor as this wears off at the beginning of this
    # turn/end of the last turn
    player_armor_boost = 7 if game.player.shield - 1 > 0 else 0

    game.player.hp -= player_hp_loss
    game.player.armor = player_armor_boost
    game.player.mana += player_mana_recharged
    game.player.shield = max(game.player.shield - 1, 0)
    game.player.recharge = max(game.player.recharge - 1, 0)

    game.boss.hp -= boss_hp_loss
    game.boss.poison = max(game.boss.poison - 1, 0)


def boss_attack(game: Game) -> None:
    game.player.hp -= max(game.boss.damage - game.player.armor, 1)


def solve(start: Game) -> int:
    mana_spent_min = float("inf")

    q: deque[tuple[int, Game]] = deque([(0, start)])
    while q:
        turn, current = q.popleft()

        # Prune search space
        if current.player.mana_spent > mana_spent_min:
            continue

        apply_effects(current)

        if current.player.hp <= 0:
            continue

        if current.boss.hp <= 0:
            mana_spent_min = min(mana_spent_min, current.player.mana_spent)
            continue

        is_player_turn = turn % 2 == 0
        if is_player_turn:
            for spell in SPELLS:
                if can_cast(spell, current):
                    next = current.copy()
                    cast_spell(spell, next)
                    q.append((turn+1, next))
        else:
            next = current.copy()
            boss_attack(next)
            q.append((turn+1, next))

    return int(mana_spent_min)


def part1(input: str) -> int:
    boss_hp, boss_damage = parse_input(input)

    game = Game(
        player=Player(50, 0, 500, 0, 0, 0),
        boss=Boss(boss_hp, boss_damage, 0),
        is_hard=False
    )

    result = solve(game)
    return result


def part2(input: str) -> int:
    boss_hp, boss_damage = parse_input(input)

    game = Game(
        player=Player(50, 0, 500, 0, 0, 0),
        boss=Boss(boss_hp, boss_damage, 0),
        is_hard=True
    )

    result = solve(game)
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day22_full.txt", part1, 1269),
        ("Part 2", "inputs/day22_full.txt", part2, 1309),
    ):
        path = Path(__file__).parent / filename
        with open(path) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)",
              "\u2B50"
              if expected and result == expected and "_full" in filename
              else "")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
