docker run -h ambari-server --name ambari-server -t -d centos

docker exec -it ambari-server /bin/bash

# instalando dependencias (both)
yum install -y chrony libselinux-utils

# enabling (both)
systemctl enable chronyd


# configure hosts (both)
echo "1.2.3.4	ambari-server" >> /etc/hosts

# configure network (both)
echo "NETWORKING=yes" >> /etc/sysconfig/network
echo "HOSTNAME=<hostname>" | sed "s/<hostname>/$(hostname -f)/g"

# disable selinux (both)
setenforce 0

# set UMASK (both)
echo umask 0022 >> /etc/profile

# (non-docker) Desabilitando firewalld temporariamente
# systemctl disable firewalld
# service firewalld stop



# (non-docker) Habilitando firewalld temporariamente
# systemctl enable firewalld
# service firewalld start