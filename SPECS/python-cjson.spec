Name:           python-cjson
Version:        1.1.0
Release:        5%{?dist}
Summary:        Fast JSON encoder/decoder for Python

License:        LGPLv2+
URL:            https://pypi.python.org/pypi/python-cjson
Source0:        https://pypi.python.org/packages/source/p/python-cjson/%{name}-%{version}.tar.gz

BuildRequires:  python2-devel

%description
This module implements a very fast JSON encoder/decoder for Python.

JSON stands for JavaScript Object Notation and is a text based lightweight
data exchange format which is easy for humans to read/write and for machines
to parse/generate. JSON is completely language independent and has multiple
implementations in most of the programming languages, making it ideal for
data exchange and storage.

The module is written in C and it is up to 250 times faster when compared to
the other python JSON implementations which are written directly in python.
This speed gain varies with the complexity of the data and the operation and
is the the range of 10-200 times for encoding operations and in the range of
100-250 times for decoding operations.


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
PYTHONPATH=$(echo build/lib.linux-*) %{__python} jsontest.py

%files
%doc README LICENSE ChangeLog
# For arch-specific packages: sitearch
%{python2_sitearch}/*


%changelog
* Sun Sep 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-5
- s/python_sitearch/python2_sitearch/

* Wed Sep 3 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-4
- Add %%doc README LICENSE ChangeLog

* Mon Aug 25 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-3
- Add %%check section.

* Tue Aug 19 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-2
- Start of Fedora review bz#1130097. Thanks to Christopher Meng.
- Chang BR to python2-devel from just python-devel.
- Drop python_sitearch declaration as it is not targeted to epel6 and early.

* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 1.1.0-1
- Initial spec.
