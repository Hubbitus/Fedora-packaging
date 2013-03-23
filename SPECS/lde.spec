Summary:		Console-based disk editor
Name:		lde
Version:		2.6.1
Release:		4%{?dist}
License:		GPLv2
Group:		Applications/System
URL:			http://lde.sourceforge.net/

Source:		http://dl.sf.net/%{name}/%{name}-%{version}.tar.gz
# I suppose it is https://sourceforge.net/tracker/?func=detail&aid=1471701&group_id=20753&atid=120753
Patch0:		lde_staticPatch.patch

# It still required for EPEL5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

# For script grep-inode
Requires:		grep, gawk
BuildRequires:	bison, gpm-devel, ncurses-devel, perl, dos2unix

%description
%{name} is a disk editor for Linux, originally written to help recover
deleted files. It has a simple ncurses interface that resembles an
old version of Norton Disk Edit for DOS.

%prep
%setup -qn %{name}
%patch0 -p1 -b .static

### Make buildsystem use standard autotools directories
perl -pi.orig -e 's|(\$\(mandir\))|$1/man8|' macros/Makefile.in

# Fix spurios permission:
chmod -x src/allfs.h

%build
%configure \
	--disable-schemas-install
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

### FIXME: Makefile doesn't create target directories
install -p -d -m0755 %{buildroot}%{_sbindir} %{buildroot}%{_datadir}/man/man8/
install -p -m0755 crash_recovery/grep-inode %{buildroot}%{_sbindir}/

%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/*.tex doc/UNERASE README src/ChangeLog TODO WARNING
%doc %{_mandir}/man?/*
%attr(0755,root,root) %{_sbindir}/%{name}
%{_sbindir}/grep-inode

%changelog
* Wed Mar 30 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.6.1-4
- Replace all occurances of name by macros %%{name} (Thanks to Mario Blättermann for all hints in this release).
- Added -p flag to install.
- Fix spurios permission on file src/allfs.h.

* Thu Nov 18 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.6.1-3
- Requires gawk instead of awk.

* Mon Nov 15 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.6.1-2
- Initial package, using as init DAG: Dag Wieers <dag@wieers.com>
- Many Fedora-relatede changes ctart from formating...
