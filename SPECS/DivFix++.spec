# Copyright (c) 2006-2008 oc2pus
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments to toni@links2linux.de

# norootforbuild

Name:		DivFix++
Summary:		A program to repair broken AVI file streams by rebuilding index part of file
Version:		0.30
Release:		3%{?dist}
License:		GPLv2+
Group:		Applications/Multimedia
URL:			http://divfixpp.sourceforge.net/
Source0:		http://downloads.sourceforge.net/divfixpp/%{name}_v%{version}-src.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	dos2unix
BuildRequires:	pkgconfig
BuildRequires:	wxGTK-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

%description
This program designed to repair broken AVI file streams by
rebuilding index part of file. This is very useful when trying
to preview movies which has no index part, like some files are
currently downloading from ed2k or bittorent networks.

DivFix++ has supports CLI tools, this means you can fix, preview
and delete movies automatically via script (by using argument
parameters...)

DivFix++ program code supports lots of operating system, because
it's writen by cross-platform API, wxWidgets.

%prep
%setup -q -n %{name}_v%{version}
sed -i.flags -e 's|-Os||' makefile

dos2unix		docs/*
%{__chmod}	644	docs/*

%build
#make %{?_smp_mflags} WXCONFIG=wx-config
# Correct handle build flags
make %{?_smp_mflags} WXCONFIG=wx-config CPP="g++ %{optflags}"

%install
rm -rf %{buildroot}

%{__install} -p -dm 755 %{buildroot}%{_bindir}
%{__install} -p -m 755 %{name} \
	%{buildroot}%{_bindir}

for i in cs_CZ hu ja tr; do
	%{__install} -p -dm 755 %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES
	%{__install} -p -m 644 locale/$i/DivFix++.mo \
		%{buildroot}%{_datadir}/locale/$i/LC_MESSAGES
done

# icon and menu-entry
%{__install} -p -dm 755 %{buildroot}%{_datadir}/pixmaps
%{__install} -p -m 644 resources/%{name}.png \
	%{buildroot}%{_datadir}/pixmaps

%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Comment=A program to repair broken AVI file streams by rebuilding index part of file
Name=%{name}
GenericName=
Type=Application
Exec=%{name}
Icon=%{name}
Encoding=UTF-8
Categories=Video;
EOF

desktop-file-install --delete-original \
	--dir=%{buildroot}/%{_datadir}/applications	\
	--mode 0644							\
	%{name}.desktop


%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc docs/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Fri Oct 10 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.30-3
- Remove '--vendor="%%{distribution}"' from installation desktop file. (Mamoru Tasaka)
	And accordingly change filename
		%%{_datadir}/applications/%%{distribution}-%%{name}.desktop
		to
		%%{_datadir}/applications/%%{name}.desktop
- Add string "Category=Video;" into desktop file and accordingly remove '--add-category="Video"'
	from desktop-file-install command. (Mamoru Tasaka)

* Thu Oct 9 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.30-2
- Correct SourceURL0 (Mamoru Tasaka)
- Correct build flags (Mamoru Tasaka: https://bugzilla.redhat.com/show_bug.cgi?id=458338#c4)
- Put desktop-file in category Video.

* Wed Oct 8 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.30-1
- All chenges made by review of Mamoru Tasaka. Thanks to him.
- Remove hand %%define _prefix
- Replace %%__make %%{?jobs:-j%%{jobs}} to make %%{?_smp_mflags}
- %%distname replaced by %%{distribution}
- Source expanded to full url.
- Correct BuildRoot: %%{_tmppath}/%%{name}-%%{version}-build to %%{_tmppath}/%%{name}-%%{version}-%%{release}-root-%%(%%{__id_u} -n)
- In each install command add -p flag to preserve timestamps.
- In clean section "[ -d %%{buildroot} -a "%%{buildroot}" != "" ] && %%__rm -rf %%{buildroot}" replaced by simple:
	rm -rf %%{buildroot}
- All $RPM_BUILD_ROOT replaced by %%{buildroot}
- %%defattr(-,root,root) changed to %%defattr(-,root,root,-)
- Remove extension .png from Icon in .desktop file

* Thu Aug 7 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.30-0
- Import from Suse: http://packman.links2linux.org/downloadsource/64219/DivFix++-0.30-0.pm.1.src.rpm
- Remove all conditions with %%suse_version
- Replace %%suse_update_desktop_file -i %%{name} AudioVideo AudioVideoEditing to invoke desktop-file-install
- Add BuildRequires:	desktop-file-utils
- Remove BuildRequires:	update-desktop-files, mDNSResponder-lib
- BR wxWidgets-devel replaced by wxGTK-devel
- Delete BuildRequires:	gcc-c++ (http://fedoraproject.org/wiki/Packaging/Guidelines#Exceptions)
- Group changed to Applications/Multimedia
- License adjusted to GPLv2+ (was GPL) according of source files.
- Remove %%debug_package
- Add BR gettext

* Sat Jun 21 2008 Toni Graffy <toni@links2linux.de> - 0.30-0.pm.1
- update to 0.29
* Fri Sep 07 2007 Toni Graffy <toni@links2linux.de> - 0.29-0.pm.2
- openSUSE-10.3 build with wxGTK
* Sun Apr 01 2007 Toni Graffy <toni@links2linux.de> - 0.29-0.pm.1
- update to 0.29
* Sun Mar 04 2007 Toni Graffy <toni@links2linux.de> - 0.28-0.pm.1
- update to 0.28
* Fri Dec 29 2006 Toni Graffy <toni@links2linux.de> - 0.27-0.pm.1
- update to 0.27
* Wed Nov 29 2006 Toni Graffy <toni@links2linux.de> - 0.26-0.pm.1
- initial release of rpm
