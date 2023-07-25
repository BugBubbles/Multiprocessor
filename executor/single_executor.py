from .executor import ExecutorBase
import warnings
from ..utils import SmallBatchWarning


class SingleExecutor(ExecutorBase):
    def __call__(self, **kwargs):
        ships = self.producer(id_proc=0, **self.producer_kwargs)
        if len(ships) < 10:
            warnings.warn(
                "The small batch of input files is deprecated",
                SmallBatchWarning,
                **kwargs
            )

        self.consumer(ships, id_proc=0, **self.consumer_kwargs)
