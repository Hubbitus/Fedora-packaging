Name:           cw
Version:        1.0.15
Release:        %mkrel 3
Epoch:          0
Summary:        Non-intrusive real-time ANSI color wrapper for common Unix-based commands
License:        GPL
Group:          Development/Other
URL:            http://cwrapper.sourceforge.net/
Source0:        http://cwrapper.sourceforge.net/cw-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
cw is a non-intrusive real-time ANSI color wrapper for common Unix-based
commands on GNU/linux. cw is designed to simulate the environment of the
commands being executed, so that if a person types 'du', 'df', 'ping',
etc. in their shell it will automatically color the output in real-time
according to a definition file containing the color format desired. cw
has support for wildcard match coloring, tokenized coloring,
headers/footers, case scenario coloring, command line dependent
definition coloring, and includes over 50 pre-made definition files.

%prep
%setup -q
%{__perl} -pi -e 's/ -o 0 -g 0//g' Makefile.in
%{__perl} -pi -e 's|/usr/local/lib|%{_datadir}|g' README

%build
%{configure2_5x}
%{make} LIBDIR=%{_datadir}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{make} install PREFIX=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_datadir} MANDIR=%{buildroot}%{_mandir}
%{__rm} %{buildroot}%{_bindir}/cwe
%{__ln_s} cw %{buildroot}%{_bindir}/cwe

%{__perl} -pi -e 's|CWLIB=.*|CWLIB="%{_datadir}/%{name}"|g' %{buildroot}%{_bindir}/colorcfg
%{__perl} -pi -e 's|%{buildroot}||g' %{buildroot}%{_datadir}/%{name}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES CONTRIB COPYING cw.lsm FILES INSTALL MD5SUM PLATFORM README VERSION doc
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*


%changelog
* Sat Jul 11 2009 Pavel Alexeev <Pahan@Hubbitus.info>
- Imported from ftp://ftp.rediris.es/volumes/vol3/carroll.cac.psu.edu/mandrakelinux/devel/cooker/SRPMS/contrib/release/cw-1.0.15-3mdv2009.0.src.rpm


* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 0:1.0.15-3mdv2009.0
+ Revision: 243841
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Oct 11 2007 David Walluck <walluck@mandriva.org> 0:1.0.15-1mdv2008.1
+ Revision: 97052
- add sources
- 1.0.15
- replace build patch with work in %%install
- fix cwe symlink


* Sat Nov 04 2006 David Walluck <walluck@mandriva.org> 1.0.14-3mdv2007.0
+ Revision: 76460
- update build patch
- birthday rebuild
- Import cw

* Tue Sep 27 2005 David Walluck <walluck@mandriva.org> 0:1.0.14-1mdk
- release

