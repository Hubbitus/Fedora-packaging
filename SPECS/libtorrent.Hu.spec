%define SVNdate 20090104
%define SVNrev 1087

Name:		libtorrent
License:		GPL
Group:		System Environment/Libraries
Version:		0.12.4
Release:		0.1.%{SVNdate}svn%{SVNrev}rev%{?dist}
Summary:		BitTorrent library with a focus on high performance & good code
URL:			http://libtorrent.rakshasa.no/
%if 0%{?SVNrev}
#svn checkout -r %{SVNrev} svn://rakshasa.no/libtorrent/trunk/%{name} %{name}-%{version}; tar -cjf '%{name}-%{version}-SVN%{SVNdate}rev%{SVNrev}.tar.bz2' %{name}-%{version}
Source0:		%{name}-%{version}-SVN%{SVNdate}rev%{SVNrev}.tar.bz2
%else
Source0:		http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	pkgconfig, openssl-devel, libsigc++20-devel
BuildRequires:	gcc > 4.1

%description
LibTorrent is a BitTorrent library written in C++ for *nix, with a focus 
on high performance and good code. The library differentiates itself 
from other implementations by transfering directly from file pages to 
the network stack. On high-bandwidth connections it is able to seed at 
3 times the speed of the official client.

%package devel
Summary: Libtorrent development environment
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header and library definition files for developing applications
with the libtorrent libraries.

%prep
%setup -q
%if 0%{?SVNrev}
./autogen.sh
%endif

%build

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README NEWS
%{_libdir}/libtorrent.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libtorrent.pc
%{_includedir}/torrent
%{_libdir}/*.so

%changelog
* Mon Jan 5 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su>
- Remove patch0 libtorrent-gcc43-v2.patch which is not needed anymore.
- Add BuildRequires: gcc > 4.1 and remove ugly hacks to build on gcc-4.1

* Sun Jan 4 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.12.4-0.1.20090104svn1087rev
- Build 0.12.4 SVN version
- Add all SVN-build logick (%%if 0%%{?SVNrev} ...)
- Disable patch0 libtorrent-gcc43-v2.patch

* Sun Jun 1 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.12.2-0.Hu.0
- Step to version 0.12.2
- For compile on gcc 4.3 (Bug 1266 http://libtorrent.rakshasa.no/ticket/1266)
	Add patch http://libtorrent.rakshasa.no/attachment/ticket/1266/libtorrent-gcc43-v2.patch?format=raw

* Sat Apr 19 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.12.0-0.Hu.0
- Step to version 0.12.0

* Mon Dec 24 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.11.9
- Stable build
- Change release enumaration to 1%{?dist}.Hu.0 from 1.Hu.0%{?dist}

* Tue Nov 27 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.11.9
- 0.11.9 unstable build

* Tue Oct 2 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.11.8
- 0.11.8 unstable build

* Fri Aug 17 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.11.7
- Switch to version 0.11.7

* Sun Jun 10 2007 Pavel Alexeev <Pahan [at] hubbitus [dot] info> - 0.11.4
- Switch to new version 0.11.4

* Sun Jan  7 2007 Pavel Alexeev <pahan@hubbitus.info> - 0.11.1
- Switch to new version 0.11.1

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Oct 02 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-3
- Bump EVR to fix broken upgrade path (BZ #208985)

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-1
- New upstream release

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-3
- FC6 rebuild, re-tag

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-1
- Upgrade to 0.10.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.9.3-1
- Upgrade to new upstream version 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-2
- Improved general summary & devel package description 
- Simplified devel package includedir files section
- Removed openssl as requires, its implied by .so dependency
- Correct devel package Group

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-1
- Initial version
