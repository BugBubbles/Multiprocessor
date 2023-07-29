mpiexec -n 4 python3 main.py -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu -fs json -o ./output -c /workspace/tmp -me -np 1 -nc 80 -cs 400 -ms 300 --mpi 4

# python3 main.py -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu -fs json -o ./output -c /workspace/tmp -me -np 1 -nc 80 -cs 400 -ms 300