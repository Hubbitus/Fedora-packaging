# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-eventlib
Version:        0.1.2
Release:        1%{?dist}
Summary:        Library to make it easy to track events in python/django apps

License:        GPLv3
URL:            http://sipsimpleclient.org/
Source0:        http://download.ag-projects.com/SipClient/python-eventlib-0.1.2.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
Long story short, eventlib is an asynchronous event tracking app for
Django. This library was built upon the following values:

* It must be deadly simple to log an event;
* It must be possible to track each event in different ways;
* Each different "event handler" must be completely separate and fail
  gracefully;
* The event system must be asynchronous, so let's use celery;
* The library must be extensible;
* 100% of test coverage is enough.

%prep
%setup -q


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
* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.1.2-1
- Initial version
