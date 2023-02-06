from .white_box_cartoonizer.cartoonize import WB_Cartoonize
import numpy as np
from PIL import Image
import os
import sys
import yaml
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open('cartoon_add/config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)

wb_cartoonizer = WB_Cartoonize(os.path.abspath(
    "cartoon_add/white_box_cartoonizer/saved_models/"), opts['gpu'])

def cartoonize(path):

    img = Image.open(path)

    if img.mode == "RGBA":
        image2 = Image.new("RGB", img.size, (255, 255, 255))
        image2.paste(img, mask=img.split()[3])
    else:
        image2 = img.convert('RGB')

    image = np.array(image2)
    cartoon_image = wb_cartoonizer.infer(image)
    final_img = Image.fromarray(cartoon_image)
    return  final_img

