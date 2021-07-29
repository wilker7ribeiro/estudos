docker run -h ambari-agent-1 --name ambari-agent-1 --network workbench -t -d centos:7

docker cp /mnt/hgfs/HDP-vm-shared/ambari/ambari-agent-2.7.4.0-118.x86_64.rpm ambari-agent-1:/tmp/

docker exec -it ambari-agent-1 /bin/bash 

yum install -y libselinux-utils ntp java-1.8.0-openjdk-devel

update-alternatives --set java java-1.8.0-openjdk.x86_64
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk' >> /root/.bashrc

systemctl enable ntpd
echo "NETWORKING=yes" >> /etc/sysconfig/network
echo "HOSTNAME=<hostname>" | sed "s/<hostname>/$(hostname -f)/g" >> /etc/sysconfig/network

setenforce 0
echo umask 0022 >> /etc/profile





echo '[HDP-UTILS-1.1.0.22-repo-52]
name=HDP-UTILS-1.1.0.22-repo-52
baseurl=http://ambari-repo/HDP-UTILS-1.1.0.22/repos/centos7
path=/
enabled=1
gpgcheck=0' >> /etc/yum.repos.d/ambari-repo.repo


yum -y install tmp/ambari-agent-2.7.4.0-118.x86_64.rpm

sed -ri 's/hostname=localhost/hostname=ambari-server/g' /etc/ambari-agent/conf/ambari-agent.ini



<selection>MANDATORY</selection>




ambari-agent start 