%global svn 1391

Name:		plowshare
Version:		0.9.4
Release:		0.5%{?svn:.svn%{svn}}%{?dist}
Summary:		CLI downloader/uploader for some of the most popular file-sharing websites
Summary(ru):	терминальный аплоадер/доунлоадер для наиболее популярных файлообменников
Group:		Applications/Multimedia
License:		GPLv3+
URL:			http://code.google.com/p/plowshare/
Source0:		http://plowshare.googlecode.com/files/%{name}-%{?svn:SVN-r%{svn}-snapshot}%{?!svn:%{version}}.tar.gz
# It is for EPEL5 too
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:		curl recode ImageMagick perl(Image::Magick) tesseract js caca-utils

%description
plowshare is a command-line downloader/uploader for some of the most popular
file-sharing websites. It works on UNIX-like systems and presently supports
Megaupload, Rapidshare, 2Shared, 4Shared, ZShare, Badongo, DepositFiles and
Mediafire. Refer to the README for more info.

%description -l ru
plowshare это терминальный аплоадер/доунлоадер для наиболее популярных файло-
обменников. Он работает на большинстве UNIX-подобных систем. На данный момент
поддерживаются следующие сервисы: Megaupload, Rapidshare, 2Shared, 4Shared,
ZShare, Badongo, DepositFiles и Mediafire. Смотрите README для подробностей.

%prep
%setup -q -n %{name}-%{?svn:SVN-r%{svn}-snapshot}%{?!svn:%{version}}

%build
# Nothing build, its simple bash scripts

%install
rm -rf %{buildroot}

DESTDIR="%{buildroot}" PREFIX="%{_prefix}" bash setup.sh install

# We do not want explicit installation documentation:
rm -f %{buildroot}%{_docdir}/%{name}/{CHANGELOG,README}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGELOG README COPYING
%{_bindir}/plowdel
%{_bindir}/plowdown
%{_bindir}/plowup
%{_bindir}/plowlist
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/core.sh
%{_datadir}/%{name}/delete.sh
%{_datadir}/%{name}/download.sh
%{_datadir}/%{name}/list.sh
%{_datadir}/%{name}/upload.sh
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/tesseract
%{_datadir}/%{name}/strip_single_color.pl
%{_datadir}/%{name}/strip_threshold.pl
%{_mandir}/man1/plow*.1*

%changelog
* Wed Mar 23 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.4-0.5.svn1394
- Update to new upstream revision (last befor import into Fedora).

* Mon Feb 28 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.4-0.4.svn1358
- Remove R gocr.

* Sun Feb 27 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.4-0.3.svn1358
- Delete bash from dependencies as it is common (thanks to Elder Marco).
- Fix summary.

* Sat Feb 26 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.4-0.2.svn1358
- Add BR perl(Image::Magick) and caca-utils (thanks to Elder Marco).

* Wed Feb 23 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.4-0.1.svn1358
- Update to last version.
- Adopt to upstream svn snapshots.
- Delete examples.
- lib.sh renamed to core.sh

* Tue Oct 5 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.3-2
- New version 0.9.3.
- Remove part %%{_prefix} from DESTDIR var and move it in new PREFIX one for script setup.sh
- Add files:
	o %%{_bindir}/plowlist and %%{_datadir}/%%{name}/list.sh
	o %%{_datadir}/%%{name}/tesseract
	o %%{_datadir}/%%{name}/strip_single_color.pl
	o %%{_datadir}/%%{name}/strip_threshold.pl
- Do not list all modules separately instead own full directory %%{_datadir}/%%{name}/modules/
- Add require gocr.
- Include mans: %%{_mandir}/man1/plow*.1*
- Include examples dir into %%doc and delete it from path where it installed automatically.

* Fri Nov 20 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.8.1-1
- Initial packaging.
- Optional requires aaview is not in Fedora repos. FR to support cacvieww filled: http://code.google.com/p/plowshare/issues/list?thanks=58&ts=1258746820
