Version: 2.7.0

%global gapmajorver %(echo %version | sed 's|\\..*||g')
%global gapminorver %(echo %version | sed 's|^%{gapmajorver}\\.||g;s|\\..*||g')
%global gapmicrover %(echo %version | sed 's|^%{gapmajorver}\\.%{gapminorver}\\.||g;s|\\..*||g')
%global gimplibdir %(pkg-config gimp-2.0 --variable=gimplibdir)
%global gimpdatadir %(pkg-config gimp-2.0 --variable=gimpdatadir)

Summary: The GIMP Animation Package.
Name: gimp-gap
Release: 1
Group: Applications/Multimedia
License: GPL
URL: http://www.gimp.org
#Source: ftp://ftp.gimp.org/pub/gimp/plug-ins/v2.6/gap/gimp-gap-%{version}.tar.bz2
# git clone https://github.com/GNOME/gimp-gap.git
#
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf >= 2.54 automake >= 1.7 glib-gettextize >= 2.2.0 intltool >= 0.17
BuildRequires: gimp-devel >= 2.6.0 sed gimp-devel-tools >= 2.6.0
BuildRequires: bzip2-devel bzip2-libs xvidcore-devel xvidcore
Requires: gimp >= 2.6.0 xvidcore bzip2-libs

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP 2.6 with capabilities to edit and create animations as
sequences of single frames.

%prep
%setup -q

# Bundled ffmpeg
#? rm -rf extern_libs

%build
aclocal
automake
autoconf
%configure \
	--disable-ff-libbz2 \
	--disable-ff-libmp3lame \
	--disable-ff-libfaac \
	--disable-ff-libfaad \
	--disable-ff-libx264 \
	--disable-ff-libxvid

make %{?_smp_mflags} CC="gcc -lm"

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{gimplibdir}/plug-ins/*
%{_libdir}/gimp-gap-%gapmajorver.%gapminorver
%{gimpdatadir}/scripts/*
%{_datadir}/locale/*/*/*

%changelog
* Tue Apr 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.6.0-1
- Import http://forums.fedoraforum.org/attachment.php?attachmentid=20693&d=12975115122C ( http://forums.fedoraforum.org/showthread.php?t=182414 )

* Thu Feb 10 2011 Oliver Mangold <o.mangold@gmail.com>
- updated to version 2.6.0

* Wed Apr 14 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.0
- initial build

