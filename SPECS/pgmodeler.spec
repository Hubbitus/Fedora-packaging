#% global GITrev ec8d48f

Name:             pgmodeler
Version:          0.8.0
Release:          1%{?GITrev:.git.%{GITrev}}%{?dist}
Summary:          PostgreSQL Database Modeler

License:          GPLv3
URL:              http://www.pgmodeler.com.br/
Group:            Applications/Databases
# Script to generate main source0 for git based builds
Source1:          %{name}.get.tarball
Source0:          https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source2:          %{name}.desktop

BuildRequires:    qt5-qtbase-devel, libxml2-devel, postgresql-devel
BuildRequires:    desktop-file-utils, gettext
#Requires:

Requires(postun): /sbin/ldconfig
Requires(post):   /sbin/ldconfig

# https://github.com/pgmodeler/pgmodeler/issues/618
Patch0:           pgmodeler-0.8.0-fixConfDumpInPri.patch

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

%patch0 -p1 -b .priConfDump

%build
# @TODO Due to the bug (https://github.com/pgmodeler/pgmodeler/issues/559) CONFDIR, LANGDIR, SAMPLESDIR, SCHEMASDIR seems ignored?
#	SHAREDIR=%%{_sharedstatedir}/%%{name} \
#	CONFDIR=%%{_sysconfdir}/%%{name} \
#	LANGDIR=%%{_datadir}/locale \
#	SCHEMASDIR=%%{_sysconfdir}/%%{name} \
%_qt5_qmake -recursive \
	PREFIX=%{_prefix} \
	BINDIR=%{_bindir} \
	PRIVATEBINDIR=%{_libexecdir} \
	PLUGINSDIR=%{_libdir}/%{name}/plugins \
	SHAREDIR=%{_datarootdir}/%{name} \
	DOCDIR=%{_docdir}/%{name} \
	PRIVATELIBDIR=%{_libdir}/%{name} \
		%{name}.pro

# May be used instead of providing CXX to make
#sed -i 's#CXX           = g++#CXX           = g++ -std=c++11#g' */Makefile */*/Makefile
make %{?_smp_mflags} CXX="g++ -std=c++11"

%install
%make_install INSTALL_ROOT=%{buildroot}

desktop-file-install --mode 644 --dir %{buildroot}%{_datadir}/applications/ %{SOURCE2}
# icon and menu-entry
install -p -dm 755 %{buildroot}%{_datadir}/pixmaps
install -p -m 644 conf/%{name}_logo.png %{buildroot}%{_datadir}/pixmaps

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CHANGELOG.md README.md RELEASENOTES.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libexecdir}/%{name}-ch
%{_libdir}/%{name}
%{_datarootdir}/%{name}
%{_datadir}/pixmaps
%{_datadir}/applications/%{name}.desktop

%files devel
%{_libdir}/%{name}/lib*.so
#? % {_includedir}/%{name}

%changelog
* Mon Mar 02 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.0-1
- Updaate to 0.8.0 by request Edson Ferreira (https://github.com/Hubbitus/Fedora-packaging/issues/1)
- Changed files layout. Big job has been donee in https://github.com/pgmodeler/pgmodeler/issues/559 so use qmake project files parameters and makefile variables instead of manual installation and various hacks.
- Spec cleanup.
- Fix mixed tab/space rpmlint warn.
- Move LICENSE into %%license from %%doc
- Include RELEASENOTES.md.

* Tue Apr 22 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.7.1-2
- Adjust also LD_LIBRARY_PATH

* Sun Apr 20 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.7.1-1
- Update to 0.7.1

* Tue Jan 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.7.0_pre-0.1
- Step to version 0.7.0-pre
- Replace qmake-qt5 by macros %%_qt5_qmake
- Drop Patch1: %%{name}-0.5.1-no-libpq.patch

* Sun Sep 29 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.0_alpha-0.3.git.ec8d48f
- By comments of Volker Fröhlich, thanks.
- Copy icon into pixmaps.
- Move all libs into %%{_libdir}/%%{name} subdir.

* Wed Aug 7 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.0_alpha-0.2.git.ec8d48f
- Move config to ~/.config/%%{name} before use

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
