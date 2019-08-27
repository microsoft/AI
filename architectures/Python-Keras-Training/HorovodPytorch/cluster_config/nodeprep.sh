#!/usr/bin/env bash
sudo cp $AZ_BATCHAI_MOUNT_ROOT/extfs/scripts/docker.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl restart docker
