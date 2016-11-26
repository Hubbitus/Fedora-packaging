# Review request: https://bugzilla.redhat.com/show_bug.cgi?id=1028743

Name:             hans
Version:          1.0
Release:          1%{?dist}
Summary:          IP over ICMP tunneling solution
Group:            System Environment/Daemons

License:          GPLv3+
URL:              http://code.gerade.org/hans/
Source0:          https://github.com/friedrich/%{name}/archive/v%{version}.tar.gz#/hans-%{version}.tar.gz
# My systemd and preconfiguration stuff
Source1:          %{name}-client.service
Source2:          %{name}-server.service
Source3:          %{name}-client.sysconfig
Source4:          %{name}-server.sysconfig
Requires(pre):    shadow-utils

%description
Hans makes it possible to tunnel IPv4 through ICMP echo packets, so you could
call it a ping tunnel. This can be useful when you find yourself in the
situation that your Internet access is firewalled, but pings are allowed.

Hans runs on Linux as a client and a server. It runs on Mac OS X,
iPhone/iPod touch, FreeBSD and OpenBSD as a client only.

You probably want also install packages %{name}-client or %{name}-server or both

%package client
Summary:          Client part of solution to tunnel IPv4 data through a ICMP
Group:            System Environment/Daemons
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
Requires:         %{name}

%description client
This is the client part of %{name} solution.

%package server
Summary:          Server part of solution to tunnel IPv4 data through a ICMP
Group:            System Environment/Daemons
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
Requires:         %{name}

%description server
This is the server part of %{name} solution.

%prep
%setup -q

%build
#%% configure
make %{?_smp_mflags}

%install
install -pD %{name} %{buildroot}/%{_sbindir}/%{name}

install -Dp -m 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}-client.service
install -Dp -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-server.service

install -Dp -m 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-client
install -Dp -m 0644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-server

%pre
getent passwd %{name} >/dev/null || useradd -r -s /sbin/nologin -c "IP over ICMP tunneling user" %{name}
exit 0

%pre server
# Add the "hans" user
/usr/sbin/useradd -c "IP over ICMP" -s /sbin/nologin -r %{name} 2> /dev/null || :

%post client
%systemd_post %{name}.service

%preun client
%systemd_preun %{name}.service

%postun client
%systemd_postun_with_restart %{name}.service

%post server
%systemd_post %{name}.service

%preun server
%systemd_preun %{name}.service

%postun server
%systemd_postun_with_restart %{name}.service

%files
%doc CHANGES README.md
%license LICENSE
%{_sbindir}/%{name}

%files client
%attr(0600,hans,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-client
%{_unitdir}/%{name}-client.service

%files server
%attr(0600,hans,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server
%{_unitdir}/%{name}-server.service

%changelog
* Sun Nov 27 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-1
- Thanks to Michal Ambroz for taking review.
- Update to version 1.0.
- Add tarball name into source url.
- Mark license with appropriate macros.

* Tue Mar 11 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.3-3
- Drop all sysvinit support because it now MUST NOT be present in new packages (https://fedoraproject.org/wiki/Packaging:SysVInitScript?rd=Packaging/SysVInitScript#Initscripts_in_addition_to_systemd_unit_files).
- Change user creation procedure, move in base package.

* Sun Nov 10 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.3-2
- Surround by condition systemd related stuff to allow build and work on EPEL.

* Fri Nov 8 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.3-1
- Inital packaging attempt
