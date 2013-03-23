Summary:		Library of Abstract Data Types 
Name:		vanessa_adt
Version:		0.0.7
Release:		6%{?dist}
License:		LGPLv2+
URL:			http://www.vergenet.net/linux/vanessa/
Group:		Development/Libraries
Source0:		http://www.vergenet.net/linux/vanessa/download/%{name}/%{version}/%{name}-%{version}.tar.gz
Requires:		vanessa_logger >= 0.0.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:	automake autoconf libtool vanessa_logger-devel >= 0.0.5

%description
Library of Abstract Data Types (ADTs) that may be useful.  Includes queue,
dynamic array and key value ADT.

%package		devel
Summary:		Headers and static libraries for development
Group:		Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		vanessa_logger-devel >= 0.0.5

%description devel
Headers and static libraries required to develop against vanessa_adt.

%prep
%setup -q

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
if [ -f configure.in ]; then
	aclocal
	libtoolize --force --copy
	automake --add-missing
	autoheader
	autoconf
fi
%configure --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{etc,%{prefix}/{lib,bin,doc}}
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.*a

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%doc README COPYING ChangeLog

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Tue Aug 25 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-6
- Add %%{?_smp_mflags}
- End Fedora review.

* Mon Aug 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-5
- Fedora Review started. Thanks to Andrew Colin Kissa.
- Historical ./configure with huge amount parameters replaced by %%configure macro.
- Removed unnecessary requires /sbin/ldconfig
- Removed the files README,COPYING from the devel package

* Sun Aug 23 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-4
- Fix typo in condition (confgure.in instead of configure.in) (thanks to Andrew Colin Kissa)
- Add --add-missing flag to automake command and put it before autoheader.

* Tue Aug 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-3
- Ressurect old http://hubbitus.net.ru/rpm/Fedora9/vanessa_adt/vanessa_adt-0.0.7-2.fc8.Hu.0.src.rpm
- Rename spec to classic %%{name}.spec.
- Remove Hu part from release.
- Strip some old comments and unneded commands/macroses.
- Replace $RPM_BUILD_ROOT by %%{buildroot}.
- Move %%doc README COPYING ChangeLog from devel to main package.
- Delete unversioned explicit provides: Provides:		%%{name}-%%{version}
- Old BuildPrereq tag replaced by BuildRequires.
- Make setup quiet.
- Remove *.*a files in %%install.
- Add Requires(postun):	/sbin/ldconfig, Requires(post):	/sbin/ldconfig, and %%post/%%postun ldconfig invoke.
- Move %%{_libdir}/*.so into -devel.
- Add COPYING also in %%doc of -devel, README in all packages.
- In devel turn "Provides: %%{name}-devel-%%{version}" to "%%{name}-devel = %%{version}-%%{release}".
- Add --disable-static in configure options (with it .la file not produced).
- Licence changed to LGPLv2+ from just LGPL.

* Mon Dec 31 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.0.7-2
- Replace Tag Copyright by License
- Change license to it abbriviation LGPL (was GNU Lesser General Public Licence)
- Reformat all with tabs
- Change BuildRoot:	to correct (intead of hardcoded path): %%{_tmppath}/%%{name}-%%{version}-%%{release}-%%(%%{__id_u} -n)
- Delete (Comment out) %%define prefix	/usr
- Change from Release:	1 to Release:	2%%{?dist}.Hu.0

* Fri Dec 14 2001 Horms <horms@verge.net.au>
  Revamped configure to use %%{_libdir} and friends. This should be more
  distribution indepentant. With thanks to Scot W. Hetzel <scot@genroco.com>

* Sat Sep 2 2000 Horms <horms@verge.net.au>
  created for version 0.0.0
