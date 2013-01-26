%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Name:	cpyrit-cuda
Version:	0.4.0
Release:	1%{?dist}
# OpenSSL exception
License:	GPLv3+ with exceptions
Group:	Applications/Internet
Summary:	A GPGPU-driven WPA/WPA2-PSK key cracker
URL:		http://code.google.com/p/pyrit/
Source0:	http://pyrit.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	python-devel, openssl-devel, zlib-devel, libpcap-devel
# Scapy and python-sqlalchemy are needed for full testing
BuildRequires:	scapy, python-sqlalchemy
Requires:	scapy, python-sqlalchemy

%description
This is CUDA extension for pyrit

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -L/opt/cuda/lib -L/opt/cuda/lib64 -L/usr/lib/nvidia -L/usr/lib64/nvidia" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root=%{buildroot}
chmod 755 %{buildroot}%{python_sitearch}/cpyrit/*.so

%check
# Can't do the tests in koji, the network tests fail, even against loopback
# pushd test
# export PYTHONPATH=%{buildroot}/%{python_sitearch}
# %{__python} test_pyrit.py 
# popd

%files
%doc COPYING PKG-INFO README
%{python_sitearch}/%( echo %{name} | sed 's/-/_/' )-%{version}-*.egg-info
%{python_sitearch}/cpyrit/_%( echo %{name} | sed 's/-/_/' ).so

%changelog
* Thu Jan 17 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.0-1
- Based on pyrit Fedora specfile.
