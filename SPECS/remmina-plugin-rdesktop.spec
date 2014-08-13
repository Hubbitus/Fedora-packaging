Name:           remmina-plugin-rdesktop
Version:        1.0.0.3
Release:        1%{?dist}
Summary:        Remmina protocol plugin to open a RDP connection with rdesktop

License:        GPLv2+
URL:            http://www.muflone.com/remmina-plugin-rdesktop/
Source0:        http://www.muflone.com/resources/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.8
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
# 1.0.0-12 introduce %%{_includedir}/remmina/* files for build plugins outside remmina source tree
BuildRequires:  remmina-devel >= 1.0.0-12
Requires:       remmina
Requires:       rdesktop
Requires:       hicolor-icon-theme

%description
Remmina Plugin RDesktop is a free software protocol plugin to establish a
RDP connection using RDesktop which sometimes performs better than the
FreeRDP integrated plugin in Remmina and also provides a lot of features
like clipboard sync, remote folders support, remote audio,
seamless RDP and various settings for performances.


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
%{_datadir}/icons/hicolor/16x16/emblems/remmina-rdesktop.png
%{_datadir}/icons/hicolor/22x22/emblems/remmina-rdesktop.png

%changelog
* Mon Jul 21 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0.3-1
- Initial spec
