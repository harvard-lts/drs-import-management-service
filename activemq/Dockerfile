FROM openjdk:8-jdk-alpine

RUN wget https://archive.apache.org/dist/activemq/5.16.3/apache-activemq-5.16.3-bin.tar.gz \
    && tar -xzf apache-activemq-5.16.3-bin.tar.gz && rm apache-activemq-5.16.3-bin.tar.gz

RUN mv apache-activemq-5.16.3 /opt/apache-activemq-5.16.3
RUN sed -i "s|127.0.0.1|0.0.0.0|g" /opt/apache-activemq-5.16.3/conf/jetty.xml

WORKDIR /opt/apache-activemq-5.16.3/bin

ENTRYPOINT ["./activemq","console"]
