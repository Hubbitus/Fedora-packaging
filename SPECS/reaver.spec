Name:           reaver
Version:        1.4
Release:        3%{?dist}
Summary:        Brute force attack against Wifi Protected Setup
License:        GPLv2
URL:            http://code.google.com/p/reaver-wps/
Source0:        http://reaver-wps.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:  libpcap-devel
BuildRequires:  sqlite-devel

%description
Reaver implements a brute force attack against Wifi Protected Setup (WPS)
registrar PINs in order to recover WPA/WPA2 passphrases, as described in
http://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf.

Reaver has been designed to be a robust and practical attack against WPS, and
has been tested against a wide variety of access points and WPS
implementations.

On average Reaver will recover the target AP's plain text WPA/WPA2 passphrase
in 4-10 hours, depending on the AP. In practice, it will generally take half
this time to guess the correct WPS pin and recover the passphrase

%prep
%setup -q

# Drop exec permissions from sources to make rpmlint happy
find -iname '*.h' -or -iname '*.c' -exec chmod -x {} \;

%build
cd src
%configure
make %{?_smp_mflags}

%install
install -m 644 -D src/reaver.db %{buildroot}/%{_sysconfdir}/%{name}/%{name}.db
install -m 755 -D src/%{name} %{buildroot}/%{_bindir}/%{name}
install -m 755 -D src/wash %{buildroot}/%{_bindir}/wash
install -m 644 -D docs/README %{buildroot}/%{_docdir}/%{name}-%{version}/README
install -m 644 -D docs/%{name}.1.gz %{buildroot}/%{_mandir}/man1/%{name}.1.gz

%files
%{_bindir}/%{name}
%{_bindir}/wash
%{_sysconfdir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_docdir}/%{name}-%{version}

%changelog
* Thu Nov 13 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.4-3
- Imported ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/home%3A/zhonghuaren/Fedora_19/src/reaver-1.4-2.1.src.rpm
- Sanitize release number.
- Add wash binary (wifite optionaly want it).
- Cleanup (drop %%clean and so on). Replace $RPM_BUILD_ROOT by %%{buildroot}
- Use always macros instead of direct name.
- Add %%{?dist} tag.

* Tue Jul 10 2012 Huaren Zhong <huaren.zhong@gmail.com> - 1.4
- Rebuild for Fedora

* Fri Jun 08 2012 qmp <glang@lavabit.com> - 1.4-1
- New upstream version
- Removed "walsh" binary

* Sat Jan 14 2012 qmp <glang@lavabit.com> - 1.3-1
- Initial packaging
