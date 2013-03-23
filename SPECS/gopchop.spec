Name:		gopchop
Version:		1.1.8
Release:		2
License:		GPLv2+
Summary:		MPEG2 GOP-accurate editor
Url:			http://outflux.net/software/pkgs/gopchop
Group:		Productivity/Multimedia/Video/Editors and Convertors
BuildRoot:	%{_tmppath}/%{name}-root
Source:		http://outflux.net/software/pkgs/gopchop/download/%{name}-%{version}.tar.gz
Requires:		gtk2 >= 2.0.0
Requires:		mpeg2dec >= 0.4.1
Requires:		libxml2 >= 2.6.6
#BuildRequires:	mpeg2dec-devel = 0.4.0
BuildRequires:	gettext libmpeg2-devel perl-XML-Parser make autoconf automake gcc gcc-c++
BuildRequires:	gtk2-devel >= 2.0.0 intltool gettext
BuildRequires:	libxml2-devel >= 2.6.6

%description
This tool is used for people wanting to take sections out of MPEG2-PS 
files without re-encoding the resulting frames.  The idea is to write 
specific "Group of Pictures" (GOP) sections to a new MPEG2-PS file.  These 
GOPs will decode correctly (in theory), and the gaps won't be noticed.  I 
wrote this tool to edit commercials out of MPEG2 files produced by my 
KFir MPEG2 capture card.  Using this tool for anything else is really beyond
the scope of its design.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog README TODO INSTALL ABOUT-NLS
%doc %{_mandir}/man1/*

%{_bindir}/*
%{_datadir}/locale/*/*/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*

%changelog
* Wed Jan 6 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.8-2
- Imported http://ftp.halifax.rwth-aachen.de/packman/suse/11.1/SRPMS/gopchop-1.1.7-0.pm.1.src.rpm
- Update to version 1.1.8
- Reformat spec. Change revision enumeration.
- Add %%{?_smp_mflags}
- Delete excessive configure and make parameters, replace by macroses.
- License from GPL changed to GPLv2+
- Add ABOUT-NLS doc.
- Add BR intltool and gettext
- Add handling i18n properly.
- Correctt %%defattr.

* Sat Jan 12 2008 - Andrea Florio <andrea@links2linux.de>
- removed mpeg2dec-devel and added libmped2-devel like BuildRequires
- spec changed with packman standards
- fixed group
* Sun Mar 21 2004 Weston Schmidt <schmidtw@users.sourceforge.net> 1.1.3-1
- Added the libxml2 requirement and build requirement.
* Sun Feb 29 2004 Weston Schmidt <schmidtw@users.sourceforge.net> 1.1.2-1
- Added the automatic menu and updated the requirements and build requirements
* Mon Feb 23 2004 Kees Cook <mpeg2@outflux.net> 1.1.2-1
- Fixed build/make/install section
* Fri Feb 13 2004 Kees Cook <mpeg2@outflux.net> 1.1.2-1
- Updated to get built by configure
* Mon Dec 12 2003 Olivier Lahaye <lahaye@noos.fr> 0.9.1-1
- First RPM release.
