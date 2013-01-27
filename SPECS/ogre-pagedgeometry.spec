Name:           ogre-pagedgeometry
Epoch:          1
Version:        1.1.0
Release:        7%{?dist}
Summary:        Ogre addon for realtime rendering of dense forests
Group:          Development/Libraries
License:        zlib
URL:            http://www.ogre3d.org/wiki/index.php/PagedGeometry_Engine
Source0:        http://ogre-paged.googlecode.com/files/pagedGeometry-%{version}.zip
Patch1:         pagedgeometry-no-force-static.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  ogre-devel
# For examples we aren't packaging (yet - need to use GLSL instead of Cg)
# If fixed a requires for ois and libX11 will be needed.
BuildRequires:  ois-devel
BuildRequires:  libX11-devel

# For now we aren't installing the pc file
#Requires: pkgconfig
Requires: ogre
# The library gets placed in a directory owned by ogre, but that dependency
# should be built automatically based on needed libraries.


%description
Real-time rendering of massive, dense forests, with not only trees, but 
bushes, grass, rocks, and other "clutter". Supports dynamic transitioned 
LOD between batched geometry and static impostors (extendable). 

%package        devel
Summary:        Development files for PagegGeometry
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    devel
The ogre-addons-pagedgeometry-devel package contains libraries and header 
files for developing applications that use the PagedGeometry OGRE Add-On.

%ifarch %{ix86}
%package        sse2
Summary:        Ogre addon for realtime rendering of dense forests using sse2 instructions
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    sse2
Real-time rendering of massive, dense forests, with not only trees, but 
bushes, grass, rocks, and other "clutter". Supports dynamic transitioned 
LOD between batched geometry and static impostors (extendable). sse2
instructions are enabled.
%endif

%prep
%setup -q -n pagedGeometry-%{version}
%patch1 -p1 -b .shared
for file in GettingStarted.txt Todo.txt ; do
   mv $file timestamp && \
   iconv -f WINDOWS-1252 -t UTF-8 -o $file timestamp && \
   touch -r timestamp $file && \
   rm timestamp
done

%build
mkdir build
cd build
%cmake -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING= -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING= .. 
# Builds out of order with _smp_mflags
make VERBOSE=1
mkdir lib
mv ../lib/libPagedGeometry.so lib/
cd ..

# For x86 build a separate sse2 library that will be autodetected at runtime
%ifarch %{ix86}
mkdir sse2
cd sse2
%cmake -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=-msse2 -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING=-msse2 ..
make VERBOSE=1 %{?_smp_mflags}
mkdir lib
mv ../lib/libPagedGeometry.so lib/
cd ..
%endif


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/OGRE/PagedGeometry
cp -a include/* %{buildroot}%{_includedir}/OGRE/PagedGeometry
rm -f %{buildroot}%{_includedir}/OGRE/PagedGeometry/PagedGeometryConfig.h.in
cp -p build/include/* %{buildroot}%{_includedir}/OGRE/PagedGeometry
mkdir -p %{buildroot}%{_libdir}/OGRE
cp -p build/lib/libPagedGeometry.so %{buildroot}%{_libdir}/OGRE/
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -p GettingStarted.txt Todo.txt docs/*.odt %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%ifarch %{ix86}
mkdir -p %{buildroot}%{_libdir}/sse2/OGRE
cp -p sse2/lib/libPagedGeometry.so %{buildroot}%{_libdir}/sse2/OGRE/
%endif

# Note: The examples are now being built by default, but they're pretty worthless without cg.
# So... I didn't package them. ~spot (21-Dec-2010)

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/OGRE/libPagedGeometry.so


%ifarch %{ix86}
%files sse2
%defattr(-,root,root,-)
# Ogre doesn't do sse2 builds so doesn't own an sse2/OGRE directory
%{_libdir}/sse2/OGRE
%{_libdir}/sse2/OGRE/libPagedGeometry.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}-%{version}
%{_includedir}/OGRE/PagedGeometry


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 05 2012 Bruno Wolff III <bruno@wolff.to> - 1:1.1.0-6
- Fix for bz 771772 PagedGeometryConfig.h was not included

* Sun May 15 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.0-5
- Rebuild for ogre 1.7.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Bruno Wolff III <bruno@wolff.to> - 1.1.0-3
- Self references need to use the epoch.

* Sat Jan 15 2011 Bruno Wolff III <bruno@wolff.to> - 1.1.0-2
- It turns out 1.1 < 1.05 so we need an epoch bump

* Tue Dec 21 2010 Tom Callaway <spot@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sat Nov 07 2009 Bruno Wolff III <bruno@wolff.to> - 1.05-4.2721svn
- Remove unnecessary option to cmake to request shared library build

* Fri Nov 06 2009 Bruno Wolff III <bruno@wolff.ro> - 1.05-3.2721svn
- Properly capitalize the include directory name
- The pkgconfig file isn't being installed so requires isn't needed

* Sun Nov 01 2009 Bruno Wolff III <bruno@wolff.ro> - 1.05-2.2721svn
- Bruno will take over as primary maintainer
- Switch to the latest svn to pick up some bug fixes
- Build an alternate sse2 library
- Keep cmake from adding compiler flags based on build type
- Keep cmake from adding -msse for gcc builds no matter the target
- Keep cmake from forcing a static library (this is very likely an upstream bug)

* Tue Sep 29 2009 Guido Grazioli <guido.grazioli@gmail.com> - 0-1.2698svn
- Initial packaging
