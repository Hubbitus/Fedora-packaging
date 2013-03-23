%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl: %{expand: %%global __pecl %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global	peclName	xdebug
#% global	SVNrev	3198

Name:		php-pecl-%peclName
Version:		2.1.0
Release:		0.beta1%{?SVNrev:.rev%{SVNrev}}%{?dist}.Hu.4
Summary:		PHP xdebug extension

License:		BSD
Group:		Development/Languages
URL:			http://pecl.php.net/package/%peclName
%if 0%{?SVNrev}
# svn co -r %{SVNrev} svn://svn.xdebug.org/svn/xdebug/xdebug/trunk xdebug-2.1.0; tar -cjf xdebug-2.1.0-rev%{SVNrev}.tar.bz2 xdebug-2.1.0
Source0:		%peclName-%{version}-rev%{SVNrev}.tar.bz2
%else
Source0:		http://xdebug.org/files/xdebug-2.1.0beta1.tgz
%endif

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	php-devel
Provides:		php-pecl(%peclName) = %{version}

%if %{?php_zend_api}0
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
# for EL-5
Requires:		php-api = %{php_apiver}
%endif
#-Patch0:		xdebug-2.0.3.max_data.option.add.patch

%description
The %peclName extension helps you debugging your script by providing a lot
of valuable debug information.

%prep
#% setup -qcn %peclName-%{version}
#?cd %peclName-%{version}

%setup -qn %peclName-%{version}beta1

#% patch0 -p1 -b .max_data

# fix rpmlint warnings
iconv -f iso8859-1 -t utf-8 Changelog > Changelog.conv && mv -f Changelog.conv Changelog

%build
#?cd %peclName-%{version}
phpize
%configure --enable-%peclName
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags}


%install
#?cd %peclName-%{version}
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%peclName.ini << 'EOF'
; Enable %peclName extension module
zend_extension=%{php_extdir}/%peclName.so

;%peclName.remote_enable=1
;%peclName.remote_host=localhost
;%peclName.remote_handler="dbgp"
;%peclName.remote_port=9000
;%peclName.remote_mode=req

; How many data send by default to IDE, when evalute expression. 0 means - all.
; http://xdebug.org/docs-dbgp.php#property-get-property-set-property-value
;%peclName.max_data=1024;

EOF

# install doc files
install -d docs
install -pm 644 Changelog CREDITS LICENSE NEWS README docs


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %peclName >/dev/null || :
fi
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %peclName-%{version}/docs/*
%config(noreplace) %{_sysconfdir}/php.d/%peclName.ini
%{php_extdir}/%peclName.so

%changelog
* Tue Jan 5 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.1.0-0.beta1.Hu.4
- "stable" beta1 build
- Add %%{?_smp_mflags} for parallel build.

* Tue Jan 5 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.1.0-0.beta1.rev3198.Hu.3
- SVN version of 2.1.0 beta1
- Switch to SVN
- Prefer %%global over %%define
- Fix %%postun macros.

* Sun Aug 23 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.1-0.CVS20090822.Hu.2
- CVS 20090822

* Wed Jul 1 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.1-0.CVS20090301.Hu.1
- Add more magic into Release define and fit it into one line.
- Rename spec, remove "Hu part from it"
- Change summary.

* Wed Mar 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.1-0.CVS20090311.Hu.0
- CVS 20090311
- From CVS source delete URL-part
- Add comment how to gat tarball.
- Disable patch0 (may be adopted after tests)

* Sat Sep 13 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.1-0.CVS20080913.Hu.0
- CVS 20080913

* Sat Jul 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.1-0.CVS20080712.Hu.0
- CVS 20080712

* Thu Jun 26 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.1-0.CVS20080626.Hu.0
- 2.1 CVS20080626 Build
- Build for Fedora9

* Mon May 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.1-0.CVS20080512.Hu.0
- 2.1 CVS20080512 Build
- Add %%define CVS.
- Add %%if%%else to handle CVS build

* Fri May 9 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0.3-0.Hu.1
- Add define %%peclName, and replece to it direct occurance of sdebug.
- Add patch xdebug-2.0.3.max_data.option.add.patch Eclipse have not support additional retrive property_value.
	So, this patch add php-option xdebug.max_data to set global default for max_data option (http://xdebug.org/docs-dbgp.php#property-get-property-set-property-value)

* Wed May 7 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.0.3-0.Hu.0
- Step to version 2.0.3
- Disable patch0, but do NOT delete it!

* Thu Feb 14 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 2.0.2
- Step to version 2.0.2
- Reformat header of spec-file with tabs
- Add patch0 xdebug.c-php-5.3.0.patch

* Tue Nov 6 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> 2.0.1-0
- Update to version 2.0.1

* Sun Sep 30 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-2
- Update to latest standards
- Fix encoding on Changelog

* Sat Sep 08 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-1
- Upstream sync
- Remove %%{?beta} tags

* Sun Mar 11 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.5.RC2
- Create directory to untar sources
- Use new ABI check for FC6
- Remove %%{release} from Provides

* Mon Jan 29 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.4.RC2
- Compile with $RPM_OPT_FLAGS
- Use $RPM_BUILD_ROOT instead of %%{buildroot}
- Fix license tag

* Mon Jan 15 2007 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.3.RC2
- Upstream sync

* Sun Oct 29 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.2.RC1
- Upstream sync

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 2.0.0-0.1.beta6
- Remove Provides php-xdebug
- Fix Release
- Remove prior changelog due to Release number change
