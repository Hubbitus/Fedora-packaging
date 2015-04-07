%define git a29d6e9

Name:           bbcp
Version:        15.02.03.00.1
Release:        1%{?git:.git.%{git}}%{?dist}
Summary:        Securely and quickly copy data from source to target

License:        LGPLv3+
URL:            http://www.slac.stanford.edu/~abh/bbcp/
Source0:        bbcp.git.a29d6e9.tar.xz
# From http://www.slac.stanford.edu/~abh/bbcp/bbcp.git
# Tarball producing: ./%%{SOURCE1} %%{git}
Source1:        bbcp.get.git

BuildRequires:  zlib-devel, openssl-devel

%description
Fast copying tools over network. Replacement for scp, rsync for big amount of
transfer with numerous optimizations and tuning capability.

%prep
%setup -q -n %{name}.%{git}


%build
cd src
# Hack to workaround of errors:
# make[2]: *** No rule to make target `makeLinuxppc64'.  Stop.
# make[2]: *** No rule to make target 'makeLinuxarmv7l'.  Stop.
if [ 'ppc64' = `uname -i` -o 'armv7l' = `uname -i` ]; then
 sed -i 's#@make makeLinux`/bin/uname -i`#@make makeLinuxx86_64#' Makefile
fi
DEST_SYSNAME=linux make %{?_smp_mflags}

%install
# There no install target in Makefile. Do it manually
install -Dm 0755 bin/linux/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license src/COPYING.LESSER
%{_bindir}/%{name}


%changelog
* Mon Mar 23 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 15.02.03.00.1-1.git.a29d6e9
- Initial spec
