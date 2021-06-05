from pyspark.sql import SparkSession

#Prepares the Spark Session.
class _SparkSessionLoader:
    def __init__(self):
        self._spark_session = SparkSession \
            .builder \
            .appName("Spark_ETL_Server") \
            .getOrCreate()
        #We set 5 partitions to deal with the data.
        self._spark_session.conf.set("spark.sql.shuffle.partitions", 5)
        #Sets the timezone to UTC to deal with the dates as is.
        self._spark_session.conf.set("spark.sql.session.timeZone", "UTC")
    def getSparkSession(self):
        return self._spark_session
