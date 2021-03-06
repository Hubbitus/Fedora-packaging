# Fedora review: https://bugzilla.redhat.com/show_bug.cgi?id=1130103

Name:           blink
Version:        0.9.1
Release:        4%{?dist}
Summary:        Real-time communications client using SIP protocol

License:        GPLv3
URL:            http://icanblink.com/
Source0:        http://download.ag-projects.com/BlinkQt/%{name}-%{version}.tar.gz

BuildRequires:  cdbs >= 0.4.47
BuildRequires:  python2-devel >= 2.7
BuildRequires:  libvncserver-devel
BuildRequires:  Cython
Requires:       PyQt4 >= 4.7
Requires:       python-sipsimple


%description
Blink is the best real-time communications client using SIP protocol.
You can use it with many SIP providers, on the LAN using Bonjour and SIP2SIP
free service. Blink is elegant, simple to use and feature-full.

%prep
%setup -q


%build
python setup.py build_ext


%install
python setup.py install --root %{buildroot}


%files
%doc
%{_bindir}/%{name}
%{_datarootdir}/%{name}
%{python2_sitearch}/%{name}
%{python2_sitearch}/%{name}*.egg-info


%changelog
* Mon Oct 27 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-4
Add Requires: python-sipsimple

* Tue Sep 9 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-3
- Move most runtime dependencies into python-sipsimple package according to its
    docs/Dependencies.txt: python-application, python-cjson, python-eventlib,
    python-twisted-names, python-eventlet, python-twisted-core,
    python-zope-interface4, python-sipsimple, python-gnutls, python-dns,
    python-xcaplib, python-msrplib

* Mon Sep 8 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-2
- Turn BR python-qt4 into R PyQt4 by suggestions in review request (bz#1130103).
- Remove requires: python-ejson, python-celery, python-redis, python-django as they are not necessary in that version (at least for start) (bz#1130103).
- Add Requires: python-msrplib

* Thu Aug 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-1
- Update to 0.9.1

* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.9.0-1
- Initial spec
