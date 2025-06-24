FROM python:alpine3.7 
RUN echo "server01" > /etc/hostname
RUN pip install flask urllib3==1.26.16
ADD rest01.py /
WORKDIR /
EXPOSE 10067
ENTRYPOINT ["python"]
CMD ["./rest01.py"]