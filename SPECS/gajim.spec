%global prerel rc1

Summary:	Jabber client written in PyGTK
Name:	gajim
Version:	0.16
Release:	0.1%{?prerel:.%prerel}%{?dist}
License:	GPLv3
Group:	Applications/Internet
URL:		http://gajim.org/
Source0:	https://gajim.org/downloads/0.16/gajim-%{version}%{?prerel:-%prerel}.tar.bz2
BuildArch:	noarch

Requires:	avahi-ui-tools
# for NSLookupResolver; a fallback when libasyncns does not work
Requires:	bind-utils
Requires:	dbus-python
#  Audio/Video calls:
Requires:	farstream-python
Requires:	gstreamer-python
# XXX: Gajim does not import bonobo directly, but some module does and
# prints an error if it's not available.
Requires:	gnome-python2-bonobo
Requires:	gnome-python2-desktop
Requires:	gnome-python2-gnome
Requires:	gnupg
Requires:	hicolor-icon-theme
Requires:	notify-python
Requires:	pyOpenSSL
Requires:	python-crypto
Requires:	python-GnuPGInterface
Requires:	python-kerberos
Requires:	python-libasyncns
Requires:	python-pyasn1
Requires:	gupnp-igd-python
Requires:	python-nbxmpp > 0.3.3

# these are dlopen'd using ctypes find_library/LoadLibrary:
Requires:	gtkspell
Requires:	libXScrnSaver

# Optional features with significatly sized deps. Gajim detects them at
# runtime. Intentionally not as hard deps.
# XXX: Gajim could install them using PackageKit when really necessary.
#  Password encryption:
#Requires:	gnome-python2-gnomekeyring
#  RST Generator:
#Requires:	python-docutils

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk2-devel
BuildRequires:	intltool
BuildRequires:	pygtk2-devel
BuildRequires:	hardlink

%description
Gajim is a Jabber client written in PyGTK. The goal of Gajim's developers is
to provide a full featured and easy to use xmpp client for the GTK+ users.
Gajim does not require GNOME to run, even though it exists with it nicely.

%prep
%setup -q -n %{name}-%{version}%{?prerel:-%prerel}

%build
%configure --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
hardlink -c $RPM_BUILD_ROOT/%{_bindir}

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category=Application \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc README.html
%doc THANKS
%doc THANKS.artists
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{name}-history-manager.1*
%doc %{_mandir}/man1/%{name}-remote.1*
%{_bindir}/%{name}
%{_bindir}/%{name}-history-manager
%{_bindir}/%{name}-remote
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/data
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/src

%changelog
* Wed May 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.16-0.1.rc1
- Specify version require python-nbxmpp > 0.3.3
- Introduce usage of %%prerel
- Change version-release handling according Fedora guidelines for pre releases (0.16.rc1-1 -> 0.16-0.1.rc1)

* Wed May 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.16.rc1-1
- Version 0.16-rc1

* Wed Mar 12 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.16.beta2-2
- Add Requires: python-nbxmpp
- Drop Patch0001: gajim-0.15.3-14476-17df4ebe8da8.patch
- Some cleanup.

* Wed Mar 12 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.16.beta2-1
- Built of 0.16-beta2 version - it have xep-0308 [Last Message Correction] (according to https://plus.google.com/+NicolasV%%C3%%A9rit%%C3%%A9/posts/ZTpK9p4KWQi).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Michal Schmidt <mschmidt@redhat.com> - 0.15.3-3
- Fix connecting to non-SSL servers (#953243).
- Remove unused patch files.

* Mon Apr 08 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.3-2
- Drop desktop vendor tag.

* Wed Mar 20 2013 Michal Schmidt <mschmidt@redhat.com> - 0.15.3-1
- Upstream bugfix release (#923692, #875820, #875809).
- Require python-pyasn1 (#826737).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 31 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15.2-1
- Upstream bugfix release.
- Dropped all patches, already included.

* Mon Aug 06 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-5
- Apply upstream patch to use farstream for audio/video (#845825)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-3
- Require gupnp-igd-python (#825035)

* Tue Apr 17 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-2
- CVE-2012-2093 gajim (LaTeX module): Insecure creation of temporary file

* Mon Mar 19 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-1
- Upstream release 0.15.

* Mon Mar 12 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-0.5.beta4
- Drop the requirement on farsight2-python. It's available no more in F17.
  Upstream needs to be ported to farstream.

* Thu Jan 26 2012 Michal Schmidt <mschmidt@redhat.com> - 0.15-0.4.beta4
- Upstream release 0.15 beta4.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.3.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Michal Schmidt <mschmidt@redhat.com> 0.15-0.2.beta3
- Upstream release 0.15 beta3.
- Drop gajim-0.13.90-pygtk-crash-python2.7-workaround.patch
  Cannot reproduce the crash anymore.

* Tue Oct 11 2011 Michal Schmidt <mschmidt@redhat.com> 0.15-0.1.beta2
- Upstream release 0.15 beta2.

* Mon Jun 20 2011 Michal Schmidt <mschmidt@redhat.com> 0.14.3-1
- Upstream bugfix release.
- gajim-0.14-handle-read-before-close.patch already applied.

* Thu Jun 09 2011 Michal Schmidt <mschmidt@redhat.com> 0.14.2-1
- Upstream bugfix release.
- Dropped a merged patch.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Michal Schmidt <mschmidt@redhat.com> 0.14.1-3
- Fix a regression noted by Peter Lemenkov in Bodhi.
  (Could not connect to gmail.com)

* Fri Nov 05 2010 Michal Schmidt <mschmidt@redhat.com> 0.14.1-2
- Fix high CPU usage when the server announces a strange streamhost
  (RHBZ#649986)

* Tue Oct 26 2010 Michal Schmidt <mschmidt@redhat.com> 0.14.1-1
- Upstream bugfix release.
- Dropped merged patches.

* Tue Sep 21 2010 Michal Schmidt <mschmidt@redhat.com> 0.14-4
- Replace our gnome-keyring patch with one picked from upstream hg.
- Prevent traceback when receiving strange reply to iq:last.

* Mon Sep 20 2010 Michal Schmidt <mschmidt@redhat.com> 0.14-3
- Require gstreamer-python too. (RHBZ#632927)

* Tue Sep 14 2010 Michal Schmidt <mschmidt@redhat.com> 0.14-2
- Require farsight2-python for audio/video. (RHBZ#632927)

* Mon Sep 06 2010 Michal Schmidt <mschmidt@redhat.com> 0.14-1
- Update to 0.14 release.

* Thu Aug 19 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.90-1
- Update to 0.13.90 (a.k.a. 0.14 beta1)
- Icon cache handling.
- Cleanups and fixes of Requires.
- Refresh pygtk crash patch.
- Update gnome-keyring patch.
- Remove now unnecessary declaration and cleaning of BuildRoot.

* Tue Aug 10 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.4-2
- Workaround pygtk crash with Python 2.7 (RHBZ#621887).

* Sat Apr 03 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.4-1
- Update to upstream bugfix release 0.13.4.

* Sun Mar 28 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.4-0.1.20100328hg
- Update to current gajim_0.13 branch to fix contact syncing (RHBZ#577534).

* Mon Mar 15 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.3-3
- What the trayicon really needs is gnome-python2-libegg (RHBZ#573358).

* Mon Mar 15 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.3-2
- Require gnome-python2-extras for trayicon (RHBZ#573358).

* Mon Mar 08 2010 Michal Schmidt <mschmidt@redhat.com> 0.13.3-1
- Update to 0.13.3.
- Add gajim-0.13.3-gnome-keyring-CancelledError.patch (RHBZ#556374).

* Fri Feb 05 2010 Michal Schmidt <mschmidt@redhat.com> - 0.13.2-1
- Version bump to 0.13.2. (RHBZ#541470)
- 0.13.1 and 0.13.2 are bugfix releases.
- New in 0.13:
  * BOSH connection support
  * Roster versioning support
  * Interface to send XHTML messages
  * Changelog: http://hg.gajim.org/gajim/file/cb35a23ac836/ChangeLog
  * Bugs fixed: http://trac.gajim.org/query?status=closed&milestone=0.13
- 'idle' and 'gtkspell' modules are now implemented in Python using ctype.
- Internal 'trayicon' module is not necessary with gnome-python2-desktop.
- With no more binary modules included the package is now noarch.
- Require python-libasyncns for src/common/resolver.py.
- --enable-remote is no longer recognized by ./configure.
- Hardlink identical scripts.
- Remove fc8, fc9 support.

* Sat Sep 19 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.12.5-1
- Version bump to 0.12.5. (Red Hat Bugzilla #516191)
  * Fixed history manager.
  * Improved file transfer.
  * http://trac.gajim.org/query?status=closed&milestone=0.12.4
  * http://trac.gajim.org/browser/ChangeLog?rev=5f8edb79072f

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.12.3-3
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.12.3-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.12.3-1
- Version bump to 0.12.3. (Red Hat Bugzilla #510803)
  * Better keepalive / ping behaviour.
  * Fixed custom port handling.
  * Fixed PEP discovery.
  * Fixed PLAIN authentication (in particular with Google Talk).
  * Fixed SSL with some servers.
  * Handle XFCE notification-daemon.
  * Improve Kerberos support.
  * NetworkManager 0.7 support.
  * Restore old behaviour of click on systray: left click to open events.
  * Totem support for played music.
  * http://trac.gajim.org/query?status=closed&milestone=0.12.2

* Tue Jul 14 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.12.1-2
- Replaced 'License: GPLv2' with 'License: GPLv3'.
- Added 'Requires: gnupg python-crypto python-GnuPGInterface'. (Red Hat
  Bugzilla #510804)

* Sat May 02 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.12.1-3
- Added 'Requires: gnome-python2-bonobo'. (Red Hat Bugzilla #470181)

* Tue Feb 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.12.1-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.12.1-1
- Version bump to 0.12.1.
  * Fixed click on notifications when text string is empty.
  * Fixed file transfer.
  * Improve systray popup menu.
  * Translation updates: de.
- /usr/share/gajim/src/gajim-{remote}.py need not contain shebangs nor have the
  executable bits.

* Thu Dec 18 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.12-1
- Version bump to 0.12.
  * Better auto-away support.
  * Better sessions support.
  * Fixed Banshee support.
  * Fixed end to end encryption autonegation.
  * Fixed GSSAPI authentication.
  * Fixed text rendering in notifications.
  * Quodlibet support.
  * http://trac.gajim.org/query?status=closed&milestone=0.12
  * http://trac.gajim.org/browser/tags/gajim-0.12/ChangeLog
- Added 'Requires: notify-python python-kerberos'.

* Sun Nov 30 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.12-0.1.beta1
- Version bump to 0.12 beta1. (Red Hat Bugzilla #471295)
- Added 'Requires: pyOpenSSL'. (Red Hat Bugzilla #467523)
- Added 'Requires: python-sexy'.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.11.4-7
- Rebuilding with python-2.6 in Rawhide.

* Sun Nov 09 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.11.4-6
- Added 'Requires: gnome-python2-gnome' on all distributions starting from
  Fedora 10. (Red Hat Bugzilla #470181)

* Tue Oct 28 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.11.4-5
- Added 'Requires: avahi-tools'.

* Mon Jul 14 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.11.4-4
- Rebuilding to overcome Koji outage.

* Mon Jul 14 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.11.4-3
- Updated BuildRoot according to Fedora packaging guidelines.
- Added 'Requires: gnome-python2-canvas'. (Red Hat Bugzilla #454622)
- Removed 'BuildRequires: pkgconfig' and dropped version from
  'BuildRequires: pygtk2-devel'.
- Fixed docdir and removed empty README.

* Tue Feb 19 2008 Release Engineering <rel-eng@fedoraproject.org> - 0.11.4-2
- Autorebuild for gcc-4.3.

* Wed Dec 26 2007 Matěj Cepl <mcepl@redhat.com> 0.11.4-1
- New upstream release.

* Sun Nov 25 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 0.11.3-2
- Fix problem with python(abi)
- Add Requires: python-docutils

* Sun Nov 18 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 0.11.3-1
- Update to 0.11.3 (#315931)
- Fix Licence tag

* Fri Feb 23 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 0.11.1-1
- Update to 0.11.1
- Remove python-sqlite2 dependency (it's now provided by python-2.5)

* Tue Jan 23 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 0.11.1-0.1.pre1
- Update to 0.11.1-pre1

* Sun Jan 14 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 0.11-1
- Update to 0.11

* Thu Dec 21 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.10.1-4
- Rebuild for new Python.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.10.1-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.10.1-2
- Rebuild for FE6
- Fix mixed-use-of-spaces-and-tabs rpmlint warning

* Mon Jun  5 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.10.1-1
- Update to 0.10.1
- Change e-mail address in ChangeLog

* Tue May  2 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.10-1
- Update to 0.10

* Wed Apr 19 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.10-0.1.pre2
- Update to 0.10-pre2

* Thu Apr 13 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.10-0.1.pre1
- Update to 0.10-pre1
- Drop patches

* Thu Mar 30 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.9.1-3
- Remove Gnome dependencies
- Fix crash with notify-daemon (#187274, Stefan Plewako)
  http://trac.gajim.org/ticket/1347

* Tue Feb 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.9.1-2
- Rebuild for Fedora Extras 5

* Sun Jan 15 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.9.1-1
- update to 0.9.1 (Eric Tanguy, #176614)
- drop aplay.patch
- fix compilation with modular X.Org X11R7

* Tue Sep  6 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8.2-1
- new version 0.8.2
- remove patches .cflags, .po, .x86_64, .remote (pushed upstream)

* Sat Sep  3 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8.1-1
- Version 0.8.1
- drop gajim-remote.py file (included in tarball)

* Wed Aug 24 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8-5
- Don't build internal modules

* Wed Aug 24 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8-4
- Add missing BuildRequires:  desktop-file-utils

* Wed Aug 24 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8-3
- add .x86_64.patch (fix broken lib dir)

* Wed Aug 24 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8-2
- fix gajim-remote.py script

* Sat Aug 20 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.8-1
- Initial RPM release.
