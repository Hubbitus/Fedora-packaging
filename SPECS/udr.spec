Name:          udr
Version:       0.9.4
Release:       1%{?shortcommit:.git.%{shortcommit}}%{?dist}
Summary:       UDR is a wrapper around rsync that enables rsync to use UDT

License:       ASL 2.0
URL:           https://github.com/LabAdvComp/UDR
Source:        https://github.com/LabAdvComp/UDR/archive/v0.9.4.tar.gz

BuildRequires: openssl-devel, udt-devel

Patch0:        udr-0.9.4-shared-udt.patch

%description
A UDT wrapper for rsync that improves throughput of large data transfers over
long distances utilize UDT protocol over UDP.

%prep
%setup -q -n UDR-%{version}

%patch0 -p1 -b .udt-sharedlib

# Remove bundled udt
rm -rf udt

%build
make -e os=LINUX arch=AMD64 %{?_smp_mflags}

%install
# There are no install tarket in Makefile
install -Dm 0755 src/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 0755 src/%{name} %{buildroot}%{_bindir}/%{name}

%files
%doc README.md
%{_bindir}/%{name}
%license LICENSE.txt


%changelog
* Mon Mar 23 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0.9.4-1
- Initial spec.
