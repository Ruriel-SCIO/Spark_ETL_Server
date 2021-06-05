FROM python:3.9.5-slim
ARG JAVA_VERSION="8.0.292-open"
ARG SPARK_VERSION="3.1.2"
ARG HADOOP_VERSION="3.2"
ENV SPARK_HOME="/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION"
ENV JAVA_HOME="/root/.sdkman/candidates/java/current"
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
COPY ./config/log4j.properties ${SPARK_HOME}/conf
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache --no-warn-script-location -r requirements.txt
COPY src/ ./src/
CMD [ "python", "src/main.py" ]
