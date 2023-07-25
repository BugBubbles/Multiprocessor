from ..utils import get_file_list_stream_batch
import os
from typing import List


def test_dataset(
    file_dir: os.PathLike,
    file_suffix: str,
    input_file_path_list: List[os.PathLike],
    test_size: int,
):
    """
    obtain a samll batch of input data to test the producer and consumer whether is valid or not.
    ### Arguments:
     - `file_dir` : the input file storage path.
     - `file_suffix` : files suffix.
     - `input_file_path_list` : the whole paths to files, stored in a list.
     - `test_size` : the test data batch size for user.
    """
    for test_data in get_file_list_stream_batch(
        file_dir, file_suffix, input_file_path_list, batch_size=test_size
    ):
        if test_data:
            break
    return test_data
