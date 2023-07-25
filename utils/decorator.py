from typing import Callable, List, Dict, Iterator, Union, Any
from . import NoSplitError, BadFormatWarning, DataShips
import warnings
from functools import wraps


def producer_typer(producer: Callable[[int, Any], DataShips]):
    """test whether the producer function is valid or not"""

    @wraps
    def warpper(id_proc: int, *producer_args, **producer_kwargs) -> DataShips:
        assert id_proc
        try:
            return producer(id_proc=id_proc, *producer_args, **producer_kwargs)
        except:
            raise TypeError("Not a valid input arguments type.")

    return warpper


def consumer_typer(consumer: Callable[[DataShips, int, Any], Any]):
    """test whether the consumer function is valid or not"""

    @wraps
    def warpper(data_ships: DataShips, id_proc: int, *consumer_args, **consumer_kwargs):
        assert id_proc and data_ships
        try:
            return consumer(
                data_ships, id_proc=id_proc, *consumer_args, **consumer_kwargs
            )
        except:
            raise TypeError("Not a valid input arguments type.")

    return warpper
