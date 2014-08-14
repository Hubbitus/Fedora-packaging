# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-ejson
Version:        0.1.6
Release:        1%{?dist}
Summary:        Extensible json serializer/deserializer library

License:        GPLv3
URL:            https://pypi.python.org/pypi/ejson
Source0:        https://pypi.python.org/packages/source/e/ejson/ejson-0.1.6.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
There are countless scenarios that we need to exchange data between
different systems, implemented in different languages and technologies.
Even in the same system, when implementing data exchange between the
backend and the frontend we face the need to convert the language data
types to another format and then do the oposite when the data arrives in
the other side of the wire.

A very simple and flexible format that seems to fit most of our needs is
the JavaScript Object Notation, or simple `json`. It is very hard to
find a programming language these days that does not support it, even
the low level ones, like C, C++, etc.

Json is enough when we need to exchange data types like integers,
doubles, strings, lists and hash tables. The problem starts when we need
to exchange a complex data type. And it's the exact aim of this
document: providing an API to extend the `json` library to make it easy
to register new serializers and new deserializers.

%prep
%setup -q -n ejson-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}


%files
%doc
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.1.6-1
- Initial spec.
