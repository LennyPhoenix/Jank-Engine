import jank


def load_animation_sheet(image: jank.pyglet.image.AbstractImage, data: dict):
    max_length = max(a["length"] for a in data["animations"])
    sprite_sheet = jank.pyglet.image.ImageGrid(
        image,
        len(data["animations"]),
        max_length
    )
    animations = {}
    for a in range(len(data["animations"])):
        animation_data = data["animations"][a]
        frames = []
        frame_length = data["animations"][a]["frame_length"]
        for i in range(animation_data["length"]):
            frames.append(
                sprite_sheet[(a, i)]
            )
        animations[
            data["animations"][a]["alias"]
        ] = jank.pyglet.image.Animation.from_image_sequence(
            frames,
            frame_length,
            loop=data["animations"][a]["loop"]
        )
    return animations
