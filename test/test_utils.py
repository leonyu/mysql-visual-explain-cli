import enum
import io
import itertools
import os
import subprocess
import sys
import tempfile

import cairosvg
import PIL

from mysql_visual_explain_cli import main

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


def pngify(file: str, tmpdir: dir) -> float:
    if file.endswith(".png"):
        return file
    if file.endswith(".svg"):
        pngfile = os.path.join(tmpdir, ".png")
        cairosvg.svg2png(url=file, write_to=pngfile)
        return pngfile
    raise ValueError(f"Unsupported image type: {file}")


def compare_images(file1: str, file2: str) -> float:
    with tempfile.TemporaryDirectory() as tmpdir:
        return compare_png(pngify(file1, tmpdir), pngify(file2, tmpdir))


def render(invoke_type: InvocationType, infile: str, outfile: str):
    match invoke_type:
        case InvocationType.CODE:
            with io.open(infile) as file:
                main.render(file.read(), outfile)
        case InvocationType.CLI:
            assert os.path.exists(PYZ_BIN), ".pyz binary does not exist"
            subprocess.run([sys.executable, PYZ_BIN, infile, outfile], check=True)
        case _:
            raise ValueError(f"Invalid type: {invoke_type}")
