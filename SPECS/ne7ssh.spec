Name:		ne7ssh
Version:		1.3.2
Release:		10%{?dist}
Summary:		SSH Library is a Secure Shell client software written in C++
Summary(ru):	SSH библиотека для построения клиентов написанная на C++

Group:		Development/Libraries
License:		QPL
URL:			http://www.netsieben.com/products/ssh/
Source0:		http://www.netsieben.com/files/%{name}-%{version}.tar.bz2

BuildRequires:	cmake botan-devel

%description
As a developer you may wish to integrate SSH client functionality into your
applications. You can now use the NetSieben's API, instead of spending countless
hours developing your own solution.

The SSH library was created by the NetSieben developers who, after researching
the limited number of options available to them from both commercial and open
source communities, found these solutions limited and at best, still in early
stages of development.

It utilizes Botan library for its cryptographic functions, allowing for a
large choice of algorithms to be used in SSH communications.

%description -l ru
Как разработчик ПО Вы можете захотеть интегрировать функциональность SSH
клиента в Вашу программу. Теперь Вы можете сделать это используя библиотеку
ne7ssh и NetSieben's API вместо того чтобы тратить бесчисленные часы
разрабатывая своё решение.

Используется библиотека Botan для криптографических целей, это позволяет
использовать большое количество алгоритмов, используемых для шифрования в SSH.

%package	devel
Summary:	Headers for %{name} library
Group:	Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	botan-devel

%description devel
Headers for development with %{name} library

%package		doc
Summary:		API documentation, examples of usage %{name} library
Group:		Documentation
Buildarch:	noarch

%description doc
API documentation and example code to try the %{name} library.
It also contains a Makefile that builds all the examples with a single
command.

WARNING: To build the included examples of code, you must have the 
%{name}-devel package installed. Install the %{name}-devel package manually 
if you plan to compile these examples.

%prep
%setup -q

# Hack to correct install on 64-bit systems.
sed -i 's#install(TARGETS net7ssh LIBRARY DESTINATION lib)#install(TARGETS net7ssh LIBRARY DESTINATION %{_lib})#' CMakeLists.txt

%build
%{cmake} .
make all %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Delete unversioned doc directory
rm -rf %{buildroot}/%{_datadir}/doc/%{name}

# Delete backaps from patch
rm -rf examples/*.stdio.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG INSTALL LICENSE.QPL README
%{_libdir}/libnet7ssh.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libnet7ssh.so

%files doc
%defattr(-,root,root,-)
%doc doc examples LICENSE.QPL

%changelog
* Wed Feb 2 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.2-10
- As it can't build on EPEL5, brop some old stuff like manual clean buildroot (thanks to Ruediger Landmann)
- Correct -doc description.

* Mon Aug 23 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.2-9
- Update to 1.3.2 version.
- Remove unneeded patch ne7ssh-1.3.1-missing_stdio_h.patch
- Add LICENSE.QPL to -doc subpackage to honor new guidelines.

* Fri Oct 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-8
- Exclude patch-backup files from examples.

* Fri Oct 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-7
- -Expand Patch0: ne7ssh-1.3.1-missing_stdio_h.patch on examples too.

* Fri Oct 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-6
- Remove -devel dependency from -doc subpackage and add warning in description instead.

* Thu Oct 1 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-5
- Use macros %%{cmake} (Thanks to Michael Schwendt)

* Sat Sep 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-4
- Honor Fedora flags.

* Sat Sep 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-3
- All changes in this release inspired by Michael Schwendt. Michael thank you.
- Turn examples subpackage into doc and move docs to them.
- Add Requires: botan-devel to -devel.
- Rearrange description in both languages.

* Tue Sep 8 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-2
- Fix installation on 64-bit systems.

* Tue Sep 8 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.3.1-1
- Initial spec.