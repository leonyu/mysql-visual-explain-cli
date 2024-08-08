import subprocess
import json

import pytest

from .test_utils import InvocationType, render

@pytest.mark.parametrize("invoke_type,infile,exception", [
    (InvocationType.CLI, "./fixtures/negative/empty_file.json", subprocess.CalledProcessError),
    (InvocationType.CLI, "./fixtures/negative/empty_json.json", subprocess.CalledProcessError),
    (InvocationType.CLI, "./fixtures/negative/empty_json_array.json", subprocess.CalledProcessError),
    (InvocationType.CLI, "./fixtures/negative/empty_query_block.json", subprocess.CalledProcessError),
    (InvocationType.CLI, "./fixtures/negative/bad_query_block.json", subprocess.CalledProcessError),
    (InvocationType.CODE, "./fixtures/negative/empty_file.json", json.decoder.JSONDecodeError),
    (InvocationType.CODE, "./fixtures/negative/empty_json.json", ValueError),
    (InvocationType.CODE, "./fixtures/negative/empty_json_array.json", ValueError),
    (InvocationType.CODE, "./fixtures/negative/empty_query_block.json", ValueError),
    (InvocationType.CODE, "./fixtures/negative/bad_query_block.json", ValueError),
])
class TestClass:
    def test_error(self, invoke_type: InvocationType, infile: str, exception: type):
        with pytest.raises(exception):
            render(invoke_type, infile, "/dev/null")
