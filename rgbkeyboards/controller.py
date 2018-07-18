"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""
# Standard Library
from datetime import datetime
import logging
from threading import Thread
from time import sleep
from warnings import warn
# Project Modules
from rgbkeyboards.effects import *
from rgbkeyboards.keyboard import BaseKeyboard
from rgbkeyboards._queue import Queue, PriorityQueue, Empty


class KeyboardController(Thread):
    """
    Thread-based handler for Keyboard instance to manage effects

    Because this class is Thread based, it allows running a loop so
    the LEDs of any backend can be controlled asynchronously. All events
    are schedules into a PriorityQueue and given a priority based on the
    period they are supposed to execute after.

    Elements with a waiting period of 0 are executed as soon as
    possible. Effects with the same scheduled moment of execution are
    executed in the order they were scheduled in.

    If for some reason the KeyboardController is not able to keep up
    with the stream of commands, the commands are skipped when they were
    scheduled more time in the past than :param margin:.

    :param keyboard: Keyboard backend to control using this handler.
        While technically it is possible to control a keyboard both
        with a handler and 'manually' (that is, synchronously in
        a different thread), this is not tested and not recommended.

    :param sleep: Sleeping period when there are no commands available
        while True loops in Python consume all the CPU time they can
        get. In order to reduce the amount of CPU time wasted on just
        checking if there are commands, the loop can be suspended for
        a short period. Lowering this value will have a positive effect
        on the response time, but a negative effect on the CPU usage.

    :param margin: Upper bound for execution of scheduled events
        The commands are scheduled to be executed at a certain point in
        time (a period after the moment they were scheduled). The margin
        is the amount of time that premature execution of commands is
        allowed.

        Example (simplified with datetimes represented as ints):
        self._start = 0
        priority = 11  # Execution time: t = 11
        margin = 0.10

        If the control loop is fast enough, it may come at a point
        that datetime.now() = 10.95. 11 - (10.95 - 0) < margin, thus the
        command will be executed in this cycle. See
        _is_approximately_now for more details.

    :param level: Logging level for the basic Logger instance
    """

    def __init__(self, keyboard, sleep=0.05, margin=0.10, level=logging.ERROR):
        """Initialize attributes and Logger"""
        assert isinstance(keyboard, BaseKeyboard)
        self._kb = keyboard
        self._exit_queue = Queue()
        self._command_queue = PriorityQueue()
        self._start = None
        self._sleep = sleep
        self._margin = margin
        self._stale = list()
        self._stale_queue = Queue()
        self._effect_queue = Queue()
        self._effects = dict()
        self._id = 1

        self._logger = logging.getLogger("KeyboardController")
        self._logger.setLevel(level)

        Thread.__init__(self)

    def run(self):
        """
        Run the keyboard control loop

        Run a loop to process commands put into the internal queue.
        Exits the loop when the function stop() is called.
        """
        self._start = datetime.now()
        with self._kb.control():  # Enables control
            if not self._kb.is_control_enabled:
                raise RuntimeError("Could not enable keyboard LED control")
            self._logger.debug("Claimed LED Control")
            while True:
                if self.get_queue_item(self._exit_queue) is not None:
                    break
                self._check_effects()
                self._process_command()
        self._logger.debug("Loop end")
        if self._kb.is_control_enabled:
            warn("Keyboard control not properly disabled", RuntimeWarning)

    def _check_effects(self):
        """Check for scheduled and cancelled Effects"""
        item = self.get_queue_item(self._stale_queue)
        while item is not None:
            self._stale.append(item)
            item = self. get_queue_item(self._stale_queue)
        item = self.get_queue_item(self._effect_queue)
        while item is not None:
            priority, id, effect = item
            if not isinstance(effect, Effect):
                # TODO: How can the (None, Effect) end up in the _effect_queue?
                return
            self._effects[id] = None
            item = (priority, id, (None, effect))
            self._command_queue.put(item)

    @staticmethod
    def get_queue_item(queue):
        """Safely retrieve an item from a given queue"""
        if queue.empty() is True:
            return None
        try:
            return queue.get()
        except Empty:
            return None

    def _process_command(self):
        """Get a single command from the PriorityQueue and execute"""
        item = self.get_queue_item(self._command_queue)
        if item is None:
            sleep(self._sleep)
            return
        priority, id, (func, args) = item
        if not self._is_approximately_now(priority):
            self._command_queue.put(item)
            return
        if id in self._effects:
            self._exec_effect_instr(priority, id, args)
            return
        self._logger.debug("Processing a single command: {}, {}(*{})".format(
            priority, func, args))
        func(*args)

    def _exec_effect_instr(self, priority, id, effect):
        """Execute a single effect instruction from an effect"""
        assert isinstance(effect, Effect)
        if id in self._stale:
            # Effect has been cancelled, cleanup
            del self._effects[id]
            return  # Not in Queue anymore
        if self._effects[id] is None:
            self._effects[id] = datetime.now()
        if len(effect.instr) == 0:  # Effect has ended
            del self._effects[id]
            return  # Not rescheduled
        # Retrieve the next instruction
        instr = effect.instr.pop(0)
        assert isinstance(instr, Instruction)
        # Execute instruction
        if instr.key is ALL_KEYS:
            self._kb.set_full_color(*instr.color)
        elif isinstance(instr.key, str):
            self._kb.set_ind_color({instr.key: instr.color})
        else:
            arg = {key: instr.color for key in instr.key}
            self._kb.set_ind_color(arg)
        # Schedule next instruction
        item = (priority + instr.duration, id, (self._exec_effect_instr, effect))
        self._command_queue.put(item)

    def stop(self):
        """Stop the running thread"""
        if not self.is_alive():
            return
        self._exit_queue.put(True)

    def sched_effect(self, after, effect):
        """Schedule an Effect for playing"""
        after = (datetime.now() - self._start).total_seconds() + after
        effect_id = self._id
        self._effect_queue.put((after, effect_id, effect))
        self._id += 1
        return effect_id

    def cancel_effect(self, effect_id):
        """Cancel the scheduling of an effect or an active effect"""
        self._stale_queue.put(effect_id)

    def set_full_color(self, after, color):
        """Schedule set the color of all the LEDs on the keyboard"""
        assert isinstance(after, int), "after paramaeter must be int ms"
        assert isinstance(color, tuple) and len(color) == 3, \
            "color parameter must be valid color tuple"
        self._after(self._kb.set_full_color, color, after)

    def set_ind_color(self, after, leds):
        """Schedule set the color of the individual LEDs"""
        assert isinstance(leds, dict)
        self._after(self._kb.set_ind_color, (leds,), after)

    def _after(self, func, args, period):
        """
        Schedule an action to be performed after int: period seconds

        Puts a function with its arguments into a reverse PriorityQueue.
        The priority is determined as the sum of the amount of seconds
        since the start of taking commands and the period in which
        the command given should be executed (a longer period results
        in a higher priority number and thus later execution).
        """
        self._logger.debug("Scheduling new task: {}(*{}) {} seconds from now".format(
            func, args, period))
        if self._start is None:
            raise RuntimeError("KeyboardController has not started")
        priority = (datetime.now() - self._start).total_seconds() + period
        self._command_queue.put((priority, 0, (func, args)))

    def _is_approximately_now(self, seconds):
        """Determines if the amount of seconds has approximately passed"""
        diff = abs(seconds - (datetime.now() - self._start).total_seconds())
        return diff < self._margin

    """
    Manual loop interface
    
    If your program already runs a loop that you can somehow schedule
    events in, like a Tkinter event loop or something similar, these
    functions can be used to integrate the Handler with such a loop.
    
    Your loop should call update() repeatedly (if possible many times a 
    second) and use close() when the loop ends to make sure that
    everything is cleaned up nicely.
    
    To not make the update() function slow down your main program, make
    sure to use a sleep time of zero when initializing the class.
    """

    def update(self):
        """Perform a single command operation cycle"""
        if self.is_alive():
            raise RuntimeError("Synchronous and thread-based interfaces used "
                               "simultaneously!")
        if not self._kb.is_control_enabled:
            r = self._kb.enable_control()
            if r is False:
                raise RuntimeError("Could not enable keyboard LED control")
            self._start = datetime.now()
        self._check_effects()
        self._process_command()

    def close(self):
        """Close and cleanup after using synchronous interface"""
        if not self._kb.is_control_enabled:
            return
        r = self._kb.disable_control()
        if r is False:
            raise RuntimeError("Could not disable keyboard LED control")


if __name__ == '__main__':
    from rgbkeyboards import Keyboards
    backend = Keyboards().keyboard
    handler = KeyboardController(backend, level=logging.DEBUG)
    handler.start()
    assert handler.is_alive()
    flash = build_flash((255, 255, 0), 1)
    breathe = build_breathe((255, 0, 0), 10)
    trans = build_transition((0, 255, 0), (0, 0, 255), 5)
    handler.sched_effect(1, flash)
    handler.sched_effect(2, breathe)
    handler.sched_effect(10, trans)
    try:
        sleep(15)
    except KeyboardInterrupt:
        pass
    handler.stop()
    handler.join(1)
