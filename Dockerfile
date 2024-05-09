FROM python:3.9
RUN pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install sqlitedict==2.1.0
RUN echo 'ICED{SqL_and_0day_mast3r}' > /flag
WORKDIR /app
COPY . /app
RUN rm /app/Dockerfile
RUN chmod 777 /app
RUN python3 generator.py
ENTRYPOINT [ "python3" ]
CMD ["render.py" ]
