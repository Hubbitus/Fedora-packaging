Name:		mysql-querybrowser
Version:		5.0r17
Release:		3%{?dist}
Summary:		A graphical tool for handling MySQL queries, construct and analize it

Group:		Applications/Databases
License:		GPLv2+
URL:			http://dev.mysql.com/downloads/gui-tools/5.0.html
Source0:		%{name}-%{version}.tar.lzma

Source3:		mysql-querybrowser.desktop

# Patch outdated configure.in. This is rudiment, because from 5.0r15 Linux sources present, but build not supported.
Patch0:		mysql-querybrowser-5.0r17-outdated-buildsys.patch
# http://bugs.mysql.com/bug.php?id=32184
Patch1:		mysql-querybrowser-5.0r17-sigc++.patch
# http://bugs.mysql.com/bug.php?id=32037
Patch2:		mysql-querybrowser-5.0r17-schema_infinite_loop.patch

# 2 patches to build gtksourceview formerly was mysql-gui-tools-5.0_p14-gtk_deprecated_typedefs.patch mysql-gui-tools-5.0r14-GNU-regex.patch
Patch3:		mysql-querybrowser-5.0r17-gtksourceview.patch

# Pack all available languages. I think it is packaging issue.
Patch4:		mysql-querybrowser-5.0r17-install-all-i18n.patch

BuildRequires:	autoconf, automake, libtool, gettext, dos2unix
BuildRequires:	openssl-devel, gtkhtml3-devel => 3.6, desktop-file-utils
BuildRequires:	expat-devel, readline-devel, xulrunner-devel
BuildRequires:	libgnomeprint22-devel, mesa-libGLU-devel
BuildRequires:	java-1.6.0-openjdk-devel, funionfs

Requires:		hicolor-icon-theme
Requires:		mysql-gui-common = %{version}
BuildRequires:	mysql-gui-common-static = %{version}, mysql-gui-common-devel = %{version}

%description
The MySQL Query Browser is a graphical tool provided by MySQL AB for creating,
executing, and optimizing queries in a graphical environment. Where the MySQL
Administrator is designed to administer a MySQL server, the MySQL Query
Browser is designed to help you query and analyze data stored within your MySQL
database.

%prep
%setup0 -q -c -n %{name}-%{version}

cd %{name}-%{version}

mkdir ../mysql-gui-common
funionfs -o dirs=/usr/include/mysql-gui-common=ro:/usr/lib/mysql-gui-common-static=ro none ../mysql-gui-common

%patch0 -p2 -b .old-buildsys
%patch1 -p2 -b .sigc++
%patch2 -p1 -b .loop
%patch3 -p1 -b .gtksourceview
%patch4 -p2 -b .all-i18n

%build
cd %{name}-%{version}
cp ../mysql-gui-common/autogen.sh ./
ln -s ../mysql-gui-common/mkinstalldirs ./

NOCONFIGURE=true sh autogen.sh

%configure --with-gtkhtml=libgtkhtml-3.14

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

pushd %{name}-%{version}
dos2unix -k ChangeLog res/linux/{query-browser.rc,compare_toolbar.glade}

make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}

install -p images/MySQLIcon_QueryBrowser_16x16.png %{buildroot}%{_iconsdir}/hicolor/16x16/
install -p images/MySQLIcon_QueryBrowser_32x32.png %{buildroot}%{_iconsdir}/hicolor/32x32/
install -p images/MySQLIcon_QueryBrowser_48x48.png %{buildroot}%{_iconsdir}/hicolor/48x48/
install -p images/MySQLIcon_Query_Browser_128x128.png %{buildroot}%{_iconsdir}/hicolor/128x128/MySQLIcon_QueryBrowser_128x128.png
rm %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_QueryBrowser_*.png

# Fix old names
mv %{buildroot}/%{_bindir}/mysql-query-browser %{buildroot}/%{_bindir}/%{name}
mv %{buildroot}/%{_bindir}/mysql-query-browser-bin %{buildroot}/%{_bindir}/%{name}-bin

sed 's@#iconsdir#@%{_iconsdir}/%{_iconstheme}/48x48@' %{SOURCE3} > mysql-querybrowser.desktop
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--add-category Development \
	--add-category Application \
	mysql-querybrowser.desktop

popd

%find_lang mysql-query-browser

%clean
fusermount -u mysql-gui-common
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

%files -f mysql-query-browser.lang
%defattr(-,root,root,-)
%doc %{name}-%{version}/ChangeLog
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%{_datadir}/mysql-gui/query-browser
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/MySQLIcon_QueryBrowser_*.png

%changelog
* Tue Dec 8 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-3
- Separate mysql-gui-common into detached package (by example with xorg-x11-server, xorg-x11-server-source).

* Sun Nov 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-2
- Switch to tar.lzma packaging sources and to "bzr export" instead of "bzr branch" to significantly decrease size of sources (100%-300%!).

* Fri Aug 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 5.0r17-1
- Fork mysql-gui-tools (it was be co-maintained with Dennis Gilmore) in several packages. New Age.
- Rename mysql-query-browser to mysql-querybrowser to be closer to upstream.
