import pyspark 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark import SparkContext, SparkConf
from pyspark.sql import Row
from pyspark.sql.types import StructType
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.appName("read_index").getOrCreate()
index_schema = StructType(
    [StructField("url", StringType(), False), StructField("mime", StringType(), True), \
        StructField("mime-detected", StringType(), True), StructField("status", IntegerType(), True), \
            StructField("digest", StringType(), True), StructField("length", IntegerType(), True), \
                StructField("offset", IntegerType(), True), StructField("filename", StringType(), True), \
                    StructField("charset", StringType(), True), StructField("languages", StringType(), True)]
)

df = spark.read.csv("hdfs:///project/index_files/index_no_domain")
df.show(2)
