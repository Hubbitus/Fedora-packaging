Summary:		Generic logging layer
Name:		vanessa_logger
Version:		0.0.8
Release:		5%{?dist}
License:		LGPLv2+
URL:			http://www.vergenet.net/linux/vanessa/
Group:		Development/Libraries
Source0:		http://www.vergenet.net/linux/vanessa/download/vanessa_logger/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
BuildRequires:	automake autoconf libtool
#Patch0:		vanessa_logger-0.0.7.error:label_at_end_of_compound_statement.patch

%description
Generic logging layer that may be used to log to one or more of syslog,
an open file handle or a file name. Though due to limitations in the
implementation of syslog opening multiple syslog loggers doesn't makes
sense. Includes the ability to limit which messages will be logged based
on priorities.

# As subpackages defined -devel subpackage also must be explicit.
%package	devel
Summary:	Headers and static libraries for development
Group:	Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers and static libraries required to develop against vanessa_logger.

%package	sample
Summary:	Example programme that demonstrates vanessa_logger
Group:	Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description	sample
Sample programme with source that demonstrates various features of
vanessa_logger.


%prep
%setup -q

#% patch0 -p0 -b .label

%build

# I am providing my own configure macro replacement. Hopefully this
# will result in fewer portability problems than using the one supplied
# by various vendours. I fear that I hope in vein.
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
if [ -f configure.in ]; then
	aclocal
	libtoolize --force --copy
	automake --add-missing
	autoheader
	autoconf
fi
%configure --disable-static

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{prefix}/doc
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_libdir}/*.*a

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc README COPYING ChangeLog

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*.h
%doc COPYING README

%files sample
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/vanessa_logger_sample.*
%doc sample/*.c sample/*.h README

%changelog
* Sun Dec 20 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.8-5
- New version 0.0.8

* Mon Aug 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-4
- Historical ./configure with huge amount parameters replaced by %%configure macro.
- Removed unnecessary requires /sbin/ldconfig
- Removed the files README,COPYING from the devel package

* Sun Aug 23 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-3
- Fix typo in condition (confgure.in instead of configure.in) (thanks to Andrew Colin Kissa)
- vanessa_logger-sample depend on vanessa_logger not on vanessa_logger-devel (thanks to Andrew Colin Kissa)
- Add --add-missing flag to automake command and put it before autoheader.

* Tue Aug 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.0.7-2
- Ressurect old http://hubbitus.net.ru/rpm/Fedora9/vanessa_logger/vanessa_logger-0.0.6-1.fc8.Hu.1.src.rpm.
- New version 0.0.7
- Rename spec to classic %%{name}.spec.
- Remove Hu part from release.
- Strip some old comments and unneded commands/macroses.
- Replace $RPM_BUILD_ROOT by %%{buildroot}.
- Move %%doc README COPYING ChangeLog from devel to main package.
- Old BuildPrereq tag replaced by BuildRequires.
- Make setup quiet.
- Adopt patch to new version, and name accordingly: vanessa_logger-0.0.7.error:label_at_end_of_compound_statement.patch.
- Remove *.*a files in %%install.
- License changed to LGPLv2+ from just LGPL according to README.
- Add Requires(postun):	/sbin/ldconfig, Requires(post):	/sbin/ldconfig, and %%post/%%postun ldconfig invoke.
- Move %%{_libdir}/*.so into -devel.
- Add COPYING also in %%doc of -devel, README in all packages.
- Add --disable-static in configure options (with it .la file not produced).

* Mon Dec 31 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.0.6-1
- Replace Tag Copyright by License
- Reformat all with tabs
- Change BuildRoot:	to correct (intead of hardcoded path): %%{_tmppath}/%%{name}-%%{version}-%%{release}-%%(%%{__id_u} -n)
- Delete (Comment out) %%define prefix	/usr
- Change from Release:	1 to Release:	%%{rel}%%{?dist}.Hu.0

* Fri Dec 14 2001 Horms <horms@verge.net.au>
  Revamped configure to use %%{_libdir} and friends. This should be more
  distribution indepentant. With thanks to Scot W. Hetzel <scot@genroco.com>
* Thu Apr 26 2001 Horms <horms@verge.net.au>
  Updated to "work" with Red Hat 7
* Sat Sep 15 2000 Horms <horms@verge.net.au>
  created for version 0.0.0
