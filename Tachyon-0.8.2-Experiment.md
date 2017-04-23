# Tachyon-0.8.2-Experiment

## Startup Tasks for New Contributors

There is a few things that new contributors can do to familiarize themselves with Tachyon:

1. [Run Tachyon Locally](https://github.com/qzweng/alluxio/blob/6b52094ab568d05fbf7632b1c052275fa00854bb/docs/Running-Tachyon-Locally.html)
2. [Run Tachyon on a Cluster](https://github.com/qzweng/alluxio/blob/6b52094ab568d05fbf7632b1c052275fa00854bb/docs/Running-Tachyon-on-a-Cluster.html) (Optional)
3. Read [Configuration-Settings](https://github.com/qzweng/alluxio/blob/6b52094ab568d05fbf7632b1c052275fa00854bb/docs/Configuration-Settings.html) (Optional) and [Command-Line Interface](https://github.com/qzweng/alluxio/blob/6b52094ab568d05fbf7632b1c052275fa00854bb/docs/Command-Line-Interface.html) (Optional)
4. Read a [Code Example](https://github.com/amplab/tachyon/blob/master/examples/src/main/java/tachyon/examples/BasicOperations.java)
5. [Build Tachyon Master Branch](https://github.com/qzweng/alluxio/blob/6b52094ab568d05fbf7632b1c052275fa00854bb/docs/Building-Tachyon-Master-Branch.html)
6. Fork the repository, add unit tests or javadoc for one or two files in the following list, and then submit a pull request. You are also welcome to address issues in our [JIRA](https://tachyon.atlassian.net/browse/TACHYON). Here is a list of [tasks](https://tachyon.atlassian.net/issues/?jql=project%20%3D%20TACHYON%20AND%20labels%20%3D%20NewContributor%20AND%20status%20%3D%20OPEN) for New Contributors. Please limit 2 tasks per New Contributor. Afterwards, try some Beginner/Intermediate tasks, or ask in the [User Mailing List](https://groups.google.com/forum/?fromgroups#!forum/tachyon-users). For a tutorial, see the GitHub guides on [forking a repo](https://help.github.com/articles/fork-a-repo) and [sending a pull request](https://help.github.com/articles/using-pull-requests).

### 1. (Skip) Run Tachyon Locally

```bash
git clone https://github.com/qzweng/alluxio.git -b branch-0.8
mv alluxio tachyon
cd tachyon
mvn clean install

cp conf/tachyon-env.sh.template conf/tachyon-env.sh

./bin/tachyon format
./bin/tachyon-start.sh local
```

- Problem: "Server Error" in WebUI (localhost:19999)
  - The same problem
    - https://groups.google.com/forum/#!topic/alluxio-users/nvYEBosTrQ0
    - https://spark-project.atlassian.net/browse/TACHYON-98
  - Solution: Compile with jdk 1.7

    - Multiple Java verisions on Mac, https://stackoverflow.com/questions/26252591/mac-os-x-and-multiple-java-versions, set default java compiler with Java 7




### 2. (Skip) Run Tachyon on VirtualBox

- Setup

```bash
vagrant init bento/centos-6.7; vagrant up --provider virtualbox; vagrant ssh
```

- Install Java
  - https://www.digitalocean.com/community/tutorials/how-to-install-java-on-centos-and-fedora

```bash
cd ~
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.rpm"
sudo yum localinstall jdk-7u79-linux-x64.rpm
# Now Java should be installed at /usr/java/jdk1.7.0_79/jre/bin/java, and linked from /usr/bin/java.

sudo alternatives --config java

export JAVA_HOME=/usr/java/jdk1.7.0_79/
export JRE_HOME=/usr/java/jdk1.7.0_79/jre
```

- Install Other components

```bash
sudo yum install wget
sudo yum install git
```

- Install maven

```bash
cd /opt
sudo wget "http://apache.communilink.net/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz"
sudo tar xzf apache-maven-3.3.9-bin.tar.gz
sudo ln -s apache-maven-3.3.9 maven
sudo vi /etc/profile.d/maven.sh
	export M2_HOME=/opt/maven
    export PATH=${M2_HOME}/bin:${PATH}
source /etc/profile.d/maven.sh
mvn -version
```

- Install Tachyon

```bash
cd ~
git clone https://github.com/qzweng/alluxio.git -b branch-0.8
mv alluxio tachyon
cd tachyon
mvn clean install

cp conf/tachyon-env.sh.template conf/tachyon-env.sh
```

- Start Tachyon in local mode

```bash
./bin/tachyon format
./bin/tachyon-start.sh local
```



### 3. (Recommended) Run Spark-Tachyon on EC2

- Reference: spark-ec2-bench tutorial: https://github.com/qzweng/spark-ec2-bench/blob/master/README.md

- Start (under `/usr/local/spark-1.6.2-bin-hadoop2.6/ec2`)

  ```bash
  ./spark-ec2 -k ec2-key-oregon -i ~/AWS/IMPORTANT_PEM/ec2-key-oregon.pem -s 1 --region=us-west-2 --zone=us-west-2a --instance-type=t2.micro launch mytest
  # change: --region, --zone, --instance-type
  ```

- Login

  ```bash
  ./spark-ec2 -k ec2-key-oregon -i ~/AWS/IMPORTANT_PEM/ec2-key-oregon.pem --region=us-west-2 --zone=us-west-2a login mytest
  ```

- Destroy

  ```bash
  ./spark-ec2 -k ec2-key-oregon -i ~/AWS/IMPORTANT_PEM/ec2-key-oregon.pem --region=us-west-2 --zone=us-west-2a destroy mytest
  ```

  Tips: DO NOT "stop" EC2 instance, which will changes the IP-address, and make everything wrong.

  You have to keep the instance running all along your experiment!



## Running Spark on Tachyon

- Reference: Alluxio and Spark RDD Cache

  - https://www.alluxio.com/blog/effective-spark-rdds-with-alluxio
  - https://spark.apache.org/docs/latest/programming-guide.html#rdd-persistence
  - https://github.com/alluxio/alluxio/blob/branch-0.8/docs/Running-Spark-on-Tachyon.md



### Persist Spark RDDs into Tachyon

This feature requires Spark 1.0 or later and Tachyon 0.4.1 or later. Please refer to [Spark guide](http://spark.apache.org/docs/latest/programming-guide.html#rdd-persistence) for more details about RDD persistence.

To persist Spark RDDs, your Spark programs need to have two parameters set: `spark.externalBlockStore.url` and `spark.externalBlockStore.baseDir`.

- `spark.externalBlockStore.url` is the URL of the Tachyon Filesystem in the TachyonStore. By default, its value is `tachyon://localhost:19998`.
- `spark.externalBlockStore.baseDir` is the base directory in the Tachyon Filesystem to store the RDDs. It can be a comma-separated list of multiple directories in Tachyon. By default, its value is `java.io.tmpdir`.

To persist an RDD into Tachyon, you need to pass the `StorageLevel.OFF_HEAP` parameter. The following is an example with Spark shell:

```python
$ ./bin/pyspark
inputPath = os.join('myData','xxxx.csv')
rdd = sc.textFile(inputPath)
rdd.persist(StorageLevel.OFF_HEAP)
```

Then go to $TACHYON to see the tachyon file system

```bash
./bin/tachyon tfs lsr /tmp_spark_tachyon/
```

### (Skip) Test on Local-Spark-Tachyon

- detech environment, `/root/spark/bin/pyspark`

  ```python
  import os
  os.getcwd()
  os.listdir(os.getcwd())
  ```

- persist file using spark

```python
csvFile = os.path.join('myData','20170405.export.csv')
localFile = sc.textFile(csvFile)
tachyonFile = sc.textFile(csvFile).persist(StorageLevel.OFF_HEAP)

len(localFile.collect()) # see total length
len(tachyonFile.take(80000)) # works when Tachyon has 100MB memory
len(tachyonFile.take(90000)) # errors when Tachyon has 100MB memory
```

- upload file through tachyon, then read it from spark

```python
csv8504 = sc.textFile("tachyon://localhost:19998/20170405.export.csv")
csv8594.take(1)
```

```python
17/04/22 12:33:18 ERROR : Block 1879048192 is not available in Tachyon
17/04/22 12:33:18 ERROR : Reading from HDFS directly
```



### My test on EC2-Spark-Tachyon

#### Try 1: fail

- Open three web pages

  - Spark: <master-public-ip>:8080
  - Tachyon: <master-public-ip>:19999
  - HDFS: <master-public-ip>:50070

- Generate random data 

  ```bash
  cd /root/; mkdir myData; cd myData; head -c 64M </dev/urandom >myfile
  ```

- Store files to HDFS

  ```bash
  cd /root/ephemeral-hdfs
  ./bin/hadoop fs -put /root/myData/myfile /myfile1-64M
  ```

- Pyspark reads files through tachyon

  ```python
  masterIp = "172.xx.xx.xx"#<PRIVATE-ip-address>
  file = sc.textFile("tachyon://"+masterIp+":19998/LICENSE")
  counts = file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
  counts.saveAsTextFile("tachyon://"+masterIp+":19998/result")
  ```

  EC2 dies here :(


#### Try 2: sample file, success!


- (sample file) Store files to Tachyon

  ```bash
  cd /root/tachyon
  ./bin/tachyon tfs copyFromLocal LICENSE /LICENSE
  ```

- (sample file) Pyspark reads files through tachyon

  ```python
  masterIp = "172.xx.xx.xx"#<PRIVATE-ip-address>
  file = sc.textFile("tachyon://"+masterIp+":19998/LICENSE")
  counts = file.flatMap(lambda line: line.split(" ")) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda a, b: a + b)
  counts.saveAsTextFile("tachyon://"+masterIp+":19998/result")

  # if want to see the `result` file in WebUI
  # action should be taken
  resultFile = sc.textFile("tachyon://"+masterIp+":19998/result")
  resultFile.take(10)
  ```

  Successful result:

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs ls /result/
  9.39KB    04-23-2017 09:17:49:026  In Memory      /result/part-00000
  8.95KB    04-23-2017 09:17:49:377  In Memory      /result/part-00001
  0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
  ```

  ​

- (sample file) Store RDD OFF_HEAP in Tachyon

  ```python
  sc._jsc.hadoopConfiguration().set("fs.tachyon.impl", "tachyon.hadoop.TFS")
  file = sc.textFile("tachyon://"+masterIp+":19998/LICENSE")
  counts = file.flatMap(lambda line: line.split(" ")) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda a, b: a + b)
  counts.persist(StorageLevel.OFF_HEAP)
  counts.take(10)
  ```

  Success result:

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /tmp_spark_tachyon
  6.83KB    04-23-2017 09:23:58:203  In Memory      /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad/3b/rdd_18_0
  ```

  If `counts.collect()`, the holding space will increase:

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /tmp_spark_tachyon
  0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225
  0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0
  0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad
  0.00B     04-23-2017 09:23:58:184                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad/3b
  6.83KB    04-23-2017 09:23:58:203  In Memory      /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad/3b/rdd_18_0
  0.00B     04-23-2017 09:27:11:342                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad/3a
  6.80KB    04-23-2017 09:27:11:380  In Memory      /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0/spark-tachyon-20170423092358-87ad/3a/rdd_18_1
  ```




#### Try 3: large file to HDFS, fail


- (large file) First, put file to HDFS
- (large file) Store RDD OFF_HEAP in Tachyon

  ```python
  sc._jsc.hadoopConfiguration().set("fs.tachyon.impl", "tachyon.hadoop.TFS")
  file = sc.textFile("/myData/myfile1-64M")
  ```
  - ```python
    17/04/23 09:49:49 INFO storage.MemoryStore: Block broadcast_15 stored as values in memory (estimated size 88.2 KB, free 452.6 KB)
    17/04/23 09:49:49 INFO storage.MemoryStore: Block broadcast_15_piece0 stored as bytes in memory (estimated size 5.6 KB, free 458.2 KB)
    17/04/23 09:49:49 INFO storage.BlockManagerInfo: Added broadcast_15_piece0 in memory on 172.31.34.169:58786 (size: 5.6 KB, free: 517.4 MB)
    17/04/23 09:49:49 INFO spark.SparkContext: Created broadcast 15 from textFile at NativeMethodAccessorImpl.java:-2
    ```

  ```python
  >>> file.persist(StorageLevel.OFF_HEAP)
  >>> file.take(10)
  ```
  - ```python
    17/04/23 09:49:56 INFO mapred.FileInputFormat: Total input paths to process : 1
    17/04/23 09:49:56 INFO spark.SparkContext: Starting job: runJob at PythonRDD.scala:393
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Got job 8 (runJob at PythonRDD.scala:393) with 1 output partitions
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Final stage: ResultStage 12 (runJob at PythonRDD.scala:393)
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Parents of final stage: List()
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Missing parents: List()
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Submitting ResultStage 12 (PythonRDD[29] at RDD at PythonRDD.scala:43), which has no missing parents
    17/04/23 09:49:56 INFO storage.MemoryStore: Block broadcast_16 stored as values in memory (estimated size 4.7 KB, free 462.9 KB)
    17/04/23 09:49:56 INFO storage.MemoryStore: Block broadcast_16_piece0 stored as bytes in memory (estimated size 3.0 KB, free 465.9 KB)
    17/04/23 09:49:56 INFO storage.BlockManagerInfo: Added broadcast_16_piece0 in memory on 172.31.34.169:58786 (size: 3.0 KB, free: 517.4 MB)
    17/04/23 09:49:56 INFO spark.SparkContext: Created broadcast 16 from broadcast at DAGScheduler.scala:1006
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Submitting 1 missing tasks from ResultStage 12 (PythonRDD[29] at RDD at PythonRDD.scala:43)
    17/04/23 09:49:56 INFO scheduler.TaskSchedulerImpl: Adding task set 12.0 with 1 tasks
    17/04/23 09:49:56 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 12.0 (TID 16, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 2182 bytes)
    17/04/23 09:49:56 INFO storage.BlockManagerInfo: Added broadcast_16_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 3.0 KB, free: 146.2 MB)
    17/04/23 09:49:56 INFO storage.BlockManagerInfo: Added broadcast_15_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 5.6 KB, free: 146.2 MB)
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: ResultStage 12 (runJob at PythonRDD.scala:393) finished in 0.326 s
    17/04/23 09:49:56 INFO scheduler.DAGScheduler: Job 8 finished: runJob at PythonRDD.scala:393, took 0.345616 s
    17/04/23 09:49:56 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 12.0 (TID 16) in 325 ms on ip-172-31-42-183.us-west-2.compute.internal (1/1)
    17/04/23 09:49:56 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 12.0, whose tasks have all completed, from pool
    [u'j;\ufffd\x13}{Fy\ufffd\x1f`q\ufffd5\ufffd\x19lh<\ufffd\ufffd\ufffd5\ufffd\ufffdy\ufffd\ufffd\ufffdpwQ\ufffdF9#9\ufffdK\x0bA|\ufffd\ufffd)\ufffd\ufffd\ufffd\x1b\ufffd\ufffd\ufffd\ufffd\\5\ufffdR\ufffd\ufffd\x07\ufffdj\ufffd\ufffd', u'\ufffdy\ufffd\ufffd\x1b\ufffd\x0c\ufffd~\x19B\u0614m\ufffd\ufffdY\x11\u0234\uf...]
    ```

  ```python
  >>> len(file.collect())
  ```
  - ```python
    17/04/23 09:51:01 INFO spark.SparkContext: Starting job: collect at <stdin>:1
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Got job 9 (collect at <stdin>:1) with 2 output partitions
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Final stage: ResultStage 13 (collect at <stdin>:1)
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Parents of final stage: List()
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Missing parents: List()
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Submitting ResultStage 13 (/myData/myfile1-64M MapPartitionsRDD[28] at textFile at NativeMethodAccessorImpl.java:-2), which has no missing parents
    17/04/23 09:51:01 INFO storage.MemoryStore: Block broadcast_17 stored as values in memory (estimated size 3.1 KB, free 469.0 KB)
    17/04/23 09:51:01 INFO storage.MemoryStore: Block broadcast_17_piece0 stored as bytes in memory (estimated size 1811.0 B, free 470.7 KB)
    17/04/23 09:51:01 INFO storage.BlockManagerInfo: Added broadcast_17_piece0 in memory on 172.31.34.169:58786 (size: 1811.0 B, free: 517.4 MB)
    17/04/23 09:51:01 INFO spark.SparkContext: Created broadcast 17 from broadcast at DAGScheduler.scala:1006
    17/04/23 09:51:01 INFO scheduler.DAGScheduler: Submitting 2 missing tasks from ResultStage 13 (/myData/myfile1-64M MapPartitionsRDD[28] at textFile at NativeMethodAccessorImpl.java:-2)
    17/04/23 09:51:01 INFO scheduler.TaskSchedulerImpl: Adding task set 13.0 with 2 tasks
    17/04/23 09:51:01 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 13.0 (TID 17, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 2182 bytes)
    17/04/23 09:51:01 INFO storage.BlockManagerInfo: Added broadcast_17_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 1811.0 B, free: 146.2 MB)
    17/04/23 09:51:14 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 13.0 (TID 18, ip-172-31-42-183.us-west-2.compute.internal, partition 1,NODE_LOCAL, 2182 bytes)
    17/04/23 09:51:17 INFO spark.ContextCleaner: Cleaned accumulator 12
    17/04/23 09:51:17 INFO storage.BlockManagerInfo: Removed broadcast_16_piece0 on 172.31.34.169:58786 in memory (size: 3.0 KB, free: 517.4 MB)
    17/04/23 09:51:18 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 13.0 (TID 17) in 16998 ms on ip-172-31-42-183.us-west-2.compute.internal (1/2)
    17/04/23 09:51:30 INFO storage.BlockManagerInfo: Removed broadcast_16_piece0 on ip-172-31-42-183.us-west-2.compute.internal:35004 in memory (size: 3.0 KB, free: 146.2 MB)
    17/04/23 09:52:00 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 13.0 (TID 18) in 46117 ms on ip-172-31-42-183.us-west-2.compute.internal (2/2)
    17/04/23 09:52:00 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 13.0, whose tasks have all completed, from pool
    17/04/23 09:52:00 INFO scheduler.DAGScheduler: ResultStage 13 (collect at <stdin>:1) finished in 59.165 s
    17/04/23 09:52:00 INFO scheduler.DAGScheduler: Job 9 finished: collect at <stdin>:1, took 59.184882 s
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/root/spark/python/pyspark/rdd.py", line 772, in collect
      return list(_load_from_socket(port, self._jrdd_deserializer))
    File "/root/spark/python/pyspark/rdd.py", line 142, in _load_from_socket
      for item in serializer.load_stream(rf):
    File "/root/spark/python/pyspark/serializers.py", line 517, in load_stream
      yield self.loads(stream)
    File "/root/spark/python/pyspark/serializers.py", line 511, in loads
      s = stream.read(length)
    File "/usr/lib64/python2.7/socket.py", line 384, in read
      data = self._sock.recv(left)
    socket.timeout: timed out
    ```


  ```python
  >>> len(file.collect())
  ```

-   ```python
    17/04/23 10:09:00 INFO mapred.FileInputFormat: Total input paths to process : 1
    17/04/23 10:09:01 INFO spark.SparkContext: Starting job: collect at <stdin>:1
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Got job 10 (collect at <stdin>:1) with 2 output partitions
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Final stage: ResultStage 14 (collect at <stdin>:1)
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Parents of final stage: List()
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Missing parents: List()
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Submitting ResultStage 14 (/myData/csv47M MapPartitionsRDD[31] at textFile at NativeMethodAccessorImpl.java:-2), which has no missing parents
    17/04/23 10:09:01 INFO storage.MemoryStore: Block broadcast_19 stored as values in memory (estimated size 3.1 KB, free 560.0 KB)
    17/04/23 10:09:01 INFO storage.MemoryStore: Block broadcast_19_piece0 stored as bytes in memory (estimated size 1810.0 B, free 561.7 KB)
    17/04/23 10:09:01 INFO storage.BlockManagerInfo: Added broadcast_19_piece0 in memory on 172.31.34.169:58786 (size: 1810.0 B, free: 517.4 MB)
    17/04/23 10:09:01 INFO spark.SparkContext: Created broadcast 19 from broadcast at DAGScheduler.scala:1006
    17/04/23 10:09:01 INFO scheduler.DAGScheduler: Submitting 2 missing tasks from ResultStage 14 (/myData/csv47M MapPartitionsRDD[31] at textFile at NativeMethodAccessorImpl.java:-2)
    17/04/23 10:09:01 INFO scheduler.TaskSchedulerImpl: Adding task set 14.0 with 2 tasks
    17/04/23 10:09:01 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 14.0 (TID 19, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 2177 bytes)
    17/04/23 10:09:01 INFO storage.BlockManagerInfo: Added broadcast_19_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 1810.0 B, free: 146.2 MB)
    17/04/23 10:09:01 INFO storage.BlockManagerInfo: Added broadcast_18_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 5.6 KB, free: 146.2 MB)
    17/04/23 10:09:05 INFO storage.BlockManagerInfo: Added rdd_31_0 on ExternalBlockStore on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 7.4 MB)
    17/04/23 10:09:51 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 14.0 (TID 20, ip-172-31-42-183.us-west-2.compute.internal, partition 1,NODE_LOCAL, 2177 bytes)
    17/04/23 10:09:55 INFO storage.BlockManagerInfo: Added rdd_31_1 on ExternalBlockStore on ip-172-31-42-183.us-west-2.compute.internal:35004 (size: 7.3 MB)
    ----------------------------------------
    Exception happened during processing of request from ('127.0.0.1', 44924)
    Traceback (most recent call last):
      File "/usr/lib64/python2.7/SocketServer.py", line 290, in _handle_request_noblock
        self.process_request(request, client_address)
      File "/usr/lib64/python2.7/SocketServer.py", line 318, in process_request
        self.finish_request(request, client_address)
      File "/usr/lib64/python2.7/SocketServer.py", line 331, in finish_request
        self.RequestHandlerClass(request, client_address, self)
      File "/usr/lib64/python2.7/SocketServer.py", line 652, in __init__
        self.handle()
      File "/root/spark/python/pyspark/accumulators.py", line 235, in handle
        num_updates = read_int(self.rfile)
      File "/root/spark/python/pyspark/serializers.py", line 545, in read_int
        raise EOFError
    EOFError
    ----------------------------------------
    ERROR:py4j.java_gateway:An error occurred while trying to connect to the Java server
    Traceback (most recent call last):
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 690, in start
        self.socket.connect((self.address, self.port))
      File "/usr/lib64/python2.7/socket.py", line 228, in meth
        return getattr(self._sock,name)(*args)
    error: [Errno 111] Connection refused
    ERROR:py4j.java_gateway:An error occurred while trying to connect to the Java server
    Traceback (most recent call last):
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 690, in start
        self.socket.connect((self.address, self.port))
      File "/usr/lib64/python2.7/socket.py", line 228, in meth
        return getattr(self._sock,name)(*args)
    error: [Errno 111] Connection refused
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/root/spark/python/pyspark/rdd.py", line 771, in collect
        port = self.ctx._jvm.PythonRDD.collectAndServe(self._jrdd.rdd())
      File "/root/spark/python/pyspark/traceback_utils.py", line 78, in __exit__
        self._context._jsc.setCallSite(None)
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 811, in __call__
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 624, in send_command
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 579, in _get_connection
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 585, in _create_connection
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 697, in start
    py4j.protocol.Py4JNetworkError: An error occurred while trying to connect to the Java server
    >>>
    ```




#### Try 4: large file to Tachyon

- (large file) First, put file to Tachyon (in bash)

  ```bash
  cd /root/tachyon
  ./bin/tachyon tfs copyFromLocal /root/myData/myfile1-64M /myData/myfile1-64M
  ```
  - ```bash
    tachyon.exception.TachyonException: Cannot complete file without all the blocks committed
    root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs ls /myData
    0.00B     04-23-2017 10:17:25:171  In Memory      /myData/myfile1-64M
    ```

- (large file) Store RDD OFF_HEAP in Tachyon (in pyspark)

  ```python
  sc._jsc.hadoopConfiguration().set("fs.tachyon.impl", "tachyon.hadoop.TFS")
  file = sc.textFile("tachyon://"+masterIp+":19998/myData/myfile1-64M”)
  file.persist(StorageLevel.OFF_HEAP)
  file.take(10)
  ```

  - ```python
    17/04/23 10:34:25 WARN scheduler.TaskSetManager: Lost task 0.0 in stage 0.0 (TID 0, ip-172-31-42-183.us-west-2.compute.internal): java.io.IOException: The file /myData/myfile1-64M is not complete.
    ```


- Retry the first step: put file to Tachyon (in bash) until success

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs copyFromLocal /root/myData/myfile1-64M /myData/myfile2-64M
  Copied /root/myData/myfile1-64M to /myData/myfile2-64M
  ```

- Store RDD OFF_HEAP as before

  first success in file.take(10)

  - ```python
    17/04/23 10:36:32 INFO : getFileStatus(/myData/myfile2-64M): HDFS Path: hdfs://ec2-34-208-49-95.us-west-2.compute.amazonaws.com:9000/myData/myfile2-64M TPath: tachyon://172.31.34.169:19998/myData/myfile2-64M
    17/04/23 10:36:32 INFO mapred.FileInputFormat: Total input paths to process : 1
    17/04/23 10:36:32 INFO spark.SparkContext: Starting job: runJob at PythonRDD.scala:393
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Got job 1 (runJob at PythonRDD.scala:393) with 1 output partitions
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Final stage: ResultStage 1 (runJob at PythonRDD.scala:393)
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Parents of final stage: List()
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Missing parents: List()
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Submitting ResultStage 1 (PythonRDD[5] at RDD at PythonRDD.scala:43), which has no missing parents
    17/04/23 10:36:33 INFO storage.MemoryStore: Block broadcast_3 stored as values in memory (estimated size 4.8 KB, free 95.6 KB)
    17/04/23 10:36:33 INFO storage.MemoryStore: Block broadcast_3_piece0 stored as bytes in memory (estimated size 3.0 KB, free 98.7 KB)
    17/04/23 10:36:33 INFO storage.BlockManagerInfo: Added broadcast_3_piece0 in memory on 172.31.34.169:47160 (size: 3.0 KB, free: 517.4 MB)
    17/04/23 10:36:33 INFO spark.SparkContext: Created broadcast 3 from broadcast at DAGScheduler.scala:1006
    17/04/23 10:36:33 INFO scheduler.DAGScheduler: Submitting 1 missing tasks from ResultStage 1 (PythonRDD[5] at RDD at PythonRDD.scala:43)
    17/04/23 10:36:33 INFO scheduler.TaskSchedulerImpl: Adding task set 1.0 with 1 tasks
    17/04/23 10:36:33 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 1.0 (TID 4, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 2151 bytes)
    17/04/23 10:36:33 INFO storage.BlockManagerInfo: Added broadcast_3_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:40540 (size: 3.0 KB, free: 146.2 MB)
    17/04/23 10:36:33 INFO storage.BlockManagerInfo: Added broadcast_2_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:40540 (size: 5.6 KB, free: 146.2 MB)
    17/04/23 10:36:36 INFO storage.BlockManagerInfo: Added rdd_4_0 on ExternalBlockStore on ip-172-31-42-183.us-west-2.compute.internal:40540 (size: 36.7 MB)
    17/04/23 10:36:37 INFO scheduler.DAGScheduler: ResultStage 1 (runJob at PythonRDD.scala:393) finished in 4.723 s
    17/04/23 10:36:37 INFO scheduler.DAGScheduler: Job 1 finished: runJob at PythonRDD.scala:393, took 4.762701 s
    17/04/23 10:36:37 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 1.0 (TID 4) in 4717 ms on ip-172-31-42-183.us-west-2.compute.internal (1/1)
    17/04/23 10:36:37 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 1.0, whose tasks have all completed, from pool
    [u'j;\ufffd\x13}{Fy\ufffd\x1f`q\ufffd5\ufffd\x19lh<\ufffd\ufffd\ufffd5\ufffd\ufffdy\ufffd\ufffd\ufffdpwQ\ufffdF9#9\ufffdK\x0bA|\ufffd\ufffd)...]
    ```

  But timed out in len(file.collect())

  - ```python
    ----------------------------------------
    Exception happened during processing of request from ('127.0.0.1', 36025)
    Traceback (most recent call last):
      File "/usr/lib64/python2.7/SocketServer.py", line 290, in _handle_request_noblock
        return list(_load_from_socket(port, self._jrdd_deserializer))
      File "/root/spark/python/pyspark/rdd.py", line 142, in _load_from_socket
        for item in serializer.load_stream(rf):
      File "/root/spark/python/pyspark/serializers.py", line 517, in load_stream
        yield self.loads(stream)
      File "/root/spark/python/pyspark/serializers.py", line 511, in loads
        s = stream.read(length)
      File "/usr/lib64/python2.7/socket.py", line 384, in read
        data = self._sock.recv(left)
    socket.timeout: timed out
        self.process_request(request, client_address)
      File "/usr/lib64/python2.7/SocketServer.py", line 318, in process_request
        self.finish_request(request, client_address)
      File "/usr/lib64/python2.7/SocketServer.py", line 331, in finish_request
        self.RequestHandlerClass(request, client_address, self)
      File "/usr/lib64/python2.7/SocketServer.py", line 652, in __init__
        self.handle()
      File "/root/spark/python/pyspark/accumulators.py", line 235, in handle
        num_updates = read_int(self.rfile)
      File "/root/spark/python/pyspark/serializers.py", line 545, in read_int
        raise EOFError
    EOFError
    ----------------------------------------
    ```

  And then, the pyspark seems to be shutted down

  - ```python
    >>> file.take(20)
    ERROR:py4j.java_gateway:An error occurred while trying to connect to the Java server
    Traceback (most recent call last):
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 690, in start
        self.socket.connect((self.address, self.port))
      File "/usr/lib64/python2.7/socket.py", line 228, in meth
        return getattr(self._sock,name)(*args)
    error: [Errno 111] Connection refused
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/root/spark/python/pyspark/rdd.py", line 1267, in take
        totalParts = self.getNumPartitions()
      File "/root/spark/python/pyspark/rdd.py", line 356, in getNumPartitions
        return self._jrdd.partitions().size()
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 811, in __call__
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 624, in send_command
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 579, in _get_connection
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 585, in _create_connection
      File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 697, in start
    py4j.protocol.Py4JNetworkError: An error occurred while trying to connect to the Java server
    >>> sc
    <pyspark.context.SparkContext object at 0x7fbfe5a91950>
    ```

  All the tmp file stored in Tachyon was deleted after the `pyspark` is shutted down

  - ```bash
    root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /tmp_spark_tachyon/
    0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225
    0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0
    0.00B     04-23-2017 10:36:33:288                 /tmp_spark_tachyon/spark-05cf2c05-6892-427f-b594-88e85a7a778d
    0.00B     04-23-2017 10:36:33:288                 /tmp_spark_tachyon/spark-05cf2c05-6892-427f-b594-88e85a7a778d/0
    root@ip-172-31-34-169 tachyon]$
    ```

  Only the file upload by `tachyon tfs` and `saveAsTextFile("tachyon://"+masterIp+":19998/result")` can be persisted after `pyspark` is shutted down

  - ```bash
    root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /
    26.23KB   04-23-2017 09:15:59:859  In Memory      /LICENSE
    0.00B     04-23-2017 09:17:45:021                 /result
    9.39KB    04-23-2017 09:17:49:026  In Memory      /result/part-00000
    8.95KB    04-23-2017 09:17:49:377  In Memory      /result/part-00001
    0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
    0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon
    0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225
    0.00B     04-23-2017 09:23:58:168                 /tmp_spark_tachyon/spark-4230665c-0653-4871-b803-4003e5fc3225/0
    0.00B     04-23-2017 10:36:33:288                 /tmp_spark_tachyon/spark-05cf2c05-6892-427f-b594-88e85a7a778d
    0.00B     04-23-2017 10:36:33:288                 /tmp_spark_tachyon/spark-05cf2c05-6892-427f-b594-88e85a7a778d/0
    0.00B     04-23-2017 10:17:25:171                 /myData
    0.00B     04-23-2017 10:17:25:171  In Memory      /myData/myfile1-64M
    64.00MB   04-23-2017 10:35:34:987  In Memory      /myData/myfile2-64M
    26.23KB   04-23-2017 10:19:21:466  In Memory      /LICENSE.txt
    root@ip-172-31-34-169 tachyon]$
    ```



Try 5: 46M file on Spark, with 6 * 64M Stored file

- push random files to Tachyon by `./bin/tachyon tfs -put xxx /myData/xxx`

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /
  26.23KB   04-23-2017 09:15:59:859  In Memory      /LICENSE
  0.00B     04-23-2017 09:17:45:021                 /result
  9.39KB    04-23-2017 09:17:49:026  In Memory      /result/part-00000
  8.95KB    04-23-2017 09:17:49:377  In Memory      /result/part-00001
  0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
  0.00B     04-23-2017 10:17:25:171                 /myData
  64.00MB   04-23-2017 10:35:34:987  In Memory      /myData/myfile2-64M
  46.67MB   04-23-2017 10:56:42:350  In Memory      /myData/csv-46M
  64.00MB   04-23-2017 10:57:30:681  In Memory      /myData/myfile1-64M
  64.00MB   04-23-2017 10:57:40:894  In Memory      /myData/myfile3-64M
  64.00MB   04-23-2017 10:57:46:499  In Memory      /myData/myfile4-64M
  64.00MB   04-23-2017 10:58:08:435  In Memory      /myData/myfile5-64M
  64.00MB   04-23-2017 10:58:13:785  In Memory      /myData/myfile6-64M
  root@ip-172-31-34-169 tachyon]$
  ```

  Finally the 

  | Workers Capacity:    | 512.00MB           |
  | -------------------- | ------------------ |
  | Workers Free / Used: | 81.28MB / 430.72MB |

- Run Pyspark dealing with csv-46M

  ```python
  masterIp = "172.xx.xx.xx"
  sc._jsc.hadoopConfiguration().set("fs.tachyon.impl", "tachyon.hadoop.TFS")
  csvFile = sc.textFile("tachyon://"+masterIp+":19998/myData/csv-46M")
  counts = csvFile.flatMap(lambda line: line.split()) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda a, b: a + b)
  counts.persist(StorageLevel.OFF_HEAP)
  counts.take(10)
  ```

  Success!

  ```bash
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389
  0.00B     04-23-2017 11:08:06:733                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a
  8.78MB    04-23-2017 11:08:06:802  In Memory      /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a/rdd_6_0
  ```

  | Workers Capacity:    | 512.00MB           |
  | -------------------- | ------------------ |
  | Workers Free / Used: | 72.51MB / 439.49MB |

  Even `counts.take(100)` the memory still doesn't change

  But when `counts.collect()`, the output becomes:

  ```bash
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389
  0.00B     04-23-2017 11:08:06:733                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a
  8.78MB    04-23-2017 11:08:06:802  In Memory      /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a/rdd_6_0
  0.00B     04-23-2017 11:10:35:425                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1b
  8.73MB    04-23-2017 11:10:35:440  In Memory      /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1b/rdd_6_1
  ```

  | Workers Capacity:    | 512.00MB           |
  | -------------------- | ------------------ |
  | Workers Free / Used: | 63.78MB / 448.22MB |

  ​

  But, the process's time is **decreased every time** in latter turns of operation! While the usage **space doesn't increase** at all (Don't know why)

  ```python
  >>> len(counts.collect())

  17/04/23 11:19:45 INFO scheduler.DAGScheduler: ResultStage 18 (collect at <stdin>:1) finished in 81.279 s
  17/04/23 11:19:45 INFO scheduler.DAGScheduler: Job 9 finished: collect at <stdin>:1, took 82.667028 s
  191020

  >>> len(counts.collect())
  17/04/23 11:21:08 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 20.0, whose tasks have all completed, from pool
  17/04/23 11:21:08 INFO scheduler.DAGScheduler: ResultStage 20 (collect at <stdin>:1) finished in 62.540 s
  17/04/23 11:21:08 INFO scheduler.DAGScheduler: Job 10 finished: collect at <stdin>:1, took 63.449390 s
  191020

  >>> len(counts.collect())
  17/04/23 11:23:22 INFO scheduler.DAGScheduler: ResultStage 22 (collect at <stdin>:1) finished in 45.244 s
  17/04/23 11:23:23 INFO scheduler.DAGScheduler: Job 11 finished: collect at <stdin>:1, took 45.364414 s
  17/04/23 11:23:23 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 22.0, whose tasks have all completed, from pool
  191020

  >>> len(counts.collect())
  17/04/23 11:24:35 INFO scheduler.DAGScheduler: ResultStage 24 (collect at <stdin>:1) finished in 43.749 s
  17/04/23 11:24:35 INFO scheduler.DAGScheduler: Job 12 finished: collect at <stdin>:1, took 44.005446 s
  17/04/23 11:24:35 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 24.0 (TID 20) in 19373 ms on ip-172-31-42-183.us-west-2.compute.internal (2/2)
  17/04/23 11:24:35 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 24.0, whose tasks have all completed, from pool
  191020

  >>> len(counts.collect())
  17/04/23 11:25:48 INFO scheduler.DAGScheduler: ResultStage 26 (collect at <stdin>:1) finished in 37.599 s
  17/04/23 11:25:48 INFO scheduler.DAGScheduler: Job 13 finished: collect at <stdin>:1, took 37.629330 s
  191020
  ```

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  0.00B     04-23-2017 11:08:06:733                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a
  8.78MB    04-23-2017 11:08:06:802  In Memory      /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1a/rdd_6_0
  0.00B     04-23-2017 11:10:35:425                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1b
  8.73MB    04-23-2017 11:10:35:440  In Memory      /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0/spark-tachyon-20170423110806-9389/1b/rdd_6_1
  ```

  ​

- Then we start another `pyspark` process to compete for the resource

  ```python
  17/04/23 11:34:04 WARN scheduler.TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
  ```

  Because of this EC2 instance only has 1 core… so cannot multi-process :(

- We cache many different files in one process

  ```python
  masterIp = "172.xx.xx.xx"
  sc._jsc.hadoopConfiguration().set("fs.tachyon.impl", "tachyon.hadoop.TFS")
  myFile2 = sc.textFile("tachyon://"+masterIp+":19998/myData/myfile2-64M")
  counts2 = myFile2.flatMap(lambda line: line.split()) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda a, b: a + b)
  counts2.persist(StorageLevel.OFF_HEAP)
  counts2.take(10)
  ```

- csv46M and myfile1-64M
  ```bash
  26.23KB   04-23-2017 09:15:59:859  In Memory      /LICENSE
  0.00B     04-23-2017 09:17:45:021                 /result
  9.39KB    04-23-2017 09:17:49:026  In Memory      /result/part-00000
  8.95KB    04-23-2017 09:17:49:377  In Memory      /result/part-00001
  0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
  0.00B     04-23-2017 10:17:25:171                 /myData
  64.00MB   04-23-2017 10:35:34:987  In Memory      /myData/myfile2-64M
  46.67MB   04-23-2017 10:56:42:350  In Memory      /myData/csv-46M
  64.00MB   04-23-2017 10:57:30:681  In Memory      /myData/myfile1-64M
  64.00MB   04-23-2017 10:57:40:894  In Memory      /myData/myfile3-64M
  64.00MB   04-23-2017 10:57:46:499  In Memory      /myData/myfile4-64M
  64.00MB   04-23-2017 10:58:08:435  In Memory      /myData/myfile5-64M
  64.00MB   04-23-2017 10:58:13:785  In Memory      /myData/myfile6-64M
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  2404.61KB 04-23-2017 11:40:52:188  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1a/rdd_6_0
  2413.68KB 04-23-2017 11:41:06:054  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1b/rdd_6_1
  43.75MB   04-23-2017 11:45:50:283  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/3e/rdd_15_0
  ```

  | Workers Capacity:    | 512.00MB           |
  | -------------------- | ------------------ |
  | Workers Free / Used: | 32.83MB / 479.17MB |

- csv46M, myfile1-64M and myfile2-64M

  First, the used memory keep growing and reaching the max capacity: 512MB limit

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /
  26.23KB   04-23-2017 09:15:59:859  In Memory      /LICENSE
  0.00B     04-23-2017 09:17:45:021                 /result
  9.39KB    04-23-2017 09:17:49:026  In Memory      /result/part-00000
  8.95KB    04-23-2017 09:17:49:377  In Memory      /result/part-00001
  0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
  0.00B     04-23-2017 10:17:25:171                 /myData
  64.00MB   04-23-2017 10:35:34:987  In Memory      /myData/myfile2-64M
  46.67MB   04-23-2017 10:56:42:350  In Memory      /myData/csv-46M
  64.00MB   04-23-2017 10:57:30:681  In Memory      /myData/myfile1-64M
  64.00MB   04-23-2017 10:57:40:894  In Memory      /myData/myfile3-64M
  64.00MB   04-23-2017 10:57:46:499  In Memory      /myData/myfile4-64M
  64.00MB   04-23-2017 10:58:08:435  In Memory      /myData/myfile5-64M
  64.00MB   04-23-2017 10:58:13:785  In Memory      /myData/myfile6-64M
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0
  0.00B     04-23-2017 11:34:18:619                 /tmp_spark_tachyon/spark-af67c227-8d3d-4d7c-9f83-f8ae72d33ff3
  0.00B     04-23-2017 11:34:18:619                 /tmp_spark_tachyon/spark-af67c227-8d3d-4d7c-9f83-f8ae72d33ff3/0
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f
  0.00B     04-23-2017 11:40:52:147                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1a
  2404.61KB 04-23-2017 11:40:52:188  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1a/rdd_6_0
  0.00B     04-23-2017 11:41:06:027                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1b
  2413.68KB 04-23-2017 11:41:06:054  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1b/rdd_6_1
  0.00B     04-23-2017 11:45:50:139                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/3e
  43.75MB   04-23-2017 11:45:50:283  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/3e/rdd_15_0
  0.00B     04-23-2017 11:53:01:030                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/21
  0.00B     04-23-2017 11:53:01:139  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/21/rdd_23_0
  ```

  And when reaches the max capacity, it kicks out certain file, and totally stored the new file

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs lsr /
  26.23KB   04-23-2017 09:15:59:859  Not In Memory  /LICENSE
  0.00B     04-23-2017 09:17:45:021                 /result
  9.39KB    04-23-2017 09:17:49:026  Not In Memory  /result/part-00000
  8.95KB    04-23-2017 09:17:49:377  Not In Memory  /result/part-00001
  0.00B     04-23-2017 09:17:49:564  In Memory      /result/_SUCCESS
  0.00B     04-23-2017 10:17:25:171                 /myData
  64.00MB   04-23-2017 10:35:34:987  Not In Memory  /myData/myfile2-64M
  46.67MB   04-23-2017 10:56:42:350  In Memory      /myData/csv-46M
  64.00MB   04-23-2017 10:57:30:681  In Memory      /myData/myfile1-64M
  64.00MB   04-23-2017 10:57:40:894  In Memory      /myData/myfile3-64M
  64.00MB   04-23-2017 10:57:46:499  In Memory      /myData/myfile4-64M
  64.00MB   04-23-2017 10:58:08:435  In Memory      /myData/myfile5-64M
  64.00MB   04-23-2017 10:58:13:785  In Memory      /myData/myfile6-64M
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405
  0.00B     04-23-2017 11:08:06:723                 /tmp_spark_tachyon/spark-4897759f-0825-4bf1-9807-258e1a62a405/0
  0.00B     04-23-2017 11:34:18:619                 /tmp_spark_tachyon/spark-af67c227-8d3d-4d7c-9f83-f8ae72d33ff3
  0.00B     04-23-2017 11:34:18:619                 /tmp_spark_tachyon/spark-af67c227-8d3d-4d7c-9f83-f8ae72d33ff3/0
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0
  0.00B     04-23-2017 11:40:52:134                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f
  0.00B     04-23-2017 11:40:52:147                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1a
  2404.61KB 04-23-2017 11:40:52:188  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1a/rdd_6_0
  0.00B     04-23-2017 11:41:06:027                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1b
  2413.68KB 04-23-2017 11:41:06:054  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/1b/rdd_6_1
  0.00B     04-23-2017 11:45:50:139                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/3e
  43.75MB   04-23-2017 11:45:50:283  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/3e/rdd_15_0
  0.00B     04-23-2017 11:53:01:030                 /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/21
  43.75MB   04-23-2017 11:53:01:139  In Memory      /tmp_spark_tachyon/spark-0365c841-00f0-4ca6-aff3-b872a16a8697/0/spark-tachyon-20170423114052-706f/21/rdd_23_0
  ```

  | Workers Capacity:    | 512.00MB           |
  | -------------------- | ------------------ |
  | Workers Free / Used: | 53.13MB / 458.87MB |

  The pyspark's processing progress:

  ```python
  >>> myFile2= sc.textFile("tachyon://"+masterIp+":19998/myData/myfile2-64M")
  17/04/23 11:48:13 INFO storage.MemoryStore: Block broadcast_8 stored as values in memory (estimated size 88.2 KB, free 234.0 KB)
  17/04/23 11:48:13 INFO storage.MemoryStore: Block broadcast_8_piece0 stored as bytes in memory (estimated size 5.6 KB, free 239.6 KB)
  17/04/23 11:48:13 INFO storage.BlockManagerInfo: Added broadcast_8_piece0 in memory on 172.31.34.169:58853 (size: 5.6 KB, free: 517.4 MB)
  17/04/23 11:48:13 INFO spark.SparkContext: Created broadcast 8 from textFile at NativeMethodAccessorImpl.java:-2
  >>> counts2 = myFile1.flatMap(lambda line: line.split()) \
  ...              .map(lambda word: (word, 1)) \
  ...              .reduceByKey(lambda a, b: a + b)
  >>> counts2.persist(StorageLevel.OFF_HEAP)
  PythonRDD[23] at RDD at PythonRDD.scala:43
  >>> counts2.take(10)
  17/04/23 11:48:50 INFO spark.SparkContext: Starting job: runJob at PythonRDD.scala:393
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Registering RDD 20 (reduceByKey at <stdin>:3)
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Got job 4 (runJob at PythonRDD.scala:393) with 1 output partitions
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Final stage: ResultStage 9 (runJob at PythonRDD.scala:393)
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Parents of final stage: List(ShuffleMapStage 8)
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Missing parents: List(ShuffleMapStage 8)
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Submitting ShuffleMapStage 8 (PairwiseRDD[20] at reduceByKey at <stdin>:3), which has no missing parents
  17/04/23 11:48:50 INFO storage.MemoryStore: Block broadcast_9 stored as values in memory (estimated size 8.0 KB, free 247.6 KB)
  17/04/23 11:48:50 INFO storage.MemoryStore: Block broadcast_9_piece0 stored as bytes in memory (estimated size 5.1 KB, free 252.7 KB)
  17/04/23 11:48:50 INFO storage.BlockManagerInfo: Added broadcast_9_piece0 in memory on 172.31.34.169:58853 (size: 5.1 KB, free: 517.4 MB)
  17/04/23 11:48:50 INFO spark.SparkContext: Created broadcast 9 from broadcast at DAGScheduler.scala:1006
  17/04/23 11:48:50 INFO scheduler.DAGScheduler: Submitting 2 missing tasks from ShuffleMapStage 8 (PairwiseRDD[20] at reduceByKey at <stdin>:3)
  17/04/23 11:48:50 INFO scheduler.TaskSchedulerImpl: Adding task set 8.0 with 2 tasks
  17/04/23 11:48:50 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 8.0 (TID 10, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 2140 bytes)
  17/04/23 11:48:51 INFO storage.BlockManagerInfo: Added broadcast_9_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:53139 (size: 5.1 KB, free: 146.2 MB)
  17/04/23 11:50:11 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 8.0 (TID 11, ip-172-31-42-183.us-west-2.compute.internal, partition 1,NODE_LOCAL, 2140 bytes)
  17/04/23 11:50:11 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 8.0 (TID 10) in 81083 ms on ip-172-31-42-183.us-west-2.compute.internal (1/2)
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: ShuffleMapStage 8 (reduceByKey at <stdin>:3) finished in 202.300 s
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: looking for newly runnable stages
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: running: Set()
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: waiting: Set(ResultStage 9)
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: failed: Set()
  17/04/23 11:52:13 INFO scheduler.TaskSetManager: Finished task 1.0 in stage 8.0 (TID 11) in 121222 ms on ip-172-31-42-183.us-west-2.compute.internal (2/2)
  17/04/23 11:52:13 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 8.0, whose tasks have all completed, from pool
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: Submitting ResultStage 9 (PythonRDD[24] at RDD at PythonRDD.scala:43), which has no missing parents
  17/04/23 11:52:13 INFO storage.MemoryStore: Block broadcast_10 stored as values in memory (estimated size 5.7 KB, free 258.4 KB)
  17/04/23 11:52:13 INFO storage.MemoryStore: Block broadcast_10_piece0 stored as bytes in memory (estimated size 3.4 KB, free 261.8 KB)
  17/04/23 11:52:13 INFO storage.BlockManagerInfo: Added broadcast_10_piece0 in memory on 172.31.34.169:58853 (size: 3.4 KB, free: 517.4 MB)
  17/04/23 11:52:13 INFO spark.SparkContext: Created broadcast 10 from broadcast at DAGScheduler.scala:1006
  17/04/23 11:52:13 INFO scheduler.DAGScheduler: Submitting 1 missing tasks from ResultStage 9 (PythonRDD[24] at RDD at PythonRDD.scala:43)
  17/04/23 11:52:13 INFO scheduler.TaskSchedulerImpl: Adding task set 9.0 with 1 tasks
  17/04/23 11:52:13 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 9.0 (TID 12, ip-172-31-42-183.us-west-2.compute.internal, partition 0,NODE_LOCAL, 1894 bytes)
  17/04/23 11:52:14 INFO storage.BlockManagerInfo: Added broadcast_10_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:53139 (size: 3.4 KB, free: 146.2 MB)
  17/04/23 11:52:14 INFO spark.MapOutputTrackerMasterEndpoint: Asked to send map output locations for shuffle 2 to ip-172-31-42-183.us-west-2.compute.internal:49096
  17/04/23 11:52:14 INFO spark.MapOutputTrackerMaster: Size of output statuses for shuffle 2 is 181 bytes
  17/04/23 11:53:46 INFO storage.BlockManagerInfo: Added rdd_23_0 on ExternalBlockStore on ip-172-31-42-183.us-west-2.compute.internal:53139 (size: 43.7 MB)
  17/04/23 11:53:49 INFO scheduler.DAGScheduler: ResultStage 9 (runJob at PythonRDD.scala:393) finished in 96.440 s
  17/04/23 11:53:49 INFO scheduler.DAGScheduler: Job 4 finished: runJob at PythonRDD.scala:393, took 298.772308 s
  17/04/23 11:53:49 INFO scheduler.TaskSetManager: Finished task 0.0 in stage 9.0 (TID 12) in 96442 ms on ip-172-31-42-183.us-west-2.compute.internal (1/1)
  17/04/23 11:53:49 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 9.0, whose tasks have all completed, from pool
  [(u'\x00\x02', 1), (u'\x06\ufffd\x0e', 1), (u'\x00\x00', 3), (u"\ufffdxF~P\ufffd\ufffdILh\ufffd\ufffd\u07b5\ufffd*\ufffdH=\ufffd'\ufffd", 1), (u'\x06\ufffd\x08', 2), (u'\x06\ufffd\x06', 2), (u'\x00\x08', 4), (u'e}\ufffdn\ufffd\ufffd.\ufffd:\ufffdgV"\ufffd\ufffd\ufffdF\ufffdMS\ufffd\ufffd\u0512\ufffd\x1aI\ufffd\u478f\ufffd\x18\ufffd\ufffd\ufffd\ufffd\ufffd6h\ufffd\'F\x7fh\ufffd\ufffd-\ufffd\ufffd\x16K', 1), (u'\ufffd\u03ef\ufffd\ufffd`\x19-\x08\ufffd\ufffd\ufffd\ufffd*a\ufffd\ufffd\u465fiE\ufffd\u0237\ufffd\ufffd8\u0378\x12{\ufffd\ufffd\x19', 1), (u'\x06\ufffd\x00', 1)]
  >>>
  ```

  ### Conclusion of Tachyon's cache policy:

  Kicking out the oldest file uploaded, according to its upload time.

  Neither the "LRU" or "LFU", because the `myfile2-64M` was just used to generate  `myFile2` and `counts2`,  but it was kicked out by Tachyon: `64.00MB   04-23-2017 10:35:34:987  Not In Memory  /myData/myfile2-64M`.



- What if we want to re-use the file that is kicked out of memory?

  Answer: File-does-not-exist Error: `17/04/23 12:17:42 WARN scheduler.TaskSetManager: Lost task 0.0 in stage 10.0 (TID 13, ip-172-31-42-183.us-west-2.compute.internal): java.io.FileNotFoundException: File does not exist: /LICENSE`

  ```python
  >>> masterIp
  '172.31.34.169'
  >>> file = sc.textFile("tachyon://"+masterIp+":19998/LICENSE")
  17/04/23 12:17:23 INFO storage.MemoryStore: Block broadcast_11 stored as values in memory (estimated size 88.2 KB, free 265.2 KB)
  17/04/23 12:17:23 INFO storage.MemoryStore: Block broadcast_11_piece0 stored as bytes in memory (estimated size 5.6 KB, free 270.8 KB)
  17/04/23 12:17:23 INFO storage.BlockManagerInfo: Added broadcast_11_piece0 in memory on 172.31.34.169:58853 (size: 5.6 KB, free: 517.4 MB)
  17/04/23 12:17:23 INFO spark.SparkContext: Created broadcast 11 from textFile at NativeMethodAccessorImpl.java:-2
  >>> counts = file.flatMap(lambda line: line.split(" ")) \
  ...              .map(lambda word: (word, 1)) \
  ...              .reduceByKey(lambda a, b: a + b)
  17/04/23 12:17:31 INFO : getFileStatus(/LICENSE): HDFS Path: hdfs://ec2-34-208-49-95.us-west-2.compute.amazonaws.com:9000/LICENSE TPath: tachyon://172.31.34.169:19998/LICENSE
  17/04/23 12:17:31 INFO mapred.FileInputFormat: Total input paths to process : 1
  >>> counts.take(2)
  17/04/23 12:17:41 INFO spark.SparkContext: Starting job: runJob at PythonRDD.scala:393
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Registering RDD 28 (reduceByKey at <stdin>:3)
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Got job 5 (runJob at PythonRDD.scala:393) with 1 output partitions
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Final stage: ResultStage 11 (runJob at PythonRDD.scala:393)
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Parents of final stage: List(ShuffleMapStage 10)
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Missing parents: List(ShuffleMapStage 10)
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Submitting ShuffleMapStage 10 (PairwiseRDD[28] at reduceByKey at <stdin>:3), which has no missing parents
  17/04/23 12:17:41 INFO storage.MemoryStore: Block broadcast_12 stored as values in memory (estimated size 8.0 KB, free 278.8 KB)
  17/04/23 12:17:41 INFO storage.MemoryStore: Block broadcast_12_piece0 stored as bytes in memory (estimated size 5.1 KB, free 283.9 KB)
  17/04/23 12:17:41 INFO storage.BlockManagerInfo: Added broadcast_12_piece0 in memory on 172.31.34.169:58853 (size: 5.1 KB, free: 517.4 MB)
  17/04/23 12:17:41 INFO spark.SparkContext: Created broadcast 12 from broadcast at DAGScheduler.scala:1006
  17/04/23 12:17:41 INFO scheduler.DAGScheduler: Submitting 2 missing tasks from ShuffleMapStage 10 (PairwiseRDD[28] at reduceByKey at <stdin>:3)
  17/04/23 12:17:41 INFO scheduler.TaskSchedulerImpl: Adding task set 10.0 with 2 tasks
  17/04/23 12:17:41 INFO scheduler.TaskSetManager: Starting task 0.0 in stage 10.0 (TID 13, ip-172-31-42-183.us-west-2.compute.internal, partition 0,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:41 INFO storage.BlockManagerInfo: Added broadcast_12_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:53139 (size: 5.1 KB, free: 146.2 MB)
  17/04/23 12:17:41 INFO storage.BlockManagerInfo: Added broadcast_11_piece0 in memory on ip-172-31-42-183.us-west-2.compute.internal:53139 (size: 5.6 KB, free: 146.2 MB)
  17/04/23 12:17:42 INFO scheduler.TaskSetManager: Starting task 1.0 in stage 10.0 (TID 14, ip-172-31-42-183.us-west-2.compute.internal, partition 1,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:42 WARN scheduler.TaskSetManager: Lost task 0.0 in stage 10.0 (TID 13, ip-172-31-42-183.us-west-2.compute.internal): java.io.FileNotFoundException: File does not exist: /LICENSE
  	at org.apache.hadoop.hdfs.DFSClient$DFSInputStream.fetchLocatedBlocks(DFSClient.java:2006)
  	at ...

  17/04/23 12:17:43 INFO scheduler.TaskSetManager: Starting task 0.1 in stage 10.0 (TID 15, ip-172-31-42-183.us-west-2.compute.internal, partition 0,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:43 WARN scheduler.TaskSetManager: Lost task 1.0 in stage 10.0 (TID 14, ip-172-31-42-183.us-west-2.compute.internal): java.io.IOException: Block 16777216 is not available in Tachyon
  	at tachyon.client.block.TachyonBlockStore.getInStream(TachyonBlockStore.java:99)
  	at ...

  17/04/23 12:17:44 INFO scheduler.TaskSetManager: Starting task 1.1 in stage 10.0 (TID 16, ip-172-31-42-183.us-west-2.compute.internal, partition 1,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:44 INFO scheduler.TaskSetManager: Lost task 0.1 in stage 10.0 (TID 15) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.FileNotFoundException (File does not exist: /LICENSE) [duplicate 1]
  17/04/23 12:17:45 INFO scheduler.TaskSetManager: Starting task 0.2 in stage 10.0 (TID 17, ip-172-31-42-183.us-west-2.compute.internal, partition 0,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:45 INFO scheduler.TaskSetManager: Lost task 1.1 in stage 10.0 (TID 16) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.IOException (Block 16777216 is not available in Tachyon) [duplicate 1]
  17/04/23 12:17:46 INFO scheduler.TaskSetManager: Starting task 1.2 in stage 10.0 (TID 18, ip-172-31-42-183.us-west-2.compute.internal, partition 1,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:46 INFO scheduler.TaskSetManager: Lost task 0.2 in stage 10.0 (TID 17) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.FileNotFoundException (File does not exist: /LICENSE) [duplicate 2]
  17/04/23 12:17:47 INFO scheduler.TaskSetManager: Starting task 0.3 in stage 10.0 (TID 19, ip-172-31-42-183.us-west-2.compute.internal, partition 0,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:47 INFO scheduler.TaskSetManager: Lost task 1.2 in stage 10.0 (TID 18) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.IOException (Block 16777216 is not available in Tachyon) [duplicate 2]
  17/04/23 12:17:48 INFO scheduler.TaskSetManager: Starting task 1.3 in stage 10.0 (TID 20, ip-172-31-42-183.us-west-2.compute.internal, partition 1,PROCESS_LOCAL, 2129 bytes)
  17/04/23 12:17:48 INFO scheduler.TaskSetManager: Lost task 0.3 in stage 10.0 (TID 19) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.FileNotFoundException (File does not exist: /LICENSE) [duplicate 3]
  17/04/23 12:17:48 ERROR scheduler.TaskSetManager: Task 0 in stage 10.0 failed 4 times; aborting job
  17/04/23 12:17:48 INFO scheduler.TaskSchedulerImpl: Cancelling stage 10
  17/04/23 12:17:48 INFO scheduler.TaskSchedulerImpl: Stage 10 was cancelled
  17/04/23 12:17:48 INFO scheduler.DAGScheduler: ShuffleMapStage 10 (reduceByKey at <stdin>:3) failed in 7.007 s
  17/04/23 12:17:48 INFO scheduler.DAGScheduler: Job 5 failed: runJob at PythonRDD.scala:393, took 7.033980 s
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/root/spark/python/pyspark/rdd.py", line 1297, in take
      res = self.context.runJob(self, takeUpToNumLeft, p)
    File "/root/spark/python/pyspark/context.py", line 939, in runJob
      port = self._jvm.PythonRDD.runJob(self._jsc.sc(), mappedRDD._jrdd, partitions)
    File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/java_gateway.py", line 813, in __call__
    File "/root/spark/python/pyspark/sql/utils.py", line 45, in deco
      return f(*a, **kw)
    File "/root/spark/python/lib/py4j-0.9-src.zip/py4j/protocol.py", line 308, in get_return_value
  py4j.protocol.Py4JJavaError17/04/23 12:17:48 INFO scheduler.TaskSetManager: Lost task 1.3 in stage 10.0 (TID 20) on executor ip-172-31-42-183.us-west-2.compute.internal: java.io.IOException (Block 16777216 is not available in Tachyon) [duplicate 3]
  17/04/23 12:17:48 INFO scheduler.TaskSchedulerImpl: Removed TaskSet 10.0, whose tasks have all completed, from pool
  : An error occurred while calling z:org.apache.spark.api.python.PythonRDD.runJob.
  : org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 10.0 failed 4 times, most recent failure: Lost task 0.3 in stage 10.0 (TID 19, ip-172-31-42-183.us-west-2.compute.internal): java.io.FileNotFoundException: File does not exist: /LICENSE
  	at org.apache.hadoop.hdfs.DFSClient$DFSInputStream.fetchLocatedBlocks(DFSClient.java:2006)
  	at ...

  Driver stacktrace:
  	at org.apache.spark.scheduler.DAGScheduler.org$apache$spark$scheduler$DAGScheduler$$failJobAndIndependentStages(DAGScheduler.scala:1431)
  	at ...

  >>>
  ```


-   It is said that the file can be reload to memory by `./bin/tachyon tfs load <path>` according to

  `https://groups.google.com/forum/#!topic/alluxio-users/mGlUct4eTzc`, but it seems doesn't work.

  ```bash
  root@ip-172-31-34-169 tachyon]$ ./bin/tachyon tfs load /myData/myfile2-64M
  Block 553648128 is not available in Tachyon
  ```

- What if changing the storage level?

  > Storage Level: https://spark.apache.org/docs/latest/programming-guide.html#rdd-persistence
  >
  > ​
  >
  > | Storage Level                          | Meaning                                  |
  > | -------------------------------------- | ---------------------------------------- |
  > | MEMORY_ONLY                            | Store RDD as deserialized Java objects in the JVM. If the RDD does not fit in memory, some partitions will not be cached and will be recomputed on the fly each time they're needed. This is the default level. |
  > | MEMORY_AND_DISK                        | Store RDD as deserialized Java objects in the JVM. If the RDD does not fit in memory, store the partitions that don't fit on disk, and read them from there when they're needed. |
  > | MEMORY_ONLY_SER (Java and Scala)       | Store RDD as *serialized* Java objects (one byte array per partition). This is generally more space-efficient than deserialized objects, especially when using a [fast serializer](https://spark.apache.org/docs/latest/tuning.html), but more CPU-intensive to read. |
  > | MEMORY_AND_DISK_SER (Java and Scala)   | Similar to MEMORY_ONLY_SER, but spill partitions that don't fit in memory to disk instead of recomputing them on the fly each time they're needed. |
  > | DISK_ONLY                              | Store the RDD partitions only on disk.   |
  > | MEMORY_ONLY_2, MEMORY_AND_DISK_2, etc. | Same as the levels above, but replicate each partition on two cluster nodes. |
  > | OFF_HEAP (experimental)                | Similar to MEMORY_ONLY_SER, but store the data in [off-heap memory](https://spark.apache.org/docs/latest/configuration.html#memory-management). This requires off-heap memory to be enabled. |
  >

  - MEMORY_AND_DISK

  ```python
  masterIp = '172.31.34.169'
  myFile3 = sc.textFile("tachyon://"+masterIp+":19998/myData/myfile3-64M")
  counts3 = myFile3.flatMap(lambda line: line.split()) \
                   .map(lambda word: (word, 1)) \
                   .reduceByKey(lambda a, b: a + b)
  counts3.persist(StorageLevel.MEMORY_AND_DISK)
  counts3.take(10)
  ```

  The Output: the used space doesn't change. But the actions are speeded up. Weird.

  -   MEMORY_ONLY

  ```python
  masterIp = '172.31.34.169'
  myFile4 = sc.textFile("tachyon://"+masterIp+":19998/myData/myfile4-64M")
  counts4 = myFile4.flatMap(lambda line: line.split()) \
                   .map(lambda word: (word, 1)) \
                   .reduceByKey(lambda a, b: a + b)
  counts4.persist(StorageLevel.MEMORY_ONLY)
  counts4.take(10)
  ```

  The Output: the used space doesn't change. But the actions are speeded up. Weird.

  ​




## Next Step

### Mount Tiered Storage

Reference: https://github.com/qzweng/alluxio/blob/branch-0.8/docs/Tiered-Storage-on-Tachyon.md#evictors



### Customize Evictor?

Reference: https://github.com/qzweng/alluxio/blob/branch-0.8/docs/Tiered-Storage-on-Tachyon.md#evictors

> Tachyon uses evictors for deciding which blocks to move to a lower tier, when space needs to be freed. Tachyon supports custom evictors, and implementations include:
>
> - **GreedyEvictor**
>
>   Evicts arbitrary blocks until the required size is freed.
>
> - **LRUEvictor**
>
>   Evicts the least-recently-used blocks until the required size is freed.
>
> - **LRFUEvictor**
>
>   Evicts blocks based on least-recently-used and least-frequently-used with a configurable weight. If the weight is completely biased toward least-recently-used, the behavior will be the same as the LRUEvictor.
>
> - **PartialLRUEvictor**
>
>   Evicts based on least-recently-used but will choose StorageDir with maximum free space and only evict from that StorageDir.
>
> In the future, additional evictors will be available. Since Tachyon supports custom evictors, you can also develop your own evictor appropriate for your workload.
>
> When using synchronous eviction, it is recommended to use small block size (around 64MB), to reduce the latency of block eviction. When using the [space reserver](https://github.com/qzweng/alluxio/blob/branch-0.8/docs/Tiered-Storage-on-Tachyon.md#space-reserver), block size does not affect eviction latency.
