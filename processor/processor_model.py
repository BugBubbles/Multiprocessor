# 可以像搭一个神经网络一样搭一个多进程程序，也要注意搭得太多了，反而会影响效率，两层就足够应付大多数情况了
from typing import Any
from ..utils.type_collector import DataShips
from ..debugger import producer_typer, consumer_typer


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


def producer(id_proc: int, num_proc: int, is_debug: bool = False, *args, **kwargs):
    @producer_typer(is_debug=is_debug)
    def produce_main(id_proc: int, num_proc: int, *args, **kwargs) -> DataShips:
        """
        The main function for producer.
        #### Explicitly NEEDED Arguments:
         - `id_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! The index of certain producer processor, it is an open API for practical applying. Of course that ignore it can be a valid usage.
         - `num_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! The total amount number of producer processors, it is an open API for practical applying. Of course that ignore it can be a valid usage.
        #### Optionally NEEDED Arguments:
         - 'iter_deco' : a decorator for each producer visualize iteration process.
        """
        raise NotImplementedError

    return produce_main(id_proc=id_proc, num_proc=num_proc, *args, **kwargs)


def consumer(
    data_ships: DataShips, id_proc: int, num_proc: int, is_debug: bool = False, **kwargs
):
    @consumer_typer(is_debug=is_debug)
    def consume_main(
        data_ships: DataShips, id_proc: int, num_proc: int, **kwargs
    ) -> Any:
        """
        The main function for consumer.
        #### Explicitly NEEDED Arguments:
         - `data_ships` : A `mutiprocessing.Manager` supported type for data sharing.
         - `id_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! the index of certain producer processor, it is an open API for practical applying. Of course that ignore it can be a valid usage.
         - `num_proc` : (TODO) MUST INCLUDE this API in you producer DEFINATION!!! the total amount number of producer processors, it is an open API for practical applying. Of course that ignore it can be a valid usage.
        #### Optionally NEEDED Arguments:
         - 'iter_deco' : a decorator for each consumer visualize iteration process.
        """
        raise NotImplementedError

    return consume_main(
        data_ships=data_ships, id_proc=id_proc, num_proc=num_proc, **kwargs
    )
