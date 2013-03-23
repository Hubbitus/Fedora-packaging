%bcond_without kde
%define SVNdate 20090821
%define SVNrev 2902

Name: 		sim
Version: 		0.9.5
Release:		0.19.%{SVNdate}svn%{SVNrev}rev%{?dist}
#svn export -r %{SVNrev} svn://svn.berlios.de/sim-im/trunk sim; find sim -iname '*win32*' -exec rm -r {} \; ; tar --use-compress-program lzma -cf 'sim-0.9.5-SVN20090821rev2902.tar.lzma' sim
Source0:		%{name}-%{version}-SVN%{SVNdate}rev%{SVNrev}.tar.lzma
Summary:		Multiprotocol Instant Messenger
Summary(de):	Multiprotokoll Instant Messenger
Summary(ru):	Мультипротокольный Мессенджер
License:		GPLv2+
Group:		Applications/Internet
URL:			http://sim-im.berlios.de/
BuildRequires:	autoconf >= 2.52, automake >= 1.5
BuildRequires:	zlib-devel, libjpeg-devel, expat-devel, flex, libart_lgpl-devel, libpng-devel, gettext, libXScrnSaver-devel
BuildRequires:	openssl-devel, pcre-devel >= 3.9, arts-devel >= 1.0, libxml2-devel, libxslt-devel, boost-devel
BuildRequires:	zip desktop-file-utils
Requires:		openssl, arts >= 1.0, kdebase3-libs
%if %{with kde}
%if %{fedora} == 8
BuildRequires:	kdebase-devel >= 3.0.0, kdelibs-devel >= 3.0.0
Requires:		kdenetwork >= 3.0.0
%else #Fedora gt 8. Lt is not supported
BuildRequires:	kdebase3-devel >= 3.0.0, kdelibs3-devel >= 3.0.0
%endif
%endif

%if %{fedora} > 9
Requires:		qt3 >= 3.0.0
BuildRequires:	qt3-devel >= 3.0.0
%else
Requires:		qt >= 3.0.0
BuildRequires:	qt-devel >= 3.0.0
%endif

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(postun):	/sbin/ldconfig
Requires(post):	/sbin/ldconfig

#https://developer.berlios.de/bugs/?func=detailbug&group_id=4482&bug_id=15875
Patch0:		sim-0.9.5svn-fix-automake-versioncompare.patch

%description
SIM (Simple Instant Messenger) is a plugins-based open-
source instant messenger that supports various protocols
(ICQ, Jabber, AIM, MSN, LiveJournal, Yahoo!). It uses the 
QT library and works on X11 (with optional KDE support).

SIM has countless features, many of them are listed at:
http://sim-im.berlios.de/

%description -l de
SIM (Simple Instant Messenger) ist ein Plugin-basierender open-source
Instant Messenger, der verschiedene Protokolle (ICQ, Jabber, AIM, MSN,
LiveJournal, Yahoo!) unterstützt.  Dafür wird die QT-Bibliothek und X11
(mit optionaler KDE- Unterstützung) verwendet.

SIM hat sehr unzählige Features, viele von diesen sind aufgelistet unter:
http://sim-im.berlios.de/


%description -l ru
SIM (Simple Instant Messenger) это базирующийся на плагинах мессенджер с
открытым исходным кодом, который поддерживает различные протоколы обмена
мнгновенными сообщениями, такие как: ICQ, Jabber, AIM, MSN, LiveJournal, Yahoo!
Графический интерфейс базируется на библиотеке QT (опционально имеется
поддержка KDE)

SIM имеет кучу возможностей, большинство из которых пердставлены на сайте:
http://sim-im.org/


%prep
%setup -q -n %{name}
%patch0 -p0 -b .vercmp

make -f admin/Makefile.common

%build
%configure --disable-rpath \
%if %{with kde}
	--enable-kde \
%else
	--disable-kde \
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if %{fedora} == 8
rm -f $RPM_BUILD_ROOT/%{_datadir}/mimelnk/application/x-icq.desktop
%endif

%find_lang %{name}

# rm symlink since we don't support developping with sim
%{__rm} $RPM_BUILD_ROOT/%{_libdir}/libsim.so

desktop-file-install --vendor="fedora" \
	--add-category="Network" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT/%{_datadir}/applications \
	$RPM_BUILD_ROOT/%{_datadir}/applications/kde/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README* TODO INSTALL
%{_bindir}/sim*
%{_libdir}/libsim*
%{_libdir}/sim/
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/apps/
%{_datadir}/icons/*/*/*/*
%if %{fedora} > 8
%{_datadir}/mimelnk/
%endif
%{_datadir}/services/

%changelog
* Fri Aug 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.5-0.19.20090821svn2902rev
- New version.
- Name directory in tarball sim instead of trunk.
- Step to lzma source packaging.
- For BUG#478341 fixing add R kdebase3-libs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-0.18.20090616svn2730rev
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.5-0.17.20090616svn2730rev
- Fix FBFS on mass-rebuild in Fedora 12 ( http://article.gmane.org/gmane.linux.redhat.fedora.devel/114737 )
- Update to fresh svn.
- In tarball creation use "svn export" instead of "svn checkout". Delete win32 stuff.
- Add patch0 - sim-0.9.5svn-fix-automake-versioncompare.patch ( https://developer.berlios.de/bugs/?func=detailbug&group_id=4482&bug_id=15875 )

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-0.16.20080923svn2261rev
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.5-0.15.20080923svn2261rev
- rebuild with new openssl

* Sat Nov 22 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.14.20080923svn2261rev
- Remove package name from package description.

* Sun Oct 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.14.20080923svn2261rev
- Add (Patrice Dumas)
	Requires(postun): /sbin/ldconfig
	Requires(post): /sbin/ldconfig

* Thu Oct 9 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.13.20080923svn2261rev
- %%bcond_with kde replaced to %%bcond_without for default build kde support (Patrice Dumas)

* Tue Oct 7 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.12.20080923svn2261rev
- Remove $RPM_BUILD_ROOT/%%{_datadir}/mimelnk/application/x-icq.desktop in %%install section for Fedora 8

* Mon Oct 6 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.11.20080923svn2261rev
- Install /usr/share/mimelnk/application/x-icq.desctop only for fedora > 8. In fedora 8 it is conflicts with same file from kdenetworks
	( https://admin.fedoraproject.org/updates/sim-0.9.5-0.10.20080923svn2261rev.fc8 ).
- Add Requires: kdenetwork >= 3.0.0 for Fedora 8

* Sat Oct 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.10.20080923svn2261rev
- Replace %post -p /sbin/ldconfig by simlply:
	%%post
	/sbin/ldconfig
	And accodingly in %%postun due tu rpmlint warning:
	sim.i386: E: postin-without-ldconfig /usr/lib/libsim.so.0.0.0
	(I not found what mean -p key, but appologise what it designed to run 1 command only)

* Sat Oct 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.9.20080923svn2261rev
- Add %%{?dist} into Release!
- Add icon-update-code into %%post/%%postun. (thanks to Patrice Dumas)

* Sat Oct 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.8.20080923svn2261rev
- Add BR desktop-file-utils

* Fri Oct 3 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.7.20080923svn2261rev
- By suggestion of Patrice Dumas use macros bcond_with instead of manual define with_kde
- For Fedora8 BR kdebase changed to kdebase-devel for fedora > 8 add BR kdebase3-devel >= 3.0.0 (Patrice Dumas)
- Remove CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" and $LOCALFLAGS
	in configure, and "rm -rf $RPM_BUILD_DIR/%%{name}-%%{version}" in %%clean,
	gcc and gcc-c++ from BR (Patrice Dumas)
- Use make %%{?_smp_mflags} instead of manually determine number of CPUs (Patrice Dumas)
- Remove Distribution: Fedora. (Patrice Dumas)

* Sun Sep 28 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.6.20080923svn2261rev
- "make install-strip" replaced by "make install" for correct build *-debuginfo package (Marcela Maslanova)

* Wed Sep 24 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.5.20080923svn2261rev
- Fix two macro-in-%%changelog
- Fix release inconsistence.

* Tue Sep 23 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.4.20080923svn2261rev
- New revision 2261
- Add BR zip (thanks Marcela Maslanova)

* Tue Sep 9 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.3.20080904svn2258rev
- Change Release format to conform Fedora standard from "3.SVN20080904rev2258" to "0.3.20080904svn2258rev" (Patrice Dumas)

* Fri Sep 5 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-3.SVN20080904rev2258
- Add correct .desktop installation via desktop-file-install (Marcela Maslanova)
- Desktop file %%{_datadir}/applications/kde/sim.desktop renamed to %%{_datadir}/applications/fedora-%%{name}.desktop

* Thu Sep 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-2.SVN20080904rev2258
- Rm %%{_libdir}/libsim.so (Patrice Dumas)
- License changed to GPLv2+ according sources (Patrice Dumas thanks again)

* Thu Sep 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-1.SVN20080904rev2258
- Spec de-part converted into UTF-8
- Changed BR kdelibs to kdelibs-devel for Fedora8

* Thu Sep 4 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.SVN20080904rev2258
- Version 0.9.5-0.SVN20080904rev2258.Hu.1
- Changes to avouid rpmlint warnings, not magor changes:
	* Adding rm -Rf $RPM_BUILD_ROOT to start of %%install
	* Escape all percent sign by doubling it.
	* Description lines truncated
	* License changed to GPLv2 according to included in source license.
	* Removed requires libxml2, libxslt to let rpm find the library dependencies by itself.
- Changes to conform Fedora standarts:
	* Spec renamed to just sim.spec
	* Delete Hu-part of Release
- Add conditional BR depend of distribution.
	Fo F8: BuildRequires: kdebase >= 3.0.0, kdelibs >= 3.0.0
	And for athers:  BuildRequires:	kdelibs3-devel >= 3.0.0
- Add %%post and %%postun sections to register library.
- Add --disable-rpath option to configure script. Avoid disabling RPATH check (export QA_RPATHS=0x0001)
- Source changed, added SVNrev part.

* Tue Jun 24 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.SVN20080328rev2217.Hu.1
- Add define SVNrev and add it into Release.
- Move configure action to build stage from prep
- Delete (comment out) R kdelibs and kdebase

* Tue Jun 24 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.SVN20080328.Hu.0
- 0.9.5-0.SVN20080624. SVN revision 2217
- Build for F9
- Change Distribution:	Fedora Core to Fedora
- Comment out Vendor and Packager
- Add Summary(ru)
- Del --with-qt-dir=/usr/lib/qt-3.3 from configure options
- Replace BuildRoot by more standart %%{_tmppath}/%%{name}-%%{version}-%%{release}-root-%%(%%{__id_u} -n)
- Change Source:
	Source0:		%%{name}-%%{version}-%%{release}.tar.bz2
	to
	Source0:		%%{name}-%%{version}-SVN%%{SVNdate}.tar.bz2
- Change BR kdelibs-devel to kdelibs3-devel

* Fri Mar 28 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.9.5-0.SVN20080328.Hu.0
- Next SVN build 2008-03-28
- Change release enumeration
	sim-0.9.5svn-2008_03_28.Hu.0
	to
	sim-0.9.5-0.SVN20080328.Hu.0
- Translate description (%%description -l ru). And use in it URL http://sim-im.org/ instead of http://sim-im.berlios.de/

* Wed Oct 10 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info>
- Next SVN build 2007-10-10

* Wed Sep 12 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info>
- Next SVN build 2007-09-12

* Wed Jun  6 2007 Pavel Alexeev <Pahan [at] Hubbitus [dot] info>
- Next SVN build
- Comment out Packager and Vendor fields:
	Vendor: 		Vladimir Shutoff <vovan@shutoff.ru>
	Packager:		Robert Scheck <sim@robert-scheck.de>

* Sat Apr 03 2004 - Robert Scheck <sim@robert-scheck.de> - 0.9.3-2
- Upgrade to 0.9.3-2 (second 0.9.3 release)

* Wed Mar 31 2004 - Robert Scheck <sim@robert-scheck.de> - 0.9.3-1
- Upgrade to 0.9.3
- Made the KDE support conditional
- Merged Red Hat Linux spec file into Fedora Core spec file

* Fri Dec 26 2003 - Robert Scheck <sim@robert-scheck.de> - 0.9.2-1
- Upgrade to 0.9.2
- Added sablotron to requirements

* Wed Nov 05 2003 - Robert Scheck <sim@robert-scheck.de> - 0.9.1-1
- Upgrade to 0.9.1

* Tue Oct 28 2003 - Robert Scheck <sim@robert-scheck.de> - 0.9.0-1
- Upgrade to 0.9.0
- Adapted spec file from Red Hat Linux

