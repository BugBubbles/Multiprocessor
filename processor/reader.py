import os
from ..utils import generator_batch, producer_typer, get_file_list_stream_id
from typing import Generator, Dict, Tuple, Iterable
import json


@producer_typer
def producer(
    id_proc: int,
    file_dir: os.PathLike,
    file_suffix: str,
    num_proc: int = 1,
    batch_size: int = 300,
    **kwargs,
) -> Generator[Iterable[Tuple[Dict, str]], Iterable, Iterable]:
    """
    multiple processing supported producer, to produce a batch of JSON string from files.
    """
    try:
        input_file_path_list = kwargs.pop("input_file_path_list")
    except:
        input_file_path_list = None
    file_path_generator = get_file_list_stream_id(
        file_dir=file_dir,
        file_suffix=file_suffix,
        id_proc=id_proc,
        num_proc=num_proc,
        input_file_path_list=input_file_path_list,
    )

    def json_reader(file_path: os.PathLike) -> Tuple[Dict, str]:
        with open(file_path, "r", encoding="utf-8") as reader:
            json_line = json.load(fp=reader)
            metadata = json_line["meta"]
        return metadata, file_path

    yield from generator_batch(
        map(json_reader, file_path_generator), batch_size=batch_size
    )


if __name__ == "__main__":
    test_dir = "/dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu"
    num_proc = 4
    for id_proc in range(num_proc):
        i = 0
        gen = producer(
            id_proc=id_proc, file_dir=test_dir, num_proc=num_proc, file_suffix=".json"
        )
        print(f"Now is {gen.__name__}:{gen.gi_frame.f_locals}:")
        for parts in gen:
            if i > 10:
                break
            i += 1
            print(*parts)
        print("=" * 20)
