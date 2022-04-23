from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
import string

#trailing_punctuation = '!,.;?'

def n_grams(words_list, n):
    ngrams_list = []
    if n > len(words_list):
        return ngrams_list
    for i in range(len(words_list)-n+1):
        tmp = ['']*n
        for j in range(n):
            tmp[j] = words_list[i+j]
        tmp_str = ' '.join(tmp)
        ngrams_list.append(tmp_str)
    return ngrams_list

def remove_punctuation(x):
    tmp = ''
    for i in range(len(x)):
        if x[i] not in string.punctuation:
            tmp = tmp + x[i].lower()
    return tmp

#spark = SparkSession.builder.appName("read_wet").getOrCreate()
#df = spark.read.text("hdfs:///project/wet_files/1_extracted_from_wet_files")
#rdd = SparkContext.textFile("hdfs:///project/wet_files/1_extracted_from_wet_files")
sc = SparkContext.getOrCreate(SparkConf())
rdd = sc.textFile("hdfs:///project/wet_files/3_extracted_from_wet_files")
ngram_count = rdd.map(remove_punctuation).flatMap(lambda x: n_grams(x.split(),3)).map(lambda x: (x, 1)).combineByKey(lambda v: v, lambda acc, v: acc + v, lambda acc1, acc2: acc1 + acc2)
ngram_count.saveAsTextFile("hdfs:///project/output_files/spark_ngram_count_output/")

