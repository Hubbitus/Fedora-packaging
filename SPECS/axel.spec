Name:	axel
Version:	2.4
Release:	3%{?dist}
Summary:	Download accelerator, wget replacement

Group:	Applications/Internet
License:	GPLv2+
URL:		http://axel.alioth.debian.org/	
#Source0:	http://alioth.debian.org/frs/download.php/2287/axel-1.1.tar.gz
#Source:	http://alioth.debian.org/frs/download.php/2605/axel-2.0.tar.gz
#Source:	http://alioth.debian.org/frs/download.php/2621/axel-2.2.tar.bz2
#Source0:	http://alioth.debian.org/frs/download.php/2717/axel-2.3.tar.gz
Source0:	https://alioth.debian.org/frs/download.php/3016/axel-2.4.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext

%description
Axel tries to accelerate HTTP/FTP downloading process by 
using multiple connections for one file. It can use 
multiple mirrors for a download. Axel has no dependencies 
and is lightweight, so it might be useful as a wget clone 
on byte-critical systems. 

%prep
%setup -q

%build
%configure --strip=0 --i18n=1
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/axel
%{_mandir}/man1/axel.1*
%{_mandir}/zh_CN/man1/axel.1*
%config(noreplace) %{_sysconfdir}/axelrc


%changelog
* Thu Jul 9 2009 Pavel Alexeev <Pahan@Hubbitus.info>
- Remove mention of unneded anymore patches.
- Remove sysconfig hack.

* Fri May 1 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.4-3
- New version released. Review stop-bug seems was be fixed.
- Most (all except /etc dir path) things from my patch arrived to upstream. So, patch does not needed anymore.
- zn_CN language files also renamed in appropriate form by upstream developer. So, drop ranaming it.

* Thu Apr 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.3-2
- $RPM_BUILD_ROOT replaced by %%{buildroot}
- Inspired by notes from Michael Schwendt in Fedora Review:
	o zn_cn.{mo,po} files renamed to zn_CN{mo,po}
	o Fedora CFLAGS appended at end of author ones, so, it have high priority now.

* Fri Feb 20 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.3-1
- Step to version 2.3
- Adopt Patch0: axel-2.0-fedora-build.patch to new version (axel-2.3-fedora-build.patch)
- Add to files chines man: %%{_mandir}/zh_CN/man1/axel.1*

* Thu Oct 23 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.2-1
- Step to version 2.2

* Tue Oct 21 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0
- Step to version 2.0
- Change version.
- Remade patch0

* Sun Aug 31 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.1-2
- Correct handling i18n files.
- Change %%{_mandir}/man1/axel.1.gz to %%{_mandir}/man1/axel.1*

* Wed Aug 6 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.1-1
- Import http://www.ankurs.com/fb/axel-1.1-1.fc9.src.rpm
- Reformat with tabs
- Correct BuildRoot
- License changed to GPLv2+
- Regular file /usr/etc/axelrc changed to %%config(noreplace) %%{_sysconfdir}/axelrc
- Add patch0 - axel-1.1-fedora-build.patch
- Disable strip binaries (switch --strip=0 to configure script)
- Add internationalisation support:
	. Switch --i18n=1 to configure script
	. Add BR gettext
	. Add files for de and nl locales.

* Fri Jul 11 2008 Ankur Shrivastava < ankur @ ankurs.com > 1.1-1
- A new maintenance release 1.1 of Axel that fixes important bugs has been made
