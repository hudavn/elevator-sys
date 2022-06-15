FROM ubuntu:18.04

RUN ln -s /usr/share/zoneinfo/Etc/GMT+7 /etc/localtime
RUN apt update \
    && apt install -y git python3 python3-pip

RUN git clone https://github.com/hudavn/elevator-sys.git
RUN cd elevator-sys/backend && \
    pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "/elevator-sys/entrypoint.sh" ]