# Test of properly function library need DNS querys. It work perfectly on my machine and pass all tests.
# But internet access is not allowed from mock chroot. So, I need disable it by default. Yo may enable it if you want.
%define do_not_test 1

Name:		dnsjava
Version:		2.0.6
Release:		5%{?dist}
Summary:		Java DNS implementation
License:		BSD and MIT
URL:			http://www.dnsjava.org/
Source0:		http://www.dnsjava.org/download/%{name}-%{version}.tar.gz
Group:		System Environment/Libraries
#Epoch:		0
#Vendor:		JPackage Project
#Distribution:	JPackage
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	ant, jpackage-utils >= 0:1.5

BuildRequires:	java-devel >= 1.7
Requires:		java >= 1.7
Requires:		jpackage-utils
BuildArch:	noarch

# For tests
BuildRequires:	ant-junit


%description
dnsjava is an implementation of DNS in Java. It supports all of the common
record types and the DNSSEC types. It can be used for queries, zone transfers,
and dynamic updates. It includes a cache which can be used by clients, and a
minimal implementation of a server. It supports TSIG authenticated messages,
partial DNSSEC verification, and EDNS0.

dnsjava provides functionality above and beyond that of the InetAddress class.
Since it is written in pure Java, dnsjava is fully threadable, and in many
cases is faster than using InetAddress.

dnsjava provides both high and low level access to DNS. The high level
functions perform queries for records of a given name, type, and class, and
return an array of records. There is also a clone of InetAddress, which is
even simpler. A cache is used to reduce the number of DNS queries sent. The
low level functions allow direct manipulation of dns messages and records, as
well as allowing additional resolver properties to be set.

A 'dig' clone and a dynamic update program are included, as well as a
primary-only server.

%package		javadoc
Summary:		Javadoc for %{name}
Group:		Documentation

%description	javadoc
Javadoc for %{name}.

%prep
%setup -q
rm -rf doc/

iconv -f iso8859-1 -t utf8 Changelog > Changelog.tmp
touch -r Changelog Changelog.tmp
mv -f Changelog.tmp Changelog

%build
export CLASSPATH=%(build-classpath jce)
ant -Dj2se.javadoc=%{_javadocdir}/java clean docsclean jar docs

%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p %{name}-%{version}.jar %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

%if ! 0%{?do_not_test}
%check
export CLASSPATH='%(build-classpath junit):%{name}-%{version}.jar'
ant -Dj2se.javadoc=%{_javadocdir}/java compile_tests
ant -Dj2se.javadoc=%{_javadocdir}/java run_tests
%endif

%files
%defattr(-,root,root,-)
%doc Changelog README USAGE examples.html *.java
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}


%changelog
* Wed Apr 15 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-5
- Continue review.
- As it can't be build by gcj, delete back this stuff from spec.
- Tests made now by conditional. As internet access is not allowed in default mock chroot, it is disabled now.
- Changelog recoded form iso8859-1 (charset is guessed by Orcan 'oget' Ogetbil)

* Wed Apr 15 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-4
- Continue review.
- Delete explicit installation in %%install *.java files.
- License from BSD changed to "BSD and MIT"
- Delete unneeded BR: jce, java-javadoc
- Fix mistake: Add Requires: jpackage-utils and delete listed twice BuildRequires: jpackage-utils
- BR: java-devel >= 1.7, R: java >= 1.7

* Tue Apr 14 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-3
- Review in progress. Thanks to Orcan 'oget' Ogetbil.
- Add *.java examplees into documentation (it is mentioned in USAGE)
- Add testing:
	o Add BuildRequires: ant-junit
	o Add %%check section.
- Group from "Development/Libraries" changed to "System Environment/Libraries" by Orcan 'oget' Ogetbil suggestion.
- rm -rf doc/ in %%prep section.
- Removee listed twice Requires: jpackage-utils

* Mon Apr 13 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-2
- Issues from review:
	o Add
		. BuildRequires:	java-devel
		. BuildRequires:	jpackage-utils
		. Requires:		java >= specific_version
		. Requires:		jpackage-utils
	o Delete "%%define section free"
	o "%%defattr(0644,root,root,0755)" replaced by "%%defattr(-,root,root,-)" in both packages.
	o Add gcj-related stuff.
	o Remove Javadoc scriptlets

* Sun Apr 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0.6-1
- Import src.rpm from JPackage - http://ftp.heanet.ie/pub/jpackage/1.6/generic/free/SRPMS/dnsjava-1.5.1-2jpp.src.rpm
- Step to last version 2.0.6
- Reformat spec with tabs.
- In Source0 tag inject %%{name} and %%{version} macroses.
- $RPM_BUILD_ROOT replaced by %%{buildroot}
- Delete (comment out) tags:
	o Epoch:		0
	o Vendor:		JPackage Project
	o Distribution:	JPackage
- Add %%{?dist} into relese instead of "jpp"
- Introduced by rpmlint:
	o Group Development/Libraries/Java changed to simple Development/Libraries
	o Licence changed to BSD
	o javadoc ackage group changed form Development/Documentation to simple Documentation

* Fri Aug 20 2004 Ralph Apel <r.ape at r-apel.de> 0:1.5.1-2jpp
- Build with ant-1.6.2

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 0:1.5.1-1jpp
- 1.5.1
- remove crosslink patch (merged upstream)

* Fri Oct 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.4.3-1jpp
- Update to 1.4.3.
- Crosslink with local J2SE javadocs.
- Spec cleanups, save in UTF-8.

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.3.2-2jpp
- update for JPackage 1.5

* Wed Mar 12 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.3.2-1jpp
- Update to 1.3.2.
- Use ant instead of make for building.
- Drop patches, and include DNSSEC/JCE code.
- Use sed instead of bash 2 extension when symlinking jars during build.

* Sat May 11 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2.4-1jpp
- updated by Ville Skyttä <ville.skytta@iki.fi>
 - Updated to 1.2.4.
 - Fixed Vendor, Distribution and Group tags.
 - Updated description.
 - Versioned javadocs.
 - Added -no-debug and -no-jce patches.
 - Doesn't BuildRequire ant.

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2.3-2jpp
- javadoc into javadoc package

* Fri Nov 2 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2.3-1jpp
- first JPackage release
