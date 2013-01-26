%define vers      1.7.9
%define patch     7
Summary:          John the Ripper password cracker
Name:             john
Version:          %{?vers}
Release:          1jumbo%{patch}%{?dist}
URL:              http://www.openwall.com/john
License:          GPLv2
Group:            Applications/System
Source0:          http://www.openwall.com/john/g/john-%{version}.tar.gz
Source1:          http://www.openwall.com/john/g/john-%{version}.tar.gz.sign
Source2:          http://www.openwall.com/john/g/john-%{version}-jumbo-%{patch}.diff.gz.sign
#Patch0:           http://www.openwall.com/john/contrib/john-%{version}-jumbo-%{patch}.diff.gz
Patch0:           http://download.openwall.net/pub/projects/john/1.7.9/john-%{version}-jumbo-%{patch}.diff.gz
BuildRequires:    openssl-devel,openssl
Requires:         openssl
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

%description
John the Ripper is a fast password cracker. Its primary purpose is to
detect weak Unix passwords, but a number of other hash types are
supported as well.

%prep
%setup -q
%patch0 -p1
chmod 0644 doc/*
rm doc/INSTALL
sed -i 's#\$JOHN/john.conf#%{_sysconfdir}/john.conf#' src/params.h

%build
export CFLAGS="-c ${RPM_OPT_FLAGS} -DJOHN_SYSTEMWIDE=1 -fopenmp -O2"
make -C src linux-x86-64 CFLAGS="${CFLAGS} ${OMPFLAGS}" LDFLAGS="${RPM_OPT_FLAGS} -s -lssl -lcrypto -lm -fopenmp"

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_sysconfdir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/john
install -d -m 755 %{buildroot}%{_datadir}/john/scripts
install -m 755 run/{john,mailer} %{buildroot}%{_bindir}
install -m 644 run/{*.chr,password.lst} %{buildroot}%{_datadir}/john
install -m 755 run/{calc_stat,genmkvpwd,mkvcalcproba,tgtsnarf} %{buildroot}%{_bindir}
install -m 644 run/stats %{buildroot}%{_datadir}/john
install -m 644 run/john.conf %{buildroot}%{_sysconfdir}
install -m 644 run/{cmpt_cp.pl,genincstats.rb,ldif2pw.pl} %{buildroot}%{_datadir}/john/scripts
install -m 644 run/{netntlm.pl,netscreen.py,sap_prepare.pl} %{buildroot}%{_datadir}/john/scripts
install -m 644 run/{sha-dump.pl,sha-test.pl} %{buildroot}%{_datadir}/john/scripts
pushd %{buildroot}%{_bindir}
ln -s john pdf2john
ln -s john rar2john
ln -s john ssh2john
ln -s john unafs
ln -s john undrop
ln -s john unique
ln -s john unshadow
ln -s john zip2john
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*
%config(noreplace) %{_sysconfdir}/john.conf
%{_bindir}/*
%{_datadir}/john

%changelog
* Tue Jan 15 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.7.9-1jumbo7
- Import from http://download.openwall.net/pub/projects/john/contrib/linux/john-1.7.8-3jumbo5.el5.src.rpm
	and build new version to get wpa algorithm work ( http://openwall.info/wiki/john/WPA-PSK ).

* Wed Aug  3 2011 Stephen Smoogen <smooge@gmail.com> - 1.7.8-3jumbo5
- Add in apps and symbolic links from extras.

* Wed Aug 03 2011 Stephen Smoogen <smooge@gmail.com> - 1.7.8-1jumbo5
- Updated to new package. Build for systems.

* Sat Jul 24 2011 Stephen Smoogen <smooge@gmail.com> - 1.7.8-1jumbo4
- Updated to new 1.7.8 jumbo 4 release

* Sat Apr 30 2011 Simon John <rpm@the-jedi.co.uk> - 1.7.7-1jumbo1
- Updated to new 1.7.7 release and jumbo-1 patch

* Fri Mar 04 2011 Simon John <rpm@the-jedi.co.uk> - 1.7.6-7-jumbo12
- Updated to jumbo12 patch, added md5-gen-3 patch (can't get hmailserver-02 or intrinsics-2 to merge)
- changed naming scheme
- removed MMX/64/SMP checks

* Sat Feb 05 2011 Simon John <rpm@the-jedi.co.uk> - 1.7.6-6
- Updated to jumbo11 patch, removed mscash2 patch
- enabled OpenMP for mscash, mscash2, crypt, blowfish (not des)

* Sun Jan 16 2011 Simon John <rpm@the-jedi.co.uk> - 1.7.6-5
- Updated to MSCash2 v1.1 patch

* Mon Jan 10 2011 Simon John <rpm@the-jedi.co.uk> - 1.7.6-4
- Added MSCash2 patch

* Tue Nov 16 2010 Simon John <rpm@the-jedi.co.uk> - 1.7.6-3
- Replaced SHA and Netscreen patches with Jumbo-9 patch

* Wed Nov 10 2010 Simon John <rpm@the-jedi.co.uk> - 1.7.6-2
- Fixed make line with thanks to Till Maas

* Tue Nov 09 2010 Simon John <rpm@the-jedi.co.uk> - 1.7.6-1
- Updated to new release
- added jumbo7 and sha1_gen patches
- tested on Fedora 13/14 for x86_64, had to remove LDFLAGS

* Mon Jan 18 2010 Till Maas <opensource@till.name> - 1.7.3.4-1
- Update to new release
- fix Source0
- add missing -m parameters to install
- set LDFLAGS to RPM_OPT_FLAGS for non mmx build
- add signature as Source1

* Fri Jan 08 2010 Till Maas <opensource@till.name> - 1.7.0.2-9
- Use %%global instead of %%define

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.7.0.2-6
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Till Maas <opensource till name> - 1.7.0.2-5
- update License Tag
- bump release for rebuild

* Sun May 05 2007 Till Maas <opensouce till name> - 1.7.0.2-4
- use correct target for ppc64

* Tue Feb 27 2007 Till Maas <opensource till name> - 1.7.0.2-3
- fixing wrong characters in specfile
- https://bugzilla.redhat.com/bugzilla/attachment.cgi?id=148873&action=view

* Wed Jan 10 2007 Till Maas <opensource till name> - 1.7.0.2-2
- no mmx version for x86_64 since it is 32bit and does not build

* Tue Jan 09 2007 Till Maas <opensource till name> - 1.7.0.2-1
- prevent stripping in Makefile to get non-empty debuginfo
- version bump
- build mmx and fallback version

* Mon Oct 09 2006 Jeremy Katz <katzj@redhat.com> - 1.6-5
- FC6 Rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.6-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Apr 25 2003 Marius Johndal <mariuslj at ifi.uio.no> 0:1.6-0.fdr.2
- Added epoch.
- Modified makefile patch to honour %%optflags.
- setup -q.
- Added full URL of source.

* Thu Mar  6 2003 Marius Johndal <mariuslj at ifi.uio.no> 1.6-0.fdr.1
- Initial Fedora RPM release.

* Sat Dec  7 2002 Marius Johndal <mariuslj at ifi.uio.no>
- Misc. RH 8.0 changes.

* Mon Dec  2 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.6-2mdk
- config file in /etc
- fix configuration problem

* Mon Sep 16 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.6-1mdk
- first mdk version
