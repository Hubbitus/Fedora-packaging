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
