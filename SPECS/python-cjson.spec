%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-cjson
Version:        1.1.0
Release:        1%{?dist}
Summary:        Fast JSON encoder/decoder for Python

License:        LGPLv2+
URL:            https://pypi.python.org/pypi/python-cjson
Source0:        https://pypi.python.org/packages/source/p/python-cjson/python-cjson-1.1.0.tar.gz

BuildRequires:  python-devel

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

%files
%doc
# For arch-specific packages: sitearch
%{python_sitearch}/*


%changelog
* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 1.1.0-1
- Initial spec.
