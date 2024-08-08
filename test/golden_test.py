import glob
import os
import pathlib
import tempfile

import pytest

from .test_utils import InvocationType, render, compare_images


@pytest.mark.parametrize("invoke_type", [InvocationType.CODE, InvocationType.CLI])
@pytest.mark.parametrize("json_file", glob.glob("./fixtures/json/*.json"))
@pytest.mark.parametrize("image_ext", [".png", ".svg"])
class TestClass:
    output_dir = tempfile.mkdtemp(prefix="mysql_visual_explain_cli")

    def make_file(
        self,
        invoke_type: InvocationType,
        json_file: str,
        output_ext: str,
    ) -> tuple[str, str]:
        json_path = pathlib.Path(json_file)
        ref_file = os.path.join("fixtures/golden", f"{json_path.stem}{output_ext}")
        assert os.path.exists(ref_file)
        output_file = os.path.join(self.output_dir, f"{json_path.stem}{output_ext}")
        render(invoke_type, json_file, output_file)
        assert os.path.exists(output_file)
        return (output_file, ref_file)

    def test_image(self, invoke_type: InvocationType, json_file: str, image_ext: str):
        (output_file, ref_file) = self.make_file(invoke_type, json_file, image_ext)
        diff = compare_images(output_file, ref_file)
        assert diff < 0.1
