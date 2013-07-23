%global vers 1.19-rc5

Summary:		Mail Retrieval Proxy
Name:		perdition
Version:		1.19
Release:		rc5.0.4%{?dist}
License:		GPLv2+
Group:		Applications/Internet
URL:			http://horms.net/projects/perdition/
Source:		http://horms.net/projects/%{name}/download/%{vers}/perdition-%{vers}.tar.bz2
# My systemd service template
Source1:		%{name}-template.service
BuildRequires:	automake autoconf libtool vanessa_logger-devel >= 0.0.10
BuildRequires:	vanessa_adt-devel >= 0.0.6 vanessa_socket-devel >= 0.0.7
BuildRequires:	gdbm-devel mysql-devel postgresql-devel openldap-devel
BuildRequires:	popt-devel pam-devel zlib-devel openssl-devel ghostscript
BuildRequires:	tetex-latex tetex-dvips libtiff unixODBC-devel tinycdb-devel
BuildRequires:	libidn-devel libdb-devel
Requires:		vanessa_logger >= 0.0.10 vanessa_adt >= 0.0.6 vanessa_socket >= 0.0.7
Requires:		initscripts
#???
Patch0:		perdition-1.19-rc5-const-version.patch
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
Perdition is a fully featured POP3 and IMAP4 proxy server. It is able to
handle both SSL and non-SSL connections and redirect users to a
real-server based on a database lookup. Perdition supports modular based
database access. ODBC, MySQL, PostgreSQL, GDBM, POSIX Regular Expression
and NIS modules ship with the distribution. The API for modules is open
allowing arbitrary modules to be written to allow access to any data store.

Perdition can be used to: Create large mail systems where a users mailbox
may be stored on one of several hosts.  Integrate different mail systems
together. Migrate between different email infrastructure. And in firewall
applications.

%package	bdb
Summary:	Library to allow perdition to access Berkely DB based pop maps
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description bdb
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
database to be sourced from a Berkely DB.


%package	cdb
Summary:	Library to allow perdition to access Constant DB based pop maps
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description cdb
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
database to be sourced from a Constant DB.

%package	ldap
Summary:	Library to allow perdition to access LDAP based pop maps
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description ldap
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
database to be sourced from LDAP.


%package	mysql
Summary:	Library to allow perdition to access MySQL based pop maps
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description mysql
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
database stored in a MySQL database.


%package	postgresql
Summary:	Library to allow perdition to access PostgreSQL based pop maps
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description postgresql
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
database stored in a PostgreSQL database.


%package	odbc
Summary:	Library to allow perdition to access pop maps via ODBC
Group:	Applications/Internet
License:	GPLv2+
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	unixODBC

%description odbc
Perdition allows for arbitrary user database access through shared
libraries much in the manner of NSS in glibc. This package allows a user
access databases via ODBC.


%package	sysvinit
Summary:	Legacy SysV initscripts for %{name}
Group:	System Environment/Daemons

%description sysvinit
Legacy SysV initscripts for init mechanisms such as upstart
which do not support the systemd unit file format.


%prep
%setup -q -n %{name}-%{vers}

%patch0 -p1 -b .const

%build
CFLAGS="${CFLAGS:-%optflags} -I/usr/kerberos/include" ; export CFLAGS
if [ -f configure.in ]; then
	aclocal
	libtoolize --force --copy
	automake --add-missing
	autoheader
	autoconf
fi
%configure %{_target_platform} \
	--with-ldap-schema-directory=%{_sysconfdir}/openldap/schema \
	--enable-shared

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}{%{_initrddir},%{_sysconfdir}/sysconfig}

make DESTDIR=%{buildroot} install-strip

install -m755 ./%{_initrddir}/%{name}.rh %{buildroot}%{_initrddir}/%{name}
install -m644 ./%{_sysconfdir}/sysconfig/%{name} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Do not start by default
sed '/Default-Start/a# chkconfig:         - 95 05/' -i %{buildroot}%{_sysconfdir}/sysconfig/%{name}

	for service in pop3 pop3s imap4 imap4s managesieve; do
	sed "s/{name}/$service/g;s/{NAME}/$(echo $service | tr '[a-z]' '[A-Z]')/g" %{SOURCE1} > %{name}-$service.service
	install -Dm 600 %{name}-$service.service %{buildroot}/%{_unitdir}/%{name}-$service.service
	done

rm -f %{buildroot}%{_libdir}/*.{a,la,so}

%clean

%post
/sbin/ldconfig
%systemd_post %{name}-pop3.service
%systemd_post %{name}-pop3s.service
%systemd_post %{name}-imap4.service
%systemd_post %{name}-imap4s.service
%systemd_post %{name}-managesieve.service

%post sysvinit
/sbin/chkconfig --add %{name}

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}-pop3.service
%systemd_postun_with_restart %{name}-pop3s.service
%systemd_postun_with_restart %{name}-imap4.service
%systemd_postun_with_restart %{name}-imap4s.service
%systemd_postun_with_restart %{name}-managesieve.service

%preun
%systemd_preun %{name}-pop3.service
%systemd_preun %{name}-pop3s.service
%systemd_preun %{name}-imap4.service
%systemd_preun %{name}-imap4s.service
%systemd_preun %{name}-managesieve.service

%preun sysvinit
if [ $1 = 0 ]; then
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
fi

%post bdb -p /sbin/ldconfig
%postun bdb -p /sbin/ldconfig

%post cdb -p /sbin/ldconfig
%postun cdb -p /sbin/ldconfig

%post ldap -p /sbin/ldconfig
%postun ldap -p /sbin/ldconfig

%post mysql -p /sbin/ldconfig
%postun mysql -p /sbin/ldconfig

%post postgresql -p /sbin/ldconfig
%postun postgresql -p /sbin/ldconfig

%post odbc -p /sbin/ldconfig
%postun odbc -p /sbin/ldconfig


%files
%doc README AUTHORS COPYING ChangeLog NEWS TODO
%{_sbindir}/%{name}
%{_sbindir}/%{name}.pop3
%{_sbindir}/%{name}.pop3s
%{_sbindir}/%{name}.imap4
%{_sbindir}/%{name}.imap4s
%{_sbindir}/%{name}.imaps
%{_sbindir}/%{name}.managesieve
#% {_libdir}/libjain.so.0
#% {_libdir}/libjain.so.0.0.0
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}
%{_mandir}/man8/%{name}.*
%{_mandir}/man5/%{name}db.*

# nis map
%{_libdir}/lib%{name}db_nis.so.0
%{_libdir}/lib%{name}db_nis.so.0.0.0

# posix_regex map
%{_libdir}/lib%{name}db_posix_regex.so.0
%{_libdir}/lib%{name}db_posix_regex.so.0.0.0
%config(noreplace) %{_sysconfdir}/%{name}/popmap.re

# gdbm map
%{_libdir}/lib%{name}db_gdbm.so.0
%{_libdir}/lib%{name}db_gdbm.so.0.0.0
%{_bindir}/makegdbm
%config(noreplace) %{_sysconfdir}/%{name}/Makefile
%config(noreplace) %{_sysconfdir}/%{name}/Makefile.popmap
%{_mandir}/man1/makegdbm.*
%config(noreplace) %{_sysconfdir}/%{name}/popmap

# daemon map
%{_libdir}/lib%{name}db_daemon.so.0
%{_libdir}/lib%{name}db_daemon.so.0.0.0

%{_libdir}/lib%{name}db_daemon_base.so.0
%{_libdir}/lib%{name}db_daemon_base.so.0.0.0

%{_unitdir}/%{name}-pop3.service
%{_unitdir}/%{name}-pop3s.service
%{_unitdir}/%{name}-imap4.service
%{_unitdir}/%{name}-imap4s.service
%{_unitdir}/%{name}-managesieve.service

%files sysvinit
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files bdb
%{_libdir}/lib%{name}db_bdb.so.0
%{_libdir}/lib%{name}db_bdb.so.0.0.0
%{_bindir}/makebdb
%{_mandir}/man1/makebdb.*

%files cdb
%{_libdir}/lib%{name}db_cdb.so.0
%{_libdir}/lib%{name}db_cdb.so.0.0.0

%files ldap
%{_libdir}/lib%{name}db_ldap.so.0
%{_libdir}/lib%{name}db_ldap.so.0.0.0
%{_sbindir}/%{name}db_ldap_makedb
%{_mandir}/man8/%{name}db_ldap_makedb.*
%config(noreplace) %{_sysconfdir}/openldap/schema/%{name}.schema

%files mysql
%{_libdir}/lib%{name}db_mysql.so.0
%{_libdir}/lib%{name}db_mysql.so.0.0.0
%{_sbindir}/%{name}db_mysql_makedb
%{_mandir}/man8/%{name}db_mysql_makedb.*

%files postgresql
%{_libdir}/lib%{name}db_postgresql.so.0
%{_libdir}/lib%{name}db_postgresql.so.0.0.0
%{_sbindir}/%{name}db_postgresql_makedb
%{_mandir}/man8/%{name}db_postgresql_makedb.*

%files odbc
%{_libdir}/lib%{name}db_odbc.so.0
%{_libdir}/lib%{name}db_odbc.so.0.0.0
%{_sbindir}/%{name}db_odbc_makedb
%{_mandir}/man8/%{name}db_odbc_makedb.*

%changelog
* Wed Jul 24 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.19-rc5.0.4
- For comments thanks Michael Schwendt in review (bz#518317):
- Macros %%systemd_requires expanded in plain requires to do not break build for f19.
- Own %%{_sysconfdir}/%%{name}
- Fix old changelog dates.

* Sun Jul 21 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.19-rc5.0.3
- Add %%{?_smp_mflags} to make.
- Remove rpath.
- Changes by Christopher Meng comments in review bz#518317:
- Drop El5 support, remove related legacy stuff like BuildRoot, explicit %%defattrs and cleanups.
- "Macroisation" deal wich systemd services (http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Macroized_scriptlets_.28Fedora_18.2B.29).

* Mon Mar 25 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 1.19-rc5.0.2
- Add patch0 - perdition-1.19-rc5-const-version.patch to build against new Fedora version of gdbm.
- Make add requirements arch-dependant by adding %%{?_isa} (thanks to Mario Blättermann).

* Mon Jul 9 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.19-rc5.0.1
- Update to version 1.19-rc5.
- Adjust URLs.
- Include cdb support.
- Delete devel subpackage.

* Mon Aug 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.17.1-4
- Historical ./configure with huge amount parameters replaced by %%configure macro.
- Removed unnecessary requires /sbin/ldconfig.
- Removed the files README,COPYING from all subpackages.

* Sun Aug 23 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.17.1-3
- Fix typo in condition (confgure.in instead of configure.in) (thanks to Andrew Colin Kissa)
- Add --add-missing flag to automake command and put it before autoheader.

* Tue Aug 18 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.17.1-2
- Ressurect http://hubbitus.net.ru/rpm/Fedora9/perdition/perdition-1.17.1-1.fc8.Hu.1.src.rpm.
- Rename spec to standard form.
- Remove Hu-part from release.
- Remove unneded comments and defines.
- $RPM_BUILD_ROOT replaced by %%{buildroot}.
- All %%defattr(-,root,root) turned to %%defattr(-,root,root,-).
- File BR /usr/include/db.h replaced by db4-devel.
- Remove unversioned explicid provides like perdition-*-%%{version}-%%{release}.
- Make setup quiet.
- Remove from %%files each .a and .la files.
- Add Requires(postun): /sbin/ldconfig, Requires(post): /sbin/ldconfig, and %%post/%%postun ldconfig invoke.
- Modify service add/delete commands.
- Exclude all unversioned devel files *.so
- Add COPYING, README also in %%doc in all packages.
- Add (noreplace) specification into %%config.
- Direct /etc/ replace by %%{_sysconfdir}.
- %%{_sysconfdir}/rc.d/init.d replace by %%{_initrddir}.
- make install-strip replaced by just install.
- Replace direct usage of perdition by %%{name}.
- License adjusted from just GPL to GPLv2+ accordingly README.
- Removee all %%{buildroot}%%{_libdir}/*.{a,la,so} files in %%install.
- Add ldconfig %%post/%%postun scripts into all subpackages: bdb, ldap, odbc, mysql, postgresql

* Tue Jan 1 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 1.17.1-1
- Add files into RPM (which are build, but not included):
	%%{_libdir}/libperditiondb_daemon_base.a
	%%{_libdir}/libperditiondb_daemon_base.la
	%%{_libdir}/libperditiondb_daemon_base.so
	%%{_libdir}/libperditiondb_daemon_base.so.0
	%%{_libdir}/libperditiondb_daemon_base.so.0.0.0

* Mon Dec 31 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 1.17.1
- Imported from ftp://ftp.ntua.gr/pub/linux/openpkg/contrib/perdition-1.15-20050121.src.rpm
- Remove difine %%ver. Replace all entry of it by %%version
- Remove difine %%rel. Replace all entry of it by %%release
- Replace all tags Copyright by License
- Change BuildRoot:	to correct (intead of hardcoded path): %%{_tmppath}/%%{name}-%%{version}-%%{release}-root-%%(%%{__id_u} -n)
- Reformat all by tabs
- Change from Release:	1 to Release:	%%{rel}%%{?dist}.Hu.0
- Remove (comment out) #-Hu Docdir:	%%{prefix}/doc

* Mon Mar  1 2004 Horms <horms@verge.net.au>
- Set localstatedir to /var

* Wed Oct 30 2002 Horms <horms@verge.net.au>
- Fixed BDB mess!

* Sun Mar 31 2002 Horms <horms@verge.net.au>
- added BDB

* Tue Mar 26 2002 Horms <horms@verge.net.au>
- added ODBC

* Sat Dec 29 2001 Horms <horms@verge.net.au>
- Forked SuSE (lsb) spec file

* Fri Dec 14 2001 Horms <horms@verge.net.au>
- Revamped configure to use %%{_libdir} and friends. This should be more
  distribution indepentant. With thanks to Scot W. Hetzel <scot@genroco.com>

* Wed Apr 18 2001 Horms <horms@verge.net.au>
- Broke MySQL, PostgreSQL and LDAP back out into separate packages

* Wed Apr 18 2001 Horms <horms@verge.net.au>
- Merged db packages into main package

* Mon Nov 27 2000 Horms <horms@verge.net.au>
- Modified to reflect build process handling instalation of config files
- Split GDBM and Posix_Regex into separate packages

* Mon Oct 16 2000 Horms <horms@verge.net.au>
- added NIS library

* Mon May 15 2000 Horms <horms@verge.net.au>
- added sysconfig file
- split libraries into separate packages so that packages such
  as postgress and mysql don't have to be installed for perdition
  to install cleanly.
- added sample ldap server configuration

* Thu May  4 2000 Horms <horms@verge.net.au>
- added perditiondb_ldap files
- added missing perditiondb_postgresql devel files

* Thu Apr 20 2000 Horms <horms@verge.net.au>
- added perditiondb_postgresql files

* Tue Jan  4 2000 Horms <horms@verge.net.au>
- added libraries
- added headers
- made devel package
- made libtcp_socket and libtcp_socket-devel package
- Included mysql and posix_regex stuff in /etc

* Mon Nov 29 1999 Horms <horms@verge.net.au>
- Added perdition.conf

* Sat Sep 18 1999 Horms <horms@verge.net.au>
- updated for 0.1.0

* Sat May 29 1999 Horms <horms@verge.net.au>
- inital release
