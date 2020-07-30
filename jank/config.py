from dataclasses import dataclass, field
import typing as t

import pyglet


@dataclass
class Config:
    caption: str = None
    icon: pyglet.image.ImageData = None
    default_size: t.Tuple[int, int] = (1000, 800)
    minimum_size: t.Tuple[int, int] = (100, 100)
    resizable: bool = True
    vsync: bool = True
    fps_label: pyglet.text.Label = None
    world_layers: t.List[str] = field(default_factory=list)
    ui_layers: t.List[str] = field(default_factory=list)
