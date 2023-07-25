import os
from ..utils import get_file_list_stream_batch
from typing import Iterator
import json


def json_reader(file_path: os.PathLike, **kwargs):
    with open(file_path, "r", encoding="utf-8") as reader:
        json_line = json.load(fp=reader, **kwargs)
    return json_line

def producer(root_dir:os.PathLike,**kwargs):
    