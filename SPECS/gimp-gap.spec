Version: 2.7.0

%global GITrev e75bd46

%global gapmajorver %(echo %version | sed 's|\\..*||g')
%global gapminorver %(echo %version | sed 's|^%{gapmajorver}\\.||g;s|\\..*||g')
%global gapmicrover %(echo %version | sed 's|^%{gapmajorver}\\.%{gapminorver}\\.||g;s|\\..*||g')
%global gimplibdir %(pkg-config gimp-2.0 --variable=gimplibdir)
%global gimpdatadir %(pkg-config gimp-2.0 --variable=gimpdatadir)

Summary:		The GIMP Animation Package
Name:		gimp-gap
Release:		1%{?GITrev:.GIT%{GITrev}}
Group:		Applications/Multimedia
License:		GPLv2+
URL:			https://github.com/GNOME/gimp-gap
#Source: ftp://ftp.gimp.org/pub/gimp/plug-ins/v2.6/gap/gimp-gap-%%{version}.tar.bz2
# See script in Source1 to reproduce tarball
Source0:		gimp-gap-%{GITrev}.tar.xz
Source1:		gimp-gap.get.tarball

BuildRequires:	autoconf >= 2.54 automake >= 1.7 intltool >= 0.17
# glib-gettextize >= 2.2.0
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:	gimp-devel >= 2.6.0 sed gimp-devel-tools >= 2.6.0
BuildRequires:	bzip2-devel xvidcore-devel xvidcore
BuildRequires:	ffmpeg-libs ffmpeg-devel
Requires:		gimp >= 2.6.0 xvidcore

# Account new version 1.12
Patch0:		autogen.sh-automake-1.12.patch

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP 2.6 with capabilities to edit and create animations as
sequences of single frames.

%prep
%setup -q -n %{name}

%patch0 -p0 -b .automake-1.12

# Bundled ffmpeg
#? rm -rf extern_libs

%build
./autogen.sh
%configure
# \
#	--disable-ff-libbz2 \
#	--disable-ff-libmp3lame \
#	--disable-ff-libfaac \
#	--disable-ff-libfaad \
#	--disable-ff-libx264 \
#	--disable-ff-libxvid

#make %%{?_smp_mflags} LIBS="$LIBS -lm"
# Parralel build terminated with error
make LIBS="$LIBS -lm"

%install
%make_install

%find_lang gimp20-gap

%files -f gimp20-gap.lang
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{gimplibdir}/plug-ins/*
%{_libdir}/gimp-gap-%gapmajorver.%gapminorver
%{gimpdatadir}/scripts/*
%{gimpdatadir}/video_encoder_presets
%{_datadir}/locale/*/*/*

%changelog
* Tue Apr 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-1.GITe75bd46
- Import http://forums.fedoraforum.org/attachment.php?attachmentid=20693&d=12975115122C ( http://forums.fedoraforum.org/showthread.php?t=182414 )

* Thu Feb 10 2011 Oliver Mangold <o.mangold@gmail.com>
- updated to version 2.6.0

* Wed Apr 14 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.0
- initial build

