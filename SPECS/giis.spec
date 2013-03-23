Name:		giis
Summary:		Solution to undelete files "gET iT i sAY"
Summary(ru):	Решение для восстановления удалённых файлов
Summary(de):	Wiederherstellen gelöschter Dateien "gET iT i sAY"
# Version 4.7 is another product with GUI by default
Version:		4.6.2
Release:		3%{?dist}
URL:			http://giis.sf.net/
Source0:		http://www.giis.co.in/giis/%{name}_%{version}.tar.gz
# Source1 and Source2 - self written Service-file and wrapper to omit use /etc/inittab to once run on boot stage and then run each 20 minuts
Source1:		%{name}.daemon
Source2:		%{name}.init
Source3:		%{name}.service
License:		GPLv2+
Group:		Applications/System
BuildRequires:	kernel-devel dos2unix
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd

%Description
gET iT i sAY giis is an ext2/ext3 File Undelete Tool.

%Description -l ru
"gET iT i sAY" это решение, регулярно сканирующее состояние вашей файловой
системы затем чтобы сделать последующее восстановление случайно удалённых файлов
на ext2/ext3/ext4 системах делом простым и удобным.

%description -l de
"gET iT i sAY" ist ein Werkzeug zum Wiederherstellen gelöschter Dateien auf
ext2/ext3-Dateisystemen.

%package sysvinit
Summary:			Legacy sysvinit scripts for daemon
Summary(ru):		Устаревшие скрипты инициализации в стиле sysvinit
Summary(de):		Sysvinit-Skripte für den Daemon
Requires(post):	chkconfig
Requires(preun):	chkconfig, initscripts
Requires(postun):	initscripts
Requires:			%{name}%{?_isa} = %{version}-%{release}

%description sysvinit
May be needed f.e. on CentOS.

%description sysvinit -l ru
Могут понадобиться например на CentOS.

%description sysvinit -l de
Startdateien für z.B. CentOS.

%prep
%setup -q -n %{name}_%{version}

#Correct permission
chmod 0644 AUTHORS COPYING README ChangeLog

%build
pushd src
%configure
make %{?_smp_mflags}
popd

dos2unix README

%install
# Fix lineendings and remove executable permissions
find \( -iname '*.c' -or -iname '*.h' \) -exec sh -c 'F="{}"; touch --reference "$F" "$F.ref"; chmod -x $F; dos2unix "$F"; touch --reference "$F.ref" "$F"; rm "$F.ref"' \;

install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_sysconfdir}
install -d %{buildroot}/%{_initrddir}/
install -m 0644 config/%{name}.conf %{buildroot}/%{_sysconfdir}/
cd src
make install DESTDIR=%{buildroot}
install -m 0755 %{SOURCE1} %{buildroot}/%{_bindir}/
install -m 0755 %{SOURCE2} %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/%{_datarootdir}/%{name}
install -Dp -m 0644 %{SOURCE3} %{buildroot}/%{_unitdir}/%{name}.service

%post
%systemd_post giis.service
# rmdir needed, because giis check it on install, and if it exists fail installation
rmdir %{_datarootdir}/%{name} && %{name} -i &>/dev/null

%post sysvinit
/sbin/chkconfig --add %{name}
# rmdir needed, because giis check it on install, and if it exists fail installation
rmdir %{_datarootdir}/%{name} && %{name} -i &>/dev/null

%preun
%systemd_preun giis.service
rm -rf %{_datarootdir}/%{name}/*

%preun sysvinit
if [ $1 = 0 ]; then
	/sbin/service %{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
	rm -rf %{_datarootdir}/%{name}/*
fi

%postun
%systemd_postun_with_restart giis.service

# https://fedoraproject.org/wiki/Packaging:SysVInitScript#Initscripts_in_addition_to_systemd_unit_files
%triggerpostun -n %{name}-sysvinit -- %{name} < 4.6-15
/sbin/chkconfig --add %{name} >/dev/null 2>&1 || :

%files
%doc ChangeLog AUTHORS COPYING README
%{_bindir}/%{name}
%{_bindir}/%{name}.daemon
%{_unitdir}/%{name}.service
%{_datarootdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files sysvinit
%{_initrddir}/%{name}

%changelog
* Sun Nov 25 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6.2-3
- Add Requires: %%{name}%%{?_isa} = %%{version}-%%{release} to sysvinit subpackage.

* Sun Nov 18 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6.2-2
- Converting to use modern systemd macroses and target package for Fedora 18 only.
- Add German translation (thanks to Mario Blättermann).

* Sun Nov 11 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6.2-1
- Update to 4.6.2 with correct license file. Thanks to Lakshmipathi.

* Mon Nov 5 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6.1-2
- Review in progress, thanks to Mario Blättermann:
- Remove INSTALL file from docs.
- Fix line endings and permissions for the source code files.
- Remove cleaning in %%install and %%defattr'ibutes.
- Add Summary(ru).

* Sun Mar 25 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6.1-1
- Error on kernel 3.3 fixed - new version coming.
- Patches should be incorporated, so removing.

* Sat Mar 17 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6-15
- Add giis.service file, move legacy sysvinit inot subpackage

* Sun Jan 22 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6-14
- Some adoptation to resent Fedora versions and cleanup for review.

* Thu Jul 29 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6-13
- Remove invoke giis -r, because it delete himself.
- Add %%{_datarootdir}/%%{name} in files.
- Add Patch2: giis-4.6.retcode.patch

* Mon Jun 21 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6-12
- Got answer and add Patch1: giis_4.6-pathes.patch
- Add %%config(noreplace) attribute to %%{_sysconfdir}/%%{name}.conf
- Add %%{name} -i/-r into %%post and %%preun accordingly.

* Sun May 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 4.6-11
- New 4.6 version (4.7 version is just GUI for it)
- AUTHORS COPYING INSTALL README now in uppercase.
- Rebase giis-4.4.kernel-source_and_destdir.patch to 4.6 version.
- Do not enable by default ( /sbin/chkconfig --level 3456 %%{name} on; /sbin/service %%{name} start )
- Add %%{_sysconfdir}/%%{name}.conf

* Sat Apr 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 4.4-10
- Step to version 4.4
- Source0 suffix changed from .bz2 to .gz
- patch0 giis-4.3.kernel-source_and_destdir.patch adopted to new version and renamed to giis-4.4.kernel-source_and_destdir.patch
- File names changed (come from upstream):
	o AUTHORS to authors
	o COPYING to copying
	o README to readme
	o INSTALL to install
- $RPM_BUILD_ROOT raplaced by %%{buildroot}
- Remove removing inittab and crontab - it is not installed now.
- Unknown now %%{_initdir} replaced by %%{_initrddir}

* Sat Dec 20 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 4.3-9
- Step to version 4.3-9
- Source changed from %%{name}-%%{version}.tar.gz to http://downloads.sourceforge.net/%%{name}/%%{name}_%%{version}.tar.bz2
- Add %%{?_smp_mflags} to make
- Rewrite giis-4.3.kernel-source_and_destdir.patch. Source changed by strange way without version bump :(
- Add Source1: giis.daemon, Source2: giis.init and accordingly it installs it.
- Replace all direct mention of giis by %%{name} in %%files section.
- Remove config (it is not used any more?) %%config(noreplace) %%{_sysconfdir}/%%{name}.conf
- Correct premissions of ChangeLog to 0644 (rpmlint produce warning)
- Add BR dos2unix.
- Convert line endings in README
- Group changet to standard "Applications/System" (was - Recovery Tools)
- Add %%{?dist} into Release tag
- Add Requires(post): chkconfig
- Add %%post/%%preun stages to register/uregister service. Start it by default.
- Change License to GPLv2+ (was GNU GPL)

* Sat Nov 1 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 4.3-8
- Import spec initiated by author - lakshmi pathi.
- Reformat header with tabs
- Add BR: kernel-devel (for linux/ext3_fs.h)
- Add BuildRoot
- Add cleaning install dir in %%install and %%clean sections
- In build step to src.
- Replace direct-invoke of configure by macros, to handle all Fedora base flags and options
- Add patch0 to correct build.
- Add DESTDIR=$RPM_BUILD_ROOT to make install command - off course we can not write into /
- Add full section %%files
- Add install missing directories:
	install -d $RPM_BUILD_ROOT/%%{_bindir}
	install -d $RPM_BUILD_ROOT/%%{_sysconfdir}