docker run -dit -h ambari-repo --name ambari-repo --network workbench -p 80 -v /mnt/hgfs/HDP-vm-shared/hortonworks-repo/ambari:/opt/repo/ambari centos:7
docker exec -it ambari-repo bash
yum install -y createrepo
createrepo /opt/repo

echo '[customrepo]
name=HortonworksRepo
baseurl=file:///opt/repo
enabled=1
gpgcheck=0' > /etc/yum.repos.d/hortonworks.repo