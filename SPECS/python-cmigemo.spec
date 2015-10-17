# Review request: https://bugzilla.redhat.com/show_bug.cgi?id=1249313
%global srcname cmigemo
%global sum A pure python binding for C/Migemo
%global summ A C/Migemo binding for python written in pure python using ctypes.

Name:          python-%{srcname}
Version:       0.1.6
Release:       2%{?dist}
Summary:       %{sum}

License:       MIT
URL:           https://pypi.python.org/pypi/%{srcname}
Source0:       https://pypi.python.org/packages/source/c/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python2-devel, python3-devel
BuildRequires: cmigemo-devel, python-six, python3-six

%description
%{summ}

%package -n python2-%{srcname}
Summary:       %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{summ}

%package -n python3-%{srcname}
Summary:       %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{summ}

%prep
%autosetup -n cmigemo-%{version}

# Remove upstream egg-info https://fedoraproject.org/wiki/Packaging:Python_Eggs#Upstream_Egg_Packages
rm -r %{srcname}.egg-info

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{srcname}
%{python2_sitelib}/*

%files -n python3-%{srcname}
%{python3_sitelib}/*

%changelog
* Sat Oct 17 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1.6-2
- Review request https://bugzilla.redhat.com/show_bug.cgi?id=1249313 in progress, thank you to Julien Enselme.
- Make package to compatible with python 2 and 3 (https://fedoraproject.org/wiki/Packaging:Python#Example_common_spec_file), use new macroses.
- Rename spec and package without digit 3.
- Ask upstream about license file inclusion: https://github.com/mooz/python-cmigemo/issues/3

* Sat Aug 01 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1.6-1
- My bug closed - version 0.1.6.

* Sun Jul 26 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.1.5-1
- Initial spec
- Test failed. Fill bugreport: https://github.com/mooz/python-cmigemo/issues/2
