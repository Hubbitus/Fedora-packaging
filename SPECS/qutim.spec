%bcond_without gnutls
%bcond_without openssl

# Checkouted from several sources, so using date instead of revision number.
#% define SVN 20091018

Name:		qutim
Version:		0.2.0
Release:		2%{?SVN:SVN%{SVN}}%{?dist}
Summary:		Multiprotocol (ICQ, Jabber, IRC etc) instant messenger with modern Qt4 interface
Summary(ru):	Мультиплатформенный, мультипротокольный (ICQ, Jabber, IRC...) мессенджер на QT4
License:		GPLv2+ and CC-BY-SA
Group:		Applications/Internet
Url:			http://www.qutim.org/
Source0:		http://www.qutim.org/uploads/src/%{name}-%{version}.tar.bz2
Source1:		%{name}.desktop
Requires:		hicolor-icon-theme
BuildRequires:	cmake >= 2.6, desktop-file-utils
BuildRequires:	qt-devel >= 1:4.0, libidn-devel, dos2unix
%if %{with gnutls}
BuildRequires:	gnutls-devel
%endif
%if %{with openssl}
BuildRequires:	openssl-devel
%endif

BuildRequires:	gloox-devel >= 1:1.0-1

%description
qutIM - free open-source multiprotocol ( ICQ, Jabber/GTalk/
/Ya.Online/LiveJournal.com, Mail.Ru, IRC ) instant messenger for
Windows and Linux systems

%description -l ru
qutIM - Открытый мультипротокольный (уже поддерживаются:
ICQ, Jabber, GTalk, Ya.Online, LiveJournal.com, Mail.Ru, IRC клиент
обмена сообщениями для Linux и Windows.
Написан с нуля и призван быть легким, простым, быстрым, красивым и
расширяемым за счет модулей-плагинов.


%package		icq
Summary:		ICQ support for %{name}
Summary(ru):	ICQ плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	icq
ICQ support plugin for %{name}

%description	icq -l ru
Поддержка (плагин) протокола ICQ для %{name}


%package		irc
Summary:		IRC support for %{name}
Summary(ru):	IRC плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	irc
IRC support plugin for %{name}

%description	irc -l ru
Поддержка (плагин) протокола IRC для %{name}


%package		jabber
Summary:		Jabber support for %{name}
Summary(ru):	Jabber плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}
Requires:		gloox >= 1:1.0-1

%description	jabber
Jabber support plugin for qutIM

%description	jabber -l ru
Поддержка (плагин) протокола Jabber для %{name}


%package		mrim
Summary:		Mrim support for %{name}
Summary(ru):	Mrim плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	mrim
Mrim (Mail.ru agent) support plugin for %{name}

%description	mrim -l ru
Поддержка (плагин) протокола Mrim (Mail.ru agent) для %{name}


%package		histman
Summary:		Histman plugin for %{name}
Summary(ru):	Histman плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	histman
Histman - History Manager plugin for %{name}
Easy and fast convert your history from other IM-clients like:
QIP, Miranda, Pidgin, Kopete, Gajim, Psi and others!

%description	histman -l ru
Плагин "Менеджер истории" для %{name}
Легко и быстро сконвертирует вашу историю из других распространенных клиентов:
QIP, Miranda, Pidgin, Kopete, Gajim, Psi и многих других!


%package		plugman
Summary:		Plugin Manager plugin for %{name}
Summary(ru):	Plugin Manager плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	plugman
Plugman - Plugin Manager plugin for %{name}
Allow you to easy install additional themes (skins), smile sets (including famous
and popular Kolobok), sound themes and other small usefulness, that helps do
qutIM better.

%description	plugman -l ru
Плагин "Менеджер плагинов" для %{name}
Позволит вам легко поставить дополнительные темы оформления, комплекты смайлов,
в том числе так полюбившиеся всем Колобки, звуковые темы и прочие маленькие
полезности, помогающие сделать qutIM красивее.


%package		vkontakte
Summary:		Vkontakte support for %{name}
Summary(ru):	Vkontakte плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	vkontakte
Vkontakte plugin to speak with vkontakte.ru users from %{name}

%description	vkontakte -l ru
Поддержка (плагин) для общения с пользователями vkontakte.ru из %{name}


%package		yandexnarod
Summary:		Yandexnarod plugin for %{name}
Summary(ru):	Yandexnarod плагин для %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}

%description	yandexnarod
Yandex.Narod - plugin for %{name}
Allow upload files to Yandex.Disk (http://narod.yandex.ru/disk) and send link
to it. What remarkably - allow to send files to offline contacts. Additional
allow to manage previosly uploaded files.

%description	yandexnarod -l ru
Плагин Yandex.Narod для %{name}
Зальет файлы на Яндекс.Диск и передаст собеседнику на него ссылку, что
примечательно — так можно слать файлы и пользователям не в сети. Помимо этого
можно управлять уже загруженными файлами.

%package		devel
Summary:		Headers for %{name}
Group:		Applications/Internet
Requires:		%{name} = %{version}-%{release}
Requires:		cmake

%description	devel
Headers for %{name}

%prep
%setup -q

# Gloox is shared, do not use bundled
rm -rf ./plugins/jabber/libs/

# Fix source files permissions to do not rpm compline spurious-executable-perm on -debuginfo sub package
find \( -name '*.cpp' -or -name '*.h' \) -and -executable -exec chmod -x {} \;

# Fix lineendings qtwin to avoid rpmlint complain wrong-script-end-of-line-encoding.
dos2unix src/3rdparty/qtwin/qtwin.{cpp,h}

%build
%{cmake} .

make

# Jabber
pushd plugins/jabber
	# Due to the BUG http://bugs.camaya.net/horde/whups/ticket/?id=163 we should add "-lpthread" manually.
	CXXFLAGS="%{optflags} `pkg-config --libs --cflags gloox` -lpthread" %{cmake} \
	%if %{with gnutls}
	-DGNUTLS=1 \
	%endif
	%if %{with openssl}
	-DOpenSSL=1 \
	%endif
	.
make
popd

	# All other plugins (which is not require additional parameters) and own
	# cmake buildsystem (other shold migrate to cmake priot 0.3 version)
	for plugin in mrim plugman; do
	pushd plugins/$plugin
	%{cmake} .
	make
	popd
	done

	# Build all plugins with qt4make buildsystem:
	for plugin in icq irc histman vkontakte yandexnarod; do
	pushd plugins/$plugin
	%{_qt4_qmake} -makefile -unix "QMAKE_CFLAGS+=%{optflags}" "QMAKE_CXXFLAGS+=%{optflags}" $plugin.pro
	make
	popd
	done



%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/16x16/apps %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps %{buildroot}%{_datadir}/%{name}/emoticons %{buildroot}%{_libdir}/%{name}
install -m 644 icons/%{name}.png %{buildroot}/%{_datadir}/icons/hicolor/16x16/apps
install -m 644 icons/%{name}_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

make install DESTDIR="%{buildroot}"

desktop-file-install \
	--add-category="Network" \
	--dir=%{buildroot}/%{_datadir}/applications \
	%{SOURCE1}

pushd plugins
	for plugin in icq irc mrim jabber histman plugman vkontakte yandexnarod; do
	install -m 755 $plugin/lib${plugin}.so %{buildroot}%{_libdir}/%{name}
	done
popd

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

%files
%defattr(-,root,root,-)
%dir %{_libdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.xpm
%doc COPYING AUTHORS CCBYSA GPL

%files icq
%defattr(-,root,root,-)
%doc plugins/icq/{COPYING,AUTHORS,GPL}
%{_libdir}/%{name}/libicq.so

%files irc
%defattr(-,root,root,-)
%doc plugins/irc/{COPYING,AUTHORS,GPL}
%{_libdir}/%{name}/libirc.so

%files jabber
%defattr(-,root,root,-)
%doc plugins/jabber/{COPYING,AUTHORS,GPL}
%{_libdir}/%{name}/libjabber.so

%files mrim
%defattr(-,root,root,-)
#% doc COPYING AUTHORS GPL
%{_libdir}/%{name}/libmrim.so

%files vkontakte
%defattr(-,root,root,-)
%doc plugins/vkontakte/{COPYING,AUTHORS,GPL}
%{_libdir}/%{name}/libvkontakte.so

%files histman
%defattr(-,root,root,-)
%doc plugins/histman/{COPYING,AUTHORS,GPL}
%{_libdir}/%{name}/libhistman.so

%files plugman
%defattr(-,root,root,-)
%doc plugins/plugman/{COPYING,COPYING.libs,AUTHORS,GPL,TODO,changelog}
%{_libdir}/%{name}/libplugman.so

%files yandexnarod
%defattr(-,root,root,-)
%doc plugins/yandexnarod/{COPYING,AUTHORS,GPL,README}
%{_libdir}/%{name}/libyandexnarod.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_datadir}/cmake/Modules/FindQutIM.cmake
%{_datadir}/cmake/Modules/qutimuic.cmake

%changelog
* Tue Dec 15 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-2
- Delete comment what qt >= 4.0 not enought and qt3-devel-0:3.3.8b-14.fc9.i386 also satisfy this, and epoch needed.
	It outdated since Fedora 9 EOL reached.
- As it is release version, change Release enumeration to 1 digit.

* Sun Nov 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1.21
- Directory %%{_libdir}/%%{name} marked as %%dir in main package
- Icon placed to /apps subdir of %%{_datadir}/icons/hicolor/16x16/

* Wed Nov 25 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1.20
- Correct paths for plugin docs.
- Remove all icons macroses as suggested by Peter and change its installation paths.
- Own %%{_libdir}/%%{name}
- In devel own full %%{_includedir}/%%{name} and don't mention each file.

* Fri Nov 13 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1.19
- Delete invoke of ldconfig, because it is nt needed if libraries placed not in %%{_libdir} directly. By words of Peter Lemenkov.
- Delete unused macros _liconsdir

* Wed Nov 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1.18
- Add epoch 1 in gloox requires.

* Sun Nov 8 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1.17
- Update to long-awaited 0.2 release! But now it version enumerated as 0.2.0.
- Up BR gloox to 1.0-1 (release)
- Add new plugins - sub packages: histman, plugman, vkontakte, vkontakte, yandexnarod
- All incoming of %%{__make} replaced by direct make
- Delete BuildRoot tag - qutim is not intended to EPEL.
- Fedora review started - thanks to Peter Lemenkov.
- Fix source files permissions in %%prep to do not rpm compline spurious-executable-perm on -debuginfo sub package
- Add BR dos2unix and fix lineendings qtwin to avoid rpmlint complain wrong-script-end-of-line-encoding.
- Add Requires hicolor-icon-theme (for /usr/share/icons/hicolor/64x64/apps )
- Add Requires cmake ot -devel subpackage.
- Fill BUG on gloox http://bugs.camaya.net/horde/whups/ticket/?id=163 and to work around this problem add "-lpthread" flag to jabber-plugin options.

* Thu Oct 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.16.beta2SVN20091018
- Add %%{_hiconsdir}
- Replace %%{_icons64dir} by %%{_hiconsdir}/64x64/apps

* Tue Oct 20 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.15.beta2SVN20091018
- Rename package from qutIM to qutim and delete all dual names anywhere.

* Sun Oct 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.14.beta2SVN20091018
- Build against new gloox-1.0rc3-0.8.SVNr4204
- Close http://trac.qutim.org/task/258
- New checkout SVN20091018
- Correct checkout process, icq and jabber plugins now have traditional branches and trunk directories.
- Delete # Fix path. Come from alt. Needed for 64-bit systems
	sed -i 's|lib/%%{name}|%%{_lib}/%%{name}|g' CMakeLists.txt src/pluginsystem.cpp plugins/jabber/CMakeLists.txt
	with hope it is not needed anymore.
- Delete cmake_flags define. cmake invoke replaced by macro %%cmake
- Fill and wait close https://mail.camaya.net/horde/whups/ticket/?id=157
- Add to %%doc files: AUTHORS, CCBYSA, GPL
- License changed from GPLv2 to "GPLv2+ and CCBYSA" according to COPYING.
- Add %%post/%%postun for each plugin subpackage.
- Add -devel subpackage and put in it files:
	%%{_includedir}/%%{lname}/iconmanagerinterface.h
	%%{_includedir}/%%{lname}/layerinterface.h
	%%{_includedir}/%%{lname}/layerscity.h
	%%{_includedir}/%%{lname}/plugininterface.h
	%%{_includedir}/%%{lname}/protocolinterface.h
	%%{_includedir}/%%{lname}/settings.h
	%%{_datadir}/cmake/Modules/FindQutIM.cmake
	%%{_datadir}/cmake/Modules/qutimuic.cmake
- Delete all sed rpath-cmake hacks, it is handled no in %%cmake macros.
- Delete %%doc plugins/mrim/TODO.txt in mrim. File does not exist anymore.

* Sat Sep 5 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.13.beta2SVN20090716
- Beta2 build SVN20090716.

* Thu Jul 16 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.12.betaSVN20090716
- Beta release come.
- Use svn export instaed of checkout to prepare tarball.
- Replace "%%makeinstall DESTDIR=%%{buildroot}" by more preferable "makei nstall DESTDIR=%%{buildroot}"
- Delete patch qutim-0.2-alpha-GCC4.4_missing_include.patch (fixed in rev316, http://qutim.org/flyspray/task/10)
	Remove temporary hack with separate jabber-plugin in Source2

* Mon Apr 6 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.11.alphaSVN20080404
- Add "-l gloox" into CXXFLAGS when jabber plugin build. It is not linked with our shared library instead.
- Delete explicit Requires: libidn (inspired by rpmlint)

* Sun Apr 5 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.10.alphaSVN20080404
- We build 0.2 alpha. It is built, but do not installable due bug: http://bugs.camaya.net/horde/whups/ticket/?id=137 (qutIM
	ship with bundled copy of gloox library). After separate gloox into another RPM package, we have another bug:
	http://qutim.org/flyspray/task/13 . QutIM jabber plugin developer fixing that in revision 305, but it is not build because API in
	gloox and qutIM changed. So, we must checkout all.
- Checkouted from several sources, so using date instead of revision number.
- Add SVN part into Release.
- Mrim plugin buildsystem changed to cmake too (was qmake-qt4)
- Direct qmake-qt4 replaced by macros %%{_qt4_qmake}

* Fri Apr 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.9.alpha
- Due to the BUG: qutIM-jabber-SVNr305.tar.bz2 Jaber plugin is not installable. Author say it is fixed in revision 305.
	Add Source2: qutIM-jabber-SVNr305.tar.bz2
- Patch1 is not needed anymore. Disabled. In talk with autor he make decision support external shared gloog installation and build
	scripts now (rev 305 also) contain automatically detect support for it.

* Wed Apr 1 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.8.alpha
- Add Requires: libidn and BuildRequires: libidn-devel after talk with qutIM developer.

* Sat Mar 28 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.7.alpha
- Due to the previousli mentioned bug, and also similar which I fill ( https://mail.camaya.net/horde/whups/ticket/?id=137 ), and
	at all, it is not well bundle into this package common library. So, I make decision pack gloox separately. For that:
	o Add Requires: gloox >= 1.0 (in jabber subpackage) and BuildRequires: gloox-devel >= 1.0 in main package
	o Delete Patch1: qutim-0.2-alpha-gloox-DNS.patch
	o Remove dir rm -rf ./plugins/jabber/libs/ in %%prep
	o Add Patch qutim-0.2-alpha.cut-off-gloox.patch to remove additional source dependencies.

* Fri Mar 27 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.6.alpha
- Add Patch1: qutim-0.2-alpha-gloox-DNS.patch to resolv installation error (build sucsessfull):
	error: Failed dependencies:
		libresolv.so.2(GLIBC_PRIVATE) is needed by qutIM-jabber-0.2-0.5.alpha.fc9.i386

* Thu Mar 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.5.alpha
- Add %%{?dist} into release.

* Thu Mar 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.4.alpha
- Exclude common RPATH from binary. Comment out all rpath-related strings in CMakeLists.txt
- Delete delete (added before) manipulation with CMakeCache.txt

* Wed Mar 25 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.3.alpha
- Rpmlint inspired tuning in this release.
- Group changed from "Networking/Instant messaging" to Applications/Internet
- Add documentation COPYING in main package and TODO.txt into mrim. Can't found any other.

* Tue Mar 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.2.alpha
- Add Patch0: qutim-0.2-alpha-GCC4.4_missing_include.patch to build on GCC 4.4. Build on rawhide with recent version of gcc.
	Build on dist-f10 now sucsessful.

* Mon Mar 23 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2-0.1.alpha
- Initial import from ftp://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/files/SRPMS/qutim-0.2-alt5.alpha.src.rpm
	( http://sisyphus.ru/srpm/Sisyphus/qutim/get )
- Version enumeration changed to - 0.2-0.1.alpha
- License chaged from GPL2 to GPLv2
- Source: %%name-%%version.tar
	changed to URL: Source:	http://qutim.org/uploads/qutim_0.2_alpha_source.tar.bz2
- qutim-0.2-alt.patch transformed to qutIM.desktop Source1
- Reformat spec with tabs.
- Delete:
	o Epoch: 2 tag
	o name from summary.
	o explicit Provides:	%%cname = %%version
	o Obsoletes:	%%cname <= 0.1-alt1.20080620 - it is a first import into Fedora.
	o %%define cname qutIM and anywhere use %%name instead.
	o Packager: Evgenii Terechkov <evg@altlinux.org>
	o # Automatically added by buildreq on Sun Jun 15 2008: BuildRequires: gcc-c++ libqt4-devel cmake
	o %%define _unpackaged_files_terminate_build 1
	o install in "%%makeinstall DESTDIR=%%{buildroot} install"
- Replace:
	o %%def_without gnutls to %%bcond_without gnutls
	o %%def_with openssl to %%bcond_without openssl
	o "%%if %%{with gnutls}" instead of alt "%%if_with gnutls"
	o "%%if %%{with openssl}" instead of alt "%%if_with openssl"
	o Direct mention of qutIM in description to %%name
	o %%make_build to simple %{__make}
	o BuildRequires: libssl-devel to BuildRequires: openssl-devel
	o BuildRequires: libgnutls-devel to BuildRequires: gnutls-devel
	o %%setup -n %%{name}-%%{version} to %%setup -qn %%( echo %%{name} | tr 'A-Z' 'a-z' )
	o %%prefix to %{_prefix}
	o ln %%{buildroot}%%{_bindir}/%%{lname} %%{buildroot}%%{_bindir}/%%{name}
		to
		ln -s %%{lname} %%{buildroot}%%{_bindir}/%%{name}
- Add:
	o Summary(ru) and Description -l ru for all packages.
	o BuildRequires: cmake >= 2.6
	o -q key in %%setup macro
	o BR qt-devel >= 1:4.0
	o BuildRoot: %%{_tmppath}/%%{name}-%%{version}-%%{release}-root-%%(%%{__id_u} -n)
	o %%defattr(-, root, root, -) in each %%files section
	o %%{__rm} -rf %%{buildroot} in %%install section
	o %%clean section with "%%{__rm} -rf %%{buildroot}" content
	o #To avoid RPATH troubles: sed -i 's/CMAKE_SKIP_RPATH:BOOL=NO/CMAKE_SKIP_RPATH:BOOL=YES/' CMakeCache.txt
	o Requires(postun):	/sbin/ldconfig, Requires(post):	/sbin/ldconfig
		and Post & Postun sections with ldconfig and icon-cache update.
	o Define Jpackage (Mandriva) macroses: _miconsdir, _iconsdir, _liconsdir
- For consistent usage brackets all (name, version, optflags ...) %%name replaced by %%{name}
- Correcthandle .desktop file:
	o Add BR desktop-file-utils
	o Use desktop-file-install instead of simple copy file and use (undefined) %%{_desktopdir}
- Install jabber as other plugins, do not any exclusions (was separate %%makeinstall).

* Wed Mar 18 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.2-alt5.alpha
- Build with OpenSSL by default (seems like gmail works only with openssl)
- Split package to plugins subpackages

* Fri Mar 13 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.2-alt4.alpha
- Missed optflags and make_build ressurected (thanks to drool@ again)

* Fri Mar 13 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.2-alt3.alpha
- Build with Gnutls support (thanks to drool@)

* Mon Mar  9 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.2-alt2.alpha
- x86_64 build "fixed" (Authors is idiots)
- bin/%%cname compat hardlink added

* Sun Mar  8 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.2-alt1.alpha
- 0.2 alpha

* Thu Jan 22 2009 Terechkov Evgenii <evg@altlinux.ru> 2:0.1.1-alt2
- Migrate to "one alt patch" gear scheme
- Update spec to new filetriggers system

* Sun Aug 17 2008 Terechkov Evgenii <evg@altlinux.ru> 2:0.1.1-alt1
- 0.1.1

* Sun Aug 17 2008 Evgenii Terechkov <evg@altlinux.ru> 1:0.1-alt1.20080720
- Svn revision: exported

* Sun Jul 20 2008 Evgenii Terechkov <evg@altlinux.ru> 1:0.1-alt1.20080720
- Svn revision: 174

* Wed Jul 09 2008 Evgenii Terechkov <evg@altlinux.ru> 1:0.1-alt1.20080709
- Svn revision: 154

* Wed Jul  2 2008 Terechkov Evgenii <evg@altlinux.ru> 1:0.1-alt1.20080702
- svn-20080702

* Mon Jun 30 2008 Terechkov Evgenii <evg@altlinux.ru> 1:0.1-alt1.20080629
- svn-20080629

* Tue Jun 24 2008 Terechkov Evgenii <evg@altlinux.ru> 1:0.1-alt1.20080624
- Package name changed due changes in upstream
- buildflags added (fix #16149)
- svn-20080624

* Fri Jun 20 2008 Terechkov Evgenii <evg@altlinux.ru> 1:0.1-alt1.20080620
- svn-20080620

* Wed Jun 18 2008 Terechkov Evgenii <evg@altlinux.ru> 1:0.1-alt1.20080618
- svn-20080618
- Obsoleted Patch1 removed (fixed in upstream)

* Wed Jun 18 2008 Terechkov Evgenii <evg@altlinux.ru> 0.1-alt3
- README.ALT included in binary package

* Tue Jun 17 2008 Terechkov Evgenii <evg@altlinux.ru> 0.1-alt2
- Patch1 added to look for emoicons in common dir (to hiddenman@)
- README.ALT added

* Sun Jun 15 2008 Terechkov Evgenii <evg@altlinux.ru> 0.1-alt1
- Initial build for ALT Linux Sisyphus
