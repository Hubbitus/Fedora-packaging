Name:		xls2csv
Version:		1.06
Release:		5%{?dist}
Summary:		A script that recodes a spreadsheet's charset and saves as CSV

Group:		Applications/Text
License:		GPL+ or Artistic
URL:			http://search.cpan.org/dist/xls2csv/
Source0:		http://search.cpan.org/CPAN/authors/id/K/KE/KEN/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	perl(ExtUtils::Embed) perl(ExtUtils::MakeMaker) perl(Test::Harness)
BuildRequires:	perl(Test::Simple) perl(Unicode::Map)
BuildRequires:	perl perl(Locale::Recode) perl(Text::CSV_XS) perl(Spreadsheet::ParseExcel)
Requires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:		perl(Unicode::Map)

%description
This script will recode a spreadsheet into a different character set
and output the recoded data as a csv file.

The script came about after many headaches from dealing with Excel
spreadsheets from clients that were being received in various character
sets.


%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{_prefix}"
%{__make} OPTIMIZE="$RPM_OPT_FLAGS"

%check
%{__make} test

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

# To avoid name conflict with catdoc package.
%{__mv} %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/convert%{name}
%{__gzip} -c9 %{buildroot}%{_mandir}/man1/%{name}.1 > %{buildroot}%{_mandir}/man1/convert%{name}.1.gz
%{__rm} %{buildroot}%{_mandir}/man1/%{name}.1


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
%attr(0755, root, root) %{_bindir}/convert%{name}
%{_mandir}/man1/convert%{name}.1.gz

%changelog
* Thu Sep 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.06-5
- Rename /usr/bin/xls2csv to /usr/bin/convertxls2csv to avoid name conflict with package catdoc (Thank you Jan Klepek)

* Mon Aug 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.06-4
- License tag changed to "GPL+ or Artistic"

* Sun Aug 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.06-3
- Rewrite all BR from  perl-Unicode-Map form to "perl(Unicode::Map)"
- Add back Requires: perl(:MODULE_COMPAT_%%(eval "`%%{__perl} -V:version`"; echo $version)), perl(Unicode::Map)

* Fri Aug 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.06-2
- Delete %%{buildroot} from PREFIX and accordingly my doubleprefix hack.
- Replace all $RPM_BUILD_ROOT by %%{buildroot} for consistency use macroses.
- Replace chmod by %%{__chmod}.
- Remove all explicit perl and perl-modules requires.

* Sat Nov 22 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.06-1
- Small cosmetics changes like use %%{__rm} instead of plain "rm" and add
	braces in all macroses as it want Jason Tibbitts in BZ review 458866
- Remove file %%{perl_vendorarch}/auto/xls2csv/.packlist and add 3 lines
	(delete .packlist, delete empty directories and change permissions)
	from /etc/rpmdevtools/spectemplate-perl.spec (Jason Tibbitts)

* Tue Aug 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.06-0
- Change BuildArch to noarch
- Add BR: perl(Test::Simple)
- Add BuildRequires: perl perl-libintl perl-Text-CSV_XS perl-Spreadsheet-ParseExcel perl-Unicode-Map for tests

* Fri Aug 8 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 1.06-0
- Initial spec
