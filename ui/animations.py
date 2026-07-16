from ursina import *


def fade_in(entity, duration=.4):

    entity.alpha = 0

    entity.animate(
        "alpha",
        1,
        duration=duration
    )


def fade_out(entity, duration=.4):

    entity.animate(
        "alpha",
        0,
        duration=duration
    )


def slide_from_bottom(entity, end_y, duration=.35):

    entity.y = end_y - .15

    entity.animate_y(
        end_y,
        duration=duration,
        curve=curve.out_quad
    )


def pulse(entity):

    entity.animate_scale(
        entity.scale * 1.05,
        duration=.4,
        loop=True
    )