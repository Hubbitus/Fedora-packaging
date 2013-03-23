Name:		Korda-release
Version:		0.1
Release:		1%{?dist}
Summary:		Base configuration for Korda-Fedora machines
Summary(ru):	Базовая конфигурация для Korda-Fedora компов
BuildArch:	noarch

Group:		System Environment/Base
License:		GPLv2+
URL:			http://hubbitus.net.ru
Source0:		%{name}.tar.lzma

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:
#Requires:

%description
This package provide base configuration for Korda-Fedora machines.

Package contain files-config and scripts to run on (un)install stages.

%description -l ru
Пакет представляет собой базовую конфигруцию Korda-Fedora компов.

Содержит как файлы, так и скрипты, выполняемые на установке/удалении.

%prep
%setup -q -n %{name}

%build

%install
# rm -rf %{buildroot}

%post
cat <<EOF >> /etc/hosts
192.168.0.148	hubbitus
192.168.0.1	korda.local
192.168.0.254	kordabsd.local
EOF



%postun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Authors

%changelog
* Sat Oct 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1-1
- Initial spec.