from pyspark.sql import SparkSession

class _SparkSessionLoader:
    def __init__(self):
        self._spark_session = SparkSession \
            .builder \
            .appName("Spark_ETL_Server") \
            .getOrCreate()
        self._spark_session.conf.set("spark.sql.shuffle.partitions", 5)
        self._spark_session.conf.set("spark.sql.session.timeZone", "UTC")
    def getSparkSession(self):
        return self._spark_session
