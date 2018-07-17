"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from collections import namedtuple

ALL_KEYS = None

OFF = (0, 0, 0)


Effect = namedtuple("Effect", ["name", "instr"])
# name: Name of the effect for debugging
# instr: List of Instructions to execute
# repeat: None or int, amount of times to repeat effect, 0: until cancelled
Instruction = namedtuple("Instruction", ["color", "key", "duration"])


def build_flash(color, duration, keys=ALL_KEYS):
    # (tuple[int], float) -> Effect
    """Create an Effect that flashes the keyboard in a single color"""
    instr = [
        Instruction(color, keys, duration),
        Instruction(OFF, keys, 0)
    ]
    return Effect("flash", instr)


def build_breathe(c, d, keys=ALL_KEYS, r=0.01):
    # (tuple[int], float, (list[str], str, ALL_KEYS), float) -> Effect
    """Build a breathe effect with a given resolution"""
    t = 0
    effect = Effect("breathe", [])
    while t <= d:
        frac = abs((t - d / 2) / (d / 2))
        color = tuple(int(v - frac * v) for v in c)
        effect.instr.append(Instruction(color, keys, r))
        t += r
    return effect


def build_transition(s, g, d, keys=ALL_KEYS, r=0.01):
    # (tuple[int], tuple[int], float, (list[str], str, ALL_KEYS), float -> Effect
    """Build an effect to transition from one color to another"""
    t = 0
    effect = Effect("transition", [])
    while t <= d:
        frac = abs((t - d) / d)
        color = tuple(int(s[i] + (g[i] - s[i]) * frac) for i in range(3))
        effect.instr.append(Instruction(color, keys, r))
        t += r
    return effect
