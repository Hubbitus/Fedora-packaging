Summary:        Inline data deduplicating filesystem
Name:           lessfs
Version:        1.0.0
Release:        4%{?dist}
License:        GPLv3+
Group:          Applications/System
URL:            http://www.lessfs.com
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

# LessFS ships with an init script missing a reload and status paramter
## Patch has been sent back upstream
Patch0: lessfs-init.patch

# LessFS appears to attempt to use lib_qlz in the build process even when the 
# file are missing, this patch removes those bits form the make process
Patch1: lessfs-1.0.0-remove_make_qlz.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  tokyocabinet-devel 
BuildRequires:  openssl-devel
BuildRequires:  fuse-devel
BuildRequires:  autoconf
BuildRequires:  lzo-devel

Requires:   fuse

%description
Filesystem for FUSE that allows for high performance inline data de-duplication 
using tokyocabinet for the database.

%prep
%setup -q

# Fix permissions on ChangeLog
chmod -x ChangeLog

# Fix permissions on README files
chmod -x README*

# For some reason a couple source files are executable.
chmod -x *.c

# Remove libqlz.{c,}
rm lib_qlz.{c,h}

# patch for build without lib_qlz
%patch1

# patch for init script
cd etc/
%patch0

%build
autoconf
%configure --with-crypto --with-sha3 --with-lzo
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# install SYSV init stuff
mkdir -p %{buildroot}/%{_initddir}
install -m755 etc/lessfs %{buildroot}/%{_initddir}/lessfs

install -D -m 644 etc/lessfs.cfg %{buildroot}/%{_sysconfdir}/lessfs.cfg

#Removing unnecessary files, only file located in this directory is the man page
rm -rf %{buildroot}%{_datadir}/%{name}

rm -rf %{buildroot}%{_libdir}/lib%{name}.a


%clean
rm -rf %{buildroot}

%post
# Register the lessfs service
/sbin/chkconfig --add lessfs

%preun
if [ $1 = 0 ]; then
    /sbin/service lessfs stop > /dev/null 2>&1
    /sbin/chkconfig --del lessfs
fi 


%files
%defattr(-, root, root, -)
#Exclude INSTALL and COPYING as they are symlinks to nothing
%doc FAQ ChangeLog README copying README.* authors
%{_bindir}/lessfs
%{_sbindir}/lessfsck
%{_sbindir}/defrag_lessfs
%{_sbindir}/mklessfs
%{_sbindir}/listdb
%{_mandir}/man1/lessfs*
%{_initddir}/lessfs
%config(noreplace) %{_sysconfdir}/lessfs.cfg

%changelog
* Tue Jan 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-4
- Changed perms on README files that were executable for some reason
- Removed un-needed quicklz source files
- Fixed rpmlint complaints about spaces/tabs

* Thu Jan 14 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-3
- Fixed lz issue

* Wed Jan 13 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-2
- Switching to LZO for compression to solve bundled library issues.

* Mon Jan 04 2010 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-1
- New version from upstream
- Worked with upstream to fix some package review issues. Still need to work on
  getting rid of bundled libraries.

* Mon Dec 21 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.9.5-1
- New version from upstream
- Added README.*, authors and copying (full GPLv3 license) to docs
- fixed macros in files
- Added comment for patch0
- Fixed permissions on README.crypto


* Thu Dec 17 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.9.4-1
- Upgrade to latest version of lessfs (fixed atime/ctime/mtime timestamp bugs)

* Thu Dec 10 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.9.0-1
- Upgraded to latest version of lessfs

* Thu Nov 19 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.3-3
- Fixed tab/space mixing issue in spec

* Tue Nov 17 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.3-2
- Added patch to include a status directive for the init script
- Changed permissions on the ChangeLog
- Got rid of dangling symlinks in docs dir


* Mon Nov 16 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.3-1
- New upstream release.
- Fixed 'lessfs.i686: E: executable-marked-as-config-file /etc/lessfs.cfg'
- Fixed 'W: name-repeated-in-summary Lessfs'

* Sun Nov 15 2009 Mark Ruijter <mruijter@gmail.com> - 0.8.3
- Fixes a major bug in the truncation code.
- This bug will crash lessfs when used with ccrypt or rsync –inplace.

* Mon Nov 09 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.2-1
- New upstream release, relevent changes in upstream changelog listed below

* Mon Nov 09 2009 Mark Ruijter <mruijter@gmail.com> - 0.8.2
- Fixes a bug that causes lessfsck and mklessfs to segfault when compiled
- with encryption support and encryption disabled in the config.
- Fixes a bug that causes lessfs to segfault on umount when compiled
- with encryption support and encryption disabled in the config.
- lessfsck,listdb and mklessfs are now installed in /usr/sbin
- instead of /usr/bin.


* Mon Nov 09 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.1-1
- New release from upstream.
- Fixed CFLAGS to use Fedora defaults
- Fixed lack of chkconfig addition and removal
- No shared libraries, so removed ldconfig
- Removed static reference to lessfs man page to allow for compression change.

* Sat Nov 07 2009 Mark Ruijter <mruijter@gmail.com> - 0.8.1
- Fixes a bug that causes mklessfs to segfault when DEBUG is not set.
- Adds lessfsck. lessfsck can be used  to check, optimize and repair 
- a lessfs filesystem.

* Wed Oct 28 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-2
- enabled --with-sha3 flag in ./configure to offer performance increase as per
  upstream recommendation.

* Wed Oct 28 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-1
- New release from upstream
- Changes config file to config(noreplace) so we don't overwrite user's
  modifications/customizations.

* Mon Oct 26 2009 Mark Ruijter <mruijter@gmail.com> - 0.8.0
- Fixes a possible segfault when lessfs is used with lzo compression.
- Fixes a problem when compiling lessfs without encryption on
- a system without openssl-devel.
- Enhances the logging facility.
- Performance has improved for higher latency storage like iscsi, drbd.
- Reduces the number of fsync operations when sync_relax>0.
- 
- Thanks to : Roland Kletzing for finding and assisting
- with solving some of the problems mentioned.

* Fri Oct 22 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.7.5-4
- Fixed missing URL field as well as missing Require for fuse
- Removed period from summary 

* Thu Oct 22 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.7.5-3
  -Added fuse-devel and autoconf as build dependencies

* Wed Oct 21 2009 Adam Miller <maxamillion@fedoraproject.org> - 0.7.5-2
  -First attempt to build for Fedora review request
  -Based on upstream .spec, full credit of initial work goes to Mark Ruijter

* Fri Oct 16 2009 Mark Ruijter <mruijter@lessfs.com> - 0.7.5-1
  Fix a segfault on free after unmounting lessfs without
  encryption support. Fix a problem that could lead to a
  deadlock when using file_io with NFS.
  A performance improvement, changed a mutex lock for a
  spinlock.
* Sun Oct 11 2009 Mark Ruijter <mruijter@lessfs.com> - 0.7.4
  This version of lessfs introduces a new hash named
  Blue Midnight Whish : http://www.q2s.ntnu.no/sha3_nist_competition/start
  This is a very fast hash that increases lessfs performance
  significantly. The implementation makes it easy to use any
  of the hashes from the NIST hash competition. MBW was 
  choosen for lessfs because of the speed.
  To use BMW : configure --with-sha3
* Tue Oct 06 2009 Mark Ruijter <mruijter@lessfs.com> - 0.7.2
  Fix a typo in lib_tc.c that can lead to data corruption.
* Mon Oct 05 2009 Mark Ruijter <mruijter@lessfs.com> - 0.7.1
  Introduced a new data storage backend, file-io.
  Higher overall performance.
* Sun Sep 06 2009 Mark Ruijter <mruijter@lessfs.com> - 0.6.1
  Never improve your code minutes before releasing it.
  Fix a silly bug with mklessfs.
* Sun Sep 06 2009 Mark Ruijter <mruijter@lessfs.com> - 0.6.0
  Added encryption support to lessfs.
  Fixed one small bug that would leave orphaned meta data in the
  metadatabase when hardlinks where removed.
* Wed Aug 26 2009 Mark Ruijter <mruijter@lessfs.com> - 0.5.0
  Improved thread locking that leads to much better performance.
  Many NFS related problems have been solved and debugging
  is now easier.
* Mon Aug 17 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.8
  Many bugfixes, including incorrect filesize on writing
  in a file with various offsets using lseek. This also
  caused problems with NFS.
* Fri Aug 14 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.7
  Fixed a problem where dbstat failed to return the proper
  filesize. One other bug could leak to a deadlock of lessfs.
* Fri Jul 17 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.6
  Fixed two bugs, one which could lead to data corruption.
  One other that would leave deleted data in the database.
* Wed Jul 08 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.5
  This release fixes to one minor and one major bug.
  One bug in the code would actually crash lessfs
  upon renaming a file or directory. lessfs-0.2.4
  is no longer available for download.
* Sun Jul 05 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.4
  Added support for automatic defragmentation.
* Tue Jun 23 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.3
  This release fixes a small memory leak and improves
  write performance in general approx 12%.
  Known issues : 
  Using direct_io with kernel 2.6.30 causes reads to
  continue for ever. I am not sure if this is a kernel
  issue or a lessfs bug. With earlier kernels direct_io
  works fine.
* Sun Jun 21 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.2
  NFS support and improved caching code.
  WARNING : nfs will only work with kernel >= 2.6.30
* Wed Jun 10 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.1
  Improved the performance of writes smaller then 
  max_write in size. These writes will now remain long
  enough in the cache so that subsequent writes to the 
  same block will update the cache instead of the database.
  Mounting lessfs without formatting the filesystem now
  logs a warning instead of creating a segfault.
  Creating of sparse files now works again after being 
  broken in release 0.1.19.
* Mon May 25 2009 Mark Ruijter <mruijter@lessfs.com> - 0.2.0
  Added a cache that improves performance with approx 30%.
* Thu May 14 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.22
  Fixed a data corruption bug (workaround) when the 
  underlying filesystems run out of space. Fixed a problem
  with hardlinking symlinks.
* Wed Apr 22 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.20
  Fixed two bugs:
  1. Truncate operations would sometimes fail.
  2. unlink of hardlinked files would sometimes fail.
* Wed Apr 04 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.19 
  Fixed a bug in the truncation routine where a delete chunk 
  would remain in the database. Cleaned up the init script.
* Mon Mar 30 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.18 
* Mon Mar 27 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.17 
  Bug fix, reenable syslog.
* Mon Mar 27 2009 Mark Ruijter <mruijter@lessfs.com> - 0.1.16
* Mon Mar 23 2009 Mark Ruijter <mruijter@gmail.com>  - 0.1.15
* Sat Mar 21 2009 Mark Ruijter <mruijter@gmail.com>  - 0.1.14
* Tue Feb 24 2009 Mark Ruijter <mruijter@gmail.com>  - 0.1.13
- Initial package
