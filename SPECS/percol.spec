# Review https://bugzilla.redhat.com/show_bug.cgi?id=1249329
%global commit0 b567f41830f3ac814e71688f9d2e13ea337f618d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:          percol
Version:       0.1.1
Release:       0.2%{?shortcommit0:.git.%{shortcommit0}}%{?dist}
Summary:       Interactive selection to the traditional pipe concept on UNIX

License:       MIT
URL:           https://github.com/mooz/percol
%if 0%{?commit0:1}
Source0:       https://github.com/mooz/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%else
Source0:       https://github.com/mooz/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-cmigemo
Requires:      python3-six python3-cmigemo

%description
percol is an interactive grep tool in your terminal. percol

receives input lines from stdin or a file,
lists up the input lines,
waits for your input that filter/select the line(s),
and finally outputs the selected line(s) to stdout.
Since percol just filters the input and output the result to stdout, it can be
used in command-chains with | in your shell (UNIX philosophy!).

%prep
%if 0%{?commit0:1}
%setup -qn %{name}-%{commit0}
%else
%setup -q
%endif

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%check
%{__python3} setup.py test

%files
%{_bindir}/%{name}
%doc README.md
%{python3_sitelib}/*

%changelog
* Sat Nov 28 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1.1-0.2.git.b567f41
- Review in progress - https://bugzilla.redhat.com/show_bug.cgi?id=1249329. Thanks to Julien Enselme.
- Change License to MIT (GPL statements removed: https://github.com/mooz/percol/commit/d0bc902555fff5abef85012af3cbc323b915843b).
- Requested license text inclusion: https://github.com/mooz/percol/issues/87
- Add requires python3-cmigemo

* Sun Jul 26 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1.1-0.1.git.b567f41
- Master build, two problems reported by me addressed now:
    o FSF address: https://github.com/mooz/percol/issues/77
    o Python3 compatability - https://github.com/mooz/percol/issues/78

* Sun Jul 26 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.1.0-1
- Initial version
- Incorrect fsf address reported: https://github.com/mooz/percol/issues/77