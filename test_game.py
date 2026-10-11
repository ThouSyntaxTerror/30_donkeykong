"""Quick self-check for the bug fix and the three optional functions.
Run: python test_game.py
"""
import random
import pygame

import game


def make_barrel_at_ladder(index):
    b = game.Barrel()
    lx, lower, upper = game.LADDERS[index]
    b.plat = upper
    b.pos.x = lx
    b.pos.y = game.platform_y(game.PLATFORMS[upper], lx) - game.BARREL_R
    b.skip = set()
    return b


def test_barrel_descends_when_roll_below_point_three():
    b = make_barrel_at_ladder(0)
    orig = random.random
    random.random = lambda: 0.25
    try:
        b.update(0.0001)
    finally:
        random.random = orig
    assert b.ladder == 0, "expected barrel to take the ladder when random()=0.25 (< 0.3)"


def test_barrel_stays_on_platform_when_roll_above_point_three():
    b = make_barrel_at_ladder(0)
    orig = random.random
    random.random = lambda: 0.5
    try:
        b.update(0.0001)
    finally:
        random.random = orig
    assert b.ladder is None, "expected barrel to NOT take the ladder when random()=0.5 (>= 0.3)"


def test_theme_color():
    assert game.theme_color(0) is None
    assert game.theme_color(2000) == (120, 60, 20)
    mid = game.theme_color(1000)
    assert isinstance(mid, tuple) and len(mid) == 3


def test_score_multiplier():
    assert game.score_multiplier(0) is None
    assert game.score_multiplier(500) == 2
    assert game.score_multiplier(1000) == 2


def test_on_barrel_jumped():
    game.floating_texts.clear()
    game.on_barrel_jumped(game.Player(), game.Barrel())
    assert len(game.floating_texts) == 1


if __name__ == "__main__":
    test_barrel_descends_when_roll_below_point_three()
    test_barrel_stays_on_platform_when_roll_above_point_three()
    test_theme_color()
    test_score_multiplier()
    test_on_barrel_jumped()
    print("All tests passed.")
