import os
import subprocess
import tempfile
import glob
import sys
from pathlib import Path

from PIL import Image, ImageChops
import numpy as np
import pytest
from cairosvg import svg2png


def compare_png(png1: str, png2: str) -> float:
    image1 = Image.open(png1)
    image2 = Image.open(png2)
    diff = ImageChops.difference(image1, image2)
    (width1, height1) = image1.size
    (width2, height2) = image2.size
    return (
        2
        * np.asarray(diff, dtype="int32").sum()
        / (256 * (width1 * height1 + width2 * height2))
    )


def compare_svg(svg1: str, svg2: str) -> float:
    svg1_content = Path(svg1).read_text()
    svg2_content = Path(svg2).read_text()
    with tempfile.TemporaryDirectory() as tmp:
        png1 = f"{tmp}/svg1.png"
        png2 = f"{tmp}/svg2.png"
        svg2png(svg1_content, write_to=png1)
        svg2png(svg2_content, write_to=png2)
        return compare_png(png1, png2)


@pytest.mark.parametrize("json_file", glob.glob("./fixtures/*.json"))
class TestClass:
    pyz_bin = "./dist/mysql_visual_explain_cli.pyz"
    output_dir = "/tmp"

    def make_file(self, json_file: str, output_ext: str) -> tuple[str, str]:
        json_path = Path(json_file)
        ref_file = os.path.join("reference", f"{json_path.stem}.{output_ext}")
        assert os.path.exists(ref_file)
        output_file = os.path.join(self.output_dir, f"{json_path.stem}.{output_ext}")
        subprocess.run(
            [sys.executable, self.pyz_bin, json_file, output_file], check=True
        )
        assert os.path.exists(output_file)
        return (output_file, ref_file)

    def setup_class(self):
        assert os.path.exists(self.pyz_bin) == True
        self.output_dir = tempfile.mkdtemp(prefix="mysql_visual_explain_cli")

    def test_png_image(self, json_file: str):
        (output_file, ref_file) = self.make_file(json_file, "png")
        diff = compare_png(output_file, ref_file)
        assert diff < 0.1

    def test_svg_image(self, json_file: str):
        (output_file, ref_file) = self.make_file(json_file, "svg")
        diff = compare_svg(output_file, ref_file)
        assert diff < 0.65  # We need better SVG comparison
