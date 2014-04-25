Name:          darkstat
Summary:       Network traffic analyzer
Version:       3.0.718
Release:       3%{?dist}
License:       GPLv2
Group:         Applications/Internet
URL:           http://unix4lyfe.org/darkstat/
Source:        http://unix4lyfe.org/%{name}/%{name}-%{version}.tar.bz2
# My own systemd files
Source1:       %{name}.service
Source2:       %{name}.sysconfig
BuildRequires: libpcap-devel, zlib-devel

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd

%description
darkstat is a network traffic analyzer. It's basically a packet sniffer
which runs as a background process on a cable/DSL router and gathers
all sorts of useless but interesting statistics.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR="%{buildroot}"

install -Dp -m 0644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -Dp -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

%pre
getent passwd %{name} >/dev/null || useradd -r -s /sbin/nologin -c "Network traffic analyzer" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc AUTHORS COPYING* LICENSE NEWS README *.txt
%{_mandir}/man8/darkstat.8*
%attr(755,-,-) %{_sbindir}/darkstat
%attr(0600,%{name},root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service

%changelog
* Fri Apr 25 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 3.0.718-3
- Add --disable-silent-rules to configure call.

* Thu Apr 24 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 3.0.718-2
- Do not mark man ad %%doc.
- Add systemd stuff.
- Provide separate user for service.

* Fri Mar 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 3.0.718-1
- Imported from http://pkgs.repoforge.org/darkstat/darkstat-3.0.717-1.rf.src.rpm and rework to prepare for Fedora.
- Update to 3.0.718.
- Cleanup.
- Update URLs.
- Remove INSTALL file from docs (install-file-in-docs rpmlint warning).
- darkstat.x86_64: E: missing-call-to-setgroups /usr/sbin/darkstat, darkstat.x86_64: E: incorrect-fsf-address /usr/share/doc/darkstat/COPYING.GPL issues mailed to author.
- Add BR zlib-devel