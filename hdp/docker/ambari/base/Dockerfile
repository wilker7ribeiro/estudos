FROM centos:7
MAINTAINER Wilker

RUN yum update -y && yum clean all
RUN yum install -y systemd-sysv && yum clean all

#Setting up systemd
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
ENTRYPOINT ["/usr/sbin/init"]

# ADD hdp-yum.repo etc/yum.repos.d/hdp-yum.repo
RUN echo 'exclude=systemd*' >> /etc/yum.conf

RUN yum install -y systemd* && yum clean all

RUN yum install -y yum-utils yum-plugin-ovl tar git curl bind-utils unzip wget && yum clean all

# Setup sshd
RUN yum install -y openssh-server openssh-clients && yum clean all
RUN systemctl enable sshd

# Generate keys
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# kerberos client
# RUN yum install -y krb5-workstation && yum clean all

# initscripts (service wrapper for servicectl) is need othewise the Ambari is unable to start postgresql
RUN yum install -y initscripts && yum clean all
# libselinux-utils ntp 
RUN curl -o /usr/bin/jq http://stedolan.github.io/jq/download/linux64/jq && chmod +x /usr/bin/jq

# install Ambari specified 1.7 jdk
RUN yum install -y java-1.8.0-openjdk-devel
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
ENV PATH $PATH:$JAVA_HOME/bin

# RUN mkdir /usr/jdk64 && cd /usr/jdk64 && wget http://public-repo-1.hortonworks.com/ARTIFACTS/$JDK_ARTIFACT && \
#     tar -xf $JDK_ARTIFACT && rm -f $JDK_ARTIFACT
# ENV JAVA_HOME /usr/jdk64/$JDK_VERSION
# ENV PATH $PATH:$JAVA_HOME/bin

RUN yum install -y ntp

RUN systemctl enable ntpd
RUN echo "NETWORKING=yes" >> /etc/sysconfig/network
RUN echo "HOSTNAME=<hostname>" | sed "s/<hostname>/$(hostname -f)/g" >> /etc/sysconfig/network
# RUN setenforce 0
# RUN echo umask 0022 >> /etc/profile

#RUN yum -y install tmp/ambari-agent-2.7.4.0-118.x86_64.rpm
#RUN sed -ri 's/hostname=localhost/hostname=ambari-server/g' /etc/ambari-agent/conf/ambari-agent.ini
#RUN ambari-agent start 


# jce
# ADD http://public-repo-1.hortonworks.com/ARTIFACTS/UnlimitedJCEPolicyJDK7.zip $JAVA_HOME/jre/lib/security/
# RUN cd $JAVA_HOME/jre/lib/security && unzip UnlimitedJCEPolicyJDK7.zip && rm -f UnlimitedJCEPolicyJDK7.zip && mv UnlimitedJCEPolicy/*jar . && rm -rf UnlimitedJCEPolicy

EXPOSE 22

ENV PS1 "[\u@docker-ambari \W]# "

