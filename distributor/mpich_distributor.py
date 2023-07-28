from typing import Any, Callable, List

from Multiprocessor.executor import Executor
from ..utils.type_collector import DataShips
from .distributor import DistributorBase
from mpi4py import MPI as mpi


class MpichDistributor(DistributorBase):
    """
    Multiple nodes executor based on mpich software. Distribute several enclosed and executable funtions to different machines, paralleling their processing. By the way, the enclosed functions should use this Operation System independently and process without connection as much as them can. Any information transmission is deprecated.
    """

    def __init__(self, *exec_args, **exec_kwargs) -> None:
        super().__init__(*exec_args, **exec_kwargs)

    def __call__(self, arg_call, *fn_args, **fn_kwargs):
        return super().__call__(arg_call, *fn_args, **fn_kwargs)

    def load_divider(
        self, divider: Callable[[List[Any], int, Any], List[Any]], **divider_kwargs
    ):
        return super().load_divider(divider, **divider_kwargs)

    def load_executor(self, executor: Executor, **executor_kwargs) -> None:
        return super().load_executor(executor, **executor_kwargs)
