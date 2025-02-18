"""A collection of all commands that a Kanna can use to interact with the game."""

import config
import time
import math
import settings
import utils
from components import Command
from vkeys import press, key_down, key_up
import random
import string


def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    # if abs(d_y) > settings.move_tolerance * 1.5:
    #     if direction == 'down':
    #         press('alt', 3)
    #     elif direction == 'up':
    #         press('alt', 1)
    press('v', num_presses)


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        Teleport('up').main()
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press('space', 3, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """REQUIRED"""

    def __init__(self):
        super().__init__(locals())
        self.buff_time = 0
        self.buff_cooldown = 160

    def main(self):
        buffs = ['c']
        now = time.time()
        if self.buff_time == 0 or now - self.buff_time > self.buff_cooldown:
            for key in buffs:
                press(key, 3, up_time=0.3)
            self.buff_time = now


class Teleport(Command):
    """
    Teleports in a given direction, jumping if specified. Adds the player's position
    to the current Layout if necessary.
    """

    def __init__(self, direction, jump='False'):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 3
        time.sleep(0.05)
        if self.direction in ['up', 'down']:
            num_presses = 2
        if self.direction != 'up':
            key_down(self.direction)
            time.sleep(0.05)
        if self.jump:
            if self.direction == 'down':
                press('alt', 3, down_time=0.1)
            else:
                press('alt', 1)
        if self.direction == 'up':
            key_down(self.direction)
            time.sleep(0.05)
        press('v', num_presses)
        key_up(self.direction)
        if settings.record_layout:
            config.layout.add(*config.player_pos)


class Reflection(Command):
    """Uses 'Reflection' once."""

    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.09)
        key_up(self.direction)
        press('a', 1, up_time=0.05)

class Sell(Command):
    def __init__(self):
        super().__init__(locals())
        self.first_sell = True

    def main(self):
        if self.first_sell:
            self.first_sell = False
            return
        random_string = random.sample(string.ascii_lowercase, 3)

        press("1", 1, down_time=0.1)
        time.sleep(0.1)
        key_down("lshift")
        press("2", 1, down_time=0.1)
        key_up("lshift")
        for char in random_string:
            press(char, 1, down_time=0.05)
        time.sleep(0.1)
        press("enter", 1, down_time=0.1)
        time.sleep(0.1)

        # Type "@sell"
        key_down("lshift")
        press("2", 1, down_time=0.1)
        key_up("lshift")
        for char in "sell":
            press(char, 1, down_time=0.03)
        time.sleep(0.1)
        press("enter", 1, down_time=0.1)
        time.sleep(0.1)


        # Down 3x, enter 3x
        press("down", 1, down_time=0.1)
        time.sleep(0.05)
        press("down", 1, down_time=0.1)
        time.sleep(0.05)
        press("down", 1, down_time=0.1)
        time.sleep(0.05)
        press("enter", 1, down_time=0.1)
        time.sleep(0.5)
        press("enter", 1, down_time=0.1)
        time.sleep(0.5)
        press("enter", 1, down_time=0.1)
        time.sleep(0.5)


        press("down", 128, down_time=0.05)

        time.sleep(0.15)
        press("enter", 1, down_time=0.1)
        time.sleep(0.15)

class Press(Command):
    """Press a key once."""

    def __init__(self, key):
        super().__init__(locals())
        self.key = key

    def main(self):
        press(self.key, 1, up_time=0.05)
