Name:           angelscript
# RigsOfRods require 2.22.1 version, notmost fresh!
# It also strongly required: http://redmine.rigsofrods.com/issues/1033
# Also old fixed version: http://redmine.rigsofrods.com/issues/956
Version:        2.22.1
Release:        1%{?dist}
Summary:        AngelCode Scripting Library

Group:          System Environment/Libraries
License:        zlib
URL:            http://www.angelcode.com/angelscript/
Source0:        http://www.angelcode.com/angelscript/sdk/files/%{name}_%{version}.zip
Patch0:         %{name}-2.22.1-link.patch

%description
The AngelScript library is a software library for easy integration of
external scripting to applications, with built-in compiler and virtual
machine. The scripting language is easily extendable to incorporate
application specific datatypes and functions. It is designed with C++
in mind, as such it shares many features with C++, for example syntax
and data types.


%package devel
Summary:        Development files for the AngelScript libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for the AngelScript library.


%prep
%setup -q -c
%patch0 -p1 -b .link

sed -i 's|$(LOCAL)/lib|$(LOCAL)/%{_lib}|g' sdk/%{name}/projects/gnuc/makefile


%build
pushd sdk/%{name}/projects/gnuc
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing" SHARED=1 VERSION=%{version}
popd


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

pushd sdk/%{name}/projects/gnuc
make install LOCAL=$RPM_BUILD_ROOT%{_prefix} SHARED=1 VERSION=%{version}
popd


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc sdk/docs/articles/*.html
%{_libdir}/lib%{name}-%{version}.so


%files devel
%defattr(-,root,root,-)
%doc sdk/docs/*
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h


%changelog
* Mon Nov 19 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.22.1-1
- Import from http://fedora.danny.cz/danny/development/SRPMS/angelscript-2.24.1-1.fc18.src.rpm
- Build 2.22.1 version due to the bug http://redmine.rigsofrods.com/issues/956

