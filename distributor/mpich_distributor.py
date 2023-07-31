from typing import Any, Callable, List, Iterable, Dict
from .distributor import DistributorBase
from mpi4py import MPI as mpi


class MpichDistributor(DistributorBase):
    """
    Multiple nodes executor based on mpich software. Distribute several enclosed and executable funtions to different machines, paralleling their processing. By the way, the enclosed functions should use this Operation System independently and process without connection as much as them can. Any information transmission is deprecated.
    """

    @staticmethod
    def __call__(
        call_func: Callable[[List, Any], Any],
        *distributable_args: Iterable,
        div_funcs: Iterable[Callable[[Any], List]] = None,
        div_func_kwargs: Iterable[Dict] = [{}],
        **shared_kwargs,
    ):
        """
        You should load the main callable function `call_func` to execute this task. Besides, all the distributable arguments should be positional forms and the others should be in keyword forms. Optionally, the divide function can be customized to divide the distributable arguments and the divide function keyword arguments is also supported.
        ### Arguments:
         - `call_func` : callable function to execute the main task.
         - `distributable_args` : positional arguments to be distribute into multiple nodes.
         - `div_funcs` : the customized divide functions, should be in Iterable forms and optionally. Noted that you should include a keyword arguments named `num_part` to pinpoint how many part should be divided.
         - `div_func_kwargs` : the divide functions' option arguments, also should be in Iterable forms (Recommand for keyword forms and the keys are the same to function names).
         - `shared_kwargs` : the shared keyword arguments for the callable function in different subordinary machines.
        """
        comm = mpi.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        comm.Barrier()
        if not div_funcs:
            for distributable_arg in distributable_args:
                try:
                    assert len(distributable_arg) == size
                except:
                    raise AttributeError(
                        f"{distributable_arg.__name__} cannot be distributed into {size} nodes."
                    )
            distributed_args = list(
                distributable_arg[rank] for distributable_arg in distributable_args
            )
            distributed_output = call_func(
                *distributed_args, ip_proc=rank, num_ip=size, **shared_kwargs
            )
        else:
            # for customized divide functions
            distributed_args = list(
                div_func(distributable_arg, num_part=size, **div_func_kwarg)[rank]
                for distributable_arg, div_func, div_func_kwarg in zip(
                    distributable_args, div_funcs, div_func_kwargs
                )
            )
            distributed_output = call_func(
                *distributed_args, ip_proc=rank, num_ip=size, **shared_kwargs
            )
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

    @staticmethod
    def run(
        call_func: Callable[[List, Any], Any],
        *distributable_args: Iterable,
        div_funcs: Iterable[Callable[[Any], List]] = None,
        div_func_kwargs: Iterable[Dict] = [{}],
        **shared_kwargs,
    ):
        """
        You should load the main callable function `call_func` to execute this task. Besides, all the distributable arguments should be positional forms and the others should be in keyword forms. Optionally, the divide function can be customized to divide the distributable arguments and the divide function keyword arguments is also supported.
        ### Arguments:
         - `call_func` : callable function to execute the main task. The distributed processing manager provide two open API for accessing the innate variables, `num_ip` (the number of workers in your distributed system, including the master) and `ip_proc` (the index of worker which execute this thread task). Use keyword arguments to access these two API and use `**kwargs` to cache them if them are needless for you.
         - `distributable_args` : positional arguments to be distribute into multiple nodes.
         - `div_funcs` : the customized divide functions, should be in Iterable forms and optionally. Noted that you should include a keyword arguments named `num_part` to pinpoint how many part should be divided.
         - `div_func_kwargs` : the divide functions' option arguments, also should be in Iterable forms (Recommand for keyword forms and the keys are the same to function names).
         - `shared_kwargs` : the shared keyword arguments for the callable function in different subordinary machines.
        ### Examples:
        If you want to use these two open API, writing your processor like below:

        >>> def my_processor(input_names, num_proc, ip_proc, **kwargs):
                print(f"Here is the {ip_proc} worker, \\
                  the total number of workers is {num_proc}")
                for name in input_names:
                    print(f"This is {name}")
                print(f"The {ip_proc} worker has finished its works")
            MpichDistributor.run(my_processor, input_names)

        #### Noted that this parameters `input_names` should be distributable or an `AttributeError` will be raised.
        ---------
        Or if you want to deploy your customized dividers, like this examples:
        >>> def my_divider(input_names, num_part, **kwargs):
                # divide the input list into several parts according to num_part
                div = [[] for i in range(num_part)]
                for i in range(len(input_names)):
                    div[i % num_part].append(input_names[i])
                return div
            MpichDistributor.run(my_processor, input_names, my_divider)
        """
        comm = mpi.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        comm.Barrier()
        if not div_funcs:
            for distributable_arg in distributable_args:
                try:
                    assert len(distributable_arg) == size
                except:
                    raise AttributeError(
                        f"{distributable_arg.__name__} cannot be distributed into {size} nodes."
                    )
            distributed_args = list(
                distributable_arg[rank] for distributable_arg in distributable_args
            )
            distributed_output = call_func(
                *distributed_args, ip_proc=rank, num_ip=size, **shared_kwargs
            )
        else:
            # for customized divide functions
            distributed_args = list(
                div_func(distributable_arg, num_part=size, **div_func_kwarg)[rank]
                for distributable_arg, div_func, div_func_kwarg in zip(
                    distributable_args, div_funcs, div_func_kwargs
                )
            )
            distributed_output = call_func(
                *distributed_args, ip_proc=rank, num_ip=size, **shared_kwargs
            )
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
