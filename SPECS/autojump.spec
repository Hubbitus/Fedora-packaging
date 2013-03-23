Name:           autojump
Version:        14
Release:        1%{?dist}

Summary:        A fast way to navigate your filesystem from the command line

Group:          Applications/Productivity
License:        GPLv3
URL:            http://wiki.github.com/joelthelion/autojump
Source:         https://github.com/downloads/joelthelion/%{name}/%{name}_v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python

%description
autojump is a faster way to navigate your filesystem. It works by maintaining 
a database of the directories you use the most from the command line.


%package zsh
Requires:       %{name}
Group:          Applications/Productivity
Summary:        Autojump for zsh

%description zsh
autojump is a faster way to navigate your filesystem. It works by maintaining 
a database of the directories you use the most from the command line.
autojump-zsh is designed to work with zsh.

%prep
%setup -q -n %{name}_v%{version}


%build

gzip %{name}.1

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

# There must be a more elegant way to do that
install -p icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/icon.png
install -Dp %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -p jumpapplet $RPM_BUILD_ROOT%{_bindir}/jumpapplet
install -Dpm 644 _j $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions/_j
install -Dpm 644 %{name}.bash $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.bash
install -Dpm 644 %{name}.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.sh
install -Dpm 644 %{name}.zsh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.zsh

install -Dpm 644 %{name}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING README.rst
%{_bindir}/*
%{_datadir}/%{name}*
%{_mandir}/man1/%{name}*
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.sh
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.bash

%files zsh
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.zsh
%dir %{_datadir}/zsh/site-functions/
%{_datadir}/zsh/site-functions/
%{_datadir}/zsh/site-functions/_j

%changelog
* Sat Dec 18 2010 Thibault North <tnorth@fedoraproject.org> - 14-1
- Initial package

