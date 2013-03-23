Name:		mysql-administrator
Version:		5.0r17
Release:		3%{?dist}
Summary:		A graphical tool for handling MySQL queries, construct and analize it

Group:		Applications/Databases
License:		GPLv2+
URL:			http://dev.mysql.com/downloads/gui-tools/5.0.html
# Tarballs not provided anymore. We got source from bazaar:
# bzr export -r tag:bundle-5.0-r17-win32 %{name}-%{version} lp:%{name}; tar --use-compress-program lzma -cf '%{name}-%{version}.tar.lzma' %{name}-%{version}
Source0:		%{name}-%{version}.tar.lzma

Source3:		mysql-administrator.desktop

# Patch outdated configure.in. This is rudiment, because from 5.0r15 Linux sources present, but build not supported.
Patch0:		mysql-administrator-5.0r17-outdated-buildsys.patch
# http://bugs.mysql.com/bug.php?id=32184
Patch1:		mysql-administrator-5.0r17-sigc++.patch
# Pack all available languages. I think it is packaging issue.
Patch2:		mysql-administrator-5.0r17-install-all-i18n.patch

BuildRequires:	autoconf, automake, libtool, gettext, dos2unix
BuildRequires:	openssl-devel, gtkhtml3-devel => 3.6, desktop-file-utils
BuildRequires:	expat-devel, readline-devel, xulrunner-devel
BuildRequires:	libgnomeprint22-devel, mesa-libGLU-devel
BuildRequires:	java-1.6.0-openjdk-devel, funionfs

Requires:		hicolor-icon-theme
Requires:		mysql-gui-common = %{version}
BuildRequires:	mysql-gui-common-static = %{version}, mysql-gui-common-devel = %{version}

%description
MySQL Administrator enables developers and DBAs to easily perform
all the command line operations visually including configuring servers,
administering users, and dynamically monitoring database health. Other
common administrative tasks such as monitoring replication status,
backup and restore, and viewing logs can also be performed through the
MySQL Administrator graphical console.

%prep
%setup0 -q -c -n %{name}-%{version}

cd %{name}-%{version}

mkdir ../mysql-gui-common
funionfs -o dirs=/usr/include/mysql-gui-common=ro:/usr/lib/mysql-gui-common-static=ro none ../mysql-gui-common

%patch0 -p1 -b .buildsys
%patch1 -p2 -b .sigc++
%patch2 -p1 -b .all-i18n


%build
cd %{name}-%{version}
chmod +x mkinstalldirs

NOCONFIGURE=true sh autogen.sh

%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

pushd %{name}-%{version}
dos2unix -k ChangeLog
make install DESTDIR=%{buildroot}

# Files which we want install separately
rm %{buildroot}/%{_datadir}/mysql-gui/MySQLIcon_Admin_{16x16,32x32,48x48}.png %{buildroot}%{_datadir}/applications/MySQLAdministrator.desktop

install -d %{buildroot}/%{_datadir}/icons/hicolor/{16x16,32x32,48x48,128x128}
install -p images/icons/MySQLIcon_Admin_16x16.png %{buildroot}/%{_datadir}/icons/hicolor/16x16/
install -p images/icons/MySQLIcon_Admin_32x32.png %{buildroot}/%{_datadir}/icons/hicolor/32x32/
install -p images/icons/MySQLIcon_Admin_48x48.png %{buildroot}/%{_datadir}/icons/hicolor/48x48/
install -p images/icons/MySQLIcon_Admin_128x128.png %{buildroot}/%{_datadir}/icons/hicolor/128x128/

sed 's@#iconsdir#@%{_datadir}/icons/%{_iconstheme}/48x48@' %{SOURCE3} > %{name}.desktop
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--add-category Development \
	--add-category Application \
	%{name}.desktop
popd

%find_lang %{name}

# Mysql-gui-common built from mysql-querybrowser, so, to avoid unpackaged files errors, we just delete unused files:
#? rm -rf %{buildroot}/%{_datadir}/mysql-gui/common
#? cut -d' ' -f2 mysql-gui-common.lang | xargs -I{} rm "%{buildroot}{}"

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor
	if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	fi

%postun
touch --no-create %{_datadir}/icons/hicolor
	if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{name}-%{version}/ChangeLog
%{_bindir}/%{name}
#it old name of inner binary. Leave to do not change scripts.
%{_bindir}/%{name}-bin
%{_datadir}/mysql-gui/administrator
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/MySQLIcon_Admin_*.png

%changelog
* Sat Dec 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-3
- Changes to reflect link with mysql-gui-common-static as separate package and do not build it again there.
- Remove mysql-gui-common tarball and according patches.

* Mon Nov 30 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-2
- Switch to tar.lzma packaging sources and to "bzr export" instead of "bzr branch" to significantly decrease size of sources (100%-300%!).

* Fri Aug 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-1
- Fork mysql-gui-tools (it was be co-maintained with Dennis Gilmore) in several packages. New Age.
- Mysql-gui-common produced from mysql-querybrowser, it is not needed there.