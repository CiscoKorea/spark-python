FROM ubuntu:14.04
MAINTAINER Hyung-Soo Kim <hyungsok@cisco.com>

EXPOSE 8080

RUN apt-get update && apt-get install python python-pip python-dev git -y 
RUN pip install flask
RUN mkdir -p /opt
WORKDIR /opt
RUN git clone https://github.com/CiscoKorea/spark-python  sparkapp
WORKDIR /opt/sparkapp
RUN python setup.py install 
WORKDIR /opt/sparkapp/samples 
CMD python spark_gui.py 
