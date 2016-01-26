Summary:            Top-like PostgreSQL statistics viewer
Name:               pgcenter
Version:            0.2.0
Release:            1%{?dist}
License:            BSD
Group:              Development/Tools
URL:                https://github.com/lesovsky/pgcenter

Source0:            https://github.com/lesovsky/%{name}/archive/%{version}.tar.gz

BuildRequires:      postgresql-devel ncurses-devel

%description
PostgreSQL provides various statistics which includes information about
tables, indexes, functions and other database objects and their usage.
Moreover, statistics has detailed information about connections, current
queries and database operations (INSERT/DELETE/UPDATE). But most of this
statistics are provided as permanently incremented counters. The pgcenter
provides convenient interface to this statistics and allow viewing statistics
changes in time interval, eg. per second. The pgcenter provides fast access
for database management task, such as editing configuration files, reloading
services, viewing log files and canceling or terminating database backends
(by pid or using state mask). However if need execute some specific
operations, pgcenter can start psql session for this purposes.

%prep
%setup -qn %{name}-%{version}

%build
make %{?_smp_mflags}

%install
%{make_install}

%files
%doc COPYRIGHT README.md
%{_bindir}/%{name}

%changelog
* Mon Jan 25 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.2.0-1
- Import http://testing.yum.kaos.io/SRPMS/repoview/pgcenter.html
- Change BR postgresql94-devel -> postgresql-devel
- Spec cleanup and full rewrite.

* Sat Dec 19 2015 Anton Novojilov <andy@essentialkaos.com> - 0.2.0-0
- Added iostat
- Added nicstat
- pg_stat_statements fixes
- One key shortcut for config editing
- Other fixes and improvements

* Wed Oct 21 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.3-0
- Added pg_stat_statements improvements
- Added query detailed report based on pg_stat_statements
- Added memory system statistics
- Added support for 9.1

* Wed Sep 09 2015 Anton Novojilov <andy@essentialkaos.com> - 0.1.2-0
- Initial build
