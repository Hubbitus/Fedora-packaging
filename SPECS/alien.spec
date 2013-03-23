Summary:	Install Debian, Slackware, and Stampede packages with rpm
Name:	alien
Version:	8.83
Release:	2
URL:		http://kitenet.net/~joey/code/alien/
Source:	http://ftp.de.debian.org/debian/pool/main/a/%{name}/%{name}_%{version}.tar.gz
License:	GPLv2
Group:	Applications/Text
Requires:	perl
BuildRequires:	perl-ExtUtils-MakeMaker
BuildArchitectures:	noarch

%description
Alien allows you to convert Debian, Slackware, and Stampede Packages into Red
Hat packages, which can be installed with rpm.

It can also generate Slackware, Debian and Stampede packages.

This is a tool only suitable for binary packages.

%prep
%setup -qn %{name}

%install
perl Makefile.PL PREFIX=%{buildroot}/usr
make
make pure_install VARPREFIX=%{buildroot}
find %{buildroot} -not -type d -printf "/%%P\n" | \
	sed '/\/man\//s/$/\*/' > manifest

%files -f manifest
%defattr(-,root,root,-)
%doc debian/changelog GPL README alien.lsm

%changelog
* Mon Jan 24 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 8.83-2
- New version 8.83
