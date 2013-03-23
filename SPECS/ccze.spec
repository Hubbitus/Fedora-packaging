Summary:		A robust log colorizer
Summary(ru):	Мощный коллоризатор логов
Name:		ccze
Version:		0.2.1
Release:		6%{?dist}
# http://web.archive.org/web/20040803024236/bonehunter.rulez.org/CCZE.phtml
URL:			http://bonehunter.rulez.org/CCZE.html
License:		GPLv2+
Group:		Applications/Text
Source:		ftp://bonehunter.rulez.org/pub/ccze/stable/ccze-%{version}.tar.gz
# Package intended to EL-5 too, so we still need define BuildRoot
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ncurses-devel >= 5.0, pcre-devel >= 3.1
# Upstream is dead. So, patch himself: Remove unsupported gcc option -Wmulticharacter
Patch0:		ccze-0.2.1-Wmulticharacter.patch

%description
CCZE is a roboust and modular log colorizer, with plugins for apm,
exim, fetchmail, httpd, postfix, procmail, squid, syslog, ulogd,
vsftpd, xferlog and more.

%description -l ru
CCZE это мощный и модульный раскрашиватель логов. Имеются модули-
-плагины для: apm, exim, fetchmail, httpd, postfix, procmail, squid,
syslog, ulogd, vsftpd, xferlog и другие.

%prep
%setup -q
%patch0 -p1 -b .-Wmulticharacter

%build
%configure --with-builtins=all
# To avoid problem: /usr/include/errno.h:69: error: two or more data types in declaration specifiers
# we add -D__error_t_defined=1 to inform what errno_t already defined.
make %{?_smp_mflags} CFLAGS="%{optflags} -D__error_t_defined=1"

%install
rm -rf %{buildroot}

iconv -f ISO-8859-1 -t UTF-8 THANKS > THANKS.new
touch --reference THANKS THANKS.new
mv -f THANKS.new THANKS

#% makeinstall
make install DESTDIR="%{buildroot}"

install -d %{buildroot}/%{_sysconfdir}
src/ccze-dump > %{buildroot}/%{_sysconfdir}/cczerc

rm %{buildroot}/%{_includedir}/ccze.h

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog ChangeLog-0.1 NEWS README THANKS FAQ
%config(noreplace) %{_sysconfdir}/cczerc
%{_bindir}/ccze
%{_bindir}/ccze-cssdump
%{_mandir}/man1/ccze.1*
%{_mandir}/man1/ccze-cssdump.1*
%{_mandir}/man7/ccze-plugin.7*

%changelog
* Tue Aug 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.1-6
- Start Fedora Review. Thanks to Jussi Lehtola.
- Increase comment of patch.

* Tue Aug 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.1-5
- Things of Martin Gieseking in informal review:
- Add %%{?_smp_mflags} to make.
- Change BuildRoot.

* Sat Jul 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.1-4
- %%makeinstall replaced by make install DESTDIR="%%{buildroot}" as pointed by Jussi Lehtola.

* Sat Jul 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.1-3
- Import form ftp://ftp.pbone.net/mirror/norlug.org/norlug/redhat-7.3/SRPMS/ccze-0.2.1-2.norlug.src.rpm
- Reformat with tabs.
- Remove unneded defines, and replece it by direct values in appropriate tags:
	%%define version 0.2.1, %%define dist stable, %%define release 2.norlug
- Add %%{?dist} part into release
- Add Fedora system optflags to build
- Add Patch0: ccze-0.2.1-Wmulticharacter.patch
- Add -D__error_t_defined=1 into CFLAGS.
- Add clan buildroot in %%install
- License changed from GPL to GPLv2+
- Add noreplace option to %%config file
- Remove devel file %%{_includedir}/ccze.h
- Add COPYING to %%doc files.
- iconv'ed THANKS from ISO-8859-1 (guessed)
- Add Summary and description on Russian.

* Thu Sep 4 2003 Chip Cuccio <chipster@norlug.org> 0.2.1-2
- initial build
