# Asterisk RPM Spec

This directory contains a SPEC and some other supporting files for building RPM packages for Asterisk.  The process I follow is below.  YMMV!

Start with a physical or virtual machine with at least 2 CPUs, 2GB RAM, 10G drive, and an Ethernet LAN interface.

Install CentOS-7 Minimal, configure a static network, install VM tools if necessary, disable selinux, apply any pending updates and reboot.

Next, we install some basic tools:
```
[root@pbx]# yum install -y vim ntp tcpdump bind-utils deltarpm net-tools lsof bash-completion wget epel-release
```

Then the necessary packaging tools:
```
[root@pbx]# yum install -y rpm-build redhat-rpm-config rpmdevtools yum-utils
```

Setup the build environment.  Never build RPMs as `root`!
```
[root@pbx]# useradd build
[root@pbx]# su - build
[build@pbx]$ rpmdev-setuptree
[build@pbx]$ wget -O rpmbuild/SPECS/asterisk.spec https://raw.githubusercontent.com/pdugas/rpms/master/asterisk.spec
[build@pbx]$ spectool -g -R rpmbuild/SPECS/asterisk.spec
  ... downloading sources ...
[build@pbx]$ exit
[root@pbx]#
```

Install the dependencies:
```
[root@pbx]# yum-builddep -y ~build/rpmbuild/SPECS/asterisk.spec 
```

Now build RPMs:
```
[root@pbx]# su - build
[build@pbx]$ rpmbuild –ba rpmbuild/SPECS/asterisk.spec
  ... get some coffee ...
[build@pbx]$ exit
```

Install them:
```
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/asterisk-13.7.2.rpm
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/asterisk-sounds-*.rpm
```

That should do it!
--Paul
