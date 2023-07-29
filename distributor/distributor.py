from typing import Any, Callable, List, Tuple
import traceback
from ..executor import Executor


class DistributorBase:
    # def __init__(self, *dist_args, **dist_kwargs) -> None:
    #     pass

    @staticmethod
    def __call__(
        call_func: Callable[[List[Any], Any], Any],
        *distributable_args: List,
        **fn_kwargs,
    ):
        """
        Using a mpich executor to callback `call_func` function in paralleled processing nodes.
        ### Arguments:
         - `call_func` : A callable function that accept at least one list like arguments.
         - `distributable_args` : serializable and position arguments, you should pre-divide these arguments and store them in different `list` like variables (`numpy.ndarray`, `Set`, `Tuple` and `dict` are also supported, all the supported types you can use are now being presented in https://mpi4py.readthedocs.io/en/stable/tutorial.html)
         - `fn_kwargs` : `call_func` keyword arguments.
        ### Usage
        You can use this method without instance this `Distributor` class, the final output will be gather into the root machine (rank = 0).
        """
        raise NotImplementedError

    @staticmethod
    def run(
        call_func: Callable[[List[Any], Any], Any],
        *distributable_args: List,
        **fn_kwargs,
    ):
        """
        Using a mpich executor to callback `call_func` function in paralleled processing nodes.
        ### Arguments:
         - `call_func` : A callable function that accept at least one list like arguments.
         - `distributable_args` : serializable and position arguments, you should pre-divide these arguments and store them in different `list` like variables (`numpy.ndarray`, `Set`, `Tuple` and `dict` are also supported, all the supported types you can use are now being presented in https://mpi4py.readthedocs.io/en/stable/tutorial.html)
         - `fn_kwargs` : `call_func` keyword arguments.
        ### Usage
        You can use this method without instance this `Distributor` class, the final output will be gather into the root machine (rank = 0).
        """
        raise NotImplementedError

    def __enter__(self):
        """support for context manager for `with ... as`"""
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type or exc_value or exc_tb:
            traceback.format_exception(etype=exc_type, value=exc_value, tb=exc_tb)
        else:
            print(
                "========== The whole DISTRIBUTED processing has successfully finished! =========="
            )
        return

    def load_executor(
        self, executor_instance: Executor, **executor_init_kwargs
    ) -> None:
        """
        Load an object-like executor (NOT an instance one) to distribute into multiple nodes.
        ### Arguments:
         - `executor` : A executor class module for distributed programme. That means it can independently execute in one machine. You must reload it before your distributor runs.
        """
        self.executor_instance = executor_instance
        self._executor_init_kwargs = executor_init_kwargs
        return

    def load_divider(
        self,
        *divider: Tuple[Callable[[List[Any], int, Any], List[Any]]],
        **divider_kwargs,
    ):
        """
        Set MPI communication divider function and its arguments, this function will instance a function that divide (maybe not a equivalent division) input arguments in accordence with the amont of clusters or nodes. Warning! You MUST include a keyword argument called `num_part` in your customized divider function! However, you may not need to include this arguments in divider_kwargs, mpich manager will auto-decide its value using mpi4py API.
        ### Arguments:
         - `divider` : divider like function, you can load more than one divider by position arguments, each divider is corespondent to one key word arguments.
         - `divider_kwargs` : divider function arguments, dictionary like, noted that you should include the definition of `num_part`. However, this arguments is not that need to be distributed.
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
            MyMpiExe.load_mpi_divider(my_divider, shuf=True) # Here is not a explicit distributable argument.

        ### Warning:
        If you have more than one arguments needed to be distributed, you should load a LIST of divider function objects and their corespondent keyword arguments instead of a single one.
        """
        self.divider = divider
        self._divider_kwargs = divider_kwargs
        return

    @property
    def divider_kwargs(self):
        return self._divider_kwargs

    @property
    def executor_init_kwargs(self):
        return self._executor_init_kwargs


class Distributor(DistributorBase):
    pass
