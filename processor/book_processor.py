from ..utils import generator_batch, get_file_list_stream_id
from typing import Generator, Dict, Tuple, Iterable, Any, List
from ..utils.type_collector import DataShips
from ..debugger import producer_typer, consumer_typer
import os
from ..utils import jaccard_similar, hard_similar
import time
import json
import tqdm

"""
The base format for multiple processor, it at least include two kinds of functions -- producer and consumer, however you can define more complicated models. To use this multiple processor, please define your processor by inherit from this `ProcessorBase`.
### Examples:
>>> class MyProcessor(ProcessorBase):

>>>   def producer(
          id_proc: int,
          num_proc: int = 1,
          file_dir: os.PathLike,
          file_suffix: str,
          batch_size: int = 300,
          **kwargs,
          ) -> Generator[Iterable[Tuple[Dict, str]], Iterable, Iterable]:
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
          yield from generator_batch(file_path_generator, batch_size=batch_size)

>>>   def consumer(
        data_ships: Iterable[Tuple[os.PathLike]],
        id_proc: int,
        output_dir: os.PathLike,
        suffix: str = "_time_" + time.strftime("%Y%m%d%H%M%S"),
        **kwargs,
    ):
        category = Books(output_dir=output_dir, id_proc=id_proc, suffix=suffix)
        def meta_parse(metadata: Dict, file_path: os.PathLike) -> os.PathLike:
            check_vals = set(metadata.values())
            check_vals.add(os.path.basename(file_path))
            if hard_similar(re_flag, "".join(map(lambda x: f"{x}", check_vals))):
                return category.fiction
            else:
                return category.nonfiction
        def json_reader(file_path: os.PathLike) -> Tuple[Dict, str]:
            with open(file_path, "r", encoding="utf-8") as reader:
                json_line = json.load(fp=reader)
                metadata = json_line["meta"]
            return metadata, file_path
        for item in tqdm.tqdm(
            map(json_reader, data_ships), desc="Determine the categories"
        ):
            metadata, file_path = item
            category_path = meta_parse(metadata, file_path)
            with open(category_path, "a", encoding="utf-8") as writer:
                print(file_path, file=writer, flush=True)
"""


def producer(
    id_proc: int,
    file_dir: os.PathLike,
    file_suffix: str,
    num_proc: int,
    batch_size: int = 300,
    is_debug: bool = False,
    input_file_path_list: List = None,
    *args,
    **kwargs,
):
    @producer_typer(is_debug=is_debug)
    def produce_main(
        id_proc: int,
        file_dir: os.PathLike,
        file_suffix: str,
        num_proc: int,
        batch_size: int,
        input_file_path_list: List = None,
        *args,
        **kwargs,
    ) -> Generator[Iterable[Tuple[Dict, str]], Iterable, Iterable]:
        """
        The main function for producer.
        #### Explicitly NEEDED Arguments:
        - `id_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! The index of certain producer processor, it is an open API for practical applying. Of course that ignore it can be a valid usage.
        - `num_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! The total amount number of producer processors, it is an open API for practical applying. Of course that ignore it can be a valid usage.
        #### Optionally NEEDED Arguments:
        - 'iter_deco' : a decorator for each producer visualize iteration process.
        """
        file_path_generator = get_file_list_stream_id(
            file_dir=file_dir,
            file_suffix=file_suffix,
            id_proc=id_proc,
            num_proc=num_proc,
            input_file_path_list=input_file_path_list,
        )

        yield from generator_batch(file_path_generator, batch_size=batch_size)

    return produce_main(
        id_proc=id_proc,
        num_proc=num_proc,
        file_dir=file_dir,
        file_suffix=file_suffix,
        batch_size=batch_size,
        input_file_path_list=input_file_path_list,
        *args,
        **kwargs,
    )


class BookCategory(str):
    pass


FICTION = [
    "小说",
    "纯美",
    "漫画",
    "科幻",
    "最近更新",  # 主要是网络小说
    "推理",
    "第.部分",  # 主要是连载小说，部分不是小说
    "爆笑",
    "搞笑",
    "都市言情",
    "文学",  # 包括了古典文学和现代文学、当代文学
    "童话",
    "名著",  # 大多是经典小说散文，计划再次细分
    "致纯书苑",
    "穿越",
    "青春校园",
    "武侠",
    "金庸",
    "玄幻",
    "重生",
    "宠文",
    "火影忍者",
    "完结",
    "番外",
    "鬼吹灯",
    "东野圭吾",
    "甜文",
    "青春校园",
    "村上春树",
]
re_flag = "|".join(map(lambda x: f"(.*{x}.*)", FICTION))


class BookCategoryBase:
    def __init__(self, **kwargs) -> None:
        pass

    @property
    def output_dir(self) -> os.PathLike:
        return self.output_dir


class Books(BookCategoryBase):
    def __init__(self, output_dir: os.PathLike, id_proc: int, suffix: str) -> None:
        self._output_dir = output_dir
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        self._fiction = os.path.join(output_dir, "fiction")
        if not os.path.exists(self._fiction):
            os.mkdir(self._fiction)
        self._nonfiction = os.path.join(output_dir, "nonfiction")
        if not os.path.exists(self._nonfiction):
            os.mkdir(self._nonfiction)
        self._fiction = os.path.join(
            output_dir, "fiction", f"book_worker_{id_proc:03d}{suffix}.txt"
        )
        self._nonfiction = os.path.join(
            output_dir, "nonfiction", f"book_worker_{id_proc:03d}{suffix}.txt"
        )

    @property
    def fiction(self) -> os.PathLike:
        return self._fiction

    @property
    def nonfiction(self) -> os.PathLike:
        return self._nonfiction


def consumer(
    data_ships: Iterable[Tuple[os.PathLike]],
    id_proc: int,
    output_dir: os.PathLike,
    num_proc: int,
    suffix: str = "_time_" + time.strftime("%Y%m%d%H%M%S"),
    is_debug: bool = False,
    **kwargs,
):
    @consumer_typer(is_debug=is_debug)
    def consume_main(
        data_ships: Iterable[Tuple[os.PathLike]],
        id_proc: int,
        output_dir: os.PathLike,
        num_proc: int,
        suffix: str,
        **kwargs,
    ):
        """
        The main function for consumer.
        #### Explicitly NEEDED Arguments:
         - `data_ships` : A `mutiprocessing.Manager` supported type for data sharing.
         - `id_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! the index of certain producer processor, it is an open API for practical applying. Of course that ignore it can be a valid usage.
         - `num_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! the total amount number of producer processors, it is an open API for practical applying. Of course that ignore it can be a valid usage.
        #### Optionally NEEDED Arguments:
         - 'iter_deco' : a decorator for each consumer visualize iteration process.
        """
        category = Books(output_dir=output_dir, id_proc=id_proc, suffix=suffix)

        def meta_parse(metadata: Dict, file_path: os.PathLike) -> os.PathLike:
            # parse the metadata, TODO the suffix is much deserved to utilized
            # 目前只需要二分类就好了，只用最原始的匹配方法，后面的分类方法再说，分类方法考虑编码
            check_vals = set(metadata.values())
            check_vals.add(os.path.basename(file_path))
            if hard_similar(re_flag, "".join(map(lambda x: f"{x}", check_vals))):
                return category.fiction
            else:
                return category.nonfiction

        def json_reader(file_path: os.PathLike) -> Tuple[Dict, str]:
            with open(file_path, "r", encoding="utf-8") as reader:
                json_line = json.load(fp=reader)
                metadata = json_line["meta"]
            return metadata, file_path

        for item in tqdm.tqdm(
            map(json_reader, data_ships), desc="Determine the categories"
        ):
            metadata, file_path = item

            category_path = meta_parse(metadata, file_path)
            with open(category_path, "a", encoding="utf-8") as writer:
                print(file_path, file=writer, flush=True)

    return consume_main(
        data_ships=data_ships,
        id_proc=id_proc,
        num_proc=num_proc,
        output_dir=output_dir,
        suffix=suffix,
        **kwargs,
    )
