# -----------------------------------------------------------------------------
# ASTERISK-RPM - RPMs for Asterisk
# Copyright (C) 2016 Paul Dugas.  All rights reserved.
# -----------------------------------------------------------------------------
# Package   RPMS
# File      asterisk/asterisk.spec
# Brief     RPM Spec File for Asterisk
# Author    Paul Dugas <paul@dugas.cc>
# URL       https://github.com/pdugas/rpms/tree/master/asterisk
# -----------------------------------------------------------------------------

Name:		asterisk
Version:	13.7.2
Release:	1%{?dist}
Summary:	Asterisk PBX
Group:		System/Telephony
Packager:	Paul Dugas <paul@dugas.cc>
URL:		http://www.asterisk.org
License:	GPL

Source0:	http://downloads.digium.com/pub/asterisk/releases/asterisk-%{version}.tar.gz
Source1:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-core-sounds-en-ulaw-current.tar.gz
Source2:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-core-sounds-en-g722-current.tar.gz
Source3:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-extra-sounds-en-ulaw-current.tar.gz
Source4:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-extra-sounds-en-g722-current.tar.gz
Source5:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-moh-opsound-ulaw-current.tar.gz
Source6:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-moh-opsound-g722-current.tar.gz
Source7:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/asterisk.service
Source8:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/sounds.custom.README
Source9:	http://downloads.polycom.com/voice/voip/sp_ss_sip/spip_ssip_3_1_8_legacy_release_sig_split.zip
Source10:	http://downloads.polycom.com/voice/voip/sp_ss_bootrom/spip_ssip_vvx_BootROM_4_1_4_release_sig.zip
Source11:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/httpd-asterisk.conf
Source12:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/asterisk-favicon.ico
Source13:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/asterisk.sql

BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	git
BuildRequires:	gmime-devel
BuildRequires:	gsm-devel
BuildRequires:	gtk2-devel
BuildRequires:	iksemel-devel
BuildRequires:	jansson-devel
BuildRequires:	libical-devel
BuildRequires:	libogg-devel
BuildRequires:	libsrtp-devel
BuildRequires:	libtool-ltdl-devel
BuildRequires:	libuuid-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	lua-devel
BuildRequires:	mysql-connector-odbc
BuildRequires:	ncurses-devel
BuildRequires:	neon-devel
BuildRequires:	net-snmp-devel
BuildRequires:	newt-devel
BuildRequires:	openssl-devel
BuildRequires:	pjproject-devel
BuildRequires:	spandsp-devel
BuildRequires:	speex-devel
BuildRequires:	subversion
BuildRequires:	sqlite-devel
BuildRequires:	systemd
BuildRequires:	unixODBC-devel
BuildRequires:	uuid-devel

Requires:	httpd
Requires:	mariadb-server

Requires(pre):		shadow-utils
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd shadow-utils

%define uname %{name}
%define gname %{name}

%description
Asterisk is an open source framework for building communications applications.
Asterisk turns an ordinary computer into a communications server. Asterisk
powers IP PBX systems, VoIP gateways, conference servers and other custom
solutions. It is used by small businesses, large businesses, call centers,
carriers and government agencies, worldwide. Asterisk is free and open source.
Asterisk is sponsored by Digium.  See http://asterisk.org/.

%package devel
Summary:       Development files for the Asterisk software PBX
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
Asterisk is an open source framework for building communications applications.
Asterisk turns an ordinary computer into a communications server. Asterisk
powers IP PBX systems, VoIP gateways, conference servers and other custom
solutions. It is used by small businesses, large businesses, call centers,
carriers and government agencies, worldwide. Asterisk is free and open source.
Asterisk is sponsored by Digium.  See http://asterisk.org/.

This package contains static libraries and header files need for development.

%package sounds-en-ulaw
Summary:       Sound files for the Asterisk software PBX
Group:         System/Telephony
Requires:      %{name} = %{version}-%{release}

%description sounds-en-ulaw
Asterisk is an open source framework for building communications applications.
Asterisk turns an ordinary computer into a communications server. Asterisk
powers IP PBX systems, VoIP gateways, conference servers and other custom
solutions. It is used by small businesses, large businesses, call centers,
carriers and government agencies, worldwide. Asterisk is free and open source.
Asterisk is sponsored by Digium.  See http://asterisk.org/.

This package contains English Asterisk sound files encoded using μ-law (G.711).
It is a combination of Asterisk's Core, Extra, and MOH sound packages.

%package sounds-en-g722
Summary:       Sound files for the Asterisk software PBX
Group:         System/Telephony
Requires:      %{name} = %{version}-%{release}

%description sounds-en-g722
Asterisk is an open source framework for building communications applications.
Asterisk turns an ordinary computer into a communications server. Asterisk
powers IP PBX systems, VoIP gateways, conference servers and other custom
solutions. It is used by small businesses, large businesses, call centers,
carriers and government agencies, worldwide. Asterisk is free and open source.
Asterisk is sponsored by Digium.  See http://asterisk.org/.

This package contains English Asterisk sound files encoded using G.722.
It is a combination of Asterisk's Core, Extra, and MOH sound packages.

%prep
%setup -q

%build
%configure
contrib/scripts/get_mp3_source.sh
make menuselect.makeopts
menuselect/menuselect \
    --disable CORE-SOUNDS-EN-GSM \
    --disable MOH-OPSOUND-WAV \
    --enable chan_ooh323 \
    --enable app_fax \
    --enable format_mp3
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install install-logrotate samples
%{__install} -Dp -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/asterisk.service
%{__install} -Dp -m 644 %{SOURCE8} %{buildroot}%{_localstatedir}/lib/asterisk/sounds/custom/README
%{__install} -d %{buildroot}%{_localstatedir}/lib/asterisk/sounds/en/
%{__tar} -xf %{SOURCE1} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds/en/
%{__tar} -xf %{SOURCE2} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds/en/
%{__tar} -xf %{SOURCE3} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds/en/
%{__tar} -xf %{SOURCE4} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds/en/
%{__tar} -xf %{SOURCE5} -C %{buildroot}%{_localstatedir}/lib/asterisk/moh/
%{__tar} -xf %{SOURCE6} -C %{buildroot}%{_localstatedir}/lib/asterisk/moh/
%{__install} -d %{buildroot}%{_localstatedir}/spool/asterisk/sounds/en/
for x in phoneprov/*; do \
  %{__install} -m 644 "$x" %{buildroot}%{_localstatedir}/lib/asterisk/phoneprov
done
%{__install} -d %{buildroot}%{_localstatedir}/lib/asterisk/phoneprov/configs/
%{__unzip} %{SOURCE9} -d %{buildroot}%{_localstatedir}/lib/asterisk/phoneprov/configs/
%{__unzip} %{SOURCE10} -d %{buildroot}%{_localstatedir}/lib/asterisk/phoneprov/configs/
%{__rm} -rf %{buildroot}%{_localstatedir}/spool/asterisk/voicemail/default/1234
%{__mv} %{buildroot}%{_sysconfdir}/asterisk/extensions.ael %{buildroot}%{_sysconfdir}/asterisk/extensions.ael.sample
%{__mv} %{buildroot}%{_sysconfdir}/asterisk/extensions.lua %{buildroot}%{_sysconfdir}/asterisk/extensions.lua.sample
%{__install} -d -m 775 %{buildroot}%{_localstatedir}/log/asterisk/polycom/
%{__install} -Dp -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/httpd/conf.d/asterisk.conf
%{__install} -Dp -m 644 %{SOURCE12} %{buildroot}%{_localstatedir}/www/html/favicon.ico
%{__install} -Dp -m 644 %{SOURCE13} %{buildroot}%{_datadir}/doc/%{name}-%{version}/asterisk.sql
%{__install} -d -m 755 %{buildroot}%{_datadir}/doc/%{name}-%{version}/configs/samples/
for x in configs/samples/*; do \
  %{__install} -m 644 "$x" "%{buildroot}%{_datadir}/doc/%{name}-%{version}/$x"
done

%pre
getent group ${gname} >/dev/null || groupadd -r ${gname}
getent passwd $au{name} >/dev/null || \
    useradd -r -g ${gname} -d %{_localstatedir}/lib/asterisk -s /sbin/nologin \
    -c "Asterisk PBX" ${uname}
exit 0

%post
%systemd_post asterisk.service

%preun
%systemd_preun asterisk.service
getent group ${name} >/dev/null && groupdel %{name}
getent passwd ${name} >/dev/null && userdel %{name}

%postun
%systemd_postun_with_restart asterisk.service

%files
%defattr(-,root,root)
%doc CREDITS LICENSE README README-addons.txt
%doc README-SERIOUSLY.bestpractices.txt UPGRADE.txt
%doc asterisk-%{version}-summary.txt BUGS ChangeLog
%dir %{_sysconfdir}/asterisk/
%config(noreplace) %{_sysconfdir}/asterisk/*
%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk
%config(noreplace) %{_sysconfdir}/httpd/conf.d/asterisk.conf
%{_libdir}/libasteriskssl.so.*
%dir %{_libdir}/asterisk/
%dir %{_libdir}/asterisk/modules/
%{_libdir}/asterisk/modules/*
%{_sbindir}/*
%{_mandir}/man8/*
%{_unitdir}/asterisk.service
%attr(-  , %{uname}, %{gname}) %dir %{_localstatedir}/lib/asterisk/
%ghost %{_localstatedir}/lib/asterisk/astdb.sqlite3
%dir %{_localstatedir}/lib/asterisk/agi-bin
%dir %{_localstatedir}/lib/asterisk/documentation
%{_localstatedir}/lib/asterisk/documentation/*
%dir %{_localstatedir}/lib/asterisk/firmware
%dir %{_localstatedir}/lib/asterisk/firmware/iax
%dir %{_localstatedir}/lib/asterisk/images
%{_localstatedir}/lib/asterisk/images/*
%dir %{_localstatedir}/lib/asterisk/keys
%dir %{_localstatedir}/lib/asterisk/moh
%dir %{_localstatedir}/lib/asterisk/phoneprov
%dir %{_localstatedir}/lib/asterisk/phoneprov/configs
%{_localstatedir}/lib/asterisk/phoneprov/configs/*
%config(noreplace) %{_localstatedir}/lib/asterisk/phoneprov/*.xml
%config(noreplace) %{_localstatedir}/lib/asterisk/phoneprov/*.cfg
%dir %{_localstatedir}/lib/asterisk/rest-api
%{_localstatedir}/lib/asterisk/rest-api/*
%dir %{_localstatedir}/lib/asterisk/sounds
%dir %{_localstatedir}/lib/asterisk/sounds/custom
%doc %{_localstatedir}/lib/asterisk/sounds/custom/README
%dir %{_localstatedir}/lib/asterisk/sounds/en
%doc %{_localstatedir}/lib/asterisk/sounds/en/*.txt
%doc %{_localstatedir}/lib/asterisk/sounds/en/CHANGES-*
%doc %{_localstatedir}/lib/asterisk/sounds/en/CREDITS-*
%doc %{_localstatedir}/lib/asterisk/sounds/en/LICENSE-*
%dir %{_localstatedir}/lib/asterisk/sounds/en/dictate
%dir %{_localstatedir}/lib/asterisk/sounds/en/digits
%dir %{_localstatedir}/lib/asterisk/sounds/en/followme
%dir %{_localstatedir}/lib/asterisk/sounds/en/letters
%dir %{_localstatedir}/lib/asterisk/sounds/en/phonetic
%dir %{_localstatedir}/lib/asterisk/sounds/en/silence
%dir %{_localstatedir}/lib/asterisk/sounds/en/ha
%dir %{_localstatedir}/lib/asterisk/sounds/en/wx
%dir %{_localstatedir}/lib/asterisk/static-http
%{_localstatedir}/lib/asterisk/static-http/*
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/log/asterisk/
%attr(770, -       , apache  ) %dir %{_localstatedir}/log/asterisk/polycom/
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/log/asterisk/cdr-csv/
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/log/asterisk/cdr-custom/
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/log/asterisk/cel-custom/
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/run/asterisk/
%attr(750, %{uname}, %{gname}) %dir %{_localstatedir}/spool/asterisk/
%{_localstatedir}/spool/asterisk/*
%{_localstatedir}/www/html/favicon.ico

%files devel
%defattr(-,root,root)
%{_includedir}/asterisk.h
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*
%{_libdir}/libasteriskssl.so

%files sounds-en-ulaw
%defattr(-,root,root)
%{_localstatedir}/lib/asterisk/moh/*ulaw
%{_localstatedir}/lib/asterisk/sounds/en/*ulaw
%{_localstatedir}/lib/asterisk/sounds/en/*/*ulaw

%files sounds-en-g722
%defattr(-,root,root)
%{_localstatedir}/lib/asterisk/moh/*g722
%{_localstatedir}/lib/asterisk/sounds/en/*g722
%{_localstatedir}/lib/asterisk/sounds/en/*/*g722

%changelog
* Mon Feb 29 2016 Paul Dugas <paul@dugas.cc> 13.7.2-1
- Initial RPM release.

# -----------------------------------------------------------------------------
# EOF
