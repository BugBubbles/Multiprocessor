from typing import Callable, List, Dict, Iterable, Optional, Any
from .type_collector import DataShips
from functools import wraps


# def producer_typer(producer: Callable[[Any], Iterable[DataShips]]):
#     """test whether the producer function is valid or not"""

#     @wraps(producer)
#     def warpper(
#         id_proc: Optional[int],
#         num_proc: Optional[int],
#         *producer_args,
#         **producer_kwargs,
#     ) -> Iterable[DataShips]:
#         return producer(
#             id_proc=id_proc, num_proc=num_proc, *producer_args, **producer_kwargs
#         )

#     return warpper


# def consumer_typer(consumer: Callable[[DataShips, Any], Any]):
#     """test whether the consumer function is valid or not"""

#     @wraps(consumer)
#     def warpper(
#         data_ships: DataShips,
#         id_proc: Optional[int],
#         num_proc: Optional[int],
#         *consumer_args,
#         **consumer_kwargs,
#     ):
#         return consumer(
#             data_ships=data_ships,
#             id_proc=id_proc,
#             num_proc=num_proc,
#             *consumer_args,
#             **consumer_kwargs,
#         )

#     return warpper
