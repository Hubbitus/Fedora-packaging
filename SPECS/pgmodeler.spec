# ReviewRequest: https://bugzilla.redhat.com/show_bug.cgi?id=977116

#global GITrev 8d1e180
#global prever beta

%global _privatelibs lib(objrenderer|parsers|pgconnector|pgmodeler|pgmodeler_ui|utils)\\.so
%global __provides_exclude (%{_privatelibs})
%global __requires_exclude (%{_privatelibs})

Name:             pgmodeler
Version:          0.8.2
Release:          4%{?prever:.%{prever}}%{?GITrev:.git.%{GITrev}}%{?dist}
Summary:          PostgreSQL Database Modeler

License:          GPLv3
URL:              http://www.pgmodeler.com.br/
Group:            Applications/Databases
# Script to generate main source0 for git based builds
Source1:          %{name}.get.tarball
Source0:          https://github.com/%{name}/%{name}/archive/v%{version}%{?prever:-%{prever}}.tar.gz#/%{name}-%{version}%{?prever:_%{prever}}%{?GITrev:.git.%{GITrev}}.tar.xz
Source2:          %{name}.desktop
Source3:          pgmodeler-mime-dbm.xml

Requires:         hicolor-icon-theme, shared-mime-info
BuildRequires:    qt5-qtbase-devel, libxml2-devel, postgresql-devel
BuildRequires:    desktop-file-utils, gettext, qt5-qtsvg-devel
# for convert 300x300 logo file to 256x256
BuildRequires:    ImageMagick, moreutils

# https://fedoraproject.org/wiki/Packaging:AppData
BuildRequires:    libappstream-glib

%description
PostgreSQL Database Modeler, or simply, pgModeler is an
open source tool for modeling databases that merges the classical
concepts of entity-relationship diagrams with specific features that
only PostgreSQL implements. The pgModeler translates the models created
by the user to SQL code and apply them onto database clusters (Version
9.x).

%prep
%setup -q -n %{name}-%{version}%{?prever:_%{prever}}

%build
# @TODO Due to the bug (https://github.com/pgmodeler/pgmodeler/issues/559) CONFDIR, LANGDIR, SAMPLESDIR, SCHEMASDIR seems ignored?
# SHAREDIR=%%{_sharedstatedir}/%%{name} \
# CONFDIR=%%{_sysconfdir}/%%{name} \
# LANGDIR=%%{_datadir}/locale \
# SCHEMASDIR=%%{_sysconfdir}/%%{name} \
%qmake_qt5 \
 PREFIX=%{_prefix} \
 BINDIR=%{_bindir} \
 PRIVATEBINDIR=%{_libexecdir} \
 PLUGINSDIR=%{_libdir}/%{name}/plugins \
 SHAREDIR=%{_datarootdir}/%{name} \
 DOCDIR=%{_docdir}/%{name} \
 PRIVATELIBDIR=%{_libdir}/%{name} \
  %{name}.pro

%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

desktop-file-install --mode 644 --dir %{buildroot}%{_datadir}/applications/ %{SOURCE2}
# icon, mime and menu-entry
convert -resize 256x256 pgmodeler_logo.png - | sponge pgmodeler_logo.png
install -p -dm 755 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ %{buildroot}%{_datadir}/mime/packages/
install -p -m 644 conf/%{name}_logo.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/mime/packages/%{name}.xml
# https://github.com/pgmodeler/pgmodeler/issues/783
mkdir -p %{buildroot}%{_libdir}/%{name}/plugins

install -Dp -m 644 %{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

# License installed separately
rm -f %{buildroot}/%{_docdir}/%{name}/LICENSE

%find_lang %{name} --with-qt --all-name

# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#desktop-database
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  update-mime-database %{_datadir}/mime &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc CHANGELOG.md README.md RELEASENOTES.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_libexecdir}/%{name}-ch
# %%{_libdir}/%%{name}/lib*.so are not devel files! All in subdirectory and needs to load plugins only
%{_libdir}/%{name}
%{_datarootdir}/%{name}
%exclude %{_datarootdir}/%{name}/lang/*
%{_datadir}/icons/hicolor/256x256/apps/pgmodeler_logo.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Tue Sep 20 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-4
- Review in progress. Thanks to Sandro Mani.
- Add Requires shared-mime-info
- Explicit require single logo file.
- Drop listing %%{_libdir}/%%{name}/lib*.so twice.
- Filter out private requires anf provides from '%%{_libdir}/%%{name}/lib*.so*'

* Sun Sep 11 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-3
- Review taken by Sandro Mani.
- Drop devel sub-package because it almost empty.

* Mon Aug 29 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-2
- Review request in progress - bz#977116. Thanks to Igor Gnatenko. Changes by comments https://github.com/Hubbitus/Fedora-packaging/commit/d0716a3d152c8d085988944bce7140b8e56f2e64#commitcomment-18686601
- Use macroses %%qmake_qt5 and %%make_build.

* Sun Aug 07 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-1
- Update version to release 0.8.2.
- Fix prerev var usage.
- Add BR qt5-qtsvg-devel.
- Use _qt5_qmake_flags macros to honor Fedora build flags, drop old hacks.
- Step to use find_lang macro for localizations.

* Tue Jan 05 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-0.2.beta
- Create plugins directory to do not complain on start: https://github.com/pgmodeler/pgmodeler/issues/783

* Sat Jan 02 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-0.1.beta
- Try build 0.8.2-beta1 by suggestion in (https://github.com/pgmodeler/pgmodeler/issues/777)

* Thu Nov 26 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.2-0.alpha.1
- New upstream version - 0.8.2-alpha1.
- New segfault issue: https://github.com/pgmodeler/pgmodeler/issues/777

* Sun Apr 05 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.1-0.alpha.1
- 0.8.1-alpha. My app-data included (https://github.com/pgmodeler/pgmodeler/issues/622). Add App-Data handling.
- Remove Patch0: pgmodeler-0.8.0-fixConfDumpInPri.patch (https://github.com/pgmodeler/pgmodeler/issues/618) which already in source.

* Sun Mar 08 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.0-2
- Install new mime application/dbm ( https://github.com/Hubbitus/Fedora-packaging/issues/1, upstream: https://github.com/pgmodeler/pgmodeler/issues/633 )
- Move icon from %%{_datadir}/pixmaps to %%{_datadir}/icons/hicolor (Add Requires: hicolor-icon-theme)
- Delete ldconfig call - only private libs installed.

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
