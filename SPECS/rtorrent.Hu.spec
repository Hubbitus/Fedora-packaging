%define SVNdate 20090104
%define SVNrev 1087

Name:		rtorrent
License:		GPL
Group:		Applications/Internet
Version:		0.8.4
Release:		0%{?dist}.Hu.0
Summary:		BitTorrent client based on libtorrent 
URL:			http://rtorrent.rakshasa.no/
%if 0%{?SVNrev}
#svn checkout -r %{SVNrev} svn://rakshasa.no/libtorrent/trunk/%{name} %{name}-%{version}; tar -cjf '%{name}-%{version}-SVN%{SVNdate}rev%{SVNrev}.tar.bz2' %{name}-%{version}
Source0:		%{name}-%{version}-SVN%{SVNdate}rev%{SVNrev}.tar.bz2
%else
Source0:		http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
%endif
Source1:		rtorrent.rc.example
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libstdc++-devel, pkgconfig, libsigc++20-devel, libtorrent-devel >= 0.11.3, curl-devel, ncurses-devel
Requires:		libtorrent >= 0.12.0
BuildRequires:	gcc > 4.1

%description
A BitTorrent client using libtorrent, which on high-bandwidth connections is 
able to seed at 3 times the speed of the official client. Using
ncurses its ideal for use with screen or dtach. It supports 
saving of sessions and allows the user to add and remove torrents and scanning
of directories for torrent files to seed and/or download.

%prep
%setup -q
%if 0%{?SVNrev}
./autogen.sh
%endif

%build
install -m 644 %{SOURCE1} .
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT
		  
%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README TODO rtorrent.rc.example 
%{_bindir}/rtorrent
%{_mandir}/man1/rtorrent*

%changelog
* Mon Jan 5 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su>
- Build 0.8.4 SVN version
- Add defining SVNdate and SVNrev
- Add all SVN-build logick (%%if 0%%{?SVNrev} ...)
- Remove Patch0: rtorrent-gcc43.patch which is not needed anymore.
- Add BuildRequires: gcc > 4.1 and remove ugly hacks to build on gcc-4.1

* Mon Aug 25 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.8.2-0.Hu.0
- Version 0.8.2
- Build for F9

* Sun Jun 1 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.8.0-0.Hu.0
- Step to version 0.8.2
- For build on gcc 4.3 ( bug http://libtorrent.rakshasa.no/ticket/1267 )
	Add patch	http://libtorrent.rakshasa.no/attachment/ticket/1267/rtorrent-gcc43.patch?format=raw

* Sat Apr 19 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.8.0-0.Hu.0
- Step to version 0.8.0
- Adjust Requires:		libtorrent >= 0.12.0

* Mon Dec 24 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.7.9
- Stable build
- Change release enumaration to 1%{?dist}.Hu.0 from 1.Hu.0%{?dist}

* Tue Oct 2 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.7.9
- 0.7.9 unstable build

* Fri Aug 17 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.7.7
- Switch to version 0.7.7

* Sun Jun 10 2007 Pavel Alexeev <Pahan [at] Hubbitus [dot] info> - 0.7.4
- Switch to new version 0.7.4
- Requires libtorrent >= 0.11.3
- Build-Requires libtorrent-devel >= 0.11.3

* Sun Jan  7 2007 Pavel Alexeev <Pahan [at] Hubbitus [dot] info> - 0.7.1
- Switch to new version 0.7.1

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> - 0.6.2-5
- rebuild against new curl

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-4
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-3
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-2
- New upstream version

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-1
- Upgrade to 0.6.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.5.3-1
- Upgrade to new upstream version 0.5.3
- And changed libtorrent dependency to >= 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-3
- Added ncurses-devel to buildrequirements

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-2
- Improved summary & description
- Removed explicit requires, leaving to rpm
- Changed mode of rtorrent.rc.example to 644

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-1
- Initial version
