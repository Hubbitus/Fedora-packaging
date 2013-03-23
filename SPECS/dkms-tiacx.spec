%global release_date 20130115
%global gitrev f988e58

Summary:			Driver for Texas Instruments' ACX100/ACX111 wireless network chips
Name:			dkms-tiacx
Version:			0
Release:			18.%{?release_date:git%{release_date}}%{?gitrev:.%{gitrev}}
License:			GPLv2+
Group:			System Environment/Kernel
URL:				http://sourceforge.net/projects/acx100
# Test version http://sourceforge.net/projects/acx100/forums/forum/257272/topic/3809996
# located only in git:
# To get tarball just run acx1xx.get script from source1
Source0:			acx-mac80211-%{gitrev}.tar.xz
# Script to get sources from git and pack it into .tar.xz
Source1:			acx1xx.get
BuildArch:		noarch
Requires:			kernel >= 2.6.32
Requires:			acx100-firmware, acx111-firmware
Requires(post):	dkms
Requires(preun):	dkms
Obsoletes:		%{name} >= 0.4.8
# Patch needed because Fedora ship Kernel 3.0.0 as 2.6.40 for transition purpose.
#Patch0:			acx-kernel-2to3-transition.patch

%description
Driver (Linux kernel module) for network interface cards based on Texas
Instruments' ACX100/ACX111 wireless network chips.

%prep
%setup -qn acx-mac80211
#% patch0 -p1 -b .k2to3

iconv -f ISO-8859-1 -t UTF-8 Changelog > Changelog.new
touch --reference Changelog Changelog.new
mv Changelog.new Changelog

%build

%install
rm -rf %{buildroot}

%global dkms_name tiacx
%global dkms_vers %{version}-%{release}
%global quiet ''

# Kernel module sources install for dkms
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/
cp -a * %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

# Configuration for dkms
cat > %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/dkms.conf << 'EOF'
PACKAGE_NAME=%{dkms_name}
PACKAGE_VERSION=%{dkms_vers}
MAKE[0]="make -C ${kernel_source_dir} M=${dkms_tree}/%{dkms_name}/%{dkms_vers}/build CONFIG_ACX_MAC80211=m CONFIG_ACX_MAC80211_PCI=y CONFIG_ACX_MAC80211_USB=n CONFIG_ACX_MAC80211_MEM=n EXTRA_CFLAGS=' -DCONFIG_ACX_MAC80211=1 -DCONFIG_ACX_MAC80211_PCI=1'"
CLEAN[0]="make -C ${kernel_source_dir} M=${dkms_tree}/%{dkms_name}/%{dkms_vers}/build clean"
BUILT_MODULE_NAME[0]=acx-mac80211
DEST_MODULE_LOCATION[0]=/kernel/drivers/net/wireless
AUTOINSTALL="YES"
EOF

%clean
rm -rf %{buildroot}

%post
# Add to DKMS registry
dkms add -m %{dkms_name} -v %{dkms_vers} %{?quiet} || :
# Rebuild and make available for the currenty running kernel
dkms build -m %{dkms_name} -v %{dkms_vers} %{?quiet} || :
dkms install -m %{dkms_name} -v %{dkms_vers} %{?quiet} --force || :

#Устанавливать сам модуль надо так:
#dkms build -m tiacx -v 0.4.7-5
#dkms install -m tiacx -v 0.4.7-5

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{dkms_vers} %{?quiet} --all || :

%files
%defattr(-, root, root, 0755)
%doc Changelog README
%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

%changelog
* Tue Jan 15 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0-18.git20130115.f988e58
- New year, new build :)
- Add acx1xx.get script as source1.

* Sun Dec 23 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0-17.git20121223.119ef57
- New build.

* Mon Nov 5 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0-16.git20121105.570b961
- New build for 3.6.2 kernel (was 3.4)

* Wed Sep 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.15.git20120602.ad2aacb065961fcf423719c68030fed7d38c578c
- New build

* Sat Jun 2 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.14.git20120602
- New build

* Fri Feb 24 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0-13.git20120224
- New build for recent kernel.
- Drop patch acx-kernel-2to3-transition.patch

* Sun Aug 21 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0-12.git20110821
- New version.
- Add patch acx-kernel-2to3-transition.patch to compatability with 2.6.40 kernel (https://sourceforge.net/projects/acx100/forums/forum/257272/topic/4667363).

* Sun Jan 9 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0-11.git20110109
- Another commint to try resolve connection problem: https://sourceforge.net/projects/acx100/forums/forum/257272/topic/3951017/index/page/2
- Delete sensitivity patch as it already in master branch.

* Sun Dec 19 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0-10.git20101213
- Try with adev->sensitivity = 3: https://sourceforge.net/projects/acx100/forums/forum/257272/topic/3951017/index/page/1 comment 18.

* Thu Dec 16 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0-9.git20101213
- Oliver offer sensitivity.20101215.patch to test, rebuild with it.

* Mon Dec 13 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0-8.git20101213
- New build to test recalibration fixes - https://sourceforge.net/projects/acx100/forums/forum/257272/topic/3951017
- Gove old versyon 0.3.37 it now absolutely wrong with new branch work.

* Sun Nov 14 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-7.git20101114
- New build.

* Sun Aug 15 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-5.git20100815
- New version from new git repository: http://sourceforge.net/projects/acx100/forums/forum/257272/topic/3809996

* Thu Jun 3 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-5.git20100603
- New major update. Build from git. Ad-Hoc should work!

* Fri May 7 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-4.git20100507
- Build new release for testing ( http://sourceforge.net/projects/acx100/forums/forum/257272/topic/3505850 ).
  module unloading should be fixed.

* Sat Apr 10 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-4.git20100410
- New git release with hope of error fix - http://sourceforge.net/projects/acx100/forums/forum/257272/topic/3505850

* Fri Apr 2 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-3.20100103
- Replace all %%define by %%global.
- New test version http://sourceforge.net/projects/acx100/forums/forum/257272/topic/3505850 .
- Delete BuildRoot because it is not intended to EPEL.
- Delete macroses for common commands like %%{__mkdir_p}, %%{__cp} to favor plain commands.
- Delete patch0 - patch3 - it is unused long time.
- In $$release_date is not used "-" anymore and all sed-magick deleted.
- Delete Requires gcc as it common
- Add Requires kernel >= 2.6.32
- Remove rm %%{buildroot}%%{_usrsrc}/%%{dkms_name}-%%{dkms_vers}/pktgen/{printhex,sendpkt}
	its does not exists anymore.
- License set to GPLv2+ (was GPL)
- Make setup quiet.
- Iconv Changelog from ISO-8859-1 (guessed) to unicode.
- Upstream module name changed to acx-mac80211. Reflect it in dkms config.

* Thu Sep 24 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.37-2.20080210
- Add new Patch3: dkms-tiacx-0.3.37-kernel.gt.2.6.30.patch
- Remove Hu-part from Release.
- Remove Hu-part from spec filename.
- Exclude %%{_usrsrc}/%%{dkms_name}-%%{dkms_vers}/pktgen/{printhex,sendpkt}
	due to error "Arch dependant binaries in noarch package"

* Sun Sep 21 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.3.37-20080210-Hu.1
- Add patch2 tiacx.kernel.gt.2.6.26.compatibility.patch. Main info to write it got from http://madwifi.org/ticket/2081

* Thu Jun 19 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 0.3.37-20080210-Hu.0
- Version 0.3.37-20080210-Hu.0
- Disable patch0, patch1, which are not compatable with new version

* Mon Jan 14 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 0.3.37-20080112_2-Hu.4
- Switch to source acx-20080112-2.tar.bz2
- Change version enumerations from strange 0.4.8-0 to version of driver
	(according to acx_config.h) and release_date of source tarball:
	-Add Obsoletes:	%%{name} >= 0.4.8
- Change release enumeration: Release: %%(echo %%{release_date} | sed 's/-/_/').Hu.0
	- According to, modify fo setup: %%setup -n acx-%%(echo %%{release_date} | cut -d- -f1 )
- Add Patch0: tiacx.kernels_after2.6.21.patch wich is adopted for new revision of - http://acx100.sourceforge.net/wiki/Patch_2.6.22
- Non-quiet build
- Add patch tiacx.SET_MODULE_OWNER.patch (self written)

* Fri Oct 5 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> 0.4.8-0
- Switch to source acx-20071003.tar.bz2 (Latest from sf.net)

* Sat Feb 17 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> 0.4.7-5
- Switch to the source http://www.cmartin.tk/acx/acx-20070101.tar.bz2 what be able build on 2.6.20 Kernel!
- Remove patch

* Sat Oct 28 2006 Matthias Saou <http://freshrpms.net/> 0.4.7-4
- Switch to the sources found in the 2.6.18-mm3 kernel since the others
  always made my test machine freeze, but these work.

* Tue Oct 10 2006 Matthias Saou <http://freshrpms.net/> 0.4.7-3
- Add the rpm release to the dkms module version, to make updating the module
  to a fixed same version work (--rpm_safe_upgrade doesn't work as advertised).
- Force modules install so that the same version can be overwritten instead of
  uninstalled by the old package's %%preun when updating.
- Add build time quiet flag for the scriplets. Undefine to do verbose testing.

* Mon Oct  9 2006 Matthias Saou <http://freshrpms.net/> 0.4.7-2
- Further patch Makefile to simplify the dkms.conf entries.

* Mon Oct  9 2006 Matthias Saou <http://freshrpms.net/> 0.4.7-1
- Initial RPM release.

