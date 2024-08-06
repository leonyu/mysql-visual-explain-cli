import glob
import itertools
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import cairosvg
import PIL
import pytest

PYZ_BIN = "./dist/mysql_visual_explain_cli.pyz"


def compare_png(png1: str, png2: str) -> float:
    image1 = PIL.Image.open(png1)
    image2 = PIL.Image.open(png2)
    diff = PIL.ImageChops.difference(image1, image2)
    (width, height) = diff.size
    return sum(itertools.chain.from_iterable(diff.getdata())) / (256 * (width * height))


def remove_pt(svg_content: str) -> str:
    return re.sub(r'"(\d+)pt"', r'"\1"', svg_content)


def compare_svg(svg1: str, svg2: str) -> float:
    svg1_content = pathlib.Path(svg1).read_text()
    svg2_content = pathlib.Path(svg2).read_text()
    with tempfile.TemporaryDirectory() as tmp:
        png1 = f"{tmp}/svg1.png"
        png2 = f"{tmp}/svg2.png"
        cairosvg.svg2png(remove_pt(svg1_content), write_to=png1)
        cairosvg.svg2png(remove_pt(svg2_content), write_to=png2)
        return compare_png(png1, png2)


@pytest.mark.parametrize("json_file", glob.glob("./fixtures/*.json"))
class TestClass:
    output_dir = tempfile.mkdtemp(prefix="mysql_visual_explain_cli")

    def make_file(self, json_file: str, output_ext: str) -> tuple[str, str]:
        json_path = pathlib.Path(json_file)
        ref_file = os.path.join("reference", f"{json_path.stem}.{output_ext}")
        assert os.path.exists(ref_file)
        output_file = os.path.join(self.output_dir, f"{json_path.stem}.{output_ext}")
        subprocess.run([sys.executable, PYZ_BIN, json_file, output_file], check=True)
        assert os.path.exists(output_file)
        return (output_file, ref_file)

    def setup_class(self):
        assert os.path.exists(PYZ_BIN)

    def test_png_image(self, json_file: str):
        (output_file, ref_file) = self.make_file(json_file, "png")
        diff = compare_png(output_file, ref_file)
        assert diff < 0.1

    def test_svg_image(self, json_file: str):
        (output_file, ref_file) = self.make_file(json_file, "svg")
        diff = compare_svg(output_file, ref_file)
        assert diff < 0.1
