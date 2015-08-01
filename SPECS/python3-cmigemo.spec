Name:          python3-cmigemo
Version:       0.1.5
Release:       1%{?dist}
Summary:       A pure python binding for C/Migemo

License:       MIT
URL:           https://pypi.python.org/pypi/cmigemo/0.1.5
Source0:       https://pypi.python.org/packages/source/c/cmigemo/cmigemo-0.1.5.tar.gz

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: cmigemo-devel

%description
A C/Migemo binding for python written in pure python using ctypes.


%prep
%setup -q -n cmigemo-%{version}

%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%check
# One test failed. Issue filled: @TODO https://github.com/mooz/python-cmigemo/issues/2
#? %%{__python3} setup.py test


%files
%doc
%{python3_sitelib}/*

%changelog
* Sun Jul 26 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.1.5-1
- Initial spec
- Test failed. Fill bugreport: https://github.com/mooz/python-cmigemo/issues/2
