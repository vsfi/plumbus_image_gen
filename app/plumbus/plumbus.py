import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from fastapi import HTTPException
from pydantic import BaseModel

from PIL import Image, ImageOps, ImageEnhance
import uuid
from pydantic import BaseModel, Field
import os

import tarfile, io, zipfile

import random
import requests
import json
import time
import uuid

from app.models import PlumbusModel
from app.core.utils import get_logger

logger = get_logger(__name__)

class PlumbusDrawer:
    def __init__(self, model: PlumbusModel):
        self.model = model
        self.shape_to_file = {
            "smooth": "img/plumbus_smooth_nocolor.png",
            # "uglovatiy": "plumbus_uglovatiy.png",
            # "multi-uglovatiy": "plumbus_multiuglovatiy.png"
        }

    def calculate_scale(self):
        size_map = {
            "nano": 0.1,
            "XS": 0.5,
            "S": 0.8,
            "M": 1.0,
            "L": 1.5,
            "XL": 2.0,
            "XXL": 3.0
        }
        if self.model.size not in size_map.keys():
            raise HTTPException(status_code=422, detail="Available sizes: nano, XS, S, M, L, XL, XXL")
        return size_map[self.model.size]

    def get_color_overlay(self, color_hex: str, size: tuple) -> Image:
        overlay = Image.new("RGBA", size, color_hex + "80")
        return overlay

    def get_background(self, size: tuple) -> Image:
        # wrap_map = {
        #     "default": (255, 255, 255),
        #     "gift": (255, 215, 0),       # gold
        #     "limited": (200, 200, 255)   # soft blue
        # }
        wrap_bg_map = {
            "default": "img/default_bg.png",
            "gift": "img/gift_bg.png",
            "limited": "img/limited_bg.png"
        }
        bg_path = wrap_bg_map[self.model.wrapping]
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f"Background image '{bg_path}' not found.")

        bg = Image.open(bg_path).convert("RGBA").resize(size, Image.LANCZOS)
        return bg

    def draw(self):
        logger.info(f"New plumbus {self.model}")
        base_path = self.shape_to_file[self.model.shape]
        if not os.path.exists(base_path):
            raise FileNotFoundError(f"Base image '{base_path}' not found.")

        base = Image.open(base_path).convert("RGBA")
        scale = self.calculate_scale()
        new_size = [int(s * scale) for s in base.size]
        base = base.resize(new_size, Image.LANCZOS)

        color_map = {
            "pink": "#FFB6C1", "deep_pink": "#FF1493", "red": "#FF0000", "blue": "#0000FF",
            "green": "#008000", "yellow": "#FFFF00", "purple": "#800080", "orange": "#FFA500",
            "cyan": "#00FFFF", "lime": "#00FF00", "teal": "#008080", "brown": "#A52A2A"
        }

        #не спрашивай, этот кусок я спиздил в чатгпт 
        if self.model.color not in color_map.keys():
            raise HTTPException(status_code=422, detail="Available colors: pink, deep_pink, red, blue, green, yellow, purple, orange, cyan, lime, teal, brown")

        r, g, b = Image.new("RGB", (1, 1), color_map[self.model.color]).getpixel((0, 0))
        pixels = base.load()
        for y in range(base.size[1]):
            for x in range(base.size[0]):
                p = pixels[x, y]
                if p[3] > 0:
                    blended = (
                        int(p[0] * 0.5 + r * 0.5),
                        int(p[1] * 0.5 + g * 0.5),
                        int(p[2] * 0.5 + b * 0.5),
                        p[3]
                    )
                    pixels[x, y] = blended
        colored = base
        
        if random.choice([True, False]):
            colored = ImageOps.flip(colored)
        
        angle = random.uniform(-5, 5)
        colored = colored.rotate(angle, resample=Image.BICUBIC, expand=True)

        canvas_size = (512, 512)
        bg = self.get_background(canvas_size)
        offset = ((canvas_size[0] - colored.width) // 2, (canvas_size[1] - colored.height) // 2)
        bg.paste(colored, offset, colored)

        filename = f"plumbus_{self.model.size}_{self.model.color}_{self.model.wrapping}_{uuid.uuid4()}.png"
        bg.save(filename)
        print(f"Saved Plumbus image as {filename}")
        return filename


if __name__ == "__main__":
    main()
