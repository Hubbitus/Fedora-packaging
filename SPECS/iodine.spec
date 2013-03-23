%global prerel -rc1

Name:		iodine
Version:		0.6.0
Release:		0.rc1.4%{?dist}
Summary:		Solution to tunnel IPv4 data through a DNS server
Summary(ru):	Решение для туннелирования IPv4 трафика через DNS сервер
Group:		System Environment/Daemons
License:		ISC
URL:			http://code.kryo.se/iodine/
Source0:		http://code.kryo.se/%{name}/%{name}-%{version}%{prerel}.tar.gz
# Initscripts and separate configs made by Nikolay Ulyanitsky
Source1:		%{name}-client.conf
Source2:		%{name}-server.conf

Source3:		%{name}-client.init
Source4:		%{name}-server.init

Source5:		%{name}.logrotate

# It is needed because I plan push it in EPEL too
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# http://dev.kryo.se/iodine/ticket/87
Patch0:		iodine-0.5.2-prefix.patch

BuildRequires:		zlib-devel
Requires(post):	chkconfig
Requires(preun):	chkconfig, initscripts
Requires(postun):	initscripts

%description
iodine lets you tunnel IPv4 data through a DNS server. This can be usable in
different situations where internet access is firewalled, but DNS queries are
allowed.

It runs on Linux, Mac OS X, FreeBSD, NetBSD, OpenBSD and Windows and needs a
TUN/TAP device. The bandwidth is asymmetrical with limited upstream and up to
1 Mbit/s downstream.

%description -l ru
iodine предоставляет возможность пробросить IPv4 туннель сквозь DNS сервер.
Это может быть очень полезно в разных ситуациях, когда доступ в интернет
запрещён фаерволом, но DNS запросы пропускаются нормально.

Iodine работает на Linux, Mac OS X, FreeBSD, NetBSD, OpenBSD и Windows и
использует TUN/TAP устройство. Пропускная способность асимметрична - аплоад не
быстр, скачивание до 1 Mbit/s.

%prep
%setup -q -n %{name}-%{version}%{prerel}
%patch0 -p0 -b .prefix

%build
make %{?_smp_mflags} PREFIX=%{_prefix}

%install
rm -rf %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}

install -Dp -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-client
install -Dp -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-server

install -Dp -m 0755 %{SOURCE3} %{buildroot}/%{_initrddir}/%{name}-client
install -Dp -m 0755 %{SOURCE4} %{buildroot}/%{_initrddir}/%{name}-server

install -Dp -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}-client
/sbin/chkconfig --add %{name}-server

%preun
if [ $1 = 0 ] ; then
	/sbin/service %{name}-client stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}-client

	/sbin/service %{name}-server stop >/dev/null 2>&1
	/sbin/chkconfig --del %{name}-server
fi

%postun
if [ "$1" -ge "1" ] ; then
	/sbin/service %{name}-client condrestart >/dev/null 2>&1 || :
	/sbin/service %{name}-server condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc CHANGELOG README TODO
%{_sbindir}/%{name}
%{_sbindir}/%{name}d
%{_mandir}/man8/%{name}.8.gz

%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-client
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%{_initrddir}/%{name}-client
%{_initrddir}/%{name}-server


%changelog
* Sun Sep 12 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.0-0.rc1.4
- Build new version 0.6.0rc1
- Define prerel.
- Delete axtra -c flag from CFLAGS. It is not required anymore.

* Sat Mar 6 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.2-3
- Honor CFLAGS

* Mon Feb 22 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.2-2
- Import some items from Nikolay Ulyanitsky package ( https://bugzilla.redhat.com/show_bug.cgi?id=530747#c1 ):
	o Add initscripts support (modified)
	o Add logrotate support
	o Exclude README-win32.txt and respective delete dos2unix BR.
	o Add BR zlib-devel

* Sat Oct 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.2-1
- Initial spec.
