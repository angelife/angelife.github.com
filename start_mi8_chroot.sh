#!/bin/sh
# chroot 内执行的启动脚本
# 关键修复：set -a 确保 source .env 后所有变量 export 给子进程
set -a
. /root/.hermes/.env
set +a

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.hermes/hermes-agent/venv/bin
export PYTHONPATH=/root/.hermes/hermes-agent
export HERMES_HOME=/root/.hermes
export HTTPS_PROXY=http://192.168.1.8:10808
export HTTP_PROXY=http://192.168.1.8:10808
export NO_PROXY=127.0.0.1,localhost,192.168.1.0/24

# 清理旧锁
rm -f /root/.hermes/gateway.lock /root/.hermes/hermes.pid

# 启动
cd /root/.hermes
nohup hermes gateway run --replace > /root/.hermes/logs/gateway.log 2>&1 &
echo "PID=$!"
