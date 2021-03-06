%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand:	%%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

%global	CVS	20090309
%global	peclName	parsekit

Summary:		PHP Opcode Analyser
Name:		php-pecl-%peclName
Version:		1.2
Release:		3%{?CVS:.CVS%{CVS}}%{?dist}
License:		PHP
Group:		Development/Libraries
%if 0%{?CVS:1}
# cvs -d :pserver:cvsread@cvs.php.net/repository export -D 2009-03-09 pecl/parsekit ; tar cjf parsekit-1.2-CVS20090309.tar.bz2 -C pecl parsekit
Source0:		%{peclName}-%{version}-CVS%{CVS}.tar.bz2
%else
Source0:		http://pecl.php.net/get/%{peclName}-%{version}.tgz
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:			http://pecl.php.net/package/%peclName
BuildRequires: php-pear >= 1.4.7 php-devel

%if %{?php_zend_api}0
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
Requires:		php-api = %{php_apiver}
%endif
Provides:		php-pecl(%peclName) = %{version}

Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}

%description
Provides a userspace interpretation of the opcodes generated by the Zend engine
compiler built into PHP.
This extension is meant for development and debug purposes only and contains
some code which is potentially non-threadsafe.

%prep
#%setup -qc -n %peclName-%{version}
%setup -qc

%build
cd %peclName
phpize
%{configure} --with-%peclName
%{__make}

%install
cd %peclName
rm -rf %{buildroot}

%{__make} install \
	INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 package.xml %{buildroot}%{pecl_xmldir}/%peclName.xml
install -d %{buildroot}%{_sysconfdir}/php.d/

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%peclName.ini
; Enable %{peclName} extension module
extension=%{peclName}.so
EOF

%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{peclName}.xml >/dev/null || :
%endif

%postun
%if 0%{?pecl_uninstall:1}
if [ $1 -eq 0 ] ; then
	%{pecl_uninstall} %{peclName} >/dev/null || :
fi
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %peclName/examples/{compile_file.php,compile_string.php,compile_string_show_errors.php} %peclName/README
%{php_extdir}/%peclName.so
%{pecl_xmldir}/%peclName.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.d/%peclName.ini

%changelog
* Tue Jun 30 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2-3.CVS20090309
- Most of changes inspired by continue Fedora review by Jason Tibbitts.
- Prefer %%global over %%define
- Source0 is not URL now for CVS build.
- "PECL" prefix removed from summary.
- Add %%release part into BuildRoot tag.
- Add more magic into Release define and fit it into one line.OD

* Mon Mar 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.2-2.CVS20090309
- php-pecl-parsekit.Hu.spec renamed to normal php-pecl-parsekit.spec
- In Version changhes: As it is post release enumereate it after 0. Remove Hu-part.
- New CVS checkout 20090309
- Add php_apiver and __pecl macroses define. Remove peardir.
- Remove define macros xmldir and replace it by common pecl_xmldir
- Add comment of command how to get source.
- Add patch Patch2: php-pecl-parsekit-1.2.APIstatic.patch to allow build on recent versions.
- Fix several inconsistent macros usages.
- Add standard Requires/provides of php-api, abi, zend abi, php-pecl(%%peclName) = %%{version}...
- Delete pathces, which is not needed anymore in ew checkout.
- Remove Obsoletes:	php-pear-%%peclName
- Add Requires(post):	%%{__pecl} and Requires(postun):	%%{__pecl}
- Rpmlint warnings:
	o Mixed spaces turned to tabs.
	o Descrioption line too long: splited.
	o License from "PHP License" changed to just PHP
	o script-without-shebang /usr/share/pear/.pkgxml/parsekit.xml: chmod to 0664

* Tue May 13 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.2-0.CVS20080513.Hu.0
- Initial spec (copy of php-pecl-imagick.Hu.spec)
- Add (import from runkit spec-file) CVS-build support
- Add patches:
	Patch0:		php-pecl-parsekit-php51.patch (http://www.mail-archive.com/pld-cvs-commit@lists.pld-linux.org/msg28512.html)
	Patch1:		php-pecl-parsekit-1.2-PHP5.3.0.patch (self)
- Post and Pustun steps replaced by it is macroses-representated form (from php-pecl-phar)