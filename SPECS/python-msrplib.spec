# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-msrplib
Version:        0.15.0
Release:        1%{?dist}
Summary:        Client library for MSRP protocol and its relay extension (RFC 4975 and RFC4976)

License:        LGPLv2+
URL:            http://sipsimpleclient.org/
Source0:        http://download.ag-projects.com/SipClient/python-msrplib-0.15.0.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
Message Session Relay Protocol (MSRP) is a protocol for transmitting a
series of related instant messages in the context of a session. Message
sessions are treated like any other media stream when set up via a
rendezvous or session creation protocol such as the Session Initiation
Protocol (SIP).

A series of related instant messages between two or more parties can be
viewed as part of a "message session", that is, a conversational exchange of
messages with a definite beginning and end. This is in contrast to
individual messages each sent independently. Messaging schemes that track
only individual messages can be described as "page-mode" messaging, whereas
messaging that is part of a "session" with a definite start and end is
called "session-mode" messaging.

Page-mode messaging is enabled in SIP via the SIP MESSAGE method, as defined
in RFC 3428. Session-mode messaging has a number of benefits over page-mode
messaging, however, such as explicit rendezvous, tighter integration with
other media-types, direct client-to-client operation, and brokered privacy
and security.

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
* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.15.0-1
- Initial version
