FROM python:alpine3.7 
RUN echo "server02" > /etc/hostname
RUN pip install flask urllib3==1.26.16
ADD rest02.py /
WORKDIR /
EXPOSE 10069
ENTRYPOINT ["python"]
CMD ["./rest02.py"]