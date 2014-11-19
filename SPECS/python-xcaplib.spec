# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:          python-xcaplib
Version:       1.0.17
Release:       2%{?dist}
Summary:       Client for managing full or partial XML documents on XCAP servers (RFC 4825)

License:       LGPLv2+
URL:           http://sipsimpleclient.org/
Source0:       http://download.ag-projects.com/SipClient/python-xcaplib-1.0.17.tar.gz

BuildArch:     noarch
BuildRequires: python-devel

%description
XCAP protocol, defined in RFC 4825, allows a client to read, write, and
modify application configuration data stored in XML format on a server. XCAP
maps XML document sub-trees and element attributes to HTTP URIs, so that
these components can be directly accessed by HTTP. An XCAP server used by
XCAP clients to store data like presence policy in combination with a SIP
Presence server that supports PUBLISH/SUBSCRIBE/NOTIFY SIP methods can
provide a complete SIP SIMPLE solution.

The XCAP client example script provided by this package can be used to
manage documents on an XCAP server.

%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc
%{_bindir}/xcapclient
# For noarch packages: sitelib
%{python_sitelib}/*

%changelog
* Wed Oct 29 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.17-2
- Fix accidentally mix spec with python-msrplib content.

* Thu Jul 17 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.17-1
- Initial version
