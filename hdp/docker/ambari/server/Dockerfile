FROM wilker/ambari-base
MAINTAINER Wilker

# add ambari repo
ADD hdp.repo /etc/yum.repos.d/
ADD ambari.repo /etc/yum.repos.d/
# docker cp /mnt/hgfs/HDP-vm-shared/ambari/ambari-server-2.7.4.0-118.x86_64.rpm ambari-server:/tmp/
# yum install -y libselinux-utils ntp java-1.8.0-openjdk-devel postgresql-jdbc* 
# initscripts (service wrapper for servicectl) is need othewise the Ambari is unable to start postgresql
# RUN sed -ri 's/exclude=systemd/# exclude=systemd/g' /etc/yum.conf 
RUN yum install -y ambari-server && yum clean all
# RUN sed -ri 's/# exclude=systemd/exclude=systemd/g' /etc/yum.conf 
# yum -y install tmp/ambari-server-2.7.4.0-118.x86_64.rpm 

RUN sed -ri 's/<selection>MANDATORY<\/selection>/<!-- <selection>MANDATORY<\/selection> -->/g' /var/lib/ambari-server/resources/stacks/HDP/3.0/services/SMARTSENSE/metainfo.xml

RUN yum install -y postgresql-jdbc && yum clean all
RUN chmod 644 /usr/share/java/postgresql-jdbc.jar

# PGPASSWORD=ambaripwd psql -h postgresql -U ambari ambari  -a -q -f /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql

RUN ambari-server setup --silent \
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

RUN echo 'local.database.user=postgres' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.database=postgres' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.driver=org.postgresql.Driver' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.hostname=postgresql' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.postgres.schema=ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.rca.driver=org.postgresql.Driver' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.rca.url=jdbc:postgresql://postgresql:5432/ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.url=jdbc:postgresql://postgresql:5432/ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.rca.user.name=ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.user.name=ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.connection-pool=internal' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.database_name=ambari' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.port=5432' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.rca.user.passwd=/etc/ambari-server/conf/password.dat' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.jdbc.user.passwd=/etc/ambari-server/conf/password.dat' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'ambari-server.user=root' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'java.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'stack.java.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'jdk1.8.home=/usr/lib/jvm/java-1.8.0-openjdk' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.os_family=redhat7' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.os_type=centos7' >> /etc/ambari-server/conf/ambari.properties
RUN echo 'server.persistence.type=remote' >> /etc/ambari-server/conf/ambari.properties

# echo 'custom.postgres.jdbc.name=postgresql-jdbc.jar' >> /etc/ambari-server/conf/ambari.properties

RUN echo 'ambaripwd' > /etc/ambari-server/conf/password.dat 

RUN systemctl enable ambari-server

RUN echo DefaultEnvironment=\"JAVA_HOME=$JAVA_HOME\" >> /etc/systemd/system.conf

EXPOSE 8080







# add ambari shell to the image so new users don't need the 1GB java image
# RUN curl -o /tmp/ambari-shell.jar https://s3-eu-west-1.amazonaws.com/maven.sequenceiq.com/releases/com/sequenceiq/ambari-shell/0.1.25/ambari-shell-0.1.25.jar
# ADD shell/install-cluster.sh /tmp/
# ADD shell/wait-for-host-number.sh /tmp/
# ADD shell/ambari-shell.sh /tmp/

# ENV PLUGIN_PATH /plugins
# WORKDIR /tmp
# 
# ADD init/init-server.sh /opt/ambari-server/init-server.sh
# RUN chmod u+x /opt/ambari-server/init-server.sh
# 
# # add mysql and psql connectors to ambari-server so it can be downloaded by services (e.g.: Ranger)
# ADD http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.39.tar.gz /var/lib/ambari-server/resources/mysql-jdbc-driver.jar
# ADD https://jdbc.postgresql.org/download/postgresql-9.4.1208.jre7.jar /var/lib/ambari-server/resources/postgres-jdbc-driver.jar
# 
# ADD init/ambari-server.service /etc/systemd/system/ambari-server.service
# RUN systemctl enable ambari-server
# 
# RUN echo DefaultEnvironment=\"JAVA_HOME=$JAVA_HOME\" >> /etc/systemd/system.conf
# 
# EXPOSE 8080