Name:           lockfile-progs
Version:        0.1.13
Release:        4%{?dist}
Summary:        Command-line programs to safely lock and unlock files

License:        GPLv2
Group:          Applications/System
# debian package, no real upstream source
URL:            http://packages.qa.debian.org/l/lockfile-progs.html
Source0:        http://ftp.de.debian.org/debian/pool/main/l/%{name}/%{name}_%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  liblockfile


%description
Lockfile-progs provide a method to lock and unlock mailboxes and  files
safely (via liblockfile).

%prep
%setup -q -n sid

%build


%install
rm -rf %{buildroot}
make 
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} -r --preserve=all bin/* %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_mandir}/man1
%{__cp} -r --preserve=all man/* %{buildroot}/%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Wed May 12 2010 Matthias Runge <mrunge@matthias-runge.de> 0.1.13-4
- added requires, homedir created

* Mon May 10 2010 Matthias Runge <mrunge@matthias-runge.de> 0.1.13-3
- patch logcheck-logfiles 

* Sat May 8 2010 Matthias Runge <mrunge@matthias-runge.de> 0.1.13-2
- install man page
- clean up permissions and files section
- user logcheck added

* Wed Apr 28 2010 Matthias Runge <mrunge@matthias-runge.de> 0.1.13-1
- initial spec
