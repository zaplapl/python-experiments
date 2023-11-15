from random import choices
import json
from itertools import cycle
from datetime import datetime


def init_time_values(tick, tagged_cycles):
    for cycle_key, time_cycle in tagged_cycles.items():
        tag_value_now = tick.__getattribute__(cycle_key)
        for i in range(0, tag_value_now):
            next(time_cycle)
    return tagged_cycles


def sensible_loop():
    while True:
        now = datetime.now()
        stringify = lambda x: str(x).zfill(2)
        print(
            "\033[?25l"
            + f"{stringify(now.hour)}:{stringify(now.minute)}:{stringify(now.second)}",
            end="\r",
        )


def start_clock(
    hour_range=range(0, 24), minute_range=range(0, 60), second_range=range(0, 60)
):
    hour_cycle = cycle(hour_range)
    second_cycle = cycle(second_range)
    minute_cycle = cycle(minute_range)

    tagged_time_values = {
        value_range[0]: value_range[1]
        for value_range in [
            ("hour", hour_cycle),
            ("minute", minute_cycle),
            ("second", second_cycle),
        ]
    }
    tick = datetime.now()
    initial_values = init_time_values(tick, tagged_time_values)
    second = next(initial_values["second"])
    minute = next(initial_values["minute"])
    hour = next(initial_values["hour"])
    while True:
        if (datetime.now() - tick).seconds == 1:
            second = next(initial_values["second"])
            if second == 0:
                minute = next(initial_values["minute"])
            if minute == 0 and second == 0:
                hour = next(initial_values["hour"])
            time_string = (
                "\033[?25l"
                + ":".join(
                    str(time_value).zfill(2) for time_value in [hour, minute, second]
                )
                if type(hour) == int
                else "\033[?25l"
                + ":".join(str(time_value) for time_value in [hour, minute, second])
            )
            print(time_string, end="\r")
            tick = datetime.now()


if __name__ == "__main__":
    clock_type = input("clock type? ")
    if clock_type == "normal cycle":
        start_clock()
    if clock_type == "sensible":
        sensible_loop()
    if clock_type == "emoji":
        emoji_selection = [
            emoji_dict["emoji"]
            for emoji_dict in choices(
                json.load(open("./emoji.json", "r"))["emojis"], k=60
            )
        ]
        start_clock(emoji_selection[:24], emoji_selection, emoji_selection)
