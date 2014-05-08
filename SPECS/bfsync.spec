%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:               bfsync
Version:            0.3.6
Release:            1
Summary:            File Synchronization Tool
Source:             http://space.twc.de/~stefan/bfsync/bfsync-%{version}.tar.bz2
URL:                http://space.twc.de/~stefan/bfsync.php
License:            GPLv3
BuildRequires:      python-devel
BuildRequires:      python-setuptools
BuildRequires:      fuse-devel
BuildRequires:      glib2-devel
BuildRequires:      libdb-cxx-devel
BuildRequires:      swig
BuildRequires:      boost-devel
BuildRequires:      pyliblzma

%description
Bfsync is a file-synchronization tool which allows to keep a collection of big
files synchronized on many machines. To do this, bfsync maintains a global and
local history of changes; every time the file collection is changed on one
machine, an entry in the local history is made. Bfsync allows to automatically
merge this local history with the global history where possible, and offers
manual conflict resolution in cases where this is not possible.

Due to history synchronization, each bfsync checkout knows precisely which
files are part of the file collection. Therefore, it can determine which file
contents (data blobs with SHA1 contents) are present in a checked out repo, and
which are missing. The user can transfer file contents between repos using
bfsync get/put, so that after transfer, the checkouts will be complete
(containing both: the history and the file contents required).

To sum it up, bfsync behaves not unlike version control systems like git or
svn, however it behaves reasonable when the file collection is big (like
hundreds of gigabytes).

The main interface to bfsync is a FuSE filesystem, so it is possible to manage
your data with a file manager or copy new data into the repository using rsync.
As soon as you "commit" the changes, they are entered into the local history
and if you "push/pull" the changes, they become part of the global history.
There is no need to transfer all new data to a central server during
"push/pull". Only the history needs to be transferred, the contents of the
files can be exchanged between different machines without need for a central
server (although you can have a central server containing all data if its
practical for you).

%prep
%setup -q

%build
%configure --disable-silent-rules
# remove Rpath - http://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} CXXFLAGS="$CXXFLAGS -ldb_cxx"

%install
%make_install

rm "%{buildroot}%{_libdir}"/*.a
rm "%{buildroot}%{_libdir}"/*.la
rm "%{buildroot}%{_libdir}"/*.so

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS README TODO
%{_bindir}/bfsync
%{_bindir}/bfsyncfs
%{_bindir}/bfsyncca
%{_libdir}/libbfsync.so.0
%{_libdir}/libbfsync.so.0.*
%{_mandir}/man1/bfsync.1*
%{_mandir}/man1/bfsyncfs.1*
%{python_sitearch}/_%{name}db.so
%{python_sitearch}/%{name}db.py*
%{python_sitearch}/%{name}db-*egg-info/
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-py*.egg-info/

%changelog
* Wed May 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.6-1
- Import ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/filesystems/SLE_11_SP2/src/bfsync-0.2.0-3.5.src.rpm and rework.
- Update to 0.3.6 version.
- Drop patches.
- Drop Source99: bfsync-rpmlintrc
- Remove rpath.
- Adjust dependencies.

* Mon May  7 2012 jeffm@suse.com
- bfsync needs unistd.h

* Sat Dec 24 2011 pascal.bleser@opensuse.org
- initial version (0.2.0)
