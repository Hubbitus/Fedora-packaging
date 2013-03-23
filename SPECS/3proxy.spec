Name:		3proxy
Version:		0.6
Release:		3%{?dist}

Summary:		Tiny but very powerful proxy
Summary(ru):	Маленький, но крайне мощный прокси-сервер

License:		BSD or ASL 2.0 or GPLv2+ or LGPLv2+
Group:		System Environment/Daemons
Url:			http://3proxy.ru/?l=EN

Source0:		http://3proxy.ru/%{version}/%{name}-%{version}.tgz
Source1:		3proxy.init
Source2:		3proxy.cfg
# EPEL still require it
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	dos2unix

%description
3proxy -- light proxy server.
Universal proxy server with HTTP, HTTPS, SOCKS v4, SOCKS v4a, SOCKS v5, FTP,
POP3, UDP and TCP portmapping, access control, bandwith control, traffic
limitation and accounting based on username, client IP, target IP, day time,
day of week, etc.

%description -l ru
3proxy -- маленький прокси сервер.
Это универсальное решение поддерживающее HTTP, HTTPS, SOCKS v4, SOCKS v4a,
SOCKS v5, FTP, POP3, UDP и TCP проброс портов (portmapping), списки доступа
управление скоростью доступа, ограничением трафика и статистикоу, базирующейся
на имени пользователя, слиентском IP адресе, IP цели, времени дня, дня недели
и т.д.

%prep
%setup -q

# To use "fedora" CFLAGS (exported)
sed -i -e "s/CFLAGS =/CFLAGS +=/" Makefile.Linux

dos2unix Changelog

%build
%{__make} -f Makefile.Linux

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_man3dir}
mkdir -p %{buildroot}%{_man8dir}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
install -m755 -D src/3proxy %{buildroot}%{_bindir}/3proxy
install -m755 -D src/dighosts %{buildroot}%{_bindir}/dighosts
install -m755 -D src/ftppr %{buildroot}%{_bindir}/ftppr
install -m755 -D src/mycrypt %{buildroot}%{_bindir}/mycrypt
install -m755 -D src/pop3p %{buildroot}%{_bindir}/pop3p
install -m755 -D src/3proxy %{buildroot}%{_bindir}/3proxy
install -m755 -D src/proxy %{buildroot}%{_bindir}/htproxy
install -m755 -D src/socks %{buildroot}%{_bindir}/socks
install -m755 -D src/tcppm %{buildroot}%{_bindir}/tcppm
install -m755 -D src/udppm %{buildroot}%{_bindir}/udppm

install -pD -m755 %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
install -pD -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}.cfg

%clean
rm -rf %{buildroot}

%post
# Register service
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%{_initrddir}/%{name}
%{_localstatedir}/log/%{name}
%doc Readme Changelog authors copying news

%changelog
* Thu Aug 20 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6-3
- Fedora Review started - thank you Peter Lemenkov.
- Change rights (0755->0644) of config.
- Disable service by default.
- Add BR dos2unix.

* Mon Aug 17 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6-2
- /usr/bin/proxy renamed to htproxy to avoid name bump with libproxy-bin.
- Add Source2: 3proxy.cfg from Alt Linux (slightly modified) - http://sisyphus.ru/ru/srpm/Sisyphus/3proxy/sources/1 (thanks to Afanasov Dmitry).
- Add log-dir %%{_localstatedir}/log/%%{name}

* Mon Aug 17 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6-1
- Ressurect old spec. New version 0.6.
- Rename spec to classic %%{name}.spec.
- Remove Hu part from release and add %%{?dist}.
- Change summary, description, URL. Add Russian localisation of sumamry and description.
- Strip some old comments.
- Add to %%doc Readme Changelog authors copying news.
- Turn macros usage from %%name to %%{name} for consistence.
- Change group from System/Servers to standard System Environment/Daemons.
- Add %%defattr(-,root,root,-) in %%files section.
- Add cleanup in %%install section.
- Add %%clean section with cleanup buildroot.
- License changed from just GPL to "BSD or ASL 2.0 or GPLv2+ or LGPLv2+" (according to Makefile.Linux)
- Add %%config(noreplace) mark to all configs.
- Add file %%{_initdir}/%%{name}
- Old %%{_initdir} macros replaced by %%{_initrddir}
- Hack makefile to use system CFLAGS.
- Add %%post/%%postun sections.

* Fri Jan 25 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.5.3k
- Import from ftp://ftp.nluug.nl/pub/os/Linux/distr/altlinux/4.0/Server/4.0.1/files/SRPMS/3proxy-0.5.3h-alt1.src.rpm
	Combine with ftp://ftp.pbone.net/mirror/ftp.sourceforge.net/pub/sourceforge/t/th/three-proxy/3proxy-0.5.3g-1.src.rpm
- Steep to version 0.5.3k
- Comment out packager
- Reformat header of spec with tabs
- Add desc from second src.rpm of import
- Correct source0
- Add -c key fo %%setup macro
- Add BuildRoot definition (this is not ALT)
- Change
	Release:	alt1
	to
	Release:	0.Hu.0

* Fri Apr 13 2007 Lunar Child <luch@altlinux.ru> 0.5.3h-alt1
- new version

* Wed Mar 21 2007 Lunar Child <luch@altlinux.ru> 0.5.3g-alt2
- Added init script.
- Added new trivial config file.

* Tue Mar 20 2007 Lunar Child <luch@altlinux.ru> 0.5.3g-alt1
- First build for ALT Linux Sisyphus
