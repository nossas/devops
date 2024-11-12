#!/bin/bash

set -e

progress() {
    echo "[ $(date +'%Y-%m-%d %H:%M:%S') ] $1"
}

run_silent() {
    "$@" > /dev/null 2>&1
}

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo privileges."
    exit 1
fi

progress "Starting Telegraf installation"

progress "Updating package list"
run_silent apt-get update

progress "Adding InfluxData repository"
curl -s https://repos.influxdata.com/influxdata-archive_compat.key > influxdata-archive_compat.key
if echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c; then
    cat influxdata-archive_compat.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
    echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | tee /etc/apt/sources.list.d/influxdata.list
else
    echo "Repository key verification failed. Aborting installation."
    exit 1
fi

progress "Updating package list with new repository"
run_silent apt-get update

progress "Installing Telegraf"
run_silent apt-get install -y telegraf

progress "Copying configuration file"
cp "$(dirname "$0")/config_files/telegraf_cluster_monitor.conf" /etc/telegraf/telegraf.conf

progress "Configuring Telegraf service"
systemctl start telegraf
systemctl enable telegraf

usermod -aG docker telegraf

progress "Restarting Telegraf service"
systemctl restart telegraf

progress "Telegraf installation and configuration completed successfully"
