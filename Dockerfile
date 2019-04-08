##### Use latest Ubuntu LTS release as the base
FROM ubuntu:bionic

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# Install GDAL dependencies
RUN apt-get install -y python3-pip libgdal-dev locales

# Ensure locales configured correctly
RUN locale-gen en_US.UTF-8
ENV LC_ALL='en_US.utf8'

# Set python aliases for python3
RUN echo 'alias python=python3' >> ~/.bashrc
RUN echo 'alias pip=pip3' >> ~/.bashrc

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir code
WORKDIR /code

#FROM ubuntu:14.04
#
## Install binary dependencies
#RUN apt-get -qqy update && \
#    apt-get install -qqy software-properties-common --no-install-recommends && \
#    apt-add-repository -y ppa:ubuntugis/ppa && \
#    apt-get install -qqy \
#        wget \
#        build-essential \
#        gdal-bin \
#        libgdal-dev \
#        libspatialindex-dev \
#        python \
#        python-dev \
#        python-pip \
#        python-tk \
#        idle \
#        python-pmw \
#        python-imaging \
#        python-opencv \
#        python-matplotlib \
#        git-all \
#        --no-install-recommends
#
##RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
##    wget --quiet https://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh -O ~/anaconda.sh && \
##    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
##    rm ~/anaconda.sh
#
#
#RUN apt-add-repository ppa:ubuntugis/ubuntugis-unstable
#
#RUN apt-get update
#
#RUN apt-get -qqy install python-gdal
#
#RUN pip install geojson && \
#    pip install shapely && \
#    pip install ipython && \
#    pip install jupyter && \
#    pip install pandas && \
#    pip install tifffile && \
#    pip install awscli --ignore-installed six
#
## Clean-up
#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD jupyter notebook --no-browser --ip=0.0.0.0 --port=8888 --allow-root