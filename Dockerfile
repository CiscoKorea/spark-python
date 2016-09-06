FROM ubuntu
MAINTAINER Hyung-Soo Kim <hyungsok@cisco.com>

EXPOSE 8080

RUN apt-get update && apt-get install python python-pip git -y 
RUN mkdir -p /opt
WORKDIR /opt
RUN git clone https://github.com/CiscoKorea/spark-python  sparkapp
WORKDIR /opt/sparkapp
RUN python setup.py install 
RUN pip install flask
WORKDIR /opt/sparkapp/samples 
CMD python spark_gui.py 
