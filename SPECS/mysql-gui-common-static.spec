# I do mysql-gui-common-static main package, because otherwise I can't mark it as arch-specific and got error:
# error: line 46: Only noarch subpackages are supported: BuildArch: i386
# Rpm does not support it yet - http://www.opensubscriber.com/message/fedora-devel-list@redhat.com/11453697.html
Name:		mysql-gui-common-static
# Aka RealName
%global		rname	mysql-gui-common
Version:		5.0r17
Release:		1%{?dist}
Summary:		Static libs for developers

Group:		Applications/Databases
License:		GPLv2+
URL:			http://dev.mysql.com/downloads/gui-tools/5.0.html
# Tarballs not provided anymore. We got source from bazaar:
# I ask Denis Gilmore and they ask what it is common practice include common sources (mysql-gui-common also in mysql-administrator and others)
#bzr export -r tag:bundle-5.0-r17-win32 mysql-gui-common-5.0r17 lp:mysql-gui-common; tar --use-compress-program lzma -cf 'mysql-gui-common-5.0r17.tar.lzma' mysql-gui-common-5.0r17
Source0:		%{rname}-%{version}.tar.lzma

# Patch outdated configure.in. This is rudiment, because from 5.0r15 Linux sources present, but build not supported.
Patch0:		%{rname}-5.0r17-outdated-buildsys.patch
# http://bugs.mysql.com/bug.php?id=32184
Patch1:		%{rname}-5.0r17-sigc++.patch
# Pack all available languages. I think it is packaging issue.
Patch2:		%{rname}-5.0r17-install-all-i18n.patch

BuildRequires:	autoconf, automake, libtool, gettext, dos2unix
BuildRequires:	libxml2-devel, glib2-devel, gtkmm24-devel >= 2.6, libglade2-devel
BuildRequires:	mysql-devel >= 4.0, pcre-devel

%description
Static libs for mysql-gui-common. Primarly for developers to build
mysql-querybrowser and mysql administrator.

%package		-n %{rname}-devel
Summary:		Headers for %{rname}
Group:		System Environment/Libraries
BuildArch:	noarch

%description -n %{rname}-devel
Headers for %{rname}

%package		-n %{rname}
Summary:		Common data shared among the MySQL GUI Suites
Group:		System Environment/Libraries
Obsoletes:	mysql-gui-tools <= 5.0r14
Provides:		mysql-gui-tools = %{version}
BuildArch:	noarch

%description -n %{rname}
This package contains glade files images and translations used by mysql tools
at runtime

%prep
%setup0 -q -n %{rname}-%{version}

# Common also
%patch0 -p2 -b .old-buildsys
%patch1 -p2 -b .sigc++
%patch2 -p2 -b .all-i18n

%build
NOCONFIGURE=true sh ./autogen.sh
%configure --enable-php-modules --enable-python-modules --enable-readline
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
dos2unix -k COPYING README README.translating ChangeLog

mv README.translating README.translating.old
iconv README.translating.old -f ISO-8859-1 -t UTF-8 > README.translating
touch --reference README.translating.old README.translating && rm README.translating.old

make install DESTDIR=%{buildroot}

	# Install static libs
	for a in source/linux/libqbcommongui.a library/base-library/source/.libs/libmysqlx.a library/sql-parser/source/.libs/libsqlparser.a library/utilities/source/.libs/libguiutil.a \
		source/linux/libmacommongui.a ; do
	install -d %{buildroot}%{_libdir}/%{rname}-static/$( dirname $a )
	install -p -m 0644 $a %{buildroot}%{_libdir}/%{rname}-static/$a
	done

	# Install devel headers
	for d in library/base-library/include library/utilities/include library/utilities/shared_include source/linux ; do
	install -d %{buildroot}/%{_includedir}/%{rname}/$d
	install -p -m 0644 $d/*.h %{buildroot}/%{_includedir}/%{rname}/$d/
	done
install -p autogen.sh mkinstalldirs %{buildroot}/%{_includedir}/%{rname}/
install -Dp -m 0644 po/mysql-gui-common-template.po %{buildroot}/%{_includedir}/%{rname}/po/mysql-gui-common-template.po

%find_lang %{rname}

%clean
rm -rf %{buildroot}

%files -n %{rname} -f %{rname}.lang
%defattr(-,root,root,-)
%doc COPYING README README.translating ChangeLog
%{_datadir}/mysql-gui

%files -n %{rname}-static
%defattr(-,root,root,-)
%{_libdir}/%{rname}-static/source/linux/libqbcommongui.a
%{_libdir}/%{rname}-static/source/linux/libmacommongui.a
%{_libdir}/%{rname}-static/library/base-library/source/.libs/libmysqlx.a
%{_libdir}/%{rname}-static/library/sql-parser/source/.libs/libsqlparser.a
%{_libdir}/%{rname}-static/library/utilities/source/.libs/libguiutil.a

%files -n %{rname}-devel
%defattr(-,root,root,-)
%{_includedir}/%{rname}

%changelog
* Wed Dec 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-1
- Initial separate release (was in mysql-querybrowser)
