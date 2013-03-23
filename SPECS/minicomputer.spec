Name:		minicomputer
Version:	1.3
Release:	3%{?dist}
Summary:	Software Synthesizer
Group:		Applications/Multimedia
License:	GPLv3+
URL:		http://minicomputer.sourceforge.net/
Source0:	http://downloads.sourceforge.net/minicomputer/MinicomputerV%{version}.tar.gz
Source1:	%{name}.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	alsa-lib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	fltk-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	liblo-devel
BuildRequires:	scons

Requires:	hicolor-icon-theme

%description
Minicomputer is a standalone Linux softwaresynthesizer for creating 
experimental electronic sounds as its often used in but not limited to
Industrial music, IDM, EBM, Glitch, sound design and minimal electronic. It is
monophonic but can produce up to 8 different sounds at the same time. It uses
Jack as realtime audio infrastructure and can be controlled via Midi.

%prep
%setup -q -n MinicomputerV%{version}

# Fix optflags
# SSE instruction set, which provides improved functionality, is only available in these archs:
%ifnarch %{ix86} x86_64 ia64
sed -i "s|\(^env.Append(CCFLAGS =\).*|\1 ['%{optflags}'.split() ])|" SConstruct
%else
sed -i "s|\(^env.Append(CCFLAGS =\).*|\1 ['%{optflags}'.split(),'-msse','-mfpmath=sse' ])|" SConstruct
%endif
sed -i "s|\(^guienv.Append(CPPFLAGS =\).*|\1 ['%{optflags}'.split() ])|" SConstruct

%build
scons %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -pm 755 %{name}{,CPU} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install				\
--dir=%{buildroot}%{_datadir}/applications	\
%{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm 644 %{name}.xpm \
	%{buildroot}%{_datadir}/icons/hicolor/32x32/apps

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README doc/*
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm

%changelog
* Sat Apr 25 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3-3
- Cleanup the compiler flags

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3-2
- Disable SSE on unsupported architectures

* Tue Mar 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.3-1
- Initial build
