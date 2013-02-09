Name:           caelum
Version:        0.6.1
Release:        4%{?dist}
Summary:        Add-on for the 3D graphics rendering engine OGRE

License:        LGPLv3+
URL:            http://code.google.com/p/caelum/
# RPM does not uderstand that full URL: http://code.google.com/p/caelum/downloads/detail?name=caelum-0.6.1.tar.gz&can=2&q=
Source0:        %{name}-%{version}.tar.gz
Patch0:         caelum-0.6.1-ogre-1.8.1.patch
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
%setup -q
%patch0 -p1 -b .ogre.1.8.1


%build
%cmake .
make %{?_smp_mflags}


%install
%make_install

rm -rf %{buildroot}/usr/doc

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc Contributors.txt ReadMe.txt lgpl.txt
%{_libdir}/libCaelum.so

%files devel
%{_includedir}/Caelum
%{_libdir}/pkgconfig/Caelum.pc


%changelog
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
