from .executor import ExecutorBase
import warnings
from ..utils import SmallBatchWarning


class SingleExecutor(ExecutorBase):
    def __call__(self, **kwargs):
        ships = self.producer(**self.producer_kwargs)
        if len(ships) < 10:
            warnings.warn(
                "The small batch of input files is deprecated",
                SmallBatchWarning,
                **kwargs
            )

        self.consumer(ships, **self.consumer_kwargs)
