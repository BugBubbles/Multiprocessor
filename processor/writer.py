import os
from ..utils import consumer_typer
from typing import Any, Dict, Tuple, Iterable

# import re


class BookCategory(str):
    pass


E_FICTION = ["修仙", "", "", ""]


class BookCategoryBase:
    def __init__(self) -> None:
        pass

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value

    def __getattr__(self, __name: str):
        return self.__dict__[__name]


class Fictions(BookCategoryBase):
    def __init__(self) -> None:
        self["修仙"] = ""
        self["test"] = ""


class NonFictions(BookCategoryBase):
    def __init__(self) -> None:
        super().__init__()


@consumer_typer
def consumer(
    data_ships: Iterable[Tuple[Dict, str]],
    id_proc: int,
    output_dir: os.PathLike,
    suffix: str = None,
    **kwargs,
):
    suffix = suffix if suffix else ""
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, f"shiti_worker_{id_proc:03d}{suffix}.jsonl")

    def meta_parse(metadata: Dict, file_path: os.PathLike) -> BookCategory:
        # parse the metadata, TODO the suffix is much deserved to utilized
        for val in metadata.values():
            pass

    for metadata, raw_file_path in data_ships:
        with open(output_path, "a", encoding="utf-8") as writer:
            # print()
            meta_parse(metadata, raw_file_path)
