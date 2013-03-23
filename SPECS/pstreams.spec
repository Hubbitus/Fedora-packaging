Name:		pstreams
Version:		0.7.0
Release:		1%{?dist}
Summary:		POSIX Process Control in C++

Group:		Development/Libraries
License:		LGPLv3+
URL:			http://%{name}.sourceforge.net/
Source0:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	doxygen
BuildArch:	noarch

%description
PStreams class is like a C++ wrapper for the POSIX.2 functions popen(3) and
pclose(3), using C++ iostreams instead of C's stdio library.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install  DESTDIR=$RPM_BUILD_ROOT prefix=/usr

%clean

%files
%doc doc/html COPYING.LIB README AUTHORS ChangeLog
%{_includedir}/pstreams

%changelog
* Wed Sep 21 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.7.0-1
- First package attempt. Spec file inherited from upstream tarball
