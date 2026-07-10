#!/system/bin/sh
ROOT=/data/local/tmp/chroot/debian
chroot "$ROOT" /bin/sh -c '
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.hermes/hermes-agent/venv/bin
export PYTHONPATH=/root/.hermes/hermes-agent
export HERMES_HOME=/root/.hermes
export HTTPS_PROXY=http://192.168.1.8:10808
export HTTP_PROXY=http://192.168.1.8:10808
export NO_PROXY=127.0.0.1,localhost,192.168.1.0/24
export TELEGRAM_BOT_TOKEN=8858037161:***
export TELEGRAM_ALLOWED_USERS=8858037161
nohup hermes gateway run --replace > /root/.hermes/logs/gateway.log 2>&1 &
echo pid=$!
'
