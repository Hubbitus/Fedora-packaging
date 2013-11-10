Name:             hans
Version:          0.4.3
Release:          1%{?dist}
Summary:          IP over ICMP tunneling solution

License:          GPLv3+
URL:              http://code.gerade.org/hans/
Source0:          https://github.com/friedrich/%{name}/archive/v%{version}.tar.gz
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    /usr/sbin/useradd
# My systemd, sysvinit and preconfiguration stuff
Source1:          %{name}-client.service
Source2:          %{name}-server.service
Source3:          %{name}-client.init
Source4:          %{name}-server.init
Source5:          %{name}-client.sysconfig
Source6:          %{name}-server.sysconfig

Requires(post):   chkconfig
Requires(preun):  chkconfig, initscripts
Requires(postun): initscripts

BuildRequires:    systemd-units

%description
Hans makes it possible to tunnel IPv4 through ICMP echo packets, so you could
call it a ping tunnel. This can be useful when you find yourself in the
situation that your Internet access is firewalled, but pings are allowed.

Hans runs on Linux as a client and a server. It runs on Mac OS X,
iPhone/iPod touch, FreeBSD and OpenBSD as a client only.

You probably want also install packages %{name}-client or %{name}-server or both

%package client
Summary:          Client part of solution to tunnel IPv4 data through a ICMP
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires:         %{name}

%description client
This is the client part of %{name} sulution.

%package client-sysvinit
Summary:          Legacy sysvinit scripts for cleint daemon
Requires(post):   chkconfig
Requires(preun):  chkconfig, initscripts
Requires(postun): initscripts

%description client-sysvinit
May be needed f.e. on CentOS.

%package server
Summary:          Server part of solution to tunnel IPv4 data through a ICMP
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires:         %{name}

%description server
This is the server part of %{name} solution.

%package server-sysvinit
Summary:          Legacy sysvinit scripts for server daemon
Requires(post):   chkconfig
Requires(preun):  chkconfig, initscripts
Requires(postun): initscripts

%description server-sysvinit
May be needed f.e. on CentOS.

%prep
%setup -q

%build
#%% configure
make %{?_smp_mflags}

%install
install -pD %{name} %{buildroot}/%{_sbindir}/%{name}

install -Dp -m 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}-client.service
install -Dp -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-server.service

install -Dp -m 0755 %{SOURCE3} %{buildroot}/%{_initrddir}/%{name}-client
install -Dp -m 0755 %{SOURCE4} %{buildroot}/%{_initrddir}/%{name}-server

install -Dp -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-client
install -Dp -m 0644 %{SOURCE6} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-server

%pre
# Add the "hans" user
/usr/sbin/useradd -c "IP over ICMP" -s /sbin/nologin -r %{name} 2> /dev/null || :

%post client
if [ $1 -eq 1 ] ; then
  # Initial installation
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun client
if [ $1 -eq 0 ] ; then
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable %{name}-client.service > /dev/null 2>&1 || :
  /bin/systemctl stop %{name}-client.service > /dev/null 2>&1 || :
fi

%postun client
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
  # Package upgrade, not uninstall
  /bin/systemctl try-restart %{name}-client.service >/dev/null 2>&1 || :
fi

%post client-sysvinit
/sbin/chkconfig --add %{name}-client

%post server-sysvinit
/sbin/chkconfig --add %{name}-server

%preun client-sysvinit
if [ $1 = 0 ] ; then
  /sbin/service %{name}-client stop >/dev/null 2>&1
  /sbin/chkconfig --del %{name}-client
fi

%post server
if [ $1 -eq 1 ] ; then
  # Initial installation
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable %{name}-server.service > /dev/null 2>&1 || :
  /bin/systemctl stop %{name}-server.service > /dev/null 2>&1 || :
fi

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
  # Package upgrade, not uninstall
  /bin/systemctl try-restart %{name}-server.service >/dev/null 2>&1 || :
fi

%preun server-sysvinit
if [ $1 = 0 ] ; then
  /sbin/service %{name}-server stop >/dev/null 2>&1
  /sbin/chkconfig --del %{name}-server
fi

%postun client-sysvinit
if [ "$1" -ge "1" ] ; then
  /sbin/service %{name}-client condrestart >/dev/null 2>&1 || :
fi

%postun server-sysvinit
if [ "$1" -ge "1" ] ; then
  /sbin/service %{name}-server condrestart >/dev/null 2>&1 || :
fi

%files
%doc CHANGES LICENSE README.md
%{_sbindir}/%{name}

%files client
%attr(0600,hans,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-client
%{_unitdir}/%{name}-client.service

%files client-sysvinit
%{_initrddir}/%{name}-client

%files server
%attr(0600,hans,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server
%{_unitdir}/%{name}-server.service

%files server-sysvinit
%{_initrddir}/%{name}-server

%changelog
* Fri Nov 8 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.3-1
- Inital packaging attempt
