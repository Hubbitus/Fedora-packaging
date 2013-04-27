Version: 2.7.0

%global GITrev e75bd46

%global gapmajorver %(echo %version | sed 's|\\..*||g')
%global gapminorver %(echo %version | sed 's|^%{gapmajorver}\\.||g;s|\\..*||g')
%global gapmicrover %(echo %version | sed 's|^%{gapmajorver}\\.%{gapminorver}\\.||g;s|\\..*||g')
%global gimplibdir %(pkg-config gimp-2.0 --variable=gimplibdir)
%global gimpdatadir %(pkg-config gimp-2.0 --variable=gimpdatadir)

Summary:		The GIMP Animation Package
Name:		gimp-gap
Release:		2%{?GITrev:.GIT%{GITrev}}
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

Requires:		gimp >= 2.6.0 xvidcore

# Account new version 1.12
Patch0:		autogen.sh-automake-1.12.patch
# Unbundle libs. Fedora-specific patch, borrowed from SUSE.
Patch1:		gimp-gap-2.7-unbandle.patch

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP with capabilities to edit and create animations as
sequences of single frames.

%prep
%setup -q -n %{name}

%patch0 -p0 -b .automake-1.12
%patch1 -p1 -b .unbundle

# Bundled libs (list from SUSE)
rm -rf extern_libs vid_enc_avi vid_enc_ffmpeg gap/gap_mpege.c gap/gap_mpege.h \
    libgapvidapi/gap_vid_api_ffmpeg.c libgapvidapi/gap_vid_api_mpeg3.c \
    libgapvidapi/gap_vid_api_mpeg3toc.c


%build
./autogen.sh
%configure --disable-libavformat

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
%{_datadir}/locale/*/*/*

%changelog
* Sat Apr 20 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-2.GITe75bd46
- Remove BuildRequires: ffmpeg-libs ffmpeg-devel
- Borrow from SUSE Patch1: gimp-gap-2.7-unbandle.patch (rebased)
- Remove bundled libs in prep.
- Add --disable-libavformat configure option.
- As ffmpeg not required anymore and there no legal issues it ready for Fedora now.

* Tue Apr 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-1.GITe75bd46
- Import http://forums.fedoraforum.org/attachment.php?attachmentid=20693&d=12975115122C ( http://forums.fedoraforum.org/showthread.php?t=182414 )

* Thu Feb 10 2011 Oliver Mangold <o.mangold@gmail.com>
- updated to version 2.6.0

* Wed Apr 14 2004 Nils Philippsen <nphilipp@redhat.com>
- version 2.0.0
- initial build

