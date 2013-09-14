%global SVN 4651

%ifarch ppc ppc64
%define oraclever 10.2.0.2
%else
%define oraclever 11.1.0.7
%endif

%ifarch x86_64
# "client64" is only on 11.1 and x86_64, (10.2 use client)
%define oraclelib %{_libdir}/oracle/%{oraclever}/client64/lib
%define oracleinc %{_includedir}/oracle/%{oraclever}/client64
%else
%define oraclelib %{_libdir}/oracle/%{oraclever}/client/lib
%define oracleinc %{_includedir}/oracle/%{oraclever}/client
%endif


Summary:       Toolkit for Oracle (Postgres and MySQL supported too)
Name:          tora
Version:       3
Release:       0.2%{?SVN:.svn%{SVN}}%{?dist}
URL:           http://tora.sourceforge.net
Group:         Applications/Databases
License:       GPLv2

# See soure1 script to reproduce tarball
Source0:       %{name}-%{version}%{?SVN:-svn%{SVN}}.tar.xz
Source1:       tora.get.tarball.svn
Source2:       tora.desktop

BuildRequires: desktop-file-utils
BuildRequires: postgresql-devel
#- BuildRequires: oracle-instantclient-devel = %%{oraclever}
#- BuildRequires: oracle-instantclient-sqlplus = %%{oraclever}
BuildRequires: qt-devel >= 4.3.0
BuildRequires: qscintilla-devel >= 2.0.0
BuildRequires: cmake >= 2.4.0
BuildRequires: perl openssl-devel glib2-devel

Requires:      qt-mysql qt-postgresql

%description
TOra - Toolkit for Oracle

TOra is supported for running with an Oracle 8.1.7 or newer
client installation. It has been verified to work with Oracle 10g and 11g.

TOra also supports PostgreSQL and MySQL.

This RPM is built to work with PostgreSQL and MySQL. Oracle %{oraclever}
should work also, but does not tested.

%prep
%setup -q -n %{name}

rm -rf CMakeFiles CMakeCache.txt

%cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DORACLE_PATH_INCLUDES=%{oracleinc} \
    -DORACLE_PATH_LIB=%{oraclelib} \
    -DPOSTGRESQL_PATH_INCLUDES=%{_includedir} \
        .

# To make rpmlint happy
dos2unix src/toraversion.h
chmod -x src/{toraversion.h,totabwidget.h,totabwidget.cpp}

# ISO-8859-1 is my assumption.
iconv -f ISO-8859-1 -t UTF-8 NEWS > NEWS.new
touch --reference NEWS NEWS.new
mv NEWS.new NEWS

%build
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" install

mkdir -p "%{buildroot}%{_datadir}/icons/hicolor/16x16/apps"
mkdir -p "%{buildroot}%{_datadir}/icons/hicolor/32x32/apps"
install --mode=644 src/icons/tora.xpm     "%{buildroot}%{_datadir}/icons/hicolor/32x32/apps/tora.xpm"
install --mode=644 src/icons/toramini.xpm "%{buildroot}%{_datadir}/icons/hicolor/16x16/apps/tora.xpm"

rm -rf %{buildroot}/%{_datadir}/doc/%{name}

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE2}


%files
%doc AUTHORS BUGS COPYING ChangeLog NEWS README* TODO doc/help
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%changelog
* Sat Sep 14 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 3-0.2.svn4651
- Changes by review comments (bz#979166), thanks to Matthias Kuhn.
- Move content of tora-desktop to separate source2.
- Move help files into doc from libdir.
- Change some source file permissions.
- Encode NEWS into UTF-8.
- Mention MySQL and Postgres in Summary.
- Report upstream about incorrect fsf address: https://sourceforge.net/p/tora/bugs/872/

* Fri Jun 14 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 3-0.1.svn4651
- Import from https://raw.github.com/remicollet/remirepo/master/tora/tora.spec (2.1.3 version) and reworked

* Thu Sep 23 2010 Remi Collet <RPMS@famillecollet.com> 2.1.3-1
- update to 2.1.3

* Mon May 10 2010 Remi Collet <RPMS@famillecollet.com> 2.1.2-1
- update to 2.1.2

* Fri Sep 25 2009 Remi Collet <RPMS@famillecollet.com> 2.1.0-1
- Update

* Sun May 10 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-3.fc11.remi
- F11 build with gcc44 patch

* Wed Jan 07 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-2.fc10.remi
- PowerPC build againt Oracle 10.2

* Tue Jan 06 2009 Remi Collet <RPMS@famillecollet.com> 2.0.0-1.fc10.remi
- Fedora 10 build

* Tue Oct  7 2008 Michael Mraka <michael.mraka@redhat.com> 2.0.0-0.3041svn
- changed to cmake driven build for 2.0.0 version
- built against oracle-instantclient

* Wed Jun 29 2005 Nathan Neulinger <nneul@neulinger.org>
- standardize on a single tora spec file
