import os
from ..utils import get_file_list_stream_batch, producer_typer
from typing import Iterator
import json


def json_reader(file_path: os.PathLike, **kwargs):
    with open(file_path, "r", encoding="utf-8") as reader:
        json_line = json.load(fp=reader, **kwargs)
    return json_line


@producer_typer
def producer(root_dir: os.PathLike, **kwargs):
    pass
