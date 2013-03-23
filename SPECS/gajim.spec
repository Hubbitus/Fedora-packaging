%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Jabber client written in PyGTK
Name:	gajim
Version:	0.12.3
Release:	4%{?dist}
License:	GPLv2
Group:	Applications/Internet
URL:		http://gajim.org/
Source0:	http://gajim.org/downloads/%{name}-%{version}.tar.bz2

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	avahi-tools
Requires:	bind-utils
Requires:	dbus-python

%if 0%{?fc8}%{?fc9}
%else
Requires:	gnome-python2-gnome
%endif

Requires:	gnome-python2-bonobo
Requires:	gnome-python2-canvas
Requires:	notify-python
Requires:	pygtk2-libglade
Requires:	pyOpenSSL
Requires:	python-docutils
Requires:	python-kerberos
Requires:	python-sexy

BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk2-devel
BuildRequires:	gtkspell-devel
BuildRequires:	intltool
BuildRequires:	libXScrnSaver-devel
BuildRequires:	pygtk2-devel

%description
Gajim is a Jabber client written in PyGTK. The goal of Gajim's developers is
to provide a full featured and easy to use xmpp client for the GTK+ users.
Gajim does not require GNOME to run, eventhough it exists with it nicely.

%prep
%setup -q

# Suppress error.
sed --in-place --expression '1d' ./src/gajim.py
sed --in-place --expression '1d' ./src/gajim-remote.py

%build
%configure --docdir=%{_docdir}/%{name}-%{version} \
  --libdir=%{python_sitearch} \
  --disable-static --enable-remote --enable-gtkspell --enable-idle \
  --enable-trayicon

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{python_sitearch}/%{name}/*.la

# Suppress rpmlint error.
chmod 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/src/history_manager.py

desktop-file-install --vendor fedora --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category=Application \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc README.html
%doc THANKS
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{name}-remote.1*
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-history-manager
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_about.png

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/data
%{_datadir}/%{name}/src

%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/gtkspell.so
%{python_sitearch}/%{name}/idle.so
%{python_sitearch}/%{name}/trayicon.so

%changelog
* Thu Jul 16 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.12.3-4
- Build 0.12.3
- Source0 to .tar.bz2
- Add file %%{_bindir}/%%{name}-history-manager

* Sat May 02 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.12.1-3
- Added 'Requires: gnome-python2-bonobo'. (Red Hat Bugzilla #470181)

* Tue Feb 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.12.1-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.12.1-1
- Version bump to 0.12.1.
- /usr/share/gajim/src/gajim-{remote}.py need not contain shebangs nor have the
  executable bits.

* Thu Dec 18 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.12-1
- Version bump to 0.12.
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

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.11.4-2
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
