Summary:		DVD authoring program with nice and clean GUI
Name:		bombono-dvd
Version:		0.5.2
Release:		1%{?dist}
License:		GPLv2+
Group:		Applications/Multimedia
URL:			http://www.bombono.org/
Source0:		http://downloads.sourceforge.net/bombono/%{name}-%{version}.tar.bz2
BuildRequires:	boost-devel gtk2-devel gtkmm24-devel GraphicsMagick-c++-devel
BuildRequires:	mjpegtools-devel libdvdread-devel
BuildRequires:	glibc >= 2.10.1 libxml++-devel libstdc++ >= 4.4.1 libxml++-devel
Requires:		hicolor-icon-theme dvdauthor scons twolame mjpegtools dvd+rw-tools
# http://sourceforge.net/apps/trac/bombono/ticket/19
Patch0:		bombono-dvd-0.5.2-twolame_pass.diff

%description
Bombono DVD is easy to use program for making DVD-Video.
The main features of Bombono DVD are:
 * excellent MPEG viewer: Timeline and Monitor
 * real WYSIWYG Menu Editor with live thumbnails
 * comfortable Drag-N-Drop support
 * you can author to folder, make ISO-image or burn directly to DVD
 * reauthoring: you can import video from DVD discs.

%prep
%setup -q

%patch0 -p1 -b .twolame

# spurious permissions
chmod 0644 COPYING
chmod 0755 resources/scons_authoring/menu_SConscript

# Remove bundled libs:
# find libs/ -not -name SConscript -not -name libs -exec rm -r {} \; || :
#rm -rf libs/{boost-lib,mpeg2dec}

%build
scons PREFIX=%{_prefix} USE_EXT_BOOST=1

%install
rm -rf %{buildroot}

scons PREFIX=%{_prefix} DESTDIR=%{buildroot} install

desktop-file-install \
	--add-category="AudioVideo" \
	--delete-original \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

# install icons
install -Dm 0644 resources/icons/%{name}_16px.png %{buildroot}%{_datadir}/icons/hicolor/16x16/%{name}.png
install -Dm 0644 resources/icons/%{name}_32px.png %{buildroot}%{_datadir}/icons/hicolor/32x32/%{name}.png
install -Dm 0644 resources/icons/%{name}_48px.png %{buildroot}%{_datadir}/icons/hicolor/48x48/%{name}.png
install -Dm 0644 resources/icons/%{name}_64px.png %{buildroot}%{_datadir}/icons/hicolor/64x64/%{name}.png
install -Dm 0644 resources/icons/%{name}_128px.png %{buildroot}%{_datadir}/icons/hicolor/128x128/%{name}.png

%clean
rm -rf %{buildroot}

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
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/mpeg2demux
%{_datadir}/bombono
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/%{name}.png
%{_datadir}/icons/hicolor/32x32/%{name}.png
%{_datadir}/icons/hicolor/48x48/%{name}.png
%{_datadir}/icons/hicolor/64x64/%{name}.png
%{_datadir}/icons/hicolor/128x128/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%doc README COPYING

%changelog
* Tue Dec 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.2-1
- Imported (primarly description) from:
	ftp://ftp.is.co.za/mirror/pclinuxos.com/apt/pclinuxos/2007/SRPMS.extra/bombono-dvd-0.5.2-1pclos2010.src.rpm
	and fully remade.

