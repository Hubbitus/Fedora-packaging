%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary:       Grep-like tool for source code
Name:          grin
Version:       1.1.1
Release:       3%{?dist}
License:       BSD
Group:         Applications/Text
URL:           http://pypi.python.org/pypi/grin
Source0:       http://pypi.python.org/packages/source/g/grin/%{name}-%{version}.tar.gz
Requires:      python-setuptools python-argparse
BuildArch:     noarch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-setuptools-devel python-nose python-argparse

%description

grin is a similar in function to GNU grep, however it's has modified
behaviour to make it simpler to use when grepping source code.

Some features grin feature are:

  * recurse directories by default
  * do not go into directories with specified names
  * do not search files with specified extensions
  * be able to show context lines before and after matched lines
  * Python regex syntax
  * unless suppressed via a command line option, display the filename 
    regardless of the number of files
  * accept a file (or stdin) with a list of newline-separated filenames
  * grep through gzipped text files
  * be useful as a library to build custom tools quickly

%prep
%setup -q
%{__chmod} 0644 examples/*
%{__sed} -i -e '1d' grin.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
nosetests

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc ANNOUNCE.txt examples LICENSE.txt README.txt THANKS.txt
%{_bindir}/%{name}
%{_bindir}/grind
%{python_sitelib}/%{name}.py*
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 21 2009 Terje Rosten <terje.rosten@ntnu.no> - 1.1.1-2
- add docs
- rpmlint clean
- add %%check section

* Sat Jan 17 2009 Terje Rosten <terje.rosten@ntnu.no> - 1.1.1-1
- initial build


