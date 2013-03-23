Name:		RabbIT
%define lname %( echo %{name} | tr 'A-Z' 'a-z' )

Version:		4.1
Release:		9%{?dist}
Summary:		Proxy for a faster web
Summary(ru):	Прокси для быстрого серфинга в ВЕБе
#By example of squid
Group:		System Environment/Daemons
License:		BSD
URL:			http://www.khelekore.org/rabbit/
Source0:		http://www.khelekore.org/rabbit/%{lname}%{version}-src.tar.gz
#Startup scrip to start/stop daemon. Self produced.
Source1:		%{lname}.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	jpackage-utils

Requires:		java >= 1:1.6.0, jpackage-utils
Requires:		ImageMagick, dnsjava

#Adjust only used paths in default config.
Patch0:		RabbIT-4.0.fedora-config-path.patch

Requires(pre):		/usr/sbin/useradd
Requires(post):	chkconfig
Requires(preun):	chkconfig
Requires(postun):	/usr/sbin/userdel

BuildArchitectures:	noarch

%description
RabbIT is a web proxy that speeds up web surfing over slow links by doing: 
	o Compress text pages to gzip streams. This reduces size by up to 75% 
	o Compress images to 10% jpeg. This reduces size by up to 95% 
	o Remove advertising 
	o Remove background images 
	o Cache filtered pages and images 
	o Uses keepalive if possible 
	o Easy and powerful configuration 
	o Multi threaded solution written in java 
	o Modular and easily extended 
	o Complete HTTP/1.1 compliance

%description -l ru
RabbIT фэто ВЕБ-прокси который ускоряет Ваш серфинг через медленные каналы.
Основные возможности и достоинства:
	o Сжимает (gzip) все текстовые страницы. Это уменьшает их размер до 75%
	o Сдимает картинки в jpeg с 10% качеством. Это уменьшает их размер до 95%!
	o Удаляет рекламу
	o Удаляет фоновые картинки
	o Кеширует страницы и картинки
	o Если доступно, использует постоянные соединения (keepalive)
	o Простая, но мощная настройка
	o Многопотоковый, написан на Java и работает практически везде.
	o Модульный и легкорасширяемый
	o Полная поддержка стандарта HTTP/1.1.

%prep
%setup -q -n %{lname}4

%patch0 -p0 -b .conf-path


%build
# https://fedoraproject.org/wiki/Packaging/Java#class-path-in-manifest
sed -i '/class-path/I d' Manifest.mf
#Adjust path ( https://fedoraproject.org/wiki/Packaging/Java#build-classpath ):
#? sed -i "s#../external_libs/dnsjava-2.[[:digit:]].[[:digit:]].jar#$(build-classpath dnsjava)#" Manifest.mf

make %{?_smp_mflags}

#Make script-wrapper
cat << HEREDOC > %{name}
#!/bin/sh
java -jar %{_javadir}/%{name}-%{version}.jar -f %{_sysconfdir}/%{name}/%{name}.conf
HEREDOC

# Author say what it is iso-8859-1
iconv -f iso-8859-1 -t UTF-8 htdocs/LICENSE.txt > htdocs/LICENSE.utf-8.txt
touch --reference htdocs/LICENSE.txt htdocs/LICENSE.utf-8.txt
iconv -f iso-8859-1 -t UTF-8 LICENSE > LICENSE.utf-8
touch --reference LICENSE LICENSE.utf-8
mv htdocs/LICENSE.utf-8.txt htdocs/LICENSE.txt
mv LICENSE.utf-8 LICENSE

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_javadir}
install -m644 jars/rabbit4.jar %{buildroot}/%{_javadir}/%{name}-%{version}.jar
install -d %{buildroot}/%{_bindir}
install -m755 %{name} %{buildroot}/%{_bindir}/%{name}

install -d %{buildroot}/%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_initrddir}/

sed 's#{{HTDOCS}}#%{_datadir}/%{name}#' %{SOURCE1} > %{buildroot}/%{_initrddir}/%{lname}

install -d %{buildroot}/%{_datadir}/%{name}/htdocs
cp -r htdocs/* %{buildroot}/%{_datadir}/%{name}/htdocs/

install -d %{buildroot}/%{_localstatedir}/log/%{name}
#install -d %{buildroot}/%{_localstatedir}/run/%{name}.pid

touch %{buildroot}/%{_localstatedir}/log/%{name}/main_run.log

# We exclude rabbit.conf.orig, so, we can't do just install whole directory
install -m644 conf/access		%{buildroot}/%{_sysconfdir}/%{name}/
install -m644 conf/allowed		%{buildroot}/%{_sysconfdir}/%{name}/
install -m644 conf/cache_only.conf	%{buildroot}/%{_sysconfdir}/%{name}/
#install -m644 conf/empty.conf		%{buildroot}/%{_sysconfdir}/%{name}/
install -m644 conf/nocache.conf	%{buildroot}/%{_sysconfdir}/%{name}/
install -m644 conf/%{lname}.conf	%{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
install -m644 conf/users			%{buildroot}/%{_sysconfdir}/%{name}/

%pre
# Add the "rabbit" user
/usr/sbin/useradd -c "%{lname}" -s /sbin/nologin -r -d "%{_docdir}/%{name}-%{version}" %{lname} 2> /dev/null || :

%post
# Register service
/sbin/chkconfig --add %{lname}

%preun
if [ $1 = 0 ]; then
	/sbin/service %{lname} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{lname}
fi

%postun
/usr/sbin/userdel %{lname}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_initrddir}/%{lname}
%doc ChangeLog README Help.txt LICENSE
%{_datadir}/%{name}/
%{_javadir}/%{name}-%{version}.jar
%attr(755,%{lname},root) %{_bindir}/%{name}
%dir %attr(755,%{lname},root) %{_localstatedir}/log/%{name}
%attr(755,%{lname},root) %ghost %{_localstatedir}/log/%{name}/main_run.log
%config(noreplace) %{_sysconfdir}/%{name}/access
%config(noreplace) %{_sysconfdir}/%{name}/allowed
%config(noreplace) %{_sysconfdir}/%{name}/cache_only.conf
#%config(noreplace) %{_sysconfdir}/%{name}/empty.conf
%config(noreplace) %{_sysconfdir}/%{name}/nocache.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/users

%changelog
* Sat Aug 15 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 4.1-9
- Step to version 4.1.
- Robert Oloffson kindly change version enumeration by my request, now tarball have version and release.
- Own log dir also by %%{lname} user

* Sun Aug 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 4.0-8
- Step to new version 4.0
- Use %%{name} in Source url
- Add %%ghost %%{_localstatedir}/log/%%{name}/main_run.log
- Own as rabbit user only binary file, not all package.
- Remove name from summary.
- Add russian localized Summary and description.
- Own %%{_datadir}/%%{name}/ instead of %%{_datadir}/%%{name}/htdocs
- Source1 RabbIT.init renamed to rabbit.init.
- Remade Patch0: RabbIT-3.17.fedora-config-path.patch -> RabbIT-4.0.fedora-config-path.patch
- Delete TODO from docs, it is not present anymore.
- Add lsb # Default-Start: 2 3 4 5, # Default-Stop: 0 1 6 to init file to do rpmlint happy. Turn pid and lock files to lowercase.
- Delete classpath from manifest.
- Default disable service running: --level -

* Mon Apr 27 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.18-7
- Accidentally leaved httpd instead on %%name in %%post script fixed.
- Path of http-root files changed from %%{_docdir}/%%{name}-%%{version} to %%{_datadir}/%%{name}

* Sun Apr 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.18-6
- In review ( https://bugzilla.redhat.com/show_bug.cgi?id=492810 ) was tald pack dnsjava separate. Do it:
	o Remove bundled jar-package
	o Cutoff classpath from manifest
	o Add Requires dnsjava

* Wed Apr 01 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.18-5
- New version 3.18

* Tue Mar 31 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.17-4
- After aontact author, now I known encoding of License (iso-8859-1) and recode it.
- Exclude /etc/RabbIT/empty.conf

* Sun Mar 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.17-3
- Add %%doc htdocs
- Add run from another user, not root! For that:
	o Add Requires(pre): /usr/sbin/useradd
	o Requires(postun): /usr/sbin/userdel
	o In pre and postun sections add/delete user rabbit.
- Add %%{_localstatedir}/log/%%{name} in package.
- Inspired by rpmlint:
	o %%{_initrddir}/%%{name} renamed to %%{_initrddir}/%%{lname}

* Sun Mar 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.17-2
- Add registration of service with chkconfig. Add it into Requires(post/preun), and according sections.
- BuildArchitectures: noarch
- Install also %%{_javadir}/dnsjava-2.0.6.jar

* Sun Mar 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 3.17-1
- Initial spec file.