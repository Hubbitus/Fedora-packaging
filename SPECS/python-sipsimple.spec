# Review request: https://bugzilla.redhat.com/show_bug.cgi?id=1130101

Name:           python-sipsimple
Version:        1.4.1
Release:        2%{?dist}
Summary:        SIP SIMPLE client SDK is a Software Development Kit for easy development of SIP multimedia end-points

License:        GPLv3
URL:            http://sipsimpleclient.org/
Source0:        http://download.ag-projects.com/SipClient/python-sipsimple-1.4.1.tar.gz

BuildRequires:  python2-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  Cython >= 0.19.0

Requires:       python-application >= 1.4.0
Requires:       python-cjson >= 1.0.5
Requires:       python-dateutil >= 1.4
Requires:       python-eventlib >= 0.1.0
Requires:       python-greenlet >= 0.3.2
Requires:       python-gnutls >= 1.1.9
Requires:       python-lxml >= 2.1.2
Requires:       python-msrplib >= 0.15.0
Requires:       python-xcaplib >= 1.0.17
Requires:       python-dns >= 1.9.0
Requires:       python-twisted-names >= 8.1.0
Requires:       python-zope-interface4 >= 3.3.1

%description
SIP SIMPLE client SDK is a Software Development Kit for easy development
of SIP multimedia end-points with features beyond VoIP like Session based
Instant Messaging, File Transfers, Desktop Sharing and Presence. Other
media types can be easily added by using an extensible high-level API.
The SDK consists of several low-level components, Unix command
line clients, a GUI client (Blink) and a server application (SylkServer).

%prep
%setup -q


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc AUTHORS Changelog LICENSE README
%{python2_sitearch}/*


%changelog
* Tue Sep 9 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.4.1-2
- Target to python2
- Add docs.
- Add dependencies from docs/Dependencies.txt (before that most was listed in blink package).

* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 1.4.1-1
- Initial version
