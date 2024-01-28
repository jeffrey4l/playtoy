install bcc

> https://github.com/iovisor/bcc/blob/v0.25.0/INSTALL.md#ubuntu---source

```bash
sudo apt install -y bison build-essential cmake flex git libedit-dev \
	libllvm14 llvm-14-dev libclang-14-dev python3 zlib1g-dev \
	libelf-dev libfl-dev python3-distutils \
	arping netperf iperf3

git clone https://github.com/iovisor/bcc
cd bcc; mkdir build; cd build
cmake ../
make -j4
make install

# fix the linux include folder, why `compat` folder is added?
cd /usr/include/bcc
ln -s compat/linux linux
```

install 

```bash
# bddisasm
git clone https://github.com/bitdefender/bddisasm
cd bddisasm
make && make install && make clean
ln -s /usr/local/lib/libbddisasm.a /usr/lib/libbddisasm.a # 建立软链接, agent 静态库目录是 /usr/lib/ 和 /usr/lib64


# libGoReSym
wget https://github.com/deepflowio/libGoReSym/archive/refs/tags/v0.0.1-2.tar.gz
tar -xzf v0.0.1-2.tar.gz
cd libGoReSym-0.0.1-2
# change the golang to system
make && make install && make clean


# libdwarf
wget https://github.com/davea42/libdwarf-code/releases/download/v0.4.1/libdwarf-0.4.1.tar.xz
tar -xf libdwarf-0.4.1.tar.xz
cd libdwarf-0.4.1
CFLAGS="-fpic" ./configure --disable-dependency-tracking
make && make install && make clean
ln -s /usr/local/lib/libdwarf.a /usr/lib/libdwarf.a


# build libpcap.a without dbus
git clone https://github.com/the-tcpdump-group/libpcap
mkdir -p libpcap/build ; cd libpcap/build
cmake ../ -DDISABLE_DBUS=1
make install 
ln -s /usr/local/lib/libpcap.a /usr/lib/x86_64-linux-gnu/libpcap.a
```

build deepflow

```
apt install cargo protobuf-compiler libpcap-dev clang llvm musl-tools
apt install openjdk-18-jdk 
ln -s /usr/lib/jvm/java-18-openjdk-amd64 /usr/lib/jvm/java

git clone --recursive https://github.com/deepflowio/deepflow.git
```

