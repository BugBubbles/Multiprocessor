# from .utils import generator_batch, producer_typer, get_file_list_stream_id
from classify_book.processor import producer

if __name__ == "__main__":
    test_dir = "/workspace/test"
    num_proc = 5
    i = 0
    for id_proc in range(num_proc):
        # i = 0
        gen = producer(
            id_proc=id_proc, file_dir=test_dir, num_proc=num_proc, file_suffix=".json"
        )
        print(f"Now is {gen.__name__}:{gen.gi_frame.f_locals}:")
        for parts in gen:
            # if i > 10:
            #     break
            # i += 1
            # print(*parts)
            i += len(parts)
    print("=" * 20)
    print(f"i:{i}")
