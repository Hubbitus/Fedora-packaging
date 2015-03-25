Name:           sachesi
Version:        2.0.0
Release:        0.rc.1%{?dist}
Summary:        Firmware, extractor, searcher and installer for Blackberry 10

License:        GPLv3
URL:            https://github.com/xsacha/Sachesi
Source0:        https://github.com/xsacha/Sachesi/archive/2.0.0rc.tar.gz
Source1:        %{name}.desktop

BuildRequires:  openssl-devel, lzo-minilzo, libusb-devel, quazip-devel
BuildRequires:  qt5-qtquick1-devel, qt5-qtdeclarative-devel
# For i18n - lrelease
BuildRequires:  qt5-qttools-devel
# libudev.so
BuildRequires:  systemd-devel
Requires:       qt5-qtquickcontrols
Requires:       hicolor-icon-theme

BuildRequires:  desktop-file-utils

%description
Sachesi allows you to extract, search for and (un)install Blackberry
firmware. It also allows you to backup, restore, wipe, reboot and nuke.
This is a continued evolution of the original Sachup and Sachibar
applications. None of its activities require development mode. That is,
you can sideload and uninstall applications without developer mode.

The application mimics communications performed by official Blackberry
tools and allows modification of the typically fixed commands that are
sent from the computer. This allows increased control and flexibility
over firmware related activies on your device.

Developed by Sacha Refshauge. Project originally known as Dingleberry.
Public release of source code on May 26, 2014.


%prep
%setup -q -n Sachesi-2.0.0rc
sed -i 's/.qm/.ts/g' translations.qrc
sed -i 's/LREL_TOOL = lrelease/LREL_TOOL = lrelease-qt5/' Sachesi.pro

# Remove bundled libs
#? rm -rf ext
#? sed -i 's/INCLUDEPATH += ext src/INCLUDEPATH += src/' Sachesi.pro

%build
%_qt5_qmake -recursive

make %{?_smp_mflags}


%install
install -Dm 0755 Sachesi %{buildroot}%{_bindir}/%{name}
install -D -p -m 644 assets/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

desktop-file-install --mode 644 --dir %{buildroot}%{_datadir}/applications/ %{SOURCE1}

# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#desktop-database
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  update-mime-database %{_datadir}/mime &> /dev/null || :
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Mar 25 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 2.0.0-0.rc.1
- Initial spec (by https://www.linkedin.com/groupItem?view=&gid=49737&item=5982643028257501187&type=member&commentID=discussion%3A5982643028257501187%3Agroup%3A49737&trk=hb_ntf_COMMENTED_ON_GROUP_DISCUSSION_YOU_COMMENTED_ON#commentID_discussion%3A5982643028257501187%3Agroup%3A49737).
