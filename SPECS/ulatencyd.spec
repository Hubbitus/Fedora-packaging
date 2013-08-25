Name:           ulatencyd
Version:        9999
Release:        9.1
Summary:	ulatencyd

Group:          System Environment/Base
License:        GPLv3
Source0:        %{name}-%{version}.tar
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake glib2-devel dbus-glib-devel dbus-python-devel PyQt4 polkit-devel libxcb-devel
BuildRequires:  lua-devel lua-posix doxygen perl-Moose pandoc libcgroup-devel libXau-devel
#BuildRequires:	luajit-devel luajit-static
Requires:       glib2 dbus-glib dbus-python systemd lua lua-posix

%description
Clementine is a modern music player and library organiser.
It is largely a port of Amarok 1.4, with some features rewritten to take
advantage of Qt4.

%prep
%setup -q
mkdir build

%build
cd build
cmake \
	-DLIBCGROUPS=0 \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DENABLE_DBUS=1 \
	-DLUA_JIT=0 \
	..
make %{?_smp_mflags}


%install
cd ../ulatencyd-9999/build
# %ifarch ppc64 s390x x86_64
# sed -i 's/\${CMAKE_INSTALL_PREFIX}\/lib\//\${CMAKE_INSTALL_PREFIX}\/lib64\//g' modules/cmake_install.cmake
# sed -i 's/\${CMAKE_INSTALL_PREFIX}\/lib\//\${CMAKE_INSTALL_PREFIX}\/lib64\//g' src/cmake_install.cmake
# %endif
sed -i 's/\${CMAKE_INSTALL_PREFIX}\/doc\//\${CMAKE_INSTALL_PREFIX}\/share\/doc\//g' docs/cmake_install.cmake
sed -i 's/\/usr\/man\//\/usr\/share\/man\//g' docs/cmake_install.cmake
make DESTDIR=%{buildroot} install

%clean
cd build
make clean

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.quamquam.ulatencyd.conf
%config(noreplace) %{_sysconfdir}/ulatencyd/*.conf
%config(noreplace) %{_sysconfdir}/ulatencyd/simple.d/*.conf
%config(noreplace) %{_sysconfdir}/ulatencyd/scheduler/*.lua
%config(noreplace) %{_sysconfdir}/ulatencyd/rules/*.lua
/lib/systemd/system/ulatencyd.service
%{_bindir}/run-game
%{_bindir}/run-single-task
%{_bindir}/ulatency
%{_bindir}/ulatency-gui
%{_sbindir}/ulatencyd
%{_libdir}/../lib/ulatencyd/*.lua
%{_libdir}/../lib/ulatencyd/modules/simplerules.so
%{_libdir}/../lib/ulatencyd/modules/xwatch.so
%{_datadir}/man/man1/run-game.1*
%{_datadir}/man/man1/ulatency.1*
%{_datadir}/man/man1/run-single-task.1*
%{_datadir}/man/man1/ulatency-gui.1*
%{_datadir}/man/man8/ulatencyd.8*
%{_datadir}/polkit-1/actions/org.quamquam.ulatencyd.policy

%changelog
* Thu May 03 2011 Anonymous
- Initial package
