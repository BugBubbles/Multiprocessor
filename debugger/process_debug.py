from typing import Callable, List, Dict, Iterable, Optional, Any
from ..utils import DataShips
from functools import wraps
import time
import traceback


def print_error(*args, width: int = 80, deco: str = "█"):
    print(deco * width)
    print(deco * width)
    for arg in args:
        res_width = (width - len(arg)) // 2
        print(deco * res_width + f" {arg} " + deco * res_width)
    print(deco * width)
    print(deco * width)


def producer_typer(is_debug: bool = False, **kwargs):
    """test whether the producer function is valid or not"""

    def args_input(producer: Callable[[Any], Iterable[DataShips]]):
        if is_debug:

            @wraps(producer)
            def warpper(
                id_proc: Optional[int],
                num_proc: Optional[int],
                *producer_args,
                **producer_kwargs,
            ) -> Iterable[DataShips]:
                assert isinstance(id_proc, int) and isinstance(num_proc, int)
                try:
                    return producer(
                        id_proc=id_proc,
                        num_proc=num_proc,
                        *producer_args,
                        **producer_kwargs,
                    )
                except Exception as exc:
                    # block the exception process
                    print_error(
                        f"ERROR IN PROCESSOR {id_proc}:{warpper.__name__}",
                        "{}".format(time.strftime("%Y-%m-%d-%H:%M:%S")),
                        deco="=",
                    )
                    traceback.print_exception(
                        etype=exc.__class__, value=exc, tb=exc.__traceback__
                    )
                    while True:
                        time.sleep(10)

        else:

            @wraps(producer)
            def warpper(
                id_proc: Optional[int],
                num_proc: Optional[int],
                *producer_args,
                **producer_kwargs,
            ) -> Iterable[DataShips]:
                return producer(
                    id_proc=id_proc,
                    num_proc=num_proc,
                    *producer_args,
                    **producer_kwargs,
                )

        return warpper

    return args_input


def consumer_typer(is_debug: bool = False):
    """test whether the consumer function is valid or not"""

    def args_input(consumer: Callable[[DataShips, Any], Any]):
        consumer.__doc__
        if is_debug:

            @wraps(consumer)
            def warpper(
                data_ships: DataShips,
                id_proc: Optional[int],
                num_proc: Optional[int],
                *consumer_args,
                **consumer_kwargs,
            ):
                assert data_ships
                assert isinstance(id_proc, int) and isinstance(num_proc, int)
                try:
                    return consumer(
                        data_ships=data_ships,
                        id_proc=id_proc,
                        num_proc=num_proc,
                        *consumer_args,
                        **consumer_kwargs,
                    )
                except Exception as exc:
                    # block the exception process
                    print_error(
                        f"ERROR IN PROCESSOR {id_proc}:{warpper.__name__}",
                        "{}".format(time.strftime("%Y-%m-%d-%H:%M:%S")),
                        deco="*",
                    )
                    traceback.print_exception(
                        etype=exc.__class__, value=exc, tb=exc.__traceback__
                    )
                    while True:
                        time.sleep(10)

        else:

            @wraps(consumer)
            def warpper(
                data_ships: DataShips,
                id_proc: Optional[int],
                num_proc: Optional[int],
                *consumer_args,
                **consumer_kwargs,
            ) -> Iterable[DataShips]:
                return consumer(
                    data_ships=data_ships,
                    id_proc=id_proc,
                    num_proc=num_proc,
                    *consumer_args,
                    **consumer_kwargs,
                )

        return warpper

    return args_input
