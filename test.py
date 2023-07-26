# from .utils import generator_batch, producer_typer, get_file_list_stream_id
from classify_book.processor import producer

if __name__ == "__main__":
    test_dir = "/dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu"
    num_proc = 4
    for id_proc in range(num_proc):
        i = 0
        gen = producer(
            id_proc=id_proc, file_dir=test_dir, num_proc=num_proc, file_suffix=".json"
        )
        print(f"Now is {gen.__name__}:{gen.gi_frame.f_locals}:")
        for parts in gen:
            if i > 10:
                break
            i += 1
            print(*parts)
        print("=" * 20)
