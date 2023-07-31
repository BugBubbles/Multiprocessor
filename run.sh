# mpiexec -n 4 python3 main.py -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu -fs json -o ./output -c /workspace/tmp -me -np 1 -nc 80 -cs 400 -ms 300 --mpi 4

# python3 main.py -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu -fs json -o ./output -c /workspace/tmp -me -np 1 -nc 8 -cs 400 -ms 300

host_num=`cat /home/cluster.conf | wc -l`
host_ip=`cat /home/cluster.conf | awk -F ' ' '{print $1}' | tr '\n' ','`

OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
    mpirun -np ${host_num}  --host ${host_ip} \
    python3 main.py \
        -f /dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu \
        -fs json \
        -o ./output \
        -c /workspace/tmp \
        -me \
        -np 1 \
        -nc 8 \
        -cs 400 \
        -ms 300 \
        --mpi 4

if [ $? -ne 0 ]; then
    echo "failed to run run_cc_mpi_single_node.sh" && exit 1
fi
done