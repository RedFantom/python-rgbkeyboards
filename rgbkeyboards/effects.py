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


"""
General instructions

The build_* functions in this file each can generate a set of 
Instructions stored in an Effect that can be scheduled on a keyboard 
using the KeyboardController. The Effects may be applied to individual
keys as well as all keys. Effects for all keys may override the effects
applied to individual keys. Multiple individual key effects can be 
scheduled for the same moment as they can be individually applied. This
may decrease performance for all applied effects.

:param color: Valid color tuple[int], len 3, 8-bit values
:param duration: Desired duration of the effect in seconds, can be float
:param keys: The keys an effect should affect. ALL_KEYS defines the use
    of set_full_color, which may put the keyboard in a different mode 
    and thus override individual effects.
:param r: Resolution of the effect (duration of individual Instructions)
    A higher resolution means less instructions and thus less time spent
    on execution, but a lower resolution may result in more instructions
    and thus provide a more fluent effect.
"""


def build_flash(color, duration, keys=ALL_KEYS):
    # (tuple[int], float, (list[str], str, ALL_KEYS)) -> Effect
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
