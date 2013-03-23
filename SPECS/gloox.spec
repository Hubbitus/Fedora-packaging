#% define prerel rc3
#% define SVN 4204

Name:		gloox
Version:		1.0
Release:		1.10%{?prerel:%{prerel}.}%{?SVN:SVNr%{SVN}}%{?dist}
Summary:		A rock-solid, full-featured Jabber/XMPP client library
Group:		System Environment/Libraries
License:		GPLv2
URL:			http://camaya.net/gloox

%if 0%{?prerel}
# svn export svn://svn.camaya.net/gloox/trunk gloox-1.0rc3 \
#	tar -cjf gloox-1.0rc3-SVNr4203.tar.bz2 gloox-1.0rc3
Source0:		%{name}-%{version}%{?prerel}%{?SVN:-SVNr%{SVN}}.tar.bz2
%else
Source0:		http://camaya.net/download/%{name}-1.0.tar.bz2
%endif

#Patch1:		gloox-no_ns_get16.patch
#Patch1:		gloox-getaddrinfo.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libtool, autoconf, automake
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	gnutls-devel >= 1.2
BuildRequires:	zlib-devel >= 1.2.3
BuildRequires:	libidn-devel >= 0.5

Requires(postun):	/sbin/ldconfig
Requires(post):	/sbin/ldconfig

%description
gloox is a rock-solid, full-featured Jabber/XMPP client library, written in
C++. It makes writing spec-compliant clients easy and allows for hassle-free
integration of Jabber/XMPP functionality into existing applications.

%package		devel
Summary:		Development files for %{name}
Group:		Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}%{?prerel}

%build
%if 0%{?SVN}
./autogen.sh
%endif

%configure --disable-static

make %{?_smp_mflags}
# recode to UTF
mv -f AUTHORS AUTHORS.old
iconv -f iso8859-1 -t UTF-8 AUTHORS.old > AUTHORS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README TODO UPGRADING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so

%changelog
* Sat Nov 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-1.10
- long-awaited release 1.0

* Mon Oct 19 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.9.rc3.SVNr4204
- As right mention Peter Lemenkov, my naming cheme is incorrect, renum it.
- Expand "beta" define and magick to "prerel".

* Sun Oct 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0rc3-0.8.SVNr4204
- New build due resolve my bugreport https://mail.camaya.net/horde/whups/ticket/?id=157

* Sun Oct 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0rc3-0.7.SVNr4203
- rc3.
- Euroelessar (one of qutIM developer, thank you) submit patches:
	http://bugs.camaya.net/horde/whups/ticket/?id=110
	http://bugs.camaya.net/horde/whups/ticket/?id=155
	http://bugs.camaya.net/horde/whups/ticket/?id=154
	http://bugs.camaya.net/horde/whups/ticket/?id=153
	http://bugs.camaya.net/horde/whups/ticket/?id=152
	http://bugs.camaya.net/horde/whups/ticket/?id=151
	http://bugs.camaya.net/horde/whups/ticket/?id=150
	http://bugs.camaya.net/horde/whups/ticket/?id=149
	all is important and rev 4200 at least required.
- Include UPGRADING to %%doc

* Wed Jul 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.6.SVNr4029
- New build due to close several bugs:
	https://mail.camaya.net/horde/whups/ticket/?id=140 - delete patch gloox-1.0-beta-SVNr4003-missed_header.patch
	https://bugs.camaya.net/horde/whups/ticket/?id=141 - delete patch gloox-1.0-GCC4.4-missing_includes.patch
	https://bugs.camaya.net/horde/whups/ticket/?id=137 - delete patch gloox-1.0-SVNr4003.glibc-private-symbol.patch
- Use "svn export" instead of "svn checkout".

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.SVNr4003
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.5.SVNr4003
- Add --exclude='.svn' to tar pack source and set time to last commit. This may allow pass hash checking soucre later.

* Tue Apr 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.4.SVNr4003
- Add Patch3: gloox-1.0-GCC4.4-missing_includes.patch to allow build on GCC4.4

* Tue Apr 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.3.SVNr4003
- REmade patch1. Instead of just comment private stuff I use temporray ugly hack - copy-past function implementation from glibc source until
	author do not reimplement it properly.

* Sun Apr 5 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.2.SVNr4003
- Add patch2 gloox-1.0-beta-SVNr4003-missed_header.patch - see bug http://bugs.camaya.net/horde/whups/ticket/?id=140

* Sun Apr 5 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.1.SVNr4003
- qutIM require gloox version 1.0 with SVN revision >= 3873. Try build current.
- Patch1 (http://bugs.camaya.net/horde/whups/ticket/?id=137) little adopted (gloox-1.0-beta7.glibc-private-symbol.patch -> gloox-1.0-SVNr4003.glibc-private-symbol.patch).
- Add SVN part into Release tag.

* Fri Mar 27 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0-0.0.beta3
- Import http://www.salstar.sk/pub/fedora/SRPMS/10/gloox-1.0-0.0beta3.fc10.src.rpm
- Step to 1.0-beta7 version
- Reformat with tabs spec file.
- %%beta (replace %%beta_version) now represent only number. According it change all mention of it.
- Add Requires(postun): /sbin/ldconfig and Requires(post): /sbin/ldconfig

* Fri Mar 7 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.9.9.4-1
- update to upstream

* Mon Feb 28 2008 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.9.9.3-1
- update to upstream

* Sun Dec 2 2007 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.9.7-2
- removed patch
- added undef for HAVE_RES_QUERY, HAVE_RES_QUERYDOMAIN, HAVE_DN_SKIPNAME
  see: https://mail.camaya.net/horde/whups/ticket/?id=52

* Wed Nov 28 2007 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.9.7-1
- update upstream
- added patch to avoid dependecny problem on libresolv.so.2(GLIBC_PRIVATE)

* Mon Sep 17 2007 Jan ONDREJ (SAL) <ondrejj(at)salstar.sk> - 0.9.4.1-1
- first release
