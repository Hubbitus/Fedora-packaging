Name:           remmina-plugin-teamviewer
Version:        1.0.0.2
Release:        1%{?dist}
Summary:        Remmina protocol plugin to open a RDP connection with TeamViewer

License:        GPLv2+
URL:            http://www.muflone.com/remmina-plugin-rdesktop/
Source0:        http://www.muflone.com/resources/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
# 1.0.0-12 introduce %%{_includedir}/remmina/* files for build plugins outside remmina source tree
BuildRequires:  remmina-devel >= 1.0.0-12
Requires:       remmina
Requires:       hicolor-icon-theme

%description
Remmina Plugin TeamViewer is a free software protocol plugin to establish
connections using TeamViewer, a remote control application with many
features and capable of connecting even through NAT, both for Windows,
Linux and others operating systems.

It require proprietary TeamViewer software! As it is in Fedora it is not listed
in dep, so you must install it separately!

%prep
%setup -q -c
# See instructions in comments %%{_includedir}/remmina/pluginBuild-CMakeLists.txt
ln -s %{_includedir}/remmina/config.h.in .
ln -s %{_includedir}/remmina/pluginBuild-CMakeLists.txt CMakeLists.txt

mkdir remmina-plugin-to-build
mv %{name}-%{version}/* remmina-plugin-to-build/
rm -rf %{name}-%{version}

%build
%{cmake} .
make %{?_smp_mflags}


%install
%make_install

%post
touch --no-create %{_datadir}/icons/hicolor
  if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi

%postun
touch --no-create %{_datadir}/icons/hicolor
  if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi

%files
%doc remmina-plugin-to-build/LICENSE remmina-plugin-to-build/README.md
%{_libdir}/remmina/plugins/%{name}.so
%{_datadir}/icons/hicolor/16x16/emblems/remmina-teamviewer.png
%{_datadir}/icons/hicolor/22x22/emblems/remmina-teamviewer.png

%changelog
* Tue Aug 12 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0.2-1
- Initial spec
