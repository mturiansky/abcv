FROM python:3.7-slim-buster

# build requirements
run apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    libtbb-dev \
    pybind11-dev

# embree
ENV CPATH=/opt/embree-3.6.1.x86_64.linux/include:$CPATH \
    LIBRARY_PATH=/opt/embree-3.6.1.x86_64.linux/lib:$LIBRARY_PATH \
    LD_LIBRARY_PATH=/opt/embree-3.6.1.x86_64.linux/lib:$LD_LIBRARY_PATH \
    EMBREE3_LINK=/opt/embree-3.6.1.x86_64.linux/lib

RUN curl -SL https://github.com/embree/embree/releases/download/v3.6.1/embree-3.6.1.x86_64.linux.tar.gz | tar xzC /opt && \
    rm -rf /opt/embree-3.6.1.x86_64.linux/bin /opt/embree-3.6.1.x86_64.linux/doc

# qhull
RUN curl -SL https://github.com/qhull/qhull/archive/2019.1.tar.gz | tar xzC /root && \
    cd /root/qhull-2019.1 && mkdir cmake_build && cd cmake_build && \
    cmake ../ -DCMAKE_INSTALL_PREFIX=/usr -DLIB_INSTALL_DIR=/usr/lib/x86_64-linux-gnu -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS=-fPIC -DCMAKE_C_FLAGS=-fPIC && \
    make install -j 10 && \
    cd / && rm -rf /root/qhull-*

# fresnel
RUN pip3 install numpy

RUN curl -SL https://glotzerlab.engin.umich.edu/Downloads/fresnel/fresnel-v0.10.1.tar.gz | tar xzC /root && \
    cd /root/fresnel-v0.10.1/ && mkdir build && cd build && \
    cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local/lib/python3.7/site-packages/ && \
    make install -j10 && \
    cd / && rm -rf /root/fresnel-*

RUN python3 -c "import fresnel; print(f'fresnel {fresnel.__version__} installed!')"

# setup user
RUN useradd --create-home --shell /bin/bash user

USER user

ENV PATH=/home/user/.local/bin:$PATH

# abcv
RUN mkdir /home/user/abcv/

WORKDIR /home/user/abcv/

COPY requirements.txt .

RUN pip3 install --user -r requirements.txt

COPY . .

RUN pip3 install --user -e .\[dev\]
