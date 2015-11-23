Summary:	An HTTP and FTP simulating application load
Name:	curl-loader
Version:	0.56
Release:	1%{?dist}
Url:		http://curl-loader.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
License:	GPLv2

BuildRequires: openssl-devel, zlib-devel, libevent-devel, libcurl-devel
BuildRequires: c-ares-devel

%description
curl-loader (also known as "omes-nik" and "davilka") is an open-source
tool written in C-language, simulating application load and application
behavior of thousands and tens of thousand HTTP/HTTPS and FTP/FTPS
clients, each with its own source IP-address. In contrast to other
tools curl-loader is using real C-written client protocol stacks,
namely, HTTP and FTP stacks of libcurl and TLS/SSL of openssl,
and simulates user behavior with support for login and authentication
flavors.

The goal of the project is to deliver a powerful and flexible
open-source testing solution as a real alternative to Spirent
Avalanche and IXIA IxLoad.

%prep
%setup

# remove bundled libs
rm -rf packages

# To make rpmlint happier
chmod -x doc/*

%build
# Unfortunately build failed with %%{?_smp_mflags}
make

%install
make install DESTDIR="%{buildroot}"


%files
%doc doc/* conf-examples
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}-config.5.gz

%changelog
* Mon Nov 23 2015 Pavel Alexeev <Pahan@Hubbitus.info>
- Mail list about patches remove and curl unbundling: http://sourceforge.net/p/curl-loader/mailman/curl-loader-devel/?viewmonth=201509

* Mon Jul 13 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.56-1
- Import http://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/i586/SRPMS.classic/curl-loader-0.56-alt1.src.rpm, rework

* Sat Feb 16 2013 Valentin Rosavitskiy <valintinr@altlinux.org> 0.56-alt1
- Initial build

