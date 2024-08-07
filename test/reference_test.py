import enum
import glob
import io
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

from mysql_visual_explain_cli import __main__

PYZ_BIN = "./dist/mysql_visual_explain_cli.pyz"


class InvocationType(enum.Enum):
    UNKNOWN = 0
    CODE = 1
    CLI = 2


def render(invoke_type: InvocationType, infile: str, outfile: str):
    match invoke_type:
        case InvocationType.CODE:
            with io.open(infile) as file:
                __main__.render(file.read(), outfile)
        case InvocationType.CLI:
            assert os.path.exists(PYZ_BIN)
            subprocess.run([sys.executable, PYZ_BIN, infile, outfile], check=True)
        case _:
            raise ValueError(f"Invalid type: {invoke_type}")


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


def compare_images(file1: str, file2: str) -> float:
    if file1.endswith("png") and file2.endswith("png"):
        return compare_png(file1, file2)
    elif file1.endswith("svg") and file2.endswith("svg"):
        return compare_svg(file1, file2)
    else:
        raise ValueError(f"Unsupported comparison: {file1} {file2}")


@pytest.mark.parametrize("invoke_type", [InvocationType.CODE, InvocationType.CLI])
@pytest.mark.parametrize("json_file", glob.glob("./fixtures/*.json"))
@pytest.mark.parametrize("image_ext", ["png", "svg"])
class TestClass:
    output_dir = tempfile.mkdtemp(prefix="mysql_visual_explain_cli")

    def make_file(
        self,
        invoke_type: InvocationType,
        json_file: str,
        output_ext: str,
    ) -> tuple[str, str]:
        json_path = pathlib.Path(json_file)
        ref_file = os.path.join("reference", f"{json_path.stem}.{output_ext}")
        assert os.path.exists(ref_file)
        output_file = os.path.join(self.output_dir, f"{json_path.stem}.{output_ext}")
        render(invoke_type, json_file, output_file)
        assert os.path.exists(output_file)
        return (output_file, ref_file)

    def test_image(self, invoke_type: InvocationType, json_file: str, image_ext: str):
        (output_file, ref_file) = self.make_file(invoke_type, json_file, image_ext)
        diff = compare_images(output_file, ref_file)
        assert diff < 0.1
