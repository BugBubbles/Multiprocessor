## For user
Thanks for cloning my project. This is a small python based multiple processor framework for python user, you can define your own processor function and, of course deploy it into the multiprocessor manager. Then it can automatically distribute and allocate the nodes, to execute among clusters of machine or only one machine for more than one processes.

## 主要目标
实现对目录下`/dataset_goosefs/cos_shanghai_1/raw_datasets/books/baidu`全部图书的分类，按一个较为粗糙的分类方法就可以了，至少实现把非网文（仙侠小说等）抽提出来。
### 实现方法
方法一：使用json内的meta字段作为分类依据，然后把该本txt的路径放在某个位置，用不着去复制粘贴这个文件吧，我感觉有点多此一举。
方法二：实在不方便就把原始文件再复制一遍，只是感觉比较占空间。

## 另外的事
理想状态下，只需要写一个生产函数和消费函数就可以了，管理器自动加载多进程和分布式执行的后续操作，目前多进程能够实现这样的操作，但是分布式还有问题。