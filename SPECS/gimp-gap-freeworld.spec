Version: 2.7.0

# review request: https://bugzilla.redhat.com/show_bug.cgi?id=954108

%global GITrev e75bd46

%global gapmajorver %(echo %version | sed 's|\\..*||g')
%global gapminorver %(echo %version | sed 's|^%{gapmajorver}\\.||g;s|\\..*||g')
%global gapmicrover %(echo %version | sed 's|^%{gapmajorver}\\.%{gapminorver}\\.||g;s|\\..*||g')
%global gimplibdir %(pkg-config gimp-2.0 --variable=gimplibdir)
%global gimpdatadir %(pkg-config gimp-2.0 --variable=gimpdatadir)

Summary:		The GIMP Animation Package for freeworld with AVI support
Name:		gimp-gap-freeworld
Release:		9%{?GITrev:.GIT%{GITrev}}%{?dist}
Group:		Applications/Multimedia
License:		GPLv2+
URL:			https://github.com/GNOME/gimp-gap
#Source: ftp://ftp.gimp.org/pub/gimp/plug-ins/v2.6/gap/gimp-gap-%%{version}.tar.bz2
# See script in Source1 to reproduce tarball
Source0:		gimp-gap-%{GITrev}.tar.xz
Source1:		gimp-gap.get.tarball

BuildRequires:	autoconf >= 2.54, automake >= 1.7, intltool >= 0.17
BuildRequires:	pkgconfig(gimp-2.0), gimp-devel-tools >= 2.6.0
BuildRequires:	bzip2-devel, glib2-devel >= 2.2.0, libjpeg-turbo-devel, yasm
BuildRequires:	SDL-devel

Requires:		gimp >= 2.6.0

Provides:		gimp-gap = %{version}-%{release}
Obsoletes:	gimp-gap < %{version}-%{release}

# Account new version 1.12: https://bugzilla.gnome.org/show_bug.cgi?id=699207
Patch0:		gimp-gap-2.7-autogen.sh-automake-1.14.patch

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP with capabilities to edit and create animations as
sequences of single frames.

Gimp-gap package already in Fedora: https://apps.fedoraproject.org/packages/gimp-gap
Unfortunately there was few issues like bundled ffmpeg and disabled libavformat
support because of patents.

For countries where law not permit software patents this package suggested as
more reach by functionality.

Please note, there no pirate or stolen parts!

%prep
%setup -q -n gimp-gap

%patch0 -p0 -b .automake-1.14

# Bundled libs (list from SUSE)
#?rm -rf extern_libs vid_enc_avi vid_enc_ffmpeg gap/gap_mpege.c gap/gap_mpege.h \
#?    libgapvidapi/gap_vid_api_ffmpeg.c libgapvidapi/gap_vid_api_mpeg3.c \
#?    libgapvidapi/gap_vid_api_mpeg3toc.c

# 1 symbol only not in UTF-8. iso8859-1 encoding is my guess
iconv -f iso8859-1 -t utf8 ChangeLog > ChangeLog.tmp
touch -r ChangeLog ChangeLog.tmp
mv -f ChangeLog.tmp ChangeLog

# Try make rpmlint happy
find \( -iname '*.c' -or -iname '*.h' \) -exec chmod -x {} \;
find -type d -exec chmod 0755 {} \;

%build

# Disable call ./configure from autogen.sh because we want it with default configured parameters
sed -i 's@$srcdir/configure@#$srcdir/configure@' autogen.sh
./autogen.sh
%configure

#Hu HACK
sed -is 's/#define restrict restrict/#define restrict __restrict__/' extern_libs/ffmpeg/config.h
# Parralel build terminated with error
make LIBS="$LIBS -lm" CFLAGS="${CFLAGS//-Werror=format-security} -I%{_includedir}/SDL/ "

%install
%make_install

%find_lang gimp20-gap

%files -f gimp20-gap.lang
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{gimplibdir}/plug-ins/*
%{_libdir}/gimp-gap-%gapmajorver.%gapminorver
%{gimpdatadir}/scripts/*
%{gimpdatadir}/video_encoder_presets

%changelog
* Thu Mar 05 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-9.GITe75bd46
- Introduce gimp-gap-freeworld (by Alex request https://github.com/Hubbitus/Fedora-packaging/issues/2), version with few changes:
	o UNOFFICIAL build without --disable-libavformat option, add BR yasm, SDL-devel.
	o Disable -Werror=format-security gcc option, hack restrict keyword for bundled ffmpeg compilation.
	o Add %%{gimpdatadir}/video_encoder_presets
- Adjust patch gimp-gap-2.7-autogen.sh-automake-1.12.patch to automake-1.14 version.
- Add gimp-gap Provides/Obsoletes

* Mon Nov 4 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-8.GITe75bd46
- Review in progress (bz#954108), for comments thanks to Mario Blättermann.
- Filled bug about incorrect FSF address - https://bugzilla.gnome.org/show_bug.cgi?id=711402
- Encode Changelog into UTF-8.
- Make rpmlint for debuginfo happy by drop executable permissions from source files and chmod directories to 0755.

* Sun Nov 3 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-7.GITe75bd46
- Change BR "gimp-devel >= 2.6.0" on "pkgconfig(gimp-2.0)", remove sed. Thanks to Mario Blättermann (review bz#954108).

* Thu May 2 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-6.GITe75bd46
- Disable call of ./configure script from autogen.sh as excessive and run it manually via macros (Michael Schwendt insist).

* Tue Apr 30 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-5.GITe75bd46
- Remove xvidcore from requires. Thanks to Vasiliy Glazov.

* Mon Apr 29 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-4.GITe75bd46
- Add %%{?dist} tag. Thanks to Vasiliy Glazov.
- Try avoid second reconfigure by passing argument in autoden.sh. Thanks to Antonio Trande.

* Mon Apr 29 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.7.0-3.GITe75bd46
- For changes thanks to Antonio Trande and their comments in Fedora review (bz#954108).
- Remove BR xvidcore-devel xvidcore (its is not required and does not present in Fedora).
- Remove %%{_datadir}/locale/*/*/*
- Remade gimp-gap-2.7-autogen.sh-automake-1.12.patch to account automake-1.13 also.
- Add BR libjpeg-turbo-devel

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

