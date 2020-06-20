import pymunk

RECT = {
    "type": "rect",
    "offset": (float, float),
    "width": float, "height": float,
    "radius": float,
    "collision_type": int
}

POLY = {
    "type": "poly",
    "vertices": [
        (float, float)
    ],
    "radius": float,
    "collision_type": int
}

CIRCLE = {
    "type": "circle",
    "offset": (float, float),
    "radius": float,
    "collision_type": int
}

SEGMENT = {
    "type": "segment",
    "a": (float, float),
    "b": (float, float),
    "radius": float,
    "collision_type": int
}


def rect(data) -> pymunk.Poly:
    transform = pymunk.Transform(
        tx=-data["width"]/2,
        ty=-data["height"]/2
    )
    collider = pymunk.Poly(
        None,
        vertices=[
            (
                data["offset"][0],
                data["offset"][1]
            ),
            (
                data["offset"][0]+data["width"],
                data["offset"][1]
            ),
            (
                data["offset"][0]+data["width"],
                data["offset"][1]+data["height"]
            ),
            (
                data["offset"][0],
                data["offset"][1]+data["height"]
            )
        ],
        transform=transform,
        radius=data["radius"]
    )
    collider.collision_type = data["collision_type"]
    return collider


def poly(data) -> pymunk.Poly:
    collider = pymunk.Poly(
        None,
        vertices=data["vertices"],
        radius=data["radius"]
    )
    collider.collision_type = data["collision_type"]
    return collider


def circle(data) -> pymunk.Circle:
    collider = pymunk.Circle(
        None,
        radius=data["radius"],
        offset=data["offset"]
    )
    collider.collision_type = data["collision_type"]
    return collider


def segment(data) -> pymunk.Segment:
    collider = pymunk.Segment(
        None,
        a=data["a"],
        b=data["b"],
        radius=data["radius"]
    )
    collider.collision_type = data["collision_type"]
    return collider


def dict_to_collider(collider) -> pymunk.Shape:
    cols = {
        "poly": poly,
        "rect": rect,
        "circle": circle,
        "segment": segment
    }

    return cols[collider["type"]](collider)
