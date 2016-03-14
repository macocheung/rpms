# Asterisk RPM Spec

This directory contains a SPEC and some other supporting files for building RPM
packages for Asterisk.  The process I follow is below followed by some notes on
what customizations I've included.

## Building the RPM

1.  Start with a physical or virtual machine with adequate resources for Asterisk.
    I typically use 2 CPUs, 2GB RAM, 10G drive, and an Ethernet LAN interface.  A
    second inteface exposed externally can also be added but I typically deploy
    behind a NAT'ing firewall and don't need it.

2.  Install CentOS-7 Minimal, configure a static network, configure NTP, install VM
    tools if necessary, disable selinux, install SSH keys, apply any pending
    updates and reboot.

3.  Next, we install some basics.
```
[root@pbx]# yum install -y deltarpm epel-release yum-cron firewalld
[root@pbx]# yum install -y vim tcpdump bind-utils net-tools lsof bash-completion wget
```

4.  Then install the necessary packaging tools.
```
[root@pbx]# yum install -y rpm-build redhat-rpm-config rpmdevtools yum-utils
```

5.  Setup the build environment.  We never build RPMs as root, right?
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

6.  Install the dependencies.  You can run this while the sources are being downloaded.
```
[root@pbx]# yum-builddep -y ~build/rpmbuild/SPECS/asterisk.spec 
```

7.  Now build the RPMs:
```
[root@pbx]# su - build
[build@pbx]$ rpmbuild -ba rpmbuild/SPECS/asterisk.spec
  ... get some coffee ...
[build@pbx]$ exit
```

8.  Install them.  Not that this will make sure _httpd_ and _mariadb-server_ are
    installed as well since our setup depends on them.
```
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/x86_64/asterisk-13.7.2-*.rpm
[root@pbx]# yum localinstall ~build/rpmbuild/RPMS/x86_64/asterisk-sounds-*.rpm
```

9.  Enable and start Apache, and MariaDB.
```
[root@pbx]# systemctl enable httpd
[root@pbx]# systemctl enable mariadb
[root@pbx]# systemctl start httpd
[root@pbx]# systemctl start mariadb
```

10. Create the database and schema.  Change _secret_ to something appropriate.
```
[root@pbx]# mysql 
MariaDB [(none)]> CREATE DATABASE asterisk;
MariaDB [(none)]> CREATE USER 'asterisk'@'localhost' IDENTIFIED BY 'secret';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON asterisk.* TO 'asterisk'@'localhost';
MariaDB [(none)]> FLUSH PRIVILEGES;
MariaDB [(none)]> EXIT;
[root@pbx]# mysql -u asterisk -p asterisk < /usr/share/doc/asterisk-*/asterisk-schema.sql
Password: 
[root@pbx]# 
```

11. Setup the ODBC connection to the database.  Create ```/etc/odbc.ini``` as below.
```
[asterisk]
Driver=MySQL
Database=asterisk
Server=localhost
port=3306
Socket=/var/lib/mysql/mysql.sock
```

13. Edit _/etc/asterisk/res_odbc.conf_ and change the _password_ setting in the
_[asterisk]_ section to whatever database password you used above in step 10.

14. Enable and start Asterisk.
```
[root@pbx]# systemctl enable asterisk
[root@pbx]# systemctl start asterisk
```

15. Open up the firewall for Asterisk and Apache
```
[root@pbx]# firewall-cmd --zone=public --add-port=80/tcp --permanent 
[root@pbx]# firewall-cmd --zone=public --add-port=443/tcp --permanent 
[root@pbx]# firewall-cmd --zone=public --add-port=5060/udp --permanent 
[root@pbx]# firewall-cmd --zone=public --add-port=10000-20000/udp --permanent 
[root@pbx]# firewall-cmd --reload
```

16. Configure DHCP for the phones.  See [here](DHCP.md).

17. Now you need to adjust the Asterisk configs in _/etc/asterisk_.  Edit
```pjsip_wizard.conf``` to setup your SIP trunks and extensions users.  Edit
```voicemail.conf``` to create voicemail boxes.  Edit ```extensions.conf```
to adjust the dialplan.  They all should be commented to explain the needed
changes.

That should do it.  Get to the console like so:
```
[root@pbx]# asterisk -rvvv
Asterisk 13.7.2, Copyright (C) 1999 - 2014, Digium, Inc. and others.
Created by Mark Spencer <markster@digium.com>
Asterisk comes with ABSOLUTELY NO WARRANTY; type 'core show warranty' for details.
This is free software, with components licensed under the GNU General Public
License version 2 and other licenses; you are welcome to redistribute it under
certain conditions. Type 'core show license' for details.
=========================================================================
Connected to Asterisk 13.7.2 currently running on svr1 (pid = 13253)
svr1*CLI> 
```

## Customizations

* __BuildRequires__ - We add a number of _BuildRequires_ entres in the Spec
  File so almost all of the optional Asterisk modules and features are 
  enabled.  We don't enable Dahdi and other hardware support since we don't
  typically use it and don't want to add the extra kernel requirements where
  we use the resulting RPMs.
* __Custom Sounds__ - We keep custom sounds separate from the stock sound
  files.  Use the _/var/lib/asterisk/sounds/custom/_ directory for these.
* __Sound Packages__ - We build _asterisk-sounds-en-*_ packages for formats
  that are enabled.  ULAW and G722 are enabled by default.  Call _rpmbuild_
  with _--define "ulaw 0"_ to disable ULAW.  Replace _ulaw_ with _wav_, _alaw_,
  _gsm_, _g722_, _g729_, _sln16_, _siren7_, or _siren14_ for other formats.
  Replace the _0_ with _1_ to enable them. i.e. ```rpmbuild -ba asterisk.spec --define "wav 1"```
* __Polycom Phones__ - We use Polycom phones so we include the firmware and
  boot files in this package.  We use _phoneprov_ to provision them.
* __Non-Root__ - We run Asterisk as the _asterisk_ user rather than _root_
  and have made the necessary permissions adjustments on the folders where
  logs and data are stored.
* __systemd Support__ - We include a service definition to start/stop Asterisk
  using systemd since this is the standard for Redhat these days.

