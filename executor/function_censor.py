from typing import Callable
from functools import wraps


def producer_censor(producer: Callable, *censor_args, **censor_kwargs):
    """test whether the producer function is valid or not"""

    @wraps
    def warpper(*producer_args, **producer_kwargs):
        output = producer(*producer_args, **producer_kwargs)
        return output

    return warpper


def consumer_censor(consumer: Callable, *censor_args, **censor_kwargs):
    """test whether the consumer function is valid or not"""

    @wraps
    def warpper(*consumer_args, **consumer_kwargs):
        output = consumer(*consumer_args, **consumer_kwargs)
        return output

    return warpper
