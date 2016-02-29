# Asterisk RPM Spec

This directory contains a SPEC and some other supporting files for building RPM packages for Asterisk.  The process I follow is below.  YMMV!

* Physical machine or VM with 2 CPUs, 2GB RAM, 10G drive, and LAN interface
* CentOS-7 Minimal with static network, VM tools, selinux disabled, & yum update
* Some basic tools
    [root@pbx]# yum install -y vim ntp tcpdump bind-utils deltarpm net-tools lsof bash-completion wget epel-release
* Packaging tools
    [root@pbx]# yum install -y rpm-build redhat-rpm-config rpmdevtools yum-utils
* Build Environment
    [root@pbx]# useradd build
    [root@pbx]# su - build
    [build@pbx]$ rpmdev-setuptree
    [build@pbx]$ wget -O rpmbuild/SPECS/asterisk.spec https://raw.githubusercontent.com/pdugas/rpms/master/asterisk.spec
    [build@pbx]$ spectool -g -R rpmbuild/SPECS/asterisk.spec
    ... downloading sources ...
    [build@pbx]$ exit
    [root@pbx]#
* Install dependencies
    [root@pbx]# yum-builddep -y ~build/rpmbuild/SPECS/asterisk.spec 
* Build RPM
    [root@pbx]# su - build
    [build@pbx]$ rpmbuild –ba rpmbuild/SPECS/asterisk.spec

Good Luck!
--Paul
