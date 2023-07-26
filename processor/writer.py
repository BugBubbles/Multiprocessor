import os
from ..utils import consumer_typer, jaccard_similar, hard_similar
from typing import Any, Dict, Tuple, Iterable
import time
import json
import tqdm

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
    "历史穿越",
]
re_flag = "|".join(map(lambda x: f"(.*{x}.*)", FICTION))


class BookCategoryBase:
    def __init__(self, **kwargs) -> None:
        pass

    @property
    def output_dir(self) -> os.PathLike:
        return self.output_dir

    # def __setattr__(self, __dirname: str, __dir: os.PathLike):
    #     if not os.path.exists(__dir):
    #         os.mkdir(__dir)
    #     self.__dict__[f"__{__dirname}"] = __dir

    # def __getattr__(self, __dirname: str):
    #     return self.__dict__[f"__{__dirname}"]


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


# def consume_initializer(output_dir:os.PathLike,id_proc:int,suffix:str):


# @consumer_typer
def consumer(
    data_ships: Iterable[Tuple[os.PathLike]],
    id_proc: int,
    output_dir: os.PathLike,
    suffix: str = "_time_" + time.strftime("%Y%m%d%H%M%S"),
    **kwargs,
):
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

    for item in tqdm.tqdm(map(json_reader, data_ships),desc='Determine the categories'):
        metadata, file_path = item

        category_path = meta_parse(metadata, file_path)
        with open(category_path, "a", encoding="utf-8") as writer:
            # 把分类结果写入对应的行中
            print(file_path, file=writer, flush=True)
