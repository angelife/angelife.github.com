#!/system/bin/sh
# Kill hermes on Mi6 and clean up
/system/bin/kill -9 $(/system/bin/pidof hermes) 2>/dev/null
/system/bin/pkill -9 -f hermes 2>/dev/null
rm -f /data/local/tmp/chroot/debian/root/.hermes/gateway.lock
rm -f /data/local/tmp/chroot/debian/root/.hermes/hermes.pid
echo DONE
