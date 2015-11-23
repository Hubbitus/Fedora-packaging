%global commit0 063fd021c33ef668de945f29fdf2e52e256206eb
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%define _enable_debug_packages	%{nil}
%define debug_package	%{nil}

Summary:	Collection of drivers for WiFi adapters by Realtek
Name:	rtlwifi_new
Version:	0.1
Release:	5.git.%{shortcommit0}%{?dist}
Source0:	https://github.com/lwfinger/rtlwifi_new/archive/%{commit0}.tar.gz#/rtlwifi_new-%{shortcommit0}.tar.gz
Source1:	rtlwifi_new.conf
License:	GPLv2
Group:	System Environment/Kernel
URL:		https://github.com/lwfinger/rtlwifi_new
Requires(post):	dkms
Requires(preun):	dkms
Requires: kernel-devel

# Rename the modules to avoid conflicts with the modules provided by the
# kernel packages. Change the path to firmware for that purpose as well.
Patch1:		001-Rename-modules-to-name_new.patch
Patch2:		002-Use-rtlwifi_new-as-firmware-dir.patch
# By default, the modules are built for the current kernel but we want them
# for the kernel that dkms specifies in KERNELRELEASE variable.
Patch3:		003-Build-for-the-right-kernel.patch

%description
This package contains the following drivers for the WiFi adapters by Realtek:
rtl8192ce, rtl8192se, rtl8192de, rtl8188ee, rtl8192ee, rtl8723ae, rtl8723be,
and rtl8821ae as well as the common modules they need. The respective
modules provided with the kernel will be blacklisted to avoid conflicts.

%prep
%setup -qn %{name}-%{commit0}

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%install
# sources to be used by DKMS
mkdir -p %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}
for subdir in \
	btcoexist \
	rtl8188ee \
	rtl8192c \
	rtl8192ce \
	rtl8192cu \
	rtl8192de \
	rtl8192ee \
	rtl8192se \
	rtl8723ae \
	rtl8723be \
	rtl8821ae; do
	mkdir -p %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/$subdir
	install -m644 $subdir/*.c $subdir/*.h $subdir/Makefile \
		%{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/$subdir
done

install -m644 *.c *.h Makefile \
  %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/

# Blacklist the corresponding drivers that might be provided by the kernel
# packages. This is needed to avoid conflicts while still keeping the
# original drivers available, just in case.
mkdir -p %{buildroot}/etc/modprobe.d/
install -m644 %{SOURCE1} %{buildroot}/etc/modprobe.d

mkdir -p %{buildroot}/lib/firmware/rtlwifi_new
install -m644 firmware/rtlwifi/* %{buildroot}/lib/firmware/rtlwifi_new/

cat > %{buildroot}%{_usr}/src/%{name}-%{version}-%{release}/dkms.conf << EOF
MAKE="make"
PACKAGE_NAME=%{name}
PACKAGE_VERSION=%{version}-%{release}
BUILT_MODULE_NAME[0]=rtlwifi_new
BUILT_MODULE_NAME[1]=rtl_pci_new
BUILT_MODULE_NAME[2]=rtl_usb_new
BUILT_MODULE_NAME[3]=btcoexist_new
BUILT_MODULE_LOCATION[3]=btcoexist/
BUILT_MODULE_NAME[4]=rtl8192c-common_new
BUILT_MODULE_LOCATION[4]=rtl8192c/
BUILT_MODULE_NAME[5]=rtl8821ae_new
BUILT_MODULE_LOCATION[5]=rtl8821ae/
BUILT_MODULE_NAME[6]=rtl8192se_new
BUILT_MODULE_LOCATION[6]=rtl8192se/
BUILT_MODULE_NAME[7]=rtl8192de_new
BUILT_MODULE_LOCATION[7]=rtl8192de/
BUILT_MODULE_NAME[8]=rtl8723be_new
BUILT_MODULE_LOCATION[8]=rtl8723be/
BUILT_MODULE_NAME[9]=rtl8192ee_new
BUILT_MODULE_LOCATION[9]=rtl8192ee/
BUILT_MODULE_NAME[10]=rtl8192cu_new
BUILT_MODULE_LOCATION[10]=rtl8192cu/
BUILT_MODULE_NAME[11]=rtl8188ee_new
BUILT_MODULE_LOCATION[11]=rtl8188ee/
BUILT_MODULE_NAME[12]=rtl8192ce_new
BUILT_MODULE_LOCATION[12]=rtl8192ce/
BUILT_MODULE_NAME[13]=rtl8723ae_new
BUILT_MODULE_LOCATION[13]=rtl8723ae/
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[1]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[2]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[3]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[4]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[5]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[6]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[7]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[8]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[9]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[10]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[11]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[12]=/kernel/3rdparty/%{name}/
DEST_MODULE_LOCATION[13]=/kernel/3rdparty/%{name}/
AUTOINSTALL=yes
EOF

%post
/usr/sbin/dkms --rpm_safe_upgrade add -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{name} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{name} -v %{version}-%{release}

%preun
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{name} -v %{version}-%{release} --all || :

%files
%dir %{_usr}/src/%{name}-%{version}-%{release}
%{_usr}/src/%{name}-%{version}-%{release}/*
%dir /lib/firmware/rtlwifi_new
/lib/firmware/rtlwifi_new/*
%config(noreplace) /etc/modprobe.d/rtlwifi_new.conf

%changelog
* Thu Aug 20 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1-4.063fd02
- Add requires kernel-devel

* Tue Aug 18 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1-4.063fd02
- Import http://abf-downloads.rosalinux.ru/rosa2014.1/container/2504568/SRPMS/contrib/release/rtlwifi_new-0.1-3.3800a129.src.rpm
- Rename with dkms- prefix, leave single package
- Use traditional versioning, add dist tag, update source, release.
- Update to 063fd021c33ef668de945f29fdf2e52e256206eb

* Tue May 26 2015 Eugene Shatokhin <eugene.shatokhin@rosalab.ru> 0.1-3.3800a129
- (63bb7ca) Build modules for the right kernel
- (63bb7ca) By default, the modules are built for the current kernel but we want
- (63bb7ca) them for the kernel that dkms specifies in KERNELRELEASE variable.
- (63bb7ca) This commit fixes the issue.