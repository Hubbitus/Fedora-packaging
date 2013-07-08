%global GITrev be5b74a

Name:           pgmodeler
Version:        0.5.1_r1
Release:        2%{?GITrev:.GIT%{GITrev}}%{?dist}
Summary:        PostgreSQL Database Modeler

License:        GPLv3
URL:            http://www.pgmodeler.com.br/
Group:          Applications/Databases
# Script to generate main source0
Source1:        %{name}.get.tarball
Source0:        %{name}-be5b74a.tar.xz
Source2:        %{name}.desktop

BuildRequires:  qt-devel > 4.0, libxml2-devel, postgresql-devel
BuildRequires:  desktop-file-utils
#Requires:

# Two patches to build against qt4 instead of qt5 for current Fedora releases
Patch0:         pgmodeler-0.5.1-Qutf8.patch
Patch1:         pgmodeler-0.5.1-qt4.patch
# Temporary fedora-related for to do not puch postgres updates (https://bugzilla.redhat.com/show_bug.cgi?id=977116#c1)
Patch2:         pgmodeler-0.5.1-no-libpq.patch

Requires(postun): /sbin/ldconfig
Requires(post):   /sbin/ldconfig

%description
PostgreSQL Database Modeler, or simply, pgModeler is an
open source tool for modeling databases that merges the classical
concepts of entity-relationship diagrams with specific features that
only PostgreSQL implements. The pgModeler translates the models created
by the user to SQL code and apply them onto database clusters (Version
9.x).

%prep
%setup -q -n %{name}

%patch0 -p1 -b .QTutf8
%patch1 -p1 -b .QT4
%patch2 -p1 -b .no-libpq

%build
qmake-qt4 %{name}.pro

# HACK
ls -1 */*.pro */*/*.pro | xargs -r -I{} sh -c 'F={}; echo =$F=; cd $(dirname $F); qmake-qt4 ${F/*\//}'
for item in libutils libobjrenderer libparsers libpgmodeler libdbconnect libpgmodeler_ui; do
    sed -i.sed "s# /${item}.so# ../${item}/${item}.so#g" */Makefile
done

# May be used instead of providing CXX to make
#sed -i 's#CXX           = g++#CXX           = g++ -std=c++11#g' */Makefile */*/Makefile

sed -r -i.bak 's# ../../build/(\w+?).so# ../../\1/\1.so#g' plugins/*/Makefile

make %{?_smp_mflags} CXX="g++ -std=c++11"


%install
rm -rf %{buildroot}

# Official install target do almost nothing
#% make_install


mkdir -p %{buildroot}%{_bindir}
install -m755 -D main/%{name} %{buildroot}%{_bindir}/%{name}
install -m755 -D main-cli/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
install -m755 -D crashhandler/crashhandler %{buildroot}%{_bindir}/crashhandler

mkdir -p %{buildroot}%{_sysconfdir}
cp -rp conf %{buildroot}/%{_sysconfdir}/%{name}
cp -rp schemas %{buildroot}/%{_sysconfdir}/%{name}/

mkdir -p %{buildroot}%{_datarootdir}/%{name}
cp -rp lang %{buildroot}%{_datarootdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
#Based on pgmodeler.vars from distr:
cat <<EOF > %{buildroot}%{_sysconfdir}/profile.d/%{name}.bash
# Specify here the full path to the pgmodeler's root directory
export PGMODELER_ROOT="%{_datarootdir}/%{name}"

export PGMODELER_CONF_DIR="%{_sysconfdir}/%{name}"
export PGMODELER_TMP_DIR="/tmp"
export PGMODELER_SCHEMAS_DIR="%{_sysconfdir}/%{name}/schemas"
export PGMODELER_LANG_DIR="%{_sysconfdir}/%{name}/lang"
export PGMODELER_PLUGINS_DIR="%{_libdir}/%{name}/plugins"
EOF

mkdir -p %{buildroot}%{_libdir}
cp -dp {libutils,libobjrenderer,libparsers,libpgmodeler,libdbconnect,libpgmodeler_ui}/*.so.* %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins
cp -p plugins/*/build/*.so %{buildroot}%{_libdir}/%{name}/plugins/

desktop-file-install --vendor="" --mode 644 \
    --dir %{buildroot}%{_datadir}/applications/ \
        %{SOURCE2}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGELOG.md LICENSE README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/crashhandler
%{_libdir}/libutils.so.1*
%{_libdir}/libobjrenderer.so.1*
%{_libdir}/libparsers.so.1*
%{_libdir}/libpgmodeler.so.1*
%{_libdir}/libdbconnect.so.1*
%{_libdir}/libpgmodeler_ui.so.1*
%{_libdir}/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.bash
%{_datarootdir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Jul 7 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.1_r1-2.GITbe5b74a
- Add Pavel Raiskup patch (https://bugzilla.redhat.com/show_bug.cgi?id=977116#c1) to build without libpq pkg-config file.
- Add BR libxml2-devel, postgresql-devel

* Wed Jun 12 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.1_r1-1.GITbe5b74a
- Initial version.
- Reported https://github.com/pgmodeler/pgmodeler/issues/260 about incorrect-fsf-address /libpgmodeler_ui/src/modeloverviewwidget.h
