Name:           mygui
Version:        3.2.0
Release:        4%{?dist}
Summary:        Fast, simple and flexible GUI library for Ogre
Group:          Development/Libraries
# UnitTests include agg-2.4, which is under a BSD variant (not built or installed here)
License:        LGPLv3+ 
URL:            http://mygui.info/
Source0:        http://downloads.sourceforge.net/my-gui/MyGUI_%{version}.zip
# Helper to run demos, based on A. Torkhov Ogre-Samples shipped with ogre-samples
Source1:        MyGUI-Demos
# Another helper for the tools
Source2:        MyGUI-Tools
# Demo and tools resources configuration
Source3:        resources.xml
# LayoutEditor desktop entry
Source4:        mygui-layouteditor.desktop
# Fix multilib and flags with cmake
Patch0:         mygui_multilib_cflags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake, autoconf, libtool, freetype-devel, desktop-file-utils
BuildRequires:  ois-devel, ogre-devel, doxygen, graphviz, cmake, dos2unix
%if 0%{?fedora} < 12
BuildRequires:  e2fsprogs-devel
%else
BuildRequires:  libuuid-devel
%endif

Requires:       dejavu-sans-fonts


%description
MyGUI is a GUI library for Ogre Rendering Engine which aims to be fast, 
flexible and simple in using. 

%package        devel
Summary:        Development files for MyGUI
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig, ois-devel, ogre-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        devel-doc
Summary:        Development documentation for MyGUI
Group:          Development/Libraries
BuildArch:      noarch

%description    devel-doc
The %{name}-devel-doc package contains reference documentation for
developing applications that use %{name}.


%package demos
Summary:        MyGUI demo executables and media
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description demos
This package contains the compiled (not the source) sample applications coming
with MyGUI.  It also contains some media (meshes, textures,...) needed by these
samples. The samples are installed in %{_libdir}/MYGUI/Demos, and an helper
script MyGUI-Demos is provided and installed in %{_bindir}.


%package tools
Summary:        MyGUI tools 
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains the MyGUI tools, installed in %{_libdir}/MYGUI/Tools. 
LayoutEditor is an application for designing UIs using MyGUI library,
ImageSetViewer and FontViewer are simple tools to preview graphical
resources in the media repository. 
An helper script MyGUI-Tools is provided and installed in %{_bindir}.


%prep
%setup -n MyGUI_%{version}
%patch0 -p0 -b .multilib
# Fix eol 
sed -i 's/\r//' COPYING.LESSER
# Fix non-UTF8 files
for file in Tools/LayoutEditor/Readme.txt ; do
   dos2unix -n $file timestamp && \
   iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp && \
   touch -r timestamp $file && \
   rm timestamp
done
# Generate README for -tools and -demos
cat > Tools/README << EOT
This package contains the MyGUI tools: ImageSetViewer, FontViewer 
and LayoutEditor; to run the tools, launch the helper script
%{_bindir}/MyGUI-Tools
EOT
cat > Demos/README << EOT
This package contains MyGUI demos; to run the demos, launch the
helper script %{_bindir}/MyGUI-Demos
EOT


%build
# Plugins are windows only atm
%cmake . \
   -DMYGUI_INSTALL_PDB:INTERNAL=FALSE -DCMAKE_BUILD_TYPE:STRING=Release \
   -DMYGUI_BUILD_PLUGINS:BOOL=OFF -DCMAKE_CXX_FLAGS_RELEASE= \
   -DCMAKE_SKIP_RPATH:BOOL=ON
make %{?_smp_mflags}
# Generate doxygen documentation
pushd Docs
doxygen
rm -f html/installdox
popd


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# install missing headers
mkdir -p %{buildroot}/%{_includedir}/MyGUI/
install -Dp -m 644 MyGUIEngine/include/*Alloc*.h %{buildroot}/%{_includedir}/MyGUI/
install -Dp -m 644 Platforms/Ogre/OgrePlatform/include/* %{buildroot}/%{_includedir}/MyGUI/

# Remove any archive
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# Remove binaries installed in %%{_bindir}
rm -rf %{buildroot}/%{_bindir}/

# Create config for ldconfig
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/MYGUI" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf 

# Install the samples 
mkdir -p %{buildroot}%{_libdir}/MYGUI/Demos 
cp -p %{SOURCE3} bin/plugins.cfg %{buildroot}%{_libdir}/MYGUI/Demos
sed -i 's|^PluginFolder=.*$|PluginFolder=%{_libdir}/OGRE|' \
    %{buildroot}%{_libdir}/MYGUI/Demos/plugins.cfg
sed -i 's|^Plugin=RenderSystem_Direct3D9$|#Plugin=RenderSystem_Direct3D9|' \
    %{buildroot}%{_libdir}/MYGUI/Demos/plugins.cfg
for file in bin/Demo_* ; do
  install -Dp -m 755 $file %{buildroot}%{_libdir}/MYGUI/Demos/`basename $file`
done
mkdir -p %{buildroot}%{_bindir}
install -Dp -m 755 %{SOURCE1} %{buildroot}%{_bindir}/

# Install the tools
mkdir -p %{buildroot}%{_libdir}/MYGUI/Tools
cp -p %{SOURCE3} bin/plugins.cfg %{buildroot}%{_libdir}/MYGUI/Tools
sed -i 's|^PluginFolder=.*$|PluginFolder=%{_libdir}/OGRE|' \
    %{buildroot}%{_libdir}/MYGUI/Tools/plugins.cfg
sed -i 's|^Plugin=RenderSystem_Direct3D9$|#Plugin=RenderSystem_Direct3D9|' \
    %{buildroot}%{_libdir}/MYGUI/Tools/plugins.cfg
for file in bin/LayoutEditor bin/ImageSetViewer bin/FontViewer ; do
  install -Dp -m 755 $file %{buildroot}%{_libdir}/MYGUI/Tools/`basename $file`
done
install -Dp -m 755 %{SOURCE2} %{buildroot}%{_bindir}/

# Install desktop entry for LayoutEditor
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE4}

# Copy Media files
mkdir -p %{buildroot}%{_datadir}/MyGUI/
cp -a Media %{buildroot}%{_datadir}/MyGUI/

# Install libMyGUI.OgrePlatform.so
mkdir -p %{buildroot}%{_libdir}/MYGUI
install -Dp -m 755 %{_lib}/libMyGUI.OgrePlatform.so %{buildroot}%{_libdir}/MYGUI/

# Move plugins to %{libdir}/MYGUI (no plugins atm)
#mv %{buildroot}%{_libdir}/libPlugin*.so %{buildroot}%{_libdir}/MYGUI

# Strip away code in media dir
#rm -rf %{buildroot}%{_datadir}/MyGUI/Media/Tools/LayoutEditor/CodeTemplates/
# Strip away unittests media 
rm -rf %{buildroot}%{_datadir}/MyGUI/Media/UnitTests

# Remove CMake stuff from Media
rm -f %{buildroot}%{_datadir}/MyGUI/Media/CMakeLists.txt

# Link fonts from dejavu package
ln -fs %{_datadir}/fonts/dejavu/DejaVuSans.ttf \
  %{buildroot}%{_datadir}/MyGUI/Media/MyGUI_Media/DejaVuSans.ttf
ln -fs %{_datadir}/fonts/dejavu/DejaVuSans-ExtraLight.ttf \
  %{buildroot}%{_datadir}/MyGUI/Media/MyGUI_Media/DejaVuSans-ExtraLight.ttf


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING.LESSER
%{_libdir}/*.so.*
%{_libdir}/MYGUI
%dir %{_datadir}/MyGUI/Media
%{_datadir}/MyGUI/Media/Common
%{_datadir}/MyGUI/Media/MyGUI_Media
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/* 


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%files devel-doc
%defattr(-,root,root,-)
%doc Docs/html


%files demos
%defattr(-,root,root,-)
%doc Demos/README
%{_bindir}/MyGUI-Demos
%{_libdir}/MYGUI/Demos
%{_datadir}/MyGUI/Media/Demos
%{_datadir}/MyGUI/Media/Wrapper


%files tools
%defattr(-,root,root,-)
%doc Tools/README Tools/LayoutEditor/Readme.txt
%{_bindir}/MyGUI-Tools
%{_libdir}/MYGUI/Tools
%{_datadir}/MyGUI/Media/Tools
%{_datadir}/applications/mygui-layouteditor.desktop


%changelog
* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.2.0-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.2.0-3
- Rebuild for Boost-1.53.0

* Wed Dec 26 2012 Kevin Fenzi <kevin@scrye.com> 3.2.0-2
- Rebuild for new libCommon

* Tue Dec 04 2012 Bruno Wolff III <bruno@wolff.to> - 3.2.0-1
- Update to upstream 3.2.0
- Changelog: http://redmine.mygui.info/repositories/entry/mygui/tags/MyGUI3.2/ChangeLog.txt

* Fri Aug 10 2012 Bruno Wolff III <bruno@wolff.to> - 3.0.1-16
- Rebuild for boost 1.50

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 04 2012 Bruno Wolff III <bruno@wolff.to> - 3.0.1-14
- Rebuild for ogre 1.7.4

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-13
- Rebuilt for c++ ABI breakage

* Tue Jan 17 2012 Bruno Wolff III <bruno@wolff.to> - 3.0.1-12
- Rebuild for ois 1.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-10
- Rebuild for boost soname bump

* Fri Jul 22 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-9
- Rebuild for boost 1.47

* Sun May 15 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-8
- Rebuild for ogre 1.7.3

* Mon May 02 2011 Kevin Fenzi <kevin@scrye.com> - 3.0.1-7
- Fix pc file issues. Fixes bug #693352

* Wed Apr 06 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-6
- Rebuild for boost soname bump to 1.46.1 in rawhide.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.0.1-4
- rebuild for new boost

* Sat Jan 08 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-3
- Clean up a few more rpmlint warnings

* Sat Jan 08 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-2
- Try to fix rpath issue

* Fri Jan 07 2011 Bruno Wolff III <bruno@wolff.to> - 3.0.1-1
- Update to 3.0.1 release
- Rebuild for ogre update

* Fri Nov 27 2009 Guido Grazioli <guido.grazioli@gmail.com> - 3.0.0-0.4.2332svn
- Install OGRE platform headers

* Wed Nov 18 2009 Guido Grazioli <guido.grazioli@gmail.com> - 3.0.0-0.3.2332svn
- Fix macros usage
- Fix Release tag
- Add desktop entry for LayoutEditor
- Update patch to fix missing undefined non-weak symbols
- Improve summaries and descriptions
- Remove redundant VERBOSE flag
- Add graphviz BR to generate doxygen graphs

* Fri Oct 30 2009 Guido Grazioli <guido.grazioli@gmail.com> - 3.0.0-2.2332svn
- Fix includes dir
- Remove plugin

* Fri Oct 23 2009 Guido Grazioli <guido.grazioli@gmail.com> - 3.0.0-1.2332svn
- Upstream to svn revision 2332
- Patch cmake build scripts to support multilib
- Fix package summaries
- Fix changelog
- Fix %%doc
- Add Require: ogre-devel to -devel subpackage
- Add -devel-doc subpackage
- Revert source tarball from xz to bzip2

* Sat Oct 03 2009 Guido Grazioli <guido.grazioli@gmail.com> - 2.3.0-4.1861svn
- Add BR: rpm >= 4.6.1-2 needed for F-10 builds (BZ #514480)

* Thu Oct 01 2009 Guido Grazioli <guido.grazioli@gmail.com> - 2.3.0-3.1861svn
- Improve package summary
- Provide scripts to run MyGUI tools

* Wed Sep 30 2009 Guido Grazioli <guido.grazioli@gmail.com> - 2.3.0-2.1861svn
- Add BR: libuuid-devel instead of BR: e2fsprogs-devel for F12+
- Fix License

* Tue Sep 29 2009 Guido Grazioli <guido.grazioli@gmail.com> - 2.3.0-1.1861svn
- Rename from libmygui to mygui
- Symlink fonts in media dir to dejavu-sans-fonts ones
- Add doxygen generated docs to -devel
- Provide a generic script to setup and run demos 
- Fix rpmlint warnings

* Mon Sep 28 2009 Guido Grazioli <guido.grazioli@gmail.com> - 2.3.0-0.1861svn
- Initial packaging
