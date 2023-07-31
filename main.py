from Multiprocessor.processor import producer, consumer
import argparse
import warnings
import os


def sinprocessor(
    input_file_path_list,
    *,
    file_dir,
    file_suffix,
    is_debug,
    output_dir,
    ip_proc=0,
    **kwargs,
):
    """这是已经被分割后的list：`input_file_path_list`"""
    from Multiprocessor.executor.single_executor import (
        SingleExecutor as single_executor,
    )

    with single_executor() as worker:
        worker.load_producer(
            producer=producer,
            file_dir=file_dir,
            file_suffix=file_suffix,
            is_debug=is_debug,
            input_file_path_list=input_file_path_list,
            ip_proc=ip_proc,
        )
        worker.load_consumer(
            consumer=consumer, output_dir=output_dir, is_debug=is_debug, ip_proc=ip_proc
        )
        worker()


def multiprocessor(
    input_file_path_list,
    *,
    file_dir,
    num_consumer,
    num_producer,
    max_size,
    file_suffix,
    cache_size,
    is_debug,
    output_dir,
    ip_proc=0,
    **kwargs,
):
    from Multiprocessor.executor.multiple_executor import (
        MultipleExecutor as multi_executor,
    )

    print(input_file_path_list)
    try:
        assert num_consumer and num_producer and max_size
    except:
        warnings.warn(
            "No num_consumer, num_producer or max_size arguments is found, using the default value",
            DeprecationWarning,
        )
    with multi_executor(
        num_producer=num_producer,
        num_consumer=num_consumer,
        max_size=max_size,
    ) as worker:
        worker.load_producer(
            producer=producer,
            file_dir=file_dir,
            file_suffix=file_suffix,
            batch_size=cache_size,
            input_file_path_list=input_file_path_list,
            is_debug=is_debug,
            ip_proc=ip_proc,
        )
        # 此处消费者函数可以省略输入文件，多进程管理器内部进行装载
        worker.load_consumer(
            consumer=consumer, output_dir=output_dir, is_debug=is_debug, ip_proc=ip_proc
        )
        worker()


def get_args() -> argparse.Namespace:
    parse = argparse.ArgumentParser()
    parse.add_argument("--file_dir", "-f", type=str)
    parse.add_argument("--output_dir", "-o", type=str)
    parse.add_argument(
        "--mpi",
        type=int,
        default=None,
        help="multiprocessing method used to process parallelly in different nodes by mpich tools",
    )
    parse.add_argument(
        "--cache_dir",
        "-c",
        type=str,
        help="Where cache files to be stored in and after the whole process they will be removed.",
    )
    parse.add_argument(
        "--file_suffix",
        "-fs",
        type=str,
        default="docx",
        help="The specific files format suffix to be processed",
    )
    parse.add_argument(
        "--multiple_enable",
        "-me",
        action="store_true",
        help="Enable a multiple processing programme.",
    )
    parse.add_argument(
        "--is_debug",
        action="store_true",
        help="Enable a debug supported mode for multiple processing programme.",
    )
    parse.add_argument(
        "--num_producer",
        "-np",
        type=int,
        default=10,
        help="The number of producer processor coresponded to a single consumer.",
    )
    parse.add_argument(
        "--num_consumer",
        "-nc",
        type=int,
        default=10,
        help="The number of consumer processor coresponded to a single producer.",
    )
    parse.add_argument(
        "--max_size",
        "-ms",
        type=int,
        default=300,
        help="The number of shared quene cache size of items for multiple processing programme.",
    )
    parse.add_argument(
        "--cache_size",
        "-cs",
        type=int,
        default=300,
        help="The number of single itom in each item for writer to use.",
    )
    args = parse.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    try:
        assert args.file_dir and args.output_dir
    except:
        raise AttributeError(
            "No file_dir or output_dir is specified. Please check your input command line for '-f' and '-o' arguments."
        )
    file_dir = args.__dict__.pop("file_dir")
    file_list = [
        os.path.join(file_dir, file_name) for file_name in os.listdir(file_dir)
    ]
    if not args.mpi:
        if not args.multiple_enable:
            sinprocessor(
                file_dir=file_dir, input_file_path_list=file_list, **args.__dict__
            )
        else:
            multiprocessor(
                file_dir=file_dir, input_file_path_list=file_list, **args.__dict__
            )
    else:
        from Multiprocessor.distributor import MpichDistributor as mpich_distributor
        import itertools
        from random import shuffle

        def div_func(file_paths, num_part: int, shuf: bool = False):
            """
            The `file_paths` must be finitely iterable, so you should load it into the memory instead of a generator.
            """

            def split_list(data_list, num_part):
                now_sum_size = len(data_list)
                now_size = now_sum_size // num_part
                now_res = now_sum_size % num_part
                if now_res != 0:
                    now_size += 1
                it = iter(data_list)
                while batch := list(itertools.islice(it, now_size)):
                    now_sum_size = len(data_list)
                    now_size = now_sum_size // num_part
                    now_res = now_sum_size % num_part
                    if now_res != 0:
                        now_size += 1

                    yield batch

            if shuf:
                file_paths = shuffle(file_paths)
            return [file_splits for file_splits in split_list(file_paths, num_part)]

        if not args.multiple_enable:
            mpich_distributor.run(
                sinprocessor,
                file_list,
                div_funcs=[div_func],
                file_dir=file_dir,
                **args.__dict__,
            )
        else:
            mpich_distributor.run(
                multiprocessor,
                file_list,
                div_funcs=[div_func],
                file_dir=file_dir,
                **args.__dict__,
            )
