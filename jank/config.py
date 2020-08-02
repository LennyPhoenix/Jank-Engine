import typing as t
from dataclasses import dataclass, field

import jank


@dataclass
class Config:
    caption: str = None
    icon: jank.pyglet.image.ImageData = None
    default_size: t.Tuple[int, int] = (1000, 800)
    minimum_size: t.Tuple[int, int] = (100, 100)
    resizable: bool = True
    vsync: bool = True
    bilinear_filtering: bool = False
    antialiasing: int = None
    fps_label: jank.pyglet.text.Label = None
    world_layers: t.List[str] = field(default_factory=list)
    ui_layers: t.List[str] = field(default_factory=list)
