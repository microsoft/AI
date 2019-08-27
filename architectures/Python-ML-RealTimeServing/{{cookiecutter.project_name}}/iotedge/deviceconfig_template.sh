
# Install the repository configuration. Replace <release> with 16.04 or 18.04 as appropriate for your release of Ubuntu
curl https://packages.microsoft.com/config/ubuntu/__release/prod.list > ./microsoft-prod.list

# Copy the generated list
sudo cp ./microsoft-prod.list /etc/apt/sources.list.d/

#Install Microsoft GPG public key
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo cp ./microsoft.gpg /etc/apt/trusted.gpg.d/

#################################################################################
#Install the container runtime. It can be skipped if Docker is already installed

# Update the apt package index
#sudo apt-get update

# Install the Moby engine.
#sudo apt-get install moby-engine
################################################################################

# Install the Azure IoT Edge Security Daemon
# Perform apt update
sudo apt-get update

# Install the Moby command-line interface (CLI). The CLI is useful for development but optional for production deployments.
sudo apt-get install moby-cli

# Install the security daemon. The package is installed at /etc/iotedge/.
sudo apt-get install iotedge -y --no-install-recommends
################################################################################

#Configure the Azure IoT Edge Security
# Manual provisioning IoT edge device
sudo sed -i "s#\(device_connection_string: \).*#\1\"__device_connection_string\"#g" /etc/iotedge/config.yaml

############################################

# double check if the IP address of the docker0 interface is 172.17.01 by using ifconfig command
sudo sed -i "s#\(management_uri: \).*#\1\"__management_uri\"#g" /etc/iotedge/config.yaml
sudo sed -i "s#\(workload_uri: \).*#\1\"__workload_uri\"#g" /etc/iotedge/config.yaml

# restart the daemon
sudo systemctl restart iotedge
###########################################

# Verify successful installation

# check the status of the IoT Edge Daemon
systemctl status iotedge

# Examine daemon logs
journalctl -u iotedge --no-pager --no-full