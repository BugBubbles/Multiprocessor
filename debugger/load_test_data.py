from ..utils import generator_batch, get_file_list_stream_id
import os
from typing import List, Any


def test_dataset(
    file_dir: os.PathLike,
    file_suffix: str,
    input_file_path_list: List[os.PathLike],
    test_size: int,
    id_proc: int = 1,
    num_proc: int = 1,
    **kwargs
) -> Any:
    """
    obtain a samll batch of input data to test the producer and consumer whether is valid or not.
    ### Arguments:
     - `file_dir` : the input file storage path.
     - `file_suffix` : files suffix.
     - `input_file_path_list` : the whole paths to files, stored in a list.
     - `test_size` : the test data batch size for user.
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
    for test_data in generator_batch(
        generator=file_path_generator, batch_size=test_size
    ):
        if test_data:
            break
    return test_data
