from .executor import ExecutorBase
from  mpi4py import MPI

class MpichExecutor(ExecutorBase):
    '''
    Multiple nodes executor based on mpich software. Distribute several enclosed and executable funtions to different machines, paralleling their processing. By the way, the enclosed functions should use this Operation System independently and process without connection as much as them can. Any information transmission is deprecated.
    '''
    def __init__(self, *exec_args, **exec_kwargs) -> None:
        super().__init__(*exec_args, **exec_kwargs)

    def __call__(self, arg_call, *fn_args, **fn_kwargs):
        return super().__call__(arg_call, *fn_args, **fn_kwargs)