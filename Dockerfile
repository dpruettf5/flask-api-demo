FROM python:3.9-slim-bullseye

LABEL author="LLC"

ENV TZ=Asia/Shanghai

COPY requirements.txt /tmp/requirements.txt

RUN \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free">> /etc/apt/sources.list  && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free">> /etc/apt/sources.list  && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free">> /etc/apt/sources.list  && \
    \
    apt-get update && \
    apt-get install -y gcc python3-dev --no-install-recommends && \
    \
    python -m pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip install supervisor uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    \
    echo_supervisord_conf > /etc/supervisord.conf && \
    echo "[include]" >> /etc/supervisord.conf && \
    echo "files = /etc/supervisord.d/*.ini" >> /etc/supervisord.conf && \
    \
    apt-get purge -y gcc  python3-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip/*


WORKDIR /work/src

ENV PYTHONPATH=/work/src

COPY conf/uwsgi.ini /work/conf/uwsgi.ini
COPY conf/supervisor.ini /etc/supervisord.d/supervisor.ini
COPY src /work/src


ENTRYPOINT ["supervisord", "-n","-c", "/etc/supervisord.conf"]
