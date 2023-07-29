from typing import Any, Callable, List, Optional
from .distributor import DistributorBase
from mpi4py import MPI as mpi


class MpichDistributor(DistributorBase):
    """
    Multiple nodes executor based on mpich software. Distribute several enclosed and executable funtions to different machines, paralleling their processing. By the way, the enclosed functions should use this Operation System independently and process without connection as much as them can. Any information transmission is deprecated.
    """

    def __init__(self, **executor_init_kwargs) -> None:
        self.comm = mpi.COMM_WORLD
        self.size = self.comm.Get_size()
        self._executor_init_kwargs = executor_init_kwargs

    @staticmethod
    def __call__(
        call_func: Callable[[List[Any], Any], Any],
        *distributable_args: List,
        **fn_kwargs,
    ):
        comm = mpi.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        for distributable_arg in distributable_args:
            try:
                assert len(distributable_arg) == size
            except:
                raise AttributeError(
                    f"{distributable_arg.__name__} cannot be distributed into {size} nodes."
                )
        distributed_args = list(
            comm.scatter(distributable_arg, root=0)
            for distributable_arg in distributable_args
        )
        distributed_output = call_func(*distributed_args, **fn_kwargs)
        gathered_output = comm.gather(distributed_output, root=0)
        if rank == 0:
            print(
                ">" * 10
                + "\n This is host machine with callback being finished \n"
                + "<" * 10
            )
            return gathered_output
        else:
            print(
                ">" * 10
                + "\n This is subordinary machine with callback being finished \n"
                + "<" * 10
            )
            return

    # def run(
    #     self,
    #     *distributable_args,
    #     num_node: Optional[int] = None,
    #     **non_distributable_kwargs,
    # ):
    #     super().run()
    #     num_node = num_node if num_node or self.size > num_node else self.size
    #     rank = self.comm.Get_rank()
    #     distributed_args = list(
    #         self.comm.scatter(divider(distributable_arg, rank), root=0)
    #         for distributable_arg, divider in zip(distributable_args, self.divider)
    #     )
    #     # initialize the executor using initialization arguments
    #     executor = self.executor(**self.executor_init_kwargs)
    #     # now we get a Executor instance
    #     # TODO how to load this two functions? Pass the arguments?
    #     executor.load_producer()
    #     executor.load_consumer()
