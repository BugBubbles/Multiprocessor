from typing import Any, Callable, List, Optional
from ..executor import Executor
from .distributor import DistributorBase
from mpi4py import MPI as mpi


class MpichDistributor(DistributorBase):
    """
    Multiple nodes executor based on mpich software. Distribute several enclosed and executable funtions to different machines, paralleling their processing. By the way, the enclosed functions should use this Operation System independently and process without connection as much as them can. Any information transmission is deprecated.
    """

    def __init__(self, **dist_kwargs) -> None:
        self.comm = mpi.COMM_WORLD
        self.size = self.comm.Get_size()

    @staticmethod
    def __call__(
        call_func: Callable[[List[Any], Any], Any],
        *splitable_args: List,
        **fn_kwargs,
    ):
        return super().__call__(call_func, *splitable_args, **fn_kwargs)

    def exect_run(
        self, input_list: List, num_node: Optional[int] = None, *args, **kwargs
    ):
        try:
            assert self.divider and self.divider_kwargs
            assert self.executor and self.executor_init_kwargs
        except Exception as exc:
            print(
                exc
                + f"\n You must load divider and executor functions first, by applying function {__class__}.load_divider and {__class__}.load_executor."
            )
        num_node = (
            num_node if num_node or self.size > num_node else self.comm.Get_size()
        )
        rank = self.comm.Get_rank()
        input_splits = self.divider(input_list, rank, **self.divider_kwargs)
        # initialize the executor using initialization arguments
        executor = self.executor(**self.executor_init_kwargs)
        # now we get a Executor instance
        # TODO how to load this two functions? Pass the arguments?
        executor.load_producer()
        executor.load_consumer()
