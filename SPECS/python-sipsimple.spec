# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-sipsimple
Version:        1.4.1
Release:        1%{?dist}
Summary:        SIP SIMPLE client SDK is a Software Development Kit for easy development of SIP multimedia end-points

License:        GPLv3
URL:            http://sipsimpleclient.org/
Source0:        http://download.ag-projects.com/SipClient/python-sipsimple-1.4.1.tar.gz

#BuildArch:      
BuildRequires:  python-devel
BuildRequires:  alsa-lib-devel

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
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc
# For arch-specific packages: sitearch
%{python_sitearch}/*


%changelog
* Thu Jul 17 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 1.4.1-1
- Initial version
