python3 -m debugpy --listen 5678 --wait-for-client main.py -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu -fs json -o ./output -c /workspace/tmp -me -np 1 -nc 40 -cs 300 -ms 300 -de