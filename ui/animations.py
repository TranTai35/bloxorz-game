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


def stagger_slide_in(entities, start_delay=0.15, step_delay=0.08, duration=.3):
    """
    Cho từng entity trong danh sách xuất hiện lần lượt (trượt nhẹ từ
    dưới lên + phóng to từ 0 -> full), thay vì hiện hết cùng lúc.
    Dùng cho danh sách menu để trông "mượt" hơn khi vào Main Menu.

    Lưu ý: cố tình KHÔNG dùng entity.alpha ở đây. Các GlowText không
    có model riêng (chỉ là Entity cha chứa nhiều Text con), nên set
    alpha trên entity cha không chắc lan xuống được các Text con.
    Scale/position thì luôn hoạt động đúng vì đó là API gốc của
    Entity, không phụ thuộc cách GlowText dựng bên trong.
    """

    for index, entity in enumerate(entities):
        end_y = entity.y
        end_scale = entity.scale

        entity.y = end_y - .04
        entity.scale = 0

        delay = start_delay + index * step_delay

        invoke(
            entity.animate_y,
            end_y,
            duration=duration,
            curve=curve.out_quad,
            delay=delay
        )

        invoke(
            entity.animate_scale,
            end_scale,
            duration=duration,
            curve=curve.out_back,
            delay=delay
        )