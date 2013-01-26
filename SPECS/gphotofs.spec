Name:           gphotofs
Version:        0.4.0
Release:        3%{?dist}
License:        GPLv2
Source0:        http://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2
Group:          System Environment/Base
URL:            http://gphoto.sourceforge.net
Summary:        User Level File System for gphoto-Based Cameras
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  fuse-devel >= 2.6
BuildRequires:  glib2-devel >= 2.6 
BuildRequires:  gphoto2-devel >= 2.1 
BuildRequires:  libjpeg-devel 
BuildRequires:  libexif-devel
Requires:       libgphoto2 >= 2.1 fuse-libs >= 2.6 glib2 >= 2.6

%description
This package provides a fuse module to make digital cameras supported
by libgphoto2 visible as a file system.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure     \
  --prefix=%{_prefix}                   \
  --libdir=%{_libdir} 
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} mandir=%{_mandir} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_bindir}/%{name}

%changelog
* Wed Aug 1 2012 Pavel Alexeev <Pahan@Hubbitus.info> 0.4.0-3
- Import from http://orion.lcg.ufrj.br/RPMS/SPECS/gphotofs.spec

* Wed Nov 14 2007 Paulo Roma <roma@lcg.ufrj.br> 0.4.0-2
- Rebuilt for Fedora 8.
- Added BR gphoto2-devel.

* Sat Nov 04 2007 Paulo Roma <roma@lcg.ufrj.br> 0.4.0-1
- Updated to 0.4.0

* Wed Jan 03 2007 Paulo Roma <roma@lcg.ufrj.br> 0.3-1
- Adapted spec file for Fedora 6

* Mon Sep 04 2006 - meissner@suse.de
- upstream 0.3:
- Command line options to select a specific camera, like gphoto2.

* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires

* Mon Jan 09 2006 - meissner@suse.de
- initial gphotofs import.
