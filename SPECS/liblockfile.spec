Name:           liblockfile
Version:        1.08
Release:        2%{?dist}
Summary:        This library implements a number of functions found in -lmail on SysV systems

Group:          Applications/System
License:        GPLv2+
URL:            http://packages.qa.debian.org/libl/liblockfile.html
Source0:        http://ftp.de.debian.org/debian/pool/main/libl/liblockfile/liblockfile_1.08.orig.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This library implements a number of functions found in -lmail on SysV
systems. These functions are designed to lock the standard mailboxes in
/var/mail (or wherever the system puts them).

In additions, this library adds a number of functions to create,
manage and remove generic lockfiles.


%package devel
Summary: header files and libs needed to build apps linked against liblockfile
Group: Development/System
%description devel 
header files and libs needed to build apps linked against liblockfile


%prep
%setup -q

# remove -g root from install
sed -i "s/install -g root -m 755 dotlockfile \$(ROOT)\$(bindir);/install -m 755 dotlockfile \$(ROOT)\$(bindir);/" Makefile.in


%build
%configure 
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_includedir}
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_libdir}
%{__mkdir} -p %{buildroot}/%{_mandir}/man1
%{__mkdir} -p %{buildroot}/%{_mandir}/man3
make ROOT=%{buildroot} install 


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/debug/*
%{_libdir}/*
%{_includedir}/*
%{_mandir}/man3/*
%doc README COPYRIGHT Changelog



%changelog
* Wed Jun 30 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-2
- replace patch by sed-script

* Sat May 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-1
- initial build
