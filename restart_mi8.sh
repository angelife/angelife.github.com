#!/system/bin/sh
# Kill and restart Mi8 gateway
pkill -9 -f hermes
sleep 2
rm -f /data/local/tmp/chroot/debian/root/.hermes/gateway.lock
rm -f /data/local/tmp/chroot/debian/root/.hermes/hermes.pid
nohup chroot /data/local/tmp/chroot/debian /bin/sh /tmp/start_mi8_chroot.sh > /data/local/tmp/chroot/debian/root/.hermes/logs/gateway.log 2>&1 &
echo RESTART_OK
