Name:           angelscript
Version:        2.26.0
Release:        1%{?dist}
Summary:        Flexible cross-platform scripting library

Group:          System Environment/Libraries
License:        zlib
URL:            http://www.angelcode.com/angelscript/
Source0:        http://www.angelcode.com/angelscript/sdk/files/%{name}_%{version}.zip
# Reported upstream http://www.gamedev.net/topic/638512-linker-problem/
Patch0:         %{name}-2.22.1-link.patch

%description
The AngelScript library is a software library for easy integration of
external scripting to applications, with built-in compiler and virtual
machine. The scripting language is easily extendable to incorporate
application specific data types and functions. It is designed with C++
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
make %{?_smp_mflags} CXFLAGS="$RPM_OPT_FLAGS" SHARED=1 VERSION=%{version}
popd


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

pushd sdk/%{name}/projects/gnuc
make install LOCAL=%{buildroot}%{_prefix} SHARED=1 VERSION=%{version}
popd


%clean
rm -rf %{buildroot}


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
* Sat Feb 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.26.0-1
- New version released.
- It seams backward capability patch doews not needed anymore.

* Sat Jan 26 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.25.2-1
- Update to 2.25.2 version.
- Apply (rebased) Patch1 to provide backward compatability with hope rigsofrods can work with it (https://bugzilla.redhat.com/show_bug.cgi?id=879931#c3) (thanks to Dan Horák).

* Mon Nov 19 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.22.1-1
- Import from http://fedora.danny.cz/danny/development/SRPMS/angelscript-2.24.1-1.fc18.src.rpm
- Build 2.22.1 version due to the bug http://redmine.rigsofrods.com/issues/956

