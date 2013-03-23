Name:		sqlite3-dbf
Version:		2011.01.24
Release:		1%{?dist}
Summary:		Converter of XBase / FoxPro tables to SQLite

Group:		Applications/Text
License:		GPLv3+
URL:			http://sqlite.mobigroup.ru/wiki?name=sqlite3-dbf
Source0:		http://mobigroup.ru/debian/pool-squeeze/main/s/sqlite3-dbf/%{name}_%{version}.tar.gz
# Still need for EL5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:		sqlite

%description
SQLiteDBF converts XBase databases, particularly FoxPro tables with memo files,
into a SQL dump. It has no dependencies other than standard Unix libraries.

SQLiteDBF is designed to be incredibly fast and as efficient as possible.

This use code base of the PgDBF project (http://pgdbf.sourceforge.net/).

%prep
%setup -q


%build
gcc %{optflags} -o %{name} %{name}.c

%install
rm -rf %{buildroot}

install -D %{name} %{buildroot}/usr/bin/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc README LICENSE

%changelog
* Mon Jan 24 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2011.01.24-1
- Initial spec.