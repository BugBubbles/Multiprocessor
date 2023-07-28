from typing import Any, Callable, Dict
from ..utils.type_collector import DataShips
import traceback


class ExecutorBase:
    def __init__(self, *exec_args, **exec_kwargs) -> None:
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

    def load_producer(
        self, producer: Callable[[int,int, Any], DataShips], **producer_kwargs
    ) -> None:
        """
        Set producer function and its arguments, keep in mind that producer function should output a DATASHIPS like data which can be obtained and utilized by consumer.
        ### Arguments:
         - `producer` : reader like function from OS.
         - `producer_kwargs` : reader function arguments, dictionary like.
        """
        self.producer = producer
        self._producer_kwargs = producer_kwargs

    def load_consumer(
        self, consumer: Callable[[DataShips, int,int, Any], Any], **consumer_kwargs
    ) -> None:
        """
        Set consumer function and its arguments, keep in mind that consumer function should take a DATASHIPS like data which is produced by producer function and transported through a shared memory or quene.
        ### Arguments:
         - `consumer` : writer like function from OS.
         - `pconsumer_kwargs` : writer function arguments, dictionary like.
        """
        self.consumer = consumer
        self._consumer_kwargs = consumer_kwargs

    @property
    def producer_kwargs(self) -> Dict:
        """
        Read only property for producer key word arguments Dictionary.
        """
        return self._producer_kwargs

    @property
    def consumer_kwargs(self) -> Dict:
        """
        Read only property for consumer key word arguments Dictionary.
        """
        return self._consumer_kwargs

class Executor(ExecutorBase):
    pass
