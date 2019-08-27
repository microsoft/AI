# Dockerfile for Azure CLI and MMLS 9.3 one-box deployment, R only
FROM ubuntu:16.04
RUN apt-get -y update \
    && apt-get install -y apt-transport-https wget \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ xenial main" | tee /etc/apt/sources.list.d/azure-cli.list \
    && wget https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb -O /tmp/prod.deb \
    && dpkg -i /tmp/prod.deb \
    && rm -f /tmp/prod.deb \
    && apt-key adv --keyserver packages.microsoft.com --recv-keys 52E16F86FEE04B979B07E28DB02C46DF417A0893 \
    && apt-get -y update \
    && apt-get install -y microsoft-r-open-foreachiterators-3.4.3 \
    && apt-get install -y microsoft-r-open-mkl-3.4.3 \
    && apt-get install -y microsoft-r-open-mro-3.4.3 \
    && apt-get install -y microsoft-mlserver-packages-r-9.3.0 \
#    && apt-get install -y microsoft-mlserver-python-9.3.0 \
#    && apt-get install -y microsoft-mlserver-packages-py-9.3.0 \
#    && apt-get install -y microsoft-mlserver-mml-r-9.3.0 \
#    && apt-get install -y microsoft-mlserver-mml-py-9.3.0 \
#    && apt-get install -y microsoft-mlserver-mlm-r-9.3.0 \
#    && apt-get install -y microsoft-mlserver-mlm-py-9.3.0 \
    && apt-get install -y azure-cli=2.0.26-1~xenial \
    && apt-get install -y dotnet-runtime-2.0.0 \
    && apt-get install -y microsoft-mlserver-adminutil-9.3.0 \
    && apt-get install -y microsoft-mlserver-config-rserve-9.3.0 \
    && apt-get install -y microsoft-mlserver-computenode-9.3.0 \
    && apt-get install -y microsoft-mlserver-webnode-9.3.0 \
    && /opt/microsoft/mlserver/9.3.0/bin/R/activate.sh

#### Tweaks to run onebox in Kubernetes

RUN echo $'library(jsonlite) \n\
 \n\
settings_file <- "/opt/microsoft/mlserver/9.3.0/o16n/Microsoft.MLServer.WebNode/appsettings.json" \n\
settings <- fromJSON(settings_file) \n\
 \n\
settings$Authentication$JWTSigningCertificate$Enabled <- TRUE \n\
settings$Authentication$JWTSigningCertificate$StoreName <- "Root" \n\
settings$Authentication$JWTSigningCertificate$StoreLocation <- "CurrentUser" \n\
settings$Authentication$JWTSigningCertificate$SubjectName <- "CN=LOCALHOST" \n\
 \n\
writeLines(toJSON(settings, auto_unbox=TRUE, pretty=TRUE), settings_file) \n\
' > configure_jwt_cert.R

RUN chmod +x configure_jwt_cert.R

RUN sed -i 's/grep docker/grep "kubepods\\|docker"/g' /opt/microsoft/mlserver/9.3.0/o16n/Microsoft.MLServer.*Node/autoStartScriptsLinux/*.sh \
    && mkdir -p /home/webnode_usr/.dotnet/corefx/cryptography/x509stores/root \
    && wget https://github.com/Microsoft/microsoft-r/raw/master/mlserver-arm-templates/enterprise-configuration/linux-postgresql/25706AA4612FC42476B8E6C72A97F58D4BB5721B.pfx -O /home/webnode_usr/.dotnet/corefx/cryptography/x509stores/root/25706AA4612FC42476B8E6C72A97F58D4BB5721B.pfx \
    && chmod 666 /home/webnode_usr/.dotnet/corefx/cryptography/x509stores/root/*.pfx \
    && /usr/bin/Rscript configure_jwt_cert.R


##########################################################################################
#### add tools and packages required to load model: this will vary depending on the model
##########################################################################################

# install C and Fortran compilers, needed for randomForest
RUN apt-get install -y make gcc gfortran

# install R package(s)
RUN Rscript -e "install.packages('randomForest')"

RUN mkdir /data
COPY data/service.R /data
COPY data/model.rds /data
WORKDIR /data


############################################################################################
#### startup script -- this will also vary depending on the authentication method
############################################################################################

RUN echo $'#!/bin/bash \n\
set -e \n\
/opt/microsoft/mlserver/9.3.0/o16n/startAll.sh \n\
/opt/microsoft/mlserver/9.3.0/o16n/Microsoft.MLServer.ComputeNode/autoStartScriptsLinux/computeNode.sh start \n\
az ml admin node setup --webnode --admin-password "Microsoft@2018" --confirm-password "Microsoft@2018" --uri http://localhost:12805 \n\
/usr/bin/Rscript --no-save --verbose service.R \n\
sleep infinity' > bootstrap.sh

RUN chmod +x bootstrap.sh

############################################################################################

EXPOSE 12800
ENTRYPOINT ["/data/bootstrap.sh"]
