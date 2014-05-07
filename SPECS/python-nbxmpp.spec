Name:           python-nbxmpp
Version:        0.4
Release:        1%{?dist}
Summary:        XMPP library by Gajim team
License:        GPLv3
Group:          Development/Languages
Url:            http://python-nbxmpp.gajim.org/
# https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Troublesome_URLs
Source0:        https://python-nbxmpp.gajim.org/downloads/4#/nbxmpp-%{version}.tar.gz
BuildRequires:  fdupes
BuildRequires:  python-devel
BuildArch:      noarch

%description
Python-nbxmpp is a Python library that provides a way for Python
applications to use Jabber/XMPP networks in a non-blocking way. This
library is initially a fork of xmpppy one, but using non-blocking sockets.

%package doc
Summary:        Nbxmpp Documentation
Group:          Development/Languages

%description doc
This packages provides documentation of Nbxmpp API.

%prep
%setup -q -n nbxmpp-%{version}

%build
python setup.py build

%install
python setup.py install -O1 --skip-build --root %{buildroot} --prefix=%{_prefix}
%fdupes %{buildroot}%{python_sitelib}

%files
%doc COPYING
%{python_sitelib}/nbxmpp-*.egg-info
%{python_sitelib}/nbxmpp/

%files doc
%doc ChangeLog README doc/apidocs doc/examples

%changelog
* Wed May 7 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4-1
- Version 0.4

* Wed Mar 12 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3-1
- Import package ftp://ftp.muug.mb.ca/mirror/opensuse/ports/aarch64/source/factory/repo/oss/suse/src/python-nbxmpp-0.2-1.1.src.rpm, rework
- Update to 0.3

* Sun Dec  8 2013 p.drouand@gmail.com
- Update to version 0.2
  + Add some namespace
  + do TLS handshake without blocking
  + store all SSL errors instead of only last one
- Set correct Group : Devel/Languages/Python
- Use download Url as source
- Remove unwanted comments in specfile
- Package the two directories in /doc to avoid providing epydoc build
  configuration file
* Thu Aug 15 2013 dap.darkness@gmail.com
- Heads up: Python2 / Python3 parallel installation.
  %%fdupes will not work if files are installed via %%doc.
* Sat Apr 20 2013 dap.darkness@gmail.com
- Fixed up to submit.
* Sat Apr  6 2013 nekolayer@yandex.ru
- Initial package.
