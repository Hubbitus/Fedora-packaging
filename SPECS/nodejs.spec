# Another package already occupies the "node" name
Name:           nodejs
Version:        0.4.1
Release:        1%{?dist}
Summary:        Event-driven I/O v8 JavaScript run-time

Group:          Development/Languages
License:        MIT
URL:            http://nodejs.org/
Source0:        http://nodejs.org/dist/node-v%{version}.tar.gz
# This should be made configurable before upstream submission
# https://github.com/ry/node/issues/698
Patch1:         0001-Use-external-http-parser-and-eio.patch
# This is specific to our build of v8
# Maybe v8 should record this in its pkgconfig file (if it had one).
Patch2:         0001-Enable-EV_MULTIPLICITY.patch
# This would need some more work before being upstreamable,
# https://github.com/ry/node/issues/699
Patch3:         0001-Use-saner-search-paths-for-modules.patch
# Not really upstreamable at this point, since it would break debug builds.
# Seems like upstream is moving to cmake anyway.
Patch4:         0001-Fix-build-with-newer-waf.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
ExclusiveArch:  %{ix86} x86_64 arm

BuildRequires:  libgpg-error-devel
BuildRequires:  openssl-devel
BuildRequires:  python
BuildRequires:  v8-devel >= 3.0.0
BuildRequires:  c-ares-devel >= 1.7.3
BuildRequires:  libev-devel
BuildRequires:  libeio-devel >= 0.3-5
BuildRequires:  http-parser-devel
BuildRequires:  waf

%description
Node's goal is to provide an easy way to build scalable network programs.
It's based on Google's v8 JavaScript engine and is accompanied with an
event-driven I/O library.


%package devel
Group:          Development/Libraries
Summary:        Development headers for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       v8-devel
Requires:       libev-devel
Requires:       libeio-devel

%description devel
Development headers for %{name}.


%prep
%setup -q -n node-v%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
rm -rf deps/* tools/wafadmin bin/node-waf tools/waf-light tools/scons
rm -rf deps/* tools/scons


%build
CC="%{__cc} %{optflags}" CXX="%{__cxx} %{optflags}" \
waf configure --prefix=%{_prefix} -v --shared-v8 --shared-cares --shared-libev \
	--shared-libev-includes=%{_includedir}/libev
# Dont pick v8's js2c module, it's different from ours
PYTHONPATH=tools/ waf build %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT waf install
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_datadir}/node
install -d $RPM_BUILD_ROOT%{_libdir}/node
#install -pm644 src/node.h $RPM_BUILD_ROOT%{_includedir}
#install -pm644 src/node_object_wrap.h $RPM_BUILD_ROOT%{_includedir}
[ %{_lib} = lib ] || mv $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig \
        $RPM_BUILD_ROOT%{_libdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_prefix}/lib*/node
%{_mandir}/man1/*.1*
%doc ChangeLog LICENSE README.md doc


%files devel
%defattr(-,root,root,-)
%{_includedir}/node
%{_libdir}/pkgconfig/*


%changelog
* Sun Feb 20 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-1
- Bump version
- Look for non-native modules in datadir
- Build with newer waf
- Use waf to install headers

* Tue Jan 11 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.3.4-1
- Update to 0.3.4

* Tue Dec 28 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.3.2-1
- Update to 0.3.2

* Wed Oct 27 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.2.3-1
- Use optflags
- Incorporated loads of suggestions from Damian Wrobel:
- Fixed up Source URL
- Dropped bundled waf
- Rebased to later upstream release
- Used correct interpreter for REPL
- Fixed up poor wordings
- Corrected devel subpackage's dependencies

* Sat Sep 18 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.2.1-3
- Fix set-cookkie handling

* Wed Sep 15 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.2.1-2
- Add devel package

* Wed Sep 15 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.2.1-1
- Bump version

* Fri Feb 12 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.1.28-1
- Bump version

* Thu Feb 04 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.1.27-1
- Initial packaging
