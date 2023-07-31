from .executor import ExecutorBase
import multiprocessing as mp
import time
import warnings
import socket


class MultipleExecutor(ExecutorBase):
    """
    Multiple processor based executor.
    """

    def __init__(
        self,
        num_producer: int = 2,
        num_consumer: int = 10,
        max_size: int = 300,
        producer_initial_kwargs: dict = dict(),
        consumer_initial_kwargs: dict = dict(),
    ) -> None:
        """
        ### Arguments
         - `num_proc` : number of `PRODUCER` processors, default is 2.
         - `rate` : the divident rate from number of consumers to number of producers.
         - `max_size` : the maximal number of cache.
         - `producer_initial_kwargs` : the dictionary input arguments for producer pool, you can use this arguments to initialize the produce pools.
         - `consumer_initial_kwargs` : the dictionary input arguments for consumer pool, you can use this arguments to initialize the consume pools.
        """
        if num_producer != 2:
            warnings.warn(
                "You are setting the producer's number to 2, which will make more computer resource idle unexpectedly.",
                DeprecationWarning,
            )
        self.quene = mp.Manager().Queue(max_size)
        self.num_producer = num_producer
        self.num_consumer = num_consumer
        self.consumer_initial_kwargs = consumer_initial_kwargs
        self.producer_initial_kwargs = producer_initial_kwargs

    def _produce(
        self,
        id_proc: int,
        num_proc: int,
        ip_proc: int,
        iter_deco: str = "=",
        **producer_kwargs,
    ) -> None:
        print(
            "\n"
            + f"{iter_deco}" * 10
            + f" Produce process <IP INDEX {ip_proc:03d}> {id_proc:03d} is now working "
            + f"{iter_deco}" * 10
        )
        for ships in self.producer(
            id_proc=id_proc, num_proc=num_proc, ip_proc=ip_proc, **producer_kwargs
        ):
            while self.quene.full():
                print(
                    f"\nQuene is full, read process <IP INDEX {ip_proc:03d}> {id_proc:03d} now rests..."
                )
                time.sleep(10)
            self.quene.put(ships)
            print(
                "\n"
                + f"{iter_deco}" * 10
                + f" Produce process <IP INDEX {ip_proc:03d}> {id_proc:03d} is temporarily finished, waiting for next loop "
                + f"{iter_deco}" * 10
            )
        i = 0
        # 只让最后一个进程放终止信号
        if id_proc == num_proc - 1:
            while i < self.num_consumer:
                if not self.quene.full():
                    self.quene.put("EOF")
                    i += 1
        print(
            f"\n+++++++++++++++++++++++++++++++++++>>>>>>>>>>>>>>>>>>>>\n\
Produce process <IP INDEX {ip_proc:03d}> {id_proc:03d}:{__name__} terminates\n\
<<<<<<<<<<<<<<<<<<<<<+++++++++++++++++++++++++++++++++++"
        )

    def _consume(
        self,
        id_proc: int,
        num_proc: int,
        ip_proc: int,
        iter_deco: str = "|",
        **consumer_kwargs,
    ) -> None:
        print(
            "\n"
            + f"{iter_deco}" * 10
            + f" Consume process <IP INDEX {ip_proc:03d}> {id_proc:03d} is now working "
            + f"{iter_deco}" * 10
        )
        while True:
            ships = self.quene.get()
            if ships == "EOF":
                break
            self.consumer(
                data_ships=ships,
                id_proc=id_proc,
                num_proc=num_proc,
                ip_proc=ip_proc,
                **consumer_kwargs,
            )
            print(
                "\n"
                + f"{iter_deco}" * 10
                + f" Consume process <IP INDEX {ip_proc:03d}> {id_proc:03d} finishes, waiting for next loop "
                + f"{iter_deco}" * 10
            )

        print(
            f"\n------------------------------------>>>>>>>>>>>>>>>>>>>>\n\
Consume process <IP INDEX {ip_proc:03d}> {id_proc:03d}:{__name__} terminates\n\
<<<<<<<<<<<<<<<<<<<<<----------------------------------"
        )

    def __call__(self,  **kwargs):
        """
        ### Arguments:
        DEPRECATED  - `ip_proc` : the ip index of temporarily executing processor.
        """
        try:
            assert self.producer and self.producer_kwargs
            assert self.consumer and self.consumer_kwargs
        except Exception as exc:
            print(
                exc
                + f"\n You must load producers and consumers functions first, by applying function {__class__}.load_producer and {__class__}load_consumer."
            )
        hostname = socket.gethostname()
        ipv4 = socket.gethostbyname(hostname)
        producer_pool = mp.Pool(
            processes=self.num_producer, **self.producer_initial_kwargs
        )
        consumer_pool = mp.Pool(
            processes=self.num_consumer, **self.consumer_initial_kwargs
        )
        for id_proc in range(self.num_producer):
            producer_pool.apply_async(
                func=self._produce,
                kwds=dict(
                    id_proc=id_proc,
                    num_proc=self.num_producer,
                    **self.producer_kwargs,
                ),
                **kwargs,
            )
        for id_proc in range(self.num_consumer):
            consumer_pool.apply_async(
                func=self._consume,
                kwds=dict(
                    id_proc=id_proc,
                    num_proc=self.num_consumer,
                    **self.consumer_kwargs,
                ),
                **kwargs,
            )
        producer_pool.close()
        consumer_pool.close()

        producer_pool.join()
        consumer_pool.join()

        now_time = time.strftime("%Y/%m/%d|%H:%M:%S")
        print(
            "=================================//////////////////////////\n\
All the processors terminate, exit the main process. \n\
This is {}-{}. Now is {}.\n\
//////////////////////////=================================".format(
                hostname, ipv4, now_time
            )
        )
