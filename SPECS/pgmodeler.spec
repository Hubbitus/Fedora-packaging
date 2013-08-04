%global GITrev ec8d48f

Name:             pgmodeler
Version:          0.6.0_alpha
Release:          0.1%{?GITrev:.git.%{GITrev}}%{?dist}
Summary:          PostgreSQL Database Modeler

License:          GPLv3
URL:              http://www.pgmodeler.com.br/
Group:            Applications/Databases
# Script to generate main source0
Source1:          %{name}.get.tarball
Source0:          %{name}-%{version}GIT%{GITrev}.tar.xz
Source2:          %{name}.desktop

BuildRequires:    qt5-qtbase-devel, libxml2-devel, postgresql-devel
BuildRequires:    desktop-file-utils, gettext
#Requires:

# Temporary fedora-related for to do not patch postgres updates (https://bugzilla.redhat.com/show_bug.cgi?id=977116#c1)
Patch1:           %{name}-0.5.1-no-libpq.patch

Requires(postun): /sbin/ldconfig
Requires(post):   /sbin/ldconfig

%description
PostgreSQL Database Modeler, or simply, pgModeler is an
open source tool for modeling databases that merges the classical
concepts of entity-relationship diagrams with specific features that
only PostgreSQL implements. The pgModeler translates the models created
by the user to SQL code and apply them onto database clusters (Version
9.x).

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%patch1 -p1 -b .no-libpq

%build
qmake-qt5 %{name}.pro

# HACK
ls -1 */*.pro */*/*.pro | xargs -r -I{} sh -c 'F={}; echo =$F=; sed -i "s/QT += core gui uitools/QT += core gui/g" $F; cd $(dirname $F); qmake-qt5 ${F/*\//}'
for item in libutils libobjrenderer libparsers libpgmodeler libdbconnect libpgmodeler_ui; do
    sed -i.sed "s# /${item}.so# ../${item}/${item}.so#g" */Makefile
done

# May be used instead of providing CXX to make
#sed -i 's#CXX           = g++#CXX           = g++ -std=c++11#g' */Makefile */*/Makefile

make %{?_smp_mflags} CXX="g++ -std=c++11"

%install
# Official install target do almost nothing
#% make_install


mkdir -p %{buildroot}%{_bindir}
install -m755 -D build/%{name} %{buildroot}%{_bindir}/%{name}-bin
install -m755 -D build/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli-bin
install -m755 -D build/%{name}-ch %{buildroot}%{_libexecdir}/%{name}-ch

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
export PGMODELER_CHANDLER_PATH="%{_libexecdir}/%{name}-ch"
EOF

# Wrappers to include enviroment-file on first run
cat <<EOF > %{buildroot}%{_bindir}/%{name}
#!/bin/bash
. %{_sysconfdir}/profile.d/%{name}.bash
%{_bindir}/%{name}-bin
EOF
cat <<EOF > %{buildroot}%{_bindir}/%{name}-cli
#!/bin/bash
. %{_sysconfdir}/profile.d/%{name}.bash
%{_bindir}/%{name}-cli-bin
EOF

chmod 0755 %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-cli

mkdir -p %{buildroot}%{_libdir}
cp -dp build/*.so* %{buildroot}%{_libdir}/

mkdir -p %{buildroot}%{_includedir}/%{name}
cp -dp lib*/src/*.h %{buildroot}%{_includedir}/%{name}/

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins
cp -p plugins/*/build/*.so %{buildroot}%{_libdir}/%{name}/plugins/

desktop-file-install --mode 644 \
    --dir %{buildroot}%{_datadir}/applications/ \
        %{SOURCE2}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGELOG.md LICENSE README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-bin
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-cli-bin
%{_libexecdir}/%{name}-ch
%{_libdir}/lib*.so.1*
%{_libdir}/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.bash
%{_datarootdir}/%{name}
%{_datadir}/applications/%{name}.desktop

%files devel
%{_libdir}/lib*.so
%{_includedir}/%{name}

%changelog
* Sun Jul 28 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.0_alpha-0.1.git.ec8d48f
- Repository moved to bitbucket.org.
- Crashhandler naming issue resolved: https://bitbucket.org/pgmodeler/pgmodeler/issue/282/please-move-crashhandler-to-libexec-dir and
    suggested build from reveng-support 0.6.0-alpha branch.
- BR qt-devel up to qt5-qtbase-devel.
- Delete qt4-compatibility patches.
- Add binaries wrapper and real binaries rename with -bin suffix to include environment variables for correct start.

* Sat Jul 13 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.1_r1-3.GITbe5b74a
- Changes by comments in review bz#977116 by Volker Fröhlich.
- Drop --vendor paremeter for desktop install.
- Use name macro for patch names.
- Delete unnecessary rm -rf %%{buildroot}.
- Add devel subpackage.

* Sun Jul 7 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.1_r1-2.GITbe5b74a
- Add Pavel Raiskup patch (https://bugzilla.redhat.com/show_bug.cgi?id=977116#c1) to build without libpq pkg-config file.
- Add BR libxml2-devel, postgresql-devel

* Wed Jun 12 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.1_r1-1.GITbe5b74a
- Initial version.
- Reported https://github.com/pgmodeler/pgmodeler/issues/260 about incorrect-fsf-address /libpgmodeler_ui/src/modeloverviewwidget.h
