Name:           lockfile
Version:        1.08
Release:        4%{?dist}
Summary:        This implements a number of functions found in -lmail on SysV systems

Group:          Applications/System
# regarding license please see file COPYRIGHT
License:        GPLv2+ or LGPLv2+
URL:            http://packages.qa.debian.org/libl/liblockfile.html
Source0:        http://ftp.de.debian.org/debian/pool/main/libl/liblockfile/liblockfile_1.08.orig.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library implements a number of functions found in -lmail on SysV
systems. These functions are designed to lock the standard mailboxes in
/var/mail (or wherever the system puts them).

In additions, this library adds a number of functions to create,
manage and remove generic lockfiles.

%package libs
Summary: Library for applications using lockfile
Group: System Environment/Libraries

%description libs
library needed for applications linked against lockfile

%package devel
Summary: Header files needed to build apps linked against lockfile
Group: Development/Libraries
Requires: lockfile-libs 

%description devel 
header files needed to build apps linked against lockfile


%prep
%setup -q -n liblockfile-%{version}

# remove -g root from install
sed -i "s/install -g root -m 755 dotlockfile \$(ROOT)\$(bindir);/install -m 755 dotlockfile \$(ROOT)\$(bindir);/" Makefile.in

sed -i "s/ln -s liblockfile.so.\$(VER) \$(ROOT)\$(libdir)\/liblockfile.so//" Makefile.in

%build
%configure 
make %{?_smp_mflags} shared


%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_includedir}
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_libdir}
%{__mkdir} -p %{buildroot}/%{_mandir}/man1
%{__mkdir} -p %{buildroot}/%{_mandir}/man3
make ROOT=%{buildroot} install_shared
ln -s %{_libdir}/liblockfile.so.1.0 %{buildroot}/%{_libdir}/liblockfile.so

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%exclude %{_libdir}/debug/
%{_libdir}/*.so*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/debug/
%{_includedir}/*
%{_mandir}/man3/*
%doc README COPYRIGHT Changelog



%changelog
* Wed Jul 28 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-4
- rename to lockfile
- sort lib to top package, fix license, build shared lib

* Sun Jul 18 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-3
- fix up hidden dirs, and links

* Wed Jun 30 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-2
- replace patch by sed-script

* Sat May 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-1
- initial build
