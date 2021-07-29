docker run -h ambari-server --name ambari-server --network workbench -p 8080:8080 -t -d centos:7
docker cp /mnt/hgfs/HDP-vm-shared/ambari/ambari-server-2.7.4.0-118.x86_64.rpm ambari-server:/tmp/

docker exec -it ambari-server /bin/bash

yum install -y libselinux-utils ntp java-1.8.0-openjdk-devel \
    postgresql-jdbc* 
    
update-alternatives --set java java-1.8.0-openjdk.x86_64
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk' >> /root/.bashrc

systemctl enable ntpd
echo "NETWORKING=yes" >> /etc/sysconfig/network
echo "HOSTNAME=<hostname>" | sed "s/<hostname>/$(hostname -f)/g" >> /etc/sysconfig/network

setenforce 0
echo umask 0022 >> /etc/profile


chmod 644 /usr/share/java/postgresql-jdbc.jar

yum -y install tmp/ambari-server-2.7.4.0-118.x86_64.rpm 



sed -ri 's/<selection>MANDATORY<\/selection>/<!-- <selection>MANDATORY<\/selection> -->/g' /var/lib/ambari-server/resources/stacks/HDP/3.0/services/SMARTSENSE/metainfo.xml


PGPASSWORD=ambaripwd psql -h postgresql -U ambaridba ambari  -a -q -f /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql

ambari-server setup --silent \
    --java-home $JAVA_HOME \
    --database postgres \
    --databasehost postgresql \
    --databaseport 5432 \
    --databasename ambari \
    --postgresschema ambari \
    --databaseusername ambari \
    --databasepassword ambaripwd \
    --jdbc-db=postgres \
    --jdbc-driver=/usr/share/java/postgresql-jdbc.jar

echo 'local.database.user=postgres' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.database=postgres' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.driver=org.postgresql.Driver' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.hostname=postgresql' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.postgres.schema=ambari' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.rca.driver=org.postgresql.Driver' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.rca.url=jdbc:postgresql://postgresql:5432/ambari' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.url=jdbc:postgresql://postgresql:5432/ambari' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.rca.user.name=ambaridba' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.user.name=ambaridba' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.connection-pool=internal' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.database_name=ambari' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.port=5432' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.rca.user.passwd=/etc/ambari-server/conf/password.dat' >> /etc/ambari-server/conf/ambari.properties
echo 'server.jdbc.user.passwd=/etc/ambari-server/conf/password.dat' >> /etc/ambari-server/conf/ambari.properties
echo 'ambari-server.user=root' >> /etc/ambari-server/conf/ambari.properties
echo 'java.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
echo 'stack.java.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
echo 'jdk1.8.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
echo 'server.os_family=redhat7' >> /etc/ambari-server/conf/ambari.properties
echo 'server.os_type=centos7' >> /etc/ambari-server/conf/ambari.properties
echo 'server.persistence.type=remote' >> /etc/ambari-server/conf/ambari.properties

# echo 'custom.postgres.jdbc.name=postgresql-jdbc.jar' >> /etc/ambari-server/conf/ambari.properties

echo 'ambaripwd' > /etc/ambari-server/conf/password.dat 

ambari-server start