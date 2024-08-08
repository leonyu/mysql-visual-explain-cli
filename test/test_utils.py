import enum
import io
import itertools
import os
import subprocess
import sys
import tempfile

import cairosvg
import PIL

from mysql_visual_explain_cli import __main__

PYZ_BIN = "./dist/mysql_visual_explain_cli.pyz"


class InvocationType(enum.Enum):
    UNKNOWN = 0
    CODE = 1
    CLI = 2


def compare_png(png1: str, png2: str) -> float:
    image1 = PIL.Image.open(png1)
    image2 = PIL.Image.open(png2)
    diff = PIL.ImageChops.difference(image1, image2)
    (width, height) = diff.size
    return sum(itertools.chain.from_iterable(diff.getdata())) / (256 * (width * height))


def compare_svg(svg1: str, svg2: str) -> float:
    with tempfile.TemporaryDirectory() as tmp:
        png1 = f"{tmp}/svg1.png"
        png2 = f"{tmp}/svg2.png"
        cairosvg.svg2png(url=svg1, write_to=png1)
        cairosvg.svg2png(url=svg2, write_to=png2)
        return compare_png(png1, png2)


def compare_images(file1: str, file2: str) -> float:
    if file1.endswith("png") and file2.endswith("png"):
        return compare_png(file1, file2)
    elif file1.endswith("svg") and file2.endswith("svg"):
        return compare_svg(file1, file2)
    else:
        raise ValueError(f"Unsupported comparison: {file1} {file2}")


def render(invoke_type: InvocationType, infile: str, outfile: str):
    match invoke_type:
        case InvocationType.CODE:
            with io.open(infile) as file:
                __main__.render(file.read(), outfile)
        case InvocationType.CLI:
            assert os.path.exists(PYZ_BIN), ".pyz binary does not exist"
            subprocess.run([sys.executable, PYZ_BIN, infile, outfile], check=True)
        case _:
            raise ValueError(f"Invalid type: {invoke_type}")
