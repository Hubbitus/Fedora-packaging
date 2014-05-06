%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global peclName  xmldiff

Name:             php-pecl-%peclName
Version:          0.9.2
Release:          1%{?dist}
Summary:          Pecl package for XML diff and merge

License:          BSD
URL:              http://pecl.php.net/package/%peclName
Source0:          http://pecl.php.net/get/%peclName-%{version}.tgz

BuildRequires:    php-pear
BuildRequires:    php-devel
BuildRequires:    diffmark-devel, dos2unix
# dom.so needed by %%check
BuildRequires:    php-xml
Requires(post):   %{__pecl}
%if 0%{?pecl_uninstall:1}
Requires(postun): %{__pecl}
%endif
Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
Requires:         php-xml

Provides:         php-%peclName = %{version}
Provides:         php-%peclName%{?_isa} = %{version}

# Filter private shared (RPM 4.9)
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$

%description
The extension is able to produce diffs of two XML documents and then
to apply the difference to the source document. The diff
is a XML document containing copy/insert/delete instruction nodes in
human readable format. DOMDocument objects, local files and strings in
memory can be processed.


%prep
%setup -qc

#rm bundled diffmark
rm -rf %peclName-%{version}/diffmark

# to make rpmlint happy
dos2unix --keepdate %peclName-%{version}/LICENSE

%build
cd %peclName-%{version}
phpize
%{configure} --with-%peclName --with-libdiffmark=%{_libdir}
make %{?_smp_mflags}


%install
cd %peclName-%{version}

make %{?_smp_mflags} install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml
install -d %{buildroot}%{php_inidir}
# install config file
install -d %{buildroot}%{php_inidir}
cat << 'EOF' | tee %{buildroot}%{php_inidir}/%peclName.ini
extension=%{php_extdir}/%peclName.so
EOF

rm -rf %{buildroot}/%{_includedir}/php/ext/%peclName/

%check
# only check if build extension can be loaded
%{_bindir}/php \
    --no-php-ini \
    --define extension=dom.so \
    --define extension=%{buildroot}%{php_extdir}/%peclName.so \
    --modules | grep %peclName

%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
  %{pecl_uninstall} %peclName >/dev/null || :
fi
%endif

%files
%doc %peclName-%{version}/{CREDITS,LICENSE}
%config(noreplace) %{php_inidir}/%peclName.ini
%{php_extdir}/%peclName.so
%{pecl_xmldir}/%{name}.xml

%changelog
* Tue May 6 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.2-1
- Initial spec
