#Uses python slim as base since it's the best cost benefit between size and stability.
FROM python:3.9.5-slim
#Sets the Java version that will be downloaded by Sdkman.
ARG JAVA_VERSION="8.0.292-open"
#Sets the Spark version that will be downloaded from Apache.
ARG SPARK_VERSION="3.1.2"
#Sets the Hadoop version that Spark is based on. However, this image only downloads Spark.
ARG HADOOP_VERSION="3.2"
#Folder where Spark will be saved.
ENV SPARK_HOME="/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION"
#Folder where Java 8 will be saved.
ENV JAVA_HOME="/root/.sdkman/candidates/java/current"
#Installs zip, unzip and curl. After that, downloads Spark and Sdkman. Then, we install Java 8, move
#Spark to its folder and remove all the temporary files involved, including zip, unzip and curl.
RUN apt-get --quiet update \
&& apt-get --quiet -y install --no-install-recommends zip unzip curl \
&& rm -rf /var/lib/apt/lists/* \
&& rm -rf /tmp/* \
&& mkdir /downloads \
&& cd /downloads \
&& curl https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
-o spark.tgz \
&& tar -zxf spark.tgz --directory / \
&& curl -s "https://get.sdkman.io" | bash \
&& bash -c "source ${HOME}/.sdkman/bin/sdkman-init.sh \
&& yes | sdk install java ${JAVA_VERSION}" \
&& rm -rf /root/.sdkman/archives/* \
&& rm -rf /root/.sdkman/tmp/* \
&& apt-get remove --quiet -y zip unzip curl \
&& apt-get --quiet -y clean \
&& apt-get --quiet -y autoclean \
&& apt-get --quiet -y autoremove \
&& cd /spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} \
&& rm -rf /downloads
#Copies the log4j configuration to Spark. This configuration sets the log root level to ERROR.
COPY ./config/log4j.properties ${SPARK_HOME}/conf
WORKDIR /app
#Copies and installs the dependencies of the project.
COPY requirements.txt .
RUN pip install --user --no-cache --no-warn-script-location -r requirements.txt
#Copies the code and starts it.
COPY src/ ./src/
CMD [ "python", "src/main.py" ]
