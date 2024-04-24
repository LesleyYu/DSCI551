## linux commands used in this Lecture

### running Hadoop 

1. upload the three files (`cars.csv`, `SQL2MR.java`, `WordCount.java`) onto EC2

   In sftp, enter:

   ```sh
   sftp> put cars.csv
   Uploading cars.csv to /home/ubuntu/cars.csv
   cars.csv                                      100%   26KB 831.1KB/s   00:00    
   sftp> put SQL2MR.java
   Uploading SQL2MR.java to /home/ubuntu/SQL2MR.java
   SQL2MR.java                                   100% 2961   164.2KB/s   00:00    
   sftp> put WordCount.java
   Uploading WordCount.java to /home/ubuntu/WordCount.java
   WordCount.java                                100% 3269   222.5KB/s   00:00 
   ```

   

2. In directory `~/hadoop-3.3.6/etc/hadoop`, our `core-site.xml` looks like this:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
   <!--
     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at
   
       http://www.apache.org/licenses/LICENSE-2.0
   
     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. See accompanying LICENSE file.
   -->
   
   <!-- Put site-specific property overrides in this file. -->
   
   <configuration>
       <property>
   			<name>fs.defaultFS</name>
   			<value>hdfs://localhost:9000</value>
       </property>
   </configuration>
   ```

   we need to comment out the `<property>` tag.

   ```xml
   <configuration>
       <!--property>
   				<name>fs.defaultFS</name>
   				<value>hdfs://localhost:9000</value>
       </property-->
   </configuration>
   ```

3. try if hadoop works

   ![image-20240405225219101](/Users/lesley/Library/Application Support/typora-user-images/image-20240405225219101.png)

4. Organize the files: move `cars.csv`, `SQL2MR.java`, `WordCount.java` to a separate directory `MapReduce`.

   ```sh
   mkdir MapReduce
   mv cars.csv SQL2MR.java WordCount.java MapReduce
   cd MapReduce
   ```

5. create a new txt file saying hello world in `MapReduce/input`.

   ```sh
   mkdir input
   cd input 
   touch hello.txt
   nano hello.txt
   ```

   `Hello.txt`looks like this:

   ```
   Hello World
   
   Hello USC
   
   Hello UCLA
   ```

6. compile `WordCount.java`

   ```
   hadoop com.sun.tools.javac.Main WordCount.java
   ```

7. 把 java 编译后的class文件都打包到一个java archive (jar) 文件夹里

   ```
   jar cf wc.jar WordCount*.class
   ```

   

8. 用hadoop指令运行

   ```
   hadoop jar wc.jar WordCount input output
   ```

   input文件夹里就是那个hello.txt。我们可以有多个input。但是output只能有一个，且最好文件夹不存在。

#### Troubleshooting 

follow the **execution** steps in [this link](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html) to format namenode, start dfs, etc.

[录播](https://uscviterbi.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=8fa4ba29-efe4-4d31-81fe-b148000030b8)2:12:50左右



9. 编译成功后，output文件夹内会有运行后的结果

	```sh
	ubuntu@ip-172-31-19-22:~/mapreduce$ cd output
	ubuntu@ip-172-31-19-22:~/mapreduce/output$ cat part-r-00000
	Hello	3
	UCLA	1
	USC	1
	World	1
	```



### What is the relation between *hadoop* and *spark*

Hadoop and Spark are both big data processing frameworks, but they have some key differences and complementary features:

1. Processing Model:
   - Hadoop uses the MapReduce processing model, which is a batch-oriented, two-stage (map and reduce) approach to data processing.
   - Spark, on the other hand, uses a more flexible and efficient processing model based on Resilient Distributed Datasets (RDDs) and Directed Acyclic Graphs (DAGs), which allows for real-time, in-memory processing.
2. Speed:
   - Hadoop is generally slower for certain types of data processing tasks, as it needs to write intermediate results to disk between the map and reduce stages.
   - Spark is designed to be faster, especially for iterative algorithms and interactive data exploration, by leveraging in-memory processing and minimizing disk I/O.
3. Data Storage:
   - Hadoop typically uses the Hadoop Distributed File System (HDFS) for data storage, although it can also work with other storage systems like Amazon S3 or Google Cloud Storage.
   - Spark can work with a variety of data storage systems, including HDFS, Apache Cassandra, Apache HBase, and cloud-based storage solutions.
4. Use Cases:
   - Hadoop is well-suited for batch processing of large datasets, data warehousing, and analysis of historical data.
   - Spark is more versatile and can handle a wider range of use cases, including real-time data processing, machine learning, graph analysis, and interactive data exploration.
5. Integration:
   - Hadoop and Spark are often used together in big data ecosystems. Spark can be run on top of Hadoop's HDFS and use Hadoop's MapReduce framework for certain tasks.
   - Spark can also be used as a standalone system, independent of Hadoop, and can integrate with other data storage and processing technologies.

In summary, Hadoop and Spark are complementary technologies that address different aspects of big data processing. Hadoop is well-suited for batch processing of large datasets, while Spark is more versatile and can handle a wider range of real-time and interactive data processing tasks. Many organizations use both Hadoop and Spark, depending on the specific requirements of their big data workloads.



## 讲`WordCount.java`文件

[录播](https://uscviterbi.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=8fa4ba29-efe4-4d31-81fe-b148000030b8)2:31:50左右开始

原本文件的`TokenizerMapper` 类长这样：

```java
public static class TokenizerMapper 
       extends Mapper<Object, Text, Text, IntWritable>{
    
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        word.set(itr.nextToken());
        context.write(word, one);
      }    
    }
  }
```

改成这样：

```java
public static class TokenizerMapper 
       extends Mapper<Object, Text, Text, IntWritable>{
    
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

      // key = 0, value = "hello world"
      
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      // StringTokenizer itr = new StringTokenizer(value.toString());
      // while (itr.hasMoreTokens()) {
      //   word.set(itr.nextToken());
      //   context.write(word, one);
      // }
      String[] toks = value.toString().split();

      for (String tok: toks) {
        System.out.print(tok + ",");
      }
      System.out.println();
    }
}
```

编译之后有bug，然后他说 算了 （？？）

我把 `.split();`改成`.split(" ");`之后编译，得到的运行结果是：

```sh
ubuntu@ip-172-31-19-22:~/mapreduce/output$ cat part-r-00000
ubuntu@ip-172-31-19-22:~/mapreduce/output$ 
```

什么都没有。迷惑。不管了



## 讲`SQL2MR.java`文件

[录播](https://uscviterbi.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=8fa4ba29-efe4-4d31-81fe-b148000030b8)2:42:50左右开始



*小技巧：

1) `history|grep hadoop` 可以查看含有关键词 `hadoop` 的历史指令。
1) `!1842`可以重新执行序号所指的那条指令。



1. compile `SQL2MR.java`

   ```sh
   hadoop com.sun.tools.javac.Main SQL2MR.java
   ```

2. 创建 cars.csv 的input文件夹，并把cars.csv复制放进去：

   ```sh
   ubuntu@ip-172-31-19-22:~/mapreduce$ mkdir input-cars
   ubuntu@ip-172-31-19-22:~/mapreduce$ cd input-cars
   ubuntu@ip-172-31-19-22:~/mapreduce/input-cars$ cp ../cars.csv .
   ubuntu@ip-172-31-19-22:~/mapreduce/input-cars$ ls
   cars.csv
   ```

3. 把 java 编译后的class文件都打包到一个java archive (jar) 文件夹里

   ```sh
   jar cf sql2mr.jar SQL2MR*.class
   ```

4. 用hadoop指令运行

   ```sh
   hadoop jar sql2mr.jar SQL2MR input-cars output-cars
   ```

5. 看output-cars 里面的文件，什么都没有。迷惑。不管了，他说下次再说。



### hw5

```sql
SELECT rating, avg(replacement_cost)
FROM film
WHERE length >= 60
GROUP BY rating
HAVING count(*) >= 160
```

> `HAVING count(*) >= 160` means that after the data has been grouped by the rating column, only those groups (ratings) where the count of films is 160 or more will be included in the final result.

Q1 编译指令

```sh
rm -rf *.class output *.class
```

```sh
hadoop com.sun.tools.javac.Main SQL2MR.java
```

```sh
jar cf sql2mr.jar SQL2MR*.class
```

```sh
hadoop jar sql2mr.jar SQL2MR input output
```



Q2

##### 本地安装 pyspark 环境  - [官方教程](https://pyspark.itversity.com/01_getting_started_pyspark/04_setup_spark_locally_mac.html)

- Here are the pre-requisites to setup Spark Locally on mac.
  - At least 8 GB RAM is highly desired.
  - Make sure JDK 1.8 is setup
  - Make sure to have Python 3. If you do not have it, you can install it using **homebrew**.
- Here are the steps to setup Pyspark and validate.
  - Create Python Virtual Environment  `python3 -m venv spark-venv`.
  - Activate the virtual environment  `source spark-venv/bin/activate`.
  - Run `pip install pyspark==2.4.6` to install Spark 2.4.6.
  - Run `pyspark` to launch Spark CLI using Python as programming language.

这个环境安装成功了，但是跑pyspark还是不行，算了。



c.

```sql
SELECT actor_id FROM film_actor WHERE film_id = 1) intersect
(SELECT actor_id FROM film_actor where film_id = 23)
```

d.

```sql
SELECT DISTINCT first_name, last_name
FROM actor JOIN film_actor 
ON actor.actor_id = film_actor.actor_id 
WHERE film_id in (1, 2, 3)
ORDER BY first_name
LIMIT 5
```

e.

```sql
SELECT rental_duration, rating, min(length), max(length), avg(length), count(length) 
FROM film
GROUP BY rental_duration, rating 
ORDER BY rental_duration desc 
LIMIT 10
```

