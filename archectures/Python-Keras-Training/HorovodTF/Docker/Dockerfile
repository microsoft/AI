FROM nvidia/cuda:9.0-devel-ubuntu16.04

# TensorFlow version is tightly coupled to CUDA and cuDNN so it should be selected carefully
ENV PYTHON_VERSION=3.5
ENV TENSORFLOW_VERSION=1.9.0
ENV CUDNN_VERSION=7.0.5.15-1+cuda9.0

RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && apt-get install -y --no-install-recommends  --allow-downgrades --allow-change-held-packages  \
        build-essential \
        cmake \
        cpio \
        git \
        curl \
        wget \
        ca-certificates \
        libdapl2 \
        libcudnn7=$CUDNN_VERSION \
        libjpeg-dev \
        libpng-dev \
        libmlx4-1 \
        libsm6 \
        libxext6 \
        python$PYTHON_VERSION \
        python$PYTHON_VERSION-dev


# install intel MPI
RUN cd /tmp && \
    wget -q 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11595/l_mpi_2017.3.196.tgz' && \
    tar zxvf l_mpi_2017.3.196.tgz && \
    sed -i -e 's/^ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' /tmp/l_mpi_2017.3.196/silent.cfg && \
    sed -i -e 's|^#ACTIVATION_LICENSE_FILE=|ACTIVATION_LICENSE_FILE=/tmp/l_mpi_2017.3.196/USE_SERVER.lic|g' \
    			/tmp/l_mpi_2017.3.196/silent.cfg && \
    sed -i -e 's/^ACTIVATION_TYPE=exist_lic/ACTIVATION_TYPE=license_server/g' /tmp/l_mpi_2017.3.196/silent.cfg && \
    cd /tmp/l_mpi_2017.3.196 && \
    ./install.sh -s silent.cfg && \
    cd .. && \
    rm -rf l_mpi_2017.3.196* && \
    echo "source /opt/intel/compilers_and_libraries_2017.4.196/linux/mpi/intel64/bin/mpivars.sh" >> ~/.bashrc

ENV PATH $PATH:/opt/intel/compilers_and_libraries/linux/mpi/bin64

RUN ln -s /usr/bin/python$PYTHON_VERSION /usr/bin/python

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install TensorFlow
RUN pip install --no-cache-dir tensorflow-gpu==$TENSORFLOW_VERSION h5py scipy jupyter ipykernel numpy toolz pandas \
 	scikit-learn

# Install Horovod, temporarily using CUDA stubs
RUN ldconfig /usr/local/cuda-9.0/targets/x86_64-linux/lib/stubs && \
    /bin/bash -c "source /opt/intel/compilers_and_libraries_2017.4.196/linux/mpi/intel64/bin/mpivars.sh" && \
    HOROVOD_WITH_TENSORFLOW=1 pip install --no-cache-dir horovod==0.13.2 && \
    ldconfig