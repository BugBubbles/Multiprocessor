from typing import Any, Callable, Dict


class DataShips(list):
    """
    The temporary datatype for transport data from producer to consumer, by default it is a list. However you can also choose to other classes.
    """

    pass


class ExecutorBase:
    def __init__(self, *exec_args, **exec_kwargs) -> None:
        self.exec_args = exec_args
        self.exec_kwargs = exec_kwargs

    def __call__(self, **kwargs):
        raise NotImplementedError

    def load_producer(
        self, producer: Callable[[Any], DataShips], **producer_kwargs
    ) -> None:
        """
        Set producer function and its arguments, keep in mind that producer function should output a DATASHIPS like data which can be obtained and utilized by consumer.
        ### Arguments:
         - `producer` : reader like function from OS.
         - `producer_kwargs` : reader function arguments, dictionary like.
        """
        self._producer = producer
        self._producer_kwargs = producer_kwargs

    def load_consumer(
        self, consumer: Callable[[DataShips, Any], Any], **consumer_kwargs
    ) -> None:
        """
        Set consumer function and its arguments, keep in mind that consumer function should take a DATASHIPS like data which is produced by producer function and transported through a shared memory or quene.
        ### Arguments:
         - `consumer` : writer like function from OS.
         - `pconsumer_kwargs` : writer function arguments, dictionary like.
        """
        self._consumer = consumer
        self._consumer_kwargs = consumer_kwargs

    @property
    def producer(self) -> Callable[[Any], DataShips]:
        """
        Read only property for producer Callable functions.
        """
        return self.producer

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

    @property
    def consumer(self) -> Callable[[DataShips, Any], Any]:
        """
        Read only property for consumer Callable functions.
        """
        return self._consumer
