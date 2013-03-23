Name:		printoxx
Version:		1.8.1
Release:		2%{?dist}
Summary:		Print image files

Group:		Applications/Multimedia
License:		GPLv2
URL:			http://kornelix.squarespace.com/%{name}/
Source0:		http://kornelix.squarespace.com/storage/downloads/%{name}-%{version}.tar.gz
Source1:		%{name}.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gtk2-devel
BuildRequires:	desktop-file-utils
Requires:		cups

# Bugtracker not found. Patch e-mailed to maintainer.
Patch0:		printoxx-1.8.1.constchar.patch

%description
Printoxx is a free open source Linux program for printing one or more image
files with a user-defined page layout. Images can be added to a layout page
using the mouse to select and drop. Images can be moved around and resized
using the mouse. Adding text (titles, notes) works the same way.
Any available font can be used. 

%prep
%setup -q -n %{name}

%patch0 -p1 -b .constchar

# To use "fedora" CFLAGS (exported)
sed -i -e "s/CFLAGS =/CFLAGS +=/" Makefile


%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
make %{?_smp_mflags} PREFIX=%{_prefix} DOCDIR=%{_docdir}/%{name}-%{version}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} DOCDIR=%{_docdir}/%{name}-%{version}
install -Dm 644 -p data/icons/%{name}.png  $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png
desktop-file-install --vendor="" \
  --mode 644 \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
  %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*
%dir %{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}/%{name}.xtext
%{_datadir}/%{name}/icons/
%{_datadir}/%{name}/locales/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Tue Feb 24 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.8.1-2
- Step to version 1.8.1
- Adjust Source0 url.
- Reformat header of spec with tabs.
- Add Patch0: printoxx-1.8.1.constchar.patch to build on gcc 4.4

* Sun Jan  4 2009  Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.8-1
- Rebuild for 1.8
* Thu Dec  4 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.7-2
- Include unowned /usr/share/printoxx/locales directory.
* Mon Dec  1 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.7-1
- Rebuild for 1.7
* Mon Oct 13 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.6-4
- Better management of documentation
* Sun Oct 12 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.6-3
- Desktop file ameliorations
- Doc files are now reachable
* Mon Oct  6 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.6-2
- add escape char in prep section
* Sun Oct  5 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.6-1
- Rebuild for 1.6
* Sat Sep 27 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.5-1
- Rebuild for 1.5
* Thu Sep 18 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.4-1
- Rebuild for 1.4
* Mon Sep  8 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.3.1-1
- Rebuild for 1.3.1
* Wed Sep  3 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.2-1
- Rebuild for 1.2
* Tue Sep  2 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.1-2
- Added desktop file support
* Mon Sep  1 2008 Nicoleau Fabien <nicoleau.fabien@gmail.com> - 1.1-1
- Initital build
