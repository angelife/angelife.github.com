#!/system/bin/sh
ROOT=/data/local/tmp/chroot/debian
# 将修复脚本写入 chroot /tmp
cp /data/local/tmp/start_mi8_fixed.sh "$ROOT/tmp/start_mi8_fixed.sh"
chmod 755 "$ROOT/tmp/start_mi8_fixed.sh"
# 通过 chroot 执行
exec chroot "$ROOT" /bin/sh /tmp/start_mi8_fixed.sh
