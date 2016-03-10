# Asterisk RPM Spec

This directory contains a SPEC and some other supporting files for building RPM
packages for Asterisk.  The process I follow is below followed by some notes on
what customizations I've included.

## Building the RPM

Start with a physical or virtual machine with at least 2 CPUs, 2GB RAM, 10G
drive, and an Ethernet LAN interface.

Install CentOS-7 Minimal, configure a static network, configure NTP, install VM
tools if necessary, disable selinux, install SSH keys, apply any pending
updates and reboot.

Next, we install some basics:
```
[root@pbx]# yum install -y deltarpm epel-release yum-cron firewalld
[root@pbx]# yum install -y vim tcpdump bind-utils net-tools lsof bash-completion wget
```

Then the necessary packaging tools:
```
[root@pbx]# yum install -y rpm-build redhat-rpm-config rpmdevtools yum-utils
```

Setup the build environment.  We never build RPMs as root, right?
```
[root@pbx]# useradd build
[root@pbx]# su - build
[build@pbx]$ rpmdev-setuptree
[build@pbx]$ wget -O rpmbuild/SPECS/asterisk.spec https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/asterisk.spec
[build@pbx]$ spectool -g -R rpmbuild/SPECS/asterisk.spec
  ... downloading sources ...
[build@pbx]$ exit
[root@pbx]#
```

Install the dependencies.  You can run this while the sources are being downloaded.
```
[root@pbx]# yum-builddep -y ~build/rpmbuild/SPECS/asterisk.spec 
```

Now build the RPMs:
```
[root@pbx]# su - build
[build@pbx]$ rpmbuild -ba rpmbuild/SPECS/asterisk.spec
  ... get some coffee ...
[build@pbx]$ exit
```

Install them:
```
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/x86_64/asterisk-13.7.2.rpm
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/x86_64/asterisk-sounds-*.rpm
```

Enable and start Asterisk:
```
[root@pbx]# systemctl enable asterisk
[root@pbx]# systemctl start asterisk
```

Allow SIP/SIPS and RTP through the firewall:
```
[root@pbx]# firewall-cmd --zone=public --add-port=5060-5061/udp --permanent 
[root@pbx]# firewall-cmd --zone=public --add-port=10000-20000/udp --permanent 
[root@pbx]# firewall-cmd --reload
```

That should do it.  Now adjust the configs in _/etc/asterisk/_.  Pull samples
from _/usr/share/doc/asterisk-*/configs/_ for other config files not installed
already.

## Customizations

* I've added a number of _BuildRequires_ entries to _asterisk.spec_ in order to
  enable almost all of the optional modules with in Asterisk.  I've not enabled
  Dahdi or other components that rely on hardare and kernel-specific drivers
  since I want to be able to use the resulting packages on both virtual and
  physical machines. 
* I like to keep my custom sound files separate from those included in the
  distribution so I've added the _/var/lib/asterisk/sounds/custom/_ directory
  where I keep them instead.
* I use the _phoneprov_ feature to provision Polycom phones so that content is
  included.  I don't expose the HTTP interface directly instead proxying it
  through a local Apache instance.  
* I don't install the sound files via the stock build system.  Instead, I list
  them as sources in _asterisk.spec_ so they're downloaded with the Asterisk
  source.  Helps when I'm rebuilding often as I don't need to redownload them
  every time.  There looks to be support for a caching scheme in the makefile but
  I'm not seeing how to use it.
* I install the _basic-pbx_ configs into _/etc/asterisk/_ and include the
  samples in _/usr/share/doc/asterisk-*/configs/_.

