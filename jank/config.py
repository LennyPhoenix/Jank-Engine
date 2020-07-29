from dataclasses import dataclass, field
from typing import List, Tuple

import pyglet


@dataclass
class Config:
    caption: str = None
    icon: pyglet.image.ImageData = None
    default_size: Tuple[int, int] = (1000, 800)
    minimum_size: Tuple[int, int] = (100, 100)
    resizable: bool = True
    vsync: bool = True
    fps_label: pyglet.text.Label = None
    world_layers: List[str] = field(default_factory=list)
    ui_layers: List[str] = field(default_factory=list)
