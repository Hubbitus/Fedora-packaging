# https://fedoraproject.org/wiki/Packaging:SourceURL#Github
%global commit 013ede3ef63473d6c4caaa6b242acd3006243e8e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           uksmtools
Version:        0
Release:        0.1%{?shortcommit:.git.%{shortcommit}}%{?dist}
Summary:        Simple tool to monitor and control UKSM
License:        GPLv3+
URL:            https://github.com/pfactum/uksmtools/
Source0:        %{name}.git.%{shortcommit}.tar.xz

%description
Various useful tools for monitoring and control UKSM kernel module like
uksmstat and uksmctl.

%prep
%setup -q -n %{name}.%{shortcommit}


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install PREFIX=%{_prefix}


%files
%doc COPYING README.md
%{_bindir}/uksmstat
%{_bindir}/uksmctl

%changelog
* Mon Apr  7 2014 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0-0.1.git.013ede3
- Initial version
