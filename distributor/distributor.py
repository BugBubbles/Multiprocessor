from typing import Any, Callable, List
import traceback
from ..executor import Executor
class DistributorBase:
    def __init__(self, *dist_args, **dist_kwargs) -> None:
        pass

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __enter__(self):
        """support for context manager for `with ... as`"""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type or exc_value or exc_tb:
            traceback.format_exception(etype=exc_type, value=exc_value, tb=exc_tb)
        else:
            print(
                "========== The whole processing has successfully finished! =========="
            )
        return


    def load_executor(self, executor: Executor, **executor_kwargs) -> None:
        """
        Load an INSTANCED executor to distribute into multiple nodes.
        ### Arguments:
         - `executor` : A executor class module for distributed programme. That means it can independently execute in one machine. You must reload it before your distributor runs.
        """
        self.executor=executor
        self.executor_kwargs=executor_kwargs


    def load_divider(self,divider:Callable[[List[Any],int,Any],List[Any]],**divider_kwargs):
        """
        Set MPI communication divider function and its arguments, this function will instance a function that divide (maybe not a equivalent division) input arguments in accordence with the amont of clusters or nodes. Warning! You MUST include a keyword argument called `num_part` in your customized divider function! However, you may not need to include this arguments in divider_kwargs, mpich manager will auto-decide its value using mpi4py API.
        ### Arguments:
         - `divider` : divider like function.
         - `divider_kwargs` : divider function arguments, dictionary like, noted that you should include the definition of `num_part`.
        ### Examples:

        >>> import os
            from random import shuffle
            import itertools

        >>> def my_divider(file_paths: List[os.PathLike], num_part: int, shuf: bool = False):
                def split_list(file_list, num_part):
                    batch_size = len(file_list) // num_part
                    it = iter(file_list)
                    while batch := list(itertools.islice(it, batch_size)):
                        yield batch
                if shuf:
                    file_paths = shuffle(file_paths)
                return [file_splits for file_splits in split_list(file_paths, num_part)]
        
        ---------------
        When loading, use it like below:
        >>> MyMpiExe = MpichExecutor(*args, **kwargs)
            MyMpiExe.load_mpi_divider(my_divider, shuf=True)
        """
        self.divider=divider
        self._divider_kwargs=divider_kwargs
