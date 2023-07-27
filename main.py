from classify_book.executor.single_executor import SingleExecutor as single_executor
from classify_book.executor.multiple_executor import MultipleExecutor as multi_executor
from classify_book.processor import producer,consumer
import argparse
import warnings


def get_args() -> argparse.Namespace:
    parse = argparse.ArgumentParser()
    parse.add_argument("--file_dir", "-f", type=str)
    parse.add_argument("--output_dir", "-o", type=str)
    parse.add_argument(
        "--mpi",
        "-m",
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
        help="The number of cache for multiple processing programme.",
    )
    parse.add_argument(
        "--cache_size",
        "-cs",
        type=int,
        default=300,
        help="The number of cache for multiple processing programme.",
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
    file_suffix = args.file_suffix
    if not args.multiple_enable:
        # worker = single_executor()
        # worker.load_producer(producer=producer,file_suffix=file_suffix,)
        # worker.load_consumer(consumer)
        pass
    else:
        try:
            assert args.num_consumer and args.num_producer and args.max_size
        except:
            warnings.warn(
                "No num_consumer, num_producer or max_size arguments is found, using the default value",
                DeprecationWarning,
            )
        worker = multi_executor(num_producer=args.num_producer, num_consumer=args.num_consumer, max_size=args.max_size)
        worker.load_producer(
            producer=producer,
            file_dir=args.file_dir,
            file_suffix=file_suffix,
            batch_size=args.cache_size,
        )
        # 此处消费者函数可以省略输入文件，多进程管理器内部进行装载
        worker.load_consumer(
            consumer=consumer,
            output_dir=args.output_dir,
        )

        # run it
        worker()
