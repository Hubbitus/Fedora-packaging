Name:          darkstat
Summary:       Network traffic analyzer
Version:       3.0.718
Release:       1%{?dist}
License:       GPLv2
Group:         Applications/Internet
URL:           http://unix4lyfe.org/darkstat/
Source:        http://unix4lyfe.org/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: libpcap-devel, zlib-devel

%description
darkstat is a network traffic analyzer. It's basically a packet sniffer
which runs as a background process on a cable/DSL router and gathers
all sorts of useless but interesting statistics.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR="%{buildroot}"

%files
%doc AUTHORS COPYING* LICENSE NEWS README *.txt
%doc %{_mandir}/man8/darkstat.8*
%attr(755,-,-) %{_sbindir}/darkstat

%changelog
* Fri Mar 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 3.0.718-1
- Imported from http://pkgs.repoforge.org/darkstat/darkstat-3.0.717-1.rf.src.rpm and rework to prepare for Fedora.
- Update to 3.0.718.
- Cleanup.
- Update URLs.
- Remove INSTALL file from docs (install-file-in-docs rpmlint warning).
- darkstat.x86_64: E: missing-call-to-setgroups /usr/sbin/darkstat, darkstat.x86_64: E: incorrect-fsf-address /usr/share/doc/darkstat/COPYING.GPL issues mailed to author.
- Add BR zlib-devel