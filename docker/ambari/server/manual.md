docker run -h ambari-server --name ambari-server -t -d centos:7 --network workbench

docker exec -it ambari-server /bin/bash

# instalando dependencias (both)
yum install -y wget ntp libselinux-utils git

# enabling ntp (both)
systemctl enable ntpd


# configure hosts (both)
echo "1.2.3.4	ambari-server" >> /etc/hosts

# configure network (both)
echo "NETWORKING=yes" >> /etc/sysconfig/network
echo "HOSTNAME=<hostname>" | sed "s/<hostname>/$(hostname -f)/g" >> /etc/sysconfig/network

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

# instalando JDBC

yum install -y postgresql-jdbc*
chmod 644 /usr/share/java/postgresql-jdbc.jar

# Instalando ambari (BOTH) (WITH SUDO)
## Instalando Dependencias
yum install -y python3 python2-setuptools rpm-build gcc-c++ python-devel python3-devel

## Instalando Java
yum install -y java-1.8.0-openjdk 
update-alternatives --set java java-1.8.0-openjdk.x86_64
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk

## Instalando maven

wget https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
tar xzf apache-maven-3.6.3-bin.tar.gz
mkdir /usr/local/maven
mv apache-maven-3.6.3/ /usr/local/maven/
alternatives --install /usr/bin/mvn mvn /usr/local/maven/apache-maven-3.6.3/bin/mvn 1
alternatives --set mvn /usr/local/maven/apache-maven-3.6.3/bin/mvn
export M2_HOME=/usr/local/maven/apache-maven-3.6.3

## Instalando PhamtonJS
yum -y install glibc fontconfig freetype freetype-devel fontconfig-devel wget bzip2
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin

## Buildando Ambari
wget http://archive.apache.org/dist/ambari/ambari-2.7.0/apache-ambari-2.7.0-src.tar.gz
tar xfvz apache-ambari-2.7.0-src.tar.gz
cd apache-ambari-2.7.0-src
mvn versions:set -DnewVersion=2.7.0.0.0
 
pushd ambari-metrics
mvn versions:set -DnewVersion=2.7.0.0.0
popd

sed -ri 's/<nodeVersion>(.*)</<nodeVersion>v11.10.0</g' ambari-admin/pom.xml
sed -ri 's/<npmVersion>(.*)</<npmVersion>6.7.0</g' ambari-admin/pom.xml

sed -ri 's/<hbase\.tar>(.*)</<hbase\.tar>https:\/\/archive\.apache\.org\/dist\/hbase\/2\.0\.2\/hbase-2\.0\.2-bin\.tar\.gz</g' ambari-metrics/pom.xml 
sed -ri 's/<hadoop\.tar>(.*)</<hadoop\.tar>https:\/\/archive\.apache\.org\/dist\/hadoop\/common\/hadoop-3\.1\.1\/hadoop-3\.1\.1\.tar\.gz</g' ambari-metrics/pom.xml 
sed -ri 's/<phoenix\.tar>(.*)</<phoenix.tar>https:\/\/downloads\.apache\.org\/phoenix\/apache-phoenix-5\.0\.0-HBase-2\.0\/bin\/apache-phoenix-5\.0\.0-HBase-2\.0-bin\.tar\.gz</g' ambari-metrics/pom.xml 

sed -ri 's/<hbase\.folder>(.*)</<hbase\.folder>hbase-2\.0\.2</g' ambari-metrics/pom.xml 
sed -ri 's/<hadoop\.folder>(.*)</<hadoop\.folder>hadoop-3\.1\.1</g' ambari-metrics/pom.xml 
sed -ri 's/<phoenix\.folder>(.*)</<phoenix\.folder>apache-phoenix-5\.0\.0-HBase-2\.0-bin</g' ambari-metrics/pom.xml 


sed -ri 's/<solr\.tar>(.*)</<hadoop\.version>3\.1\.1</g' ambari-metrics/ambari-metrics-timelineservice/pom.xml 
sed -ri 's/<phoenix\.version>(.*)</<phoenix\.version>5\.0\.0-HBase-2\.0</g' ambari-metrics/ambari-metrics-timelineservice/pom.xml 
sed -ri 's/<hbase\.version>(.*)</<hbase\.version>2\.0\.2</g' ambari-metrics/ambari-metrics-timelineservice/pom.xml 

sed -ri 's/<solr\.tar>(.*)</<solr\.tar>http:\/\/archive\.apache\.org\/dist\/lucene\/solr\/\$\{solr\.version\}\/solr-\$\{solr\.version\}\.tgz</g' ambari-infra/ambari-infra-assembly/pom.xml


mvn -B clean install rpm:rpm -DnewVersion=2.7.5.0.0 -DbuildNumber=5895e4ed6b30a2da8a90fee2403b6cab91d19972 -DskipTests -Dpython.ver="python >= 2.6" -Drat.skip=true

## Instalando o ambari
yum -y install ambari-server/target/rpm/ambari-server/RPMS/x86_64/ambari-server*.rpm


ambari-server setup --jdbc-db=postgres --jdbc-driver=/usr/share/java/postgresql-jdbc.jar

ambari-server start

## Cria base de dados
PGPASSWORD=ambaripwd psql -h postgresql -U ambaridba ambari  -a -q -f /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql