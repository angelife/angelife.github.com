#!/system/bin/sh
MOUNT=/data/local/tmp/chroot/debian
ROOTFS=/data/local/tmp/debian/debian-rootfs
ETH_SETUP=/data/local/tmp/eth-setup/eth-static.sh
LOG=/data/local/tmp/chroot-start.log
mount --bind "$ROOTFS" "$MOUNT"
mount -t proc proc "$MOUNT/proc"
mount -t sysfs sysfs "$MOUNT/sys"
mount --rbind /dev "$MOUNT/dev"
[ -x "$ETH_SETUP" ] && su 0 -c "$ETH_SETUP" >/dev/null 2>&1 || true
exec >>"$LOG" 2>&1
echo chroot-services-started
while true; do
  if ! chroot "$MOUNT" /bin/bash -lc "pgrep -x alist >/dev/null 2>&1"; then
    chroot "$MOUNT" /bin/bash -lc "cd /data/alist && nohup alist server --force-bin-dir > /var/log/alist/alist.log 2>&1 &" || true
  fi
  if ! chroot "$MOUNT" /bin/bash -lc "pgrep -x aria2c >/dev/null 2>&1"; then
    chroot "$MOUNT" /bin/bash -lc "nohup aria2c --conf-path=/etc/aria2/aria2.conf -D > /var/log/aria2/aria2.log 2>&1 &" || true
  fi
  if ! chroot "$MOUNT" /bin/bash -lc "pgrep -x nginx >/dev/null 2>&1"; then
    chroot "$MOUNT" /bin/bash -lc "nginx -c /etc/nginx/nginx.conf || nginx || true" || true
  fi
  sleep 30
done
