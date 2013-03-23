Name:		fotoxx
Version:		8.0
Release:		5%{?dist}
Summary:		Photo editor

Group:		Applications/Multimedia
License:		GPLv2
URL:			http://kornelix.squarespace.com/%{name}
Source0:		http://kornelix.squarespace.com/storage/downloads/%{name}-%{version}.tar.gz
Source1:		%{name}.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gtk2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	freeimage-devel
Requires:		exiv2
Requires:		printoxx

# Presents checked at build time
BuildRequires:	perl-Image-ExifTool ufraw
Requires:		perl-Image-ExifTool ufraw

# No public bugtracker. Sent to author by mail 2009-08-09
Patch0:		fotoxx-8.0-mandir.patch

%description
Fotoxx is a free open source Linux program for editing image files
from a digital camera. The goal of fotoxx is to meet most image editing
needs while remaining easy to use.

%prep
%setup -q
%patch0 -p0 -b .mandir

# To use "fedora" CFLAGS (exported)
sed -i -e "s/CFLAGS =/CFLAGS +=/" Makefile

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; 
make %{?_smp_mflags} PREFIX=%{_prefix}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} DOCDIR=%{_docdir}/%{name}-%{version}
install -Dm 644 -p data/icons/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
desktop-file-install --vendor="" \
	--mode 644 \
	--remove-category="Application" \
	--dir %{buildroot}%{_datadir}/applications/ \
	%{SOURCE1}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*
%doc %{_mandir}/man1/%{name}.1*
%dir %{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}/icons/
%{_datadir}/%{name}/locales/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Sun Aug 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 8.0-5
- Update to version 8.0
- Delete old pathces.
- Remove rm libfreeimage.a, name of dir in %%setup.
- Replace all $RPM_BUILD_ROOT by %%{buildroot}
- Add Patch0: fotoxx-8.0-mandir.patch
- Add new file %%doc %%{_mandir}/man1/%%{name}.1*

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Dennis Gilmore <dennis@ausil.us> - 6.0-3
- add patch to dynamically link to libfreeimage

* Wed Feb 25 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 6.0-2
- Forgot patch

* Wed Feb 25 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 6.0-1
- New version 6.0
- Adjust Source0 url (inspired by Kevin Fenzi in fedora-devel-list: https://www.redhat.com/archives/fedora-devel-list/2009-February/msg01622.html ).

* Wed Feb 25 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 5.8-2
- Add patch0 fotoxx-5.8.constchar.patch
- Reformat spec with tabs, remove trailing spaces.

* Sun Jan  4 2009 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.8-1
- Rebuild for 5.8
* Mon Dec  1 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.7-1
- Rebuild for 5.7
* Sun Nov 16 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.6-1
- Rebuild for 5.6
* Tue Nov  4 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.5-1
- Rebuild for 5.5
* Thu Oct  9 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.4-1
- Rebuild for 5.4
* Thu Sep 18 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.3-1
- Rebuild for 5.3
* Sun Aug 31 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.2-1
- Rebuild for 5.2
* Sun Aug 24 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.1-1
- Rebuild for 5.1
* Fri Aug  8 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.0.1-1
- Rebuild for 5.0.1
* Sat Aug  2 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 5.0-1
- Rebuild for 5.0
* Tue Jul 22 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 4.9-1
- Initial build
