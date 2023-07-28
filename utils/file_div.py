import os
from typing import List, Any, Optional, Generator, Iterable
import tqdm
import itertools


def _get_balanced_part_nums(total, part_size):
    base = total // part_size
    remainder = total % part_size
    return [base + int(i < remainder) for i in range(part_size)]


def _balanced_ranges(total, part_size):
    balanced_part_nums = _get_balanced_part_nums(total, part_size)
    ranges = []
    start = 0
    for part_num in balanced_part_nums:
        end = start + part_num
        ranges.append((start, end))
        start = end
    return ranges


def split_list(file_list: List[Any], n: int, i: int) -> List[Any]:
    """
    with the total `n` nodes worker setting, return the distributed files for worker indexing at `i` .
    """
    ranges = _balanced_ranges(len(file_list), n)
    start, end = ranges[i]
    return file_list[start:end]


def get_file_list(
    file_dir: os.PathLike, file_suffix: str, input_file_path_list: Optional[str] = None
) -> List[os.PathLike]:
    """
    ### Arguments:
     - `file_dir` : the root directory of whole files
     - `file_suffix` : each files' suffix, for example '.docx'
     - `input_file_path_list` : a list of completely mapped file paths to the files
    """
    file_list = []
    if input_file_path_list == None:
        for f_dir, _, f_list in tqdm.tqdm(
            os.walk(file_dir), desc="fetch file path", unit="it"
        ):
            for f in f_list:
                if f.endswith(file_suffix):
                    file_list.append(os.path.join(f_dir, f))
    else:
        for f in input_file_path_list.split(","):
            if f.endswith(file_suffix):
                file_list.append(f)
    return file_list


def get_file_list_stream(
    file_dir: os.PathLike,
    file_suffix: str,
    input_file_path_list: Optional[List[str]] = None,
) -> Generator[os.PathLike, Any, Any]:
    """
    scan the whole file by a streaming process to save computer resource.
    ### Arguments:
     - `file_dir` : the root directory of whole files
     - `file_suffix` : each files' suffix, for example '.docx'
     - `input_file_path_list` : a list of completely mapped file paths to the files
    """
    if input_file_path_list == None:
        for f_dir, _, f_list in tqdm.tqdm(
            os.walk(file_dir), desc="fetch file path", unit="it"
        ):
            for f in f_list:
                if f.endswith(file_suffix):
                    yield os.path.join(f_dir, f)
    else:
        for sub_file in input_file_path_list:
            yield from get_file_list_stream(sub_file, file_suffix)


def generator_batch(
    generator: Iterable[Any],
    batch_size: Optional[int] = 300,
) -> Generator[Iterable, Iterable, Iterable]:
    """
    scan the whole file by a streaming process to save computer resource, yield batches by customized size.
    ### Arguments:
     - `file_dir` : the root directory of whole files
     - `file_suffix` : each files' suffix, for example '.docx'
     - `batch_size` : the customizable batch size for user.
     - `input_file_path_list` : a list of completely mapped file paths to the files
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least one")
    it = iter(generator)
    while batch := list(itertools.islice(it, batch_size)):
        yield batch


def get_file_list_stream_id(
    file_dir: os.PathLike,
    file_suffix: str,
    id_proc: int = 0,
    num_proc: int = 1,
    input_file_path_list: Optional[List[str]] = None,
) -> Generator[os.PathLike, Any, Any]:
    """
    get file paths from a specified file directory, spliting to several threads of generator in accordence with `id_proc` and `total_num` arguments.
    ### Arguments:
     - `file_dir` : the root directory of whole files
     - `file_suffix` : each files' suffix, for example '.docx'
     - `id_proc` : contemporary index of generator.
     - `num_proc` : total number of generators.
     - `input_file_path_list` : a list of completely mapped file paths to the files
    """
    yield from itertools.islice(
        get_file_list_stream(file_dir, file_suffix, input_file_path_list),
        id_proc,
        None,
        num_proc,
    )


if __name__ == "__main__":
    # test_dir = "/dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu/"
    test_dir = "/workspace/tmp"
    num_proc = 4
    gens = [
        get_file_list_stream_id(test_dir, ".jsonl", id_proc, num_proc)
        for id_proc in range(num_proc)
    ]
    for gen in gens:
        print(f"this is thread {gen.__name__}:{gen.gi_frame.f_locals}")
        lines = [line for line in gen]
        print(*lines)
