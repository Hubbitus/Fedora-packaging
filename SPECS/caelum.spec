%global commit0 e776a806407a85bd7ea2ba3fb05a47b86f2f5b54
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           caelum
Version:        0.6.2
Release:        0.1%{?shortcommit0:.git.%{shortcommit0}}%{?dist}
Summary:        Add-on for the 3D graphics rendering engine OGRE

License:        LGPLv3+
URL:            https://bitbucket.org/ogreaddons/caelum/overview
Source0:        https://github.com/RigsOfRods/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  ogre-devel, cmake, ois-devel

%description
Caelum is an add-on for the 3D graphics rendering engine OGRE, aimed to render
atmospheric effects.

%package devel
Summary:        Development files for caelum
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{name}-%{commit0}

%build
%cmake .
make %{?_smp_mflags}


%install
%make_install

# It just OGRE plugin (http://www.rigsofrods.com/wiki/pages/Compiling_Sources_under_Linux#Caelum_.28dynamic_sky_-_optional.29)
mkdir -p %{buildroot}/%{_libdir}/OGRE/
mv %{buildroot}/%{_libdir}/libCaelum.so %{buildroot}/%{_libdir}/OGRE/libCaelum.so

rm -rf %{buildroot}/usr/doc

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc Contributors.txt ReadMe.txt lgpl.txt gpl.txt
%{_libdir}/OGRE/libCaelum.so

%files devel
%{_includedir}/Caelum
%{_libdir}/pkgconfig/Caelum.pc


%changelog
* Wed Jan 06 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.2-0.1.git.e776a80
- Change upstream to https://github.com/RigsOfRods/caelum
- Update to unreleased version 0.6.2 (change versioning).
- Update spec to use upstream VCS.
- Move so file in OGRE dir as it is just plugin.
- Drop old patch.

* Sat Feb 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.1-4
- Add BR ois-devel
- Exclude gpl.txt.

* Sun Jan 27 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.1-3
- Build against ogre 1.8.1
- Add patch Patch1: caelum-0.6.1-ogre-1.8.1.patch

* Mon Nov 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.1-2
- Using %%cmake macro instead of hacks as sugested by Susi Lehtola in review (bz#879933).
- Thanks to comments of Volker Fröhlich:
    o Add %%{?_isa} to devel require.
    o Move Requires: pkgconfig to devel package.
    o Add cmake as BR.

* Sun Sep 23 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.6.1-1
- Initial version.
