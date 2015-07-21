%global commit d41883a9140b769893256a9427d59d2c8ce4bec9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:          Enable compressed swap in memory
Name:             zram
Version:          1.0.0
Release:          2.git.%{shortcommit}%{?dist}
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
%{_unitdir}/mkzram.service
%{_sbindir}/zramstart
%{_sbindir}/zramstop
%{_sbindir}/zramstat


%changelog
* Sun Jul 05 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0-2.git.d41883a
- Build new release to resolve name conflict with anaconda service - https://github.com/mystilleef/FedoraZram/commit/d41883a9140b769893256a9427d59d2c8ce4bec9

* Mon Dec 01 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0-1.git.5602a90
- Import upstream spec file and rework.
- Replace $RPM_BUILD_ROOT by macros.
- Use systemd macroses.
- Gone epoch tag and debug package generation disabling.
- Release 1 with git.
- Use %%make_install in flawor of %%makeinstall

* Tue Mar 19 2013 Doncho Gunchev <dgunchev@gmail.com> - 0:1.0.0-0
- Initial package
