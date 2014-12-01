%global commit 5602a907e068bbabaeeba5d5965664433be60556
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:          Enable compressed swap in memory
Name:             zram
Version:          1.0.0
Release:          1.git.%{shortcommit}%{?dist}
License:          GPLv2
Group:            System Environment/Daemons
URL:              https://github.com/mystilleef/FedoraZram
Source:           https://github.com/mystilleef/FedoraZram/archive/%{commit}/FedoraZram-%{commit}.tar.gz
BuildArch:        noarch

BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:         bc > 1.0

%description
zram compresses swap partitions into RAM for performance.


%prep
%setup -qn FedoraZram-%{commit}

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sbindir}
%make_install DESTDIR=%{buildroot}


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README.md
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/zram.service
%{_sbindir}/zramstart
%{_sbindir}/zramstop
%{_sbindir}/zramstat


%changelog
* Mon Dec 01 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0-1.git.5602a90
- Import upstream spec file and rework.
- Replace $RPM_BUILD_ROOT by macros.
- Use systemd macroses.
- Gone epoch tag and debug package generation disabling.
- Release 1 with git.
- Use %%make_install in flawor of %%makeinstall

* Tue Mar 19 2013 Doncho Gunchev <dgunchev@gmail.com> - 0:1.0.0-0
- Initial package
