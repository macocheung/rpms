# $Id$
# Authority: pdugas

# https://github.com/pdugas/rpms/master/asterisk/asterisk.spec

Name:		asterisk
Version:	13.7.2
Release:	1%{?dist}
Summary:	Asterisk PBX
Group:		System/Telephony
Packager:	Paul Dugas <paul@dugas.cc>
URL:		http://www.asterisk.org
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Source0:	http://downloads.digium.com/pub/asterisk/releases/asterisk-%{version}.tar.gz
Source1:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-core-sounds-en-ulaw-current.tar.gz
Source2:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-core-sounds-en-g722-current.tar.gz
Source3:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-extra-sounds-en-ulaw-current.tar.gz
Source4:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-extra-sounds-en-g722-current.tar.gz
Source5:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-moh-opsound-ulaw-current.tar.gz
Source6:	http://downloads.asterisk.org/pub/telephony/sounds/asterisk-moh-opsound-g722-current.tar.gz
Source7:	https://raw.githubusercontent.com/pdugas/rpms/master/asterisk/asterisk.service

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

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

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
%make_install install-logrotate basic-pbx
%{__mkdir} -p %{buildroot}%{_unitdir}/
%{__install} -D -m 644 %{SOURCE7} %{buildroot}%{_unitdir}
%{__tar} -xf %{SOURCE1} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds
%{__tar} -xf %{SOURCE2} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds
%{__tar} -xf %{SOURCE3} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds
%{__tar} -xf %{SOURCE4} -C %{buildroot}%{_localstatedir}/lib/asterisk/sounds
%{__tar} -xf %{SOURCE5} -C %{buildroot}%{_localstatedir}/lib/asterisk/moh
%{__tar} -xf %{SOURCE6} -C %{buildroot}%{_localstatedir}/lib/asterisk/moh

%post
%systemd_post asterisk.service

%preun
%systemd_preun asterisk.service

%postun
%systemd_postun_with_restart asterisk.service

%files
%defattr(-,root,root)
%doc CREDITS LICENSE
%dir %{_sysconfdir}/asterisk/
%doc %{_sysconfdir}/asterisk/README
%config(noreplace) %{_sysconfdir}/asterisk/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk
%{_libdir}/libasteriskssl.so.*
%dir %{_libdir}/asterisk/
%dir %{_libdir}/asterisk/modules/
%{_libdir}/asterisk/modules/*
%{_sbindir}/*
%{_mandir}/man8/*
%{_unitdir}/asterisk.service
%dir %{_localstatedir}/lib/asterisk/
%dir %{_localstatedir}/lib/asterisk/moh
%dir %{_localstatedir}/lib/asterisk/sounds
%{_localstatedir}/lib/asterisk/*
%dir %{_localstatedir}/log/asterisk/
#%ghost %{_localstatedir}/log/asterisk/*
%dir %{_localstatedir}/log/asterisk/cdr-csv/
#%ghost %{_localstatedir}/log/asterisk/cdr-csv/*
%dir %{_localstatedir}/log/asterisk/cdr-custom/
#%ghost %{_localstatedir}/log/asterisk/cdr-custom/*
%dir %{_localstatedir}/log/asterisk/cel-custom/
#%ghost %{_localstatedir}/log/asterisk/cel-custom/*
%dir %{_localstatedir}/run/asterisk/
#%ghost %{_localstatedir}/run/asterisk/*
%dir %{_localstatedir}/spool/asterisk/
%{_localstatedir}/spool/asterisk/*

%files devel
%defattr(-,root,root)
%doc BUGS ChangeLog README
%doc doc/api/html/*
%{_includedir}/asterisk.h
%dir %{_includedir}/asterisk
%{_includedir}/asterisk/*
%{_libdir}/libasteriskssl.so

%changelog
* Mon Feb 29 2016 Paul Dugas <paul@dugas.cc> 13.7.2-1
- Initial RPM release.
