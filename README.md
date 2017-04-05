# spark-ec2-bench
Running Spark 1.6.2 on Tachyon 0.8.2 on EC2, spark-bench by SparkTC

### Launch a Cluster on EC2

- Under /usr/local/spark-1.6.2-bin-hadoop2.6/ec2  

  ```
  ./spark-ec2 -k ec2-key-oregon -i ~/AWS/IMPORTANT_PEM/ec2-key-oregon.pem -s 1 --region=us-west-2 --zone=us-west-2a --instance-type=t2.micro launch mytest
  ```

  - instanceType = t2.micro

### Init

- Login:

  ```
  ./spark-ec2 -k ec2-key-oregon -i ~/AWS/IMPORTANT_PEM/ec2-key-oregon.pem --region=us-west-2 --zone=us-west-2a login mytest
  ```

- Update:  `sudo yum -y update` 

- Install mvn: 

  ```
  cd /opt
  wget "http://apache.communilink.net/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz"
  sudo tar xzf apache-maven-3.3.9-bin.tar.gz
  sudo ln -s apache-maven-3.3.9 maven
  sudo vi /etc/profile.d/maven.sh
  ```

  - ```
    export M2_HOME=/opt/maven
    export PATH=${M2_HOME}/bin:${PATH}
    ```

  ```
  source /etc/profile.d/maven.sh
  mvn -version
  ```

------

### File Transfer

- On local: ` scp -i ec2-key-oregon.pem ~/Desktop/1184-0.txt root@52.33.194.128:/root/`
- On Master:`/root/ephemeral-hdfs/bin/hadoop fs -put 1184-0.txt /`
- Now the file is stored at `hdfs://172.31.47.83:9000/1184-0.txt`

### Run Applications

- Run python: `/root/spark/bin/pyspark`
- Run Example:
  - Hadoop fs -put`/root/ephemeral-hdfs/bin/hadoop fs -put /root/spark/data/mllib/sample_linear_regression_data.txt /``
  - Run LinearRegression: ``/root/spark/bin/run-example org.apache.spark.examples.mllib.LinearRegression hdfs://172.31.47.83:9000/sample_linear_regression_data.txt`

### Monitoring

- webUI:

  - Spark: `http://<public-ip-address-of-master>:8080/`  // or  `:4040` 
  - HDFS: `http://<public-ip-address-of-master>:50070/`
  - Tachyon: `http://<public-ip-address-of-master>:19999` 

  > Reference: https://spark.apache.org/docs/1.6.2/monitoring.html

------

### Spark-bench

#### Setup

- Install Java 8 (see solution below "Install WikiXMLj")


- Install WikiXMLJ:

  ```
  cd /root/
  git clone https://github.com/synhershko/wikixmlj.git
  cd wikixmlj
  mvn package install
  ```

  - **BUG**:  (52.0 is Java 8)

  - ```
    Running edu.jhu.nlp.wikipedia.WikiXMLParserTest
    Tests run: 1, Failures: 0, Errors: 1, Skipped: 0, Time elapsed: 0.076 sec <<< FAILURE!
    testSaxParser(edu.jhu.nlp.wikipedia.WikiXMLParserTest)  Time elapsed: 0.027 sec  <<< ERROR!
    java.lang.UnsupportedClassVersionError: org/apache/tools/bzip2/CBZip2InputStream : Unsupported major.minor version 52.0
    ```

    Linux version: `Linux version 3.4.37-40.44.amzn1.x86_64 (mockbuild@gobi-build-31005) (gcc version 4.6.3 20120306 (Red Hat 4.6.3-2) (GCC) ) #1 SMP Thu Mar 21 01:17:08 UTC 2013`

    Java version: `java version "1.7.0_131"`
    `OpenJDK Runtime Environment (amzn-2.6.9.0.71.amzn1-x86_64 u131-b00)`
    `OpenJDK 64-Bit Server VM (build 24.131-b00, mixed mode)`

  - **Solution**: Install Java 8

  - ```
    cd /opt/
    wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jdk-8u121-linux-x64.tar.gz"

    tar xzf jdk-8u121-linux-x64.tar.gz
    cd /opt/jdk1.8.0_121/
    alternatives --install /usr/bin/java java /opt/jdk1.8.0_121/bin/java 2
    alternatives --config java

    4 #(choose "/opt/jdk1.8.0_121/bin/java")

    alternatives --install /usr/bin/jar jar /opt/jdk1.8.0_121/bin/jar 2
    alternatives --install /usr/bin/javac javac /opt/jdk1.8.0_121/bin/javac 2
    alternatives --set jar /opt/jdk1.8.0_121/bin/jar
    alternatives --set javac /opt/jdk1.8.0_121/bin/javac

    java -version

    export JAVA_HOME=/opt/jdk1.8.0_121
    export JRE_HOME=/opt/jdk1.8.0_121/jre
    export PATH=$PATH:/opt/jdk1.8.0_121/bin:/opt/jdk1.8.0_121/jre/bin
    # Also put all above environment variables in /etc/environment file for auto loading on system boot.
    ```

    - Reference: https://tecadmin.net/install-java-8-on-centos-rhel-and-fedora/

- Install Spark-bench

    Chengliang's version`git clone https://github.com/marcoszh/spark-bench.git`
    original GitHub: `git clone https://github.com/SparkTC/spark-bench.git`

  ```
  cd /root/
  git clone https://github.com/qzweng/spark-bench.git # My version for Spark 1.6
  cd spark-bench
  ./bin/build-all.sh
  ```

  - Reference: https://github.com/SparkTC/spark-bench

  Copy `<SparkBench_Root>/conf/env.sh.template` to `<SparkBench_Root>/conf/env.sh`, and set it according to your cluster.

- Update $PATH:

  > Actually may not need to do update the SPARK_MASTER or HDFS_MASTER.
  > Instead, edit the `testBench/spark-bench/conf/env.sh`

  ```
  ## export PUBLIC_IP_ADDRESS=<public-ip-address-of-master>
  export SPARK_HOME=/root/spark
  export HADOOP_HOME=/root/ephemeral-hdfs
  export HADOOP_PREFIX=${HADOOP_HOME}
  # the data in this HDFS goes away when restart, 
  # otherwise, please use /root/persistent-hdfs

  ## export SPARK_MASTER=spark://$PUBLIC_IP_ADDRESS:7077
  ## export HDFS_MASTER=hdfs://$PUBLIC_IP_ADDRESS:8020/root/
  # The default address of namenode web UI is http://localhost:50070/
  # The default address of namenode server is hdfs://localhost:8020/

  export PATH=$SPARK_HOME:$HADOOP_HOME:$HADOOP_PREFIX/bin:$PATH
  ## export PATH=$SPARK_MASTER:$HDFS_MASTER:$PATH
  ```

- Link hadoop with hdfs (in $HADOOP_HOME)
  `ln -s $HADOOP_HOME/bin/hadoop $HADOOP_HOME/bin/hdfs`

#### Execute

- Generate data & Run, e.g. SQL

  ```
  ./SQL/bin/gen_data.sh
  ./SQL/bin/run.sh
  ```

  - BUG1

    `du: Cannot access -s: No such file or directory.`
    `du: unknown host: pts00450-vm16`

  - SOLUTION1: edit the `spark-bench/conf/env.sh`  should be

    ```
    master=`cat /root/spark-ec2/masters` # CHANGE HERE
    	# public-ip-address does not work here, have to be the entire name
    MC_LIST=`cat /root/spark-ec2/slaves` # CHANGE HERE # The list of workers

    [ -z "$HADOOP_HOME" ] &&     export HADOOP_HOME=/root/ephemeral-hdfs # CHANGE HERE
    # base dir for DataSet
    HDFS_URL="hdfs://${master}:9000"
    HDFS_MASTER=$HDFS_URL
    SPARK_HADOOP_FS_LOCAL_BLOCK_SIZE=536870912

    DATA_HDFS="hdfs://${master}:9000/SparkBench"

    #Local dataset optional
    #DATASET_DIR=/home/`whoami`/SparkBench/dataset # CHANGE HERE

    SPARK_VERSION=1.6.3  #1.5.1
    [ -z "$SPARK_HOME" ] &&     export SPARK_HOME=/root/spark # CHANGE HERE

    SPARK_MASTER=spark://${master}:7077

    SPARK_SERIALIZER=org.apache.spark.serializer.KryoSerializer
    SPARK_RDD_COMPRESS=false
    SPARK_IO_COMPRESSION_CODEC=lzf

    SPARK_EXECUTOR_MEMORY=1g

    export SPARK_DRIVER_MEMORY=2g
    export SPARK_EXECUTOR_INSTANCES=4
    export SPARK_EXECUTOR_CORES=1

    STORAGE_LEVEL=MEMORY_AND_DISK

    NUM_OF_PARTITIONS=2
    NUM_TRIALS=1
    ```

  - BUG2:  `Unsupported major.minor version 52.0`

  - SOLUTION2: Your spark-bench version doesn't match with your spark or java. checkout an older version of spark-bench, e.g. `cd spark-bench/` `git checkout 2377268a91ba0e814cf08f3afe43d1388b2f0d9a` (2016-11-19)

------

### Run Spark on Tachyon

> Run Spark: http://www.alluxio.org/docs/0.8/Running-Tachyon-on-EC2.html
>
> Application: http://www.alluxio.org/docs/0.8/Getting-Started.html

#### Test Tachyon (version 0.8.2)

- ```
  /tachyon/bin/tachyon runTests
  ```

- Browser: Tachyon: `http://<public-ip-address-of-master>:19999` 

​
