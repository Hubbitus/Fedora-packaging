Name:		Hubbitus-config
Version:		1
Release:		25%{?dist}
Summary:		Hubbitus system configuration
Summary(ru):	Настройки системы Hubbitus

Group:		System Environment/Base
License:		GPLv2+
URL:			http://hubbitus.info/rpm
Source0:		.screenrc
Source1:		.screenrc-remote
Source2:		.toprc
Source3:		.rpmmacros
Source4:		authorized_keys
Source5:		.bash_profile
Source6:		.bashrc
Source7:		.rsync_shared_options

Source50:		root.screenrc
Source51:		root.toprc
Source52:		root.bashrc

BuildArch:	noarch
Requires:		Hubbitus-release
Requires:		screen, mc, bash-completion, colorize, git, colorize, php, ferm
Requires:		wireshark, iotop, moreutils, grin, sshfs, htop, darkstat, glances
Requires:		strace, sysstat, dstat, psmisc, nethogs, telnet, elmon, trafshow
Requires:		the_silver_searcher
# Request for epel7 was: https://bugzilla.redhat.com/show_bug.cgi?id=1141182
Requires:		bmon
# Request for epel7 was: https://bugzilla.redhat.com/show_bug.cgi?id=1141199
Requires:		atop
Requires(pre):	/usr/sbin/useradd
Requires(post):subversion

%description
My initially settings of new system.
Mostly it contain Requires of useful packages and some settings.
Also creates pasha user without password but with access by keys.
THIS PACKAGE DOES NOT INTENDED FOR FOREIGN USE, but may be good idea to start
customize it for you own needs. Please note INSTALLS MY PUBLIC KEYS FOR access
to host by ssh without password (authorized_keys)! Use it on you own risk only.

%description -l ru
Мои основные настройки новой системы.
Прежде всего пакет содержит зависимости к другим пакетам, которые я считаю
необходимыми, но также ещё некоторые настройки и скрипты.
ПАКЕТ НЕ ПРЕДНАЗНАЧЕН ДЛЯ ВНЕШНЕГО ИСПОЛЬЗОВАНИЯ, но может стать хорошим стартом
для создания подобного для своих нужд. Пожалуйста учтите что ИНСТАЛЛИРУЮТСЯ МОИ
ОТКРЫТЕ КЛЮЧИ ДЛЯ БЕСПАРОЛЬНОГО ДОСТУПА К СЕРВЕРУ (authorized_keys).
Используйте только на свой страх риск.

%package gui
Group:		System Environment/Base
Summary:		Hubbitus system configuration
Requires:		%{name} = %{version}-%{release}
Requires:		firefox, thunderbird, gajim, meld, java-1.7.0-openjdk
Requires:		wireshark-gnome, mplayer

%description gui
My initially settings of new system with GUI.
Mostly it contain Requires of useful packages and some settings.
THIS PACKAGE DOES NOT INTENDED FOR FOREIGN USE, but may be good idea to start
customize it for own needs.

%description -l ru gui
Мои основные настройки новой системы c ГРАФИКОЙ.
Прежде всего пакет содержит зависимости к другим пакетам, которые я считаю
необходимыми, но также ещё некоторые настройки и скрипты.
ПАКЕТ НЕ ПРЕДНАЗНАЧЕН ДЛЯ ВНЕШНЕГО ИСПОЛЬЗОВАНИЯ, но моет быть хорошим стартом
для создания подобного для себя.

%prep
%setup -c -T

%build

%install
rm -rf %{buildroot}

install -dm 755 %{buildroot}{/home/_SHARED_,/home/pasha/bin,/root/bin,/home/pasha/.ssh,/root/.ssh}

install -pm 644 %{SOURCE0} %{buildroot}/home/pasha/
install -pm 644 %{SOURCE1} %{buildroot}/home/pasha/
install -pm 644 %{SOURCE2} %{buildroot}/home/pasha/
install -pm 644 %{SOURCE3} %{buildroot}/home/pasha/
install -pm 600 %{SOURCE4} %{buildroot}/home/pasha/.ssh/
install -pm 644 %{SOURCE5} %{buildroot}/home/pasha/
install -pm 644 %{SOURCE6} %{buildroot}/home/pasha/
install -pm 644 %{SOURCE7} %{buildroot}/home/pasha/

install -pm 600 %{SOURCE4} %{buildroot}/root/.ssh/
install -pm 644 %{SOURCE50} %{buildroot}/root/.screenrc
install -pm 644 %{SOURCE51} %{buildroot}/root/.toprc
install -pm 644 %{SOURCE52} %{buildroot}/root/.bashrc.hubbitus


%clean
rm -rf %{buildroot}

%pre
# Add the "pasha" user
/usr/sbin/useradd pasha 2>/dev/null || :

%post
function git_up(){
	[ -e "$2/.svn" ] && rm -rf "$2" # migration from SVN
	# git -C "$2" pull --strategy=recursive || git clone "$1" "$2"
	# Unfortunately git 1.8 (on epel7) does not known -C option, workaround
	mkdir -p "$2" ; pushd "$2"
	git pull --strategy=recursive 2>/dev/null || git clone "$1" .
	popd
}

# Checkout ~/bin
git_up 'https://github.com/Hubbitus/HuPHP.git' '/home/_SHARED_'
git_up 'https://github.com/Hubbitus/shell.scripts.git' '/home/pasha/bin'
git_up 'https://github.com/Hubbitus/shell.scripts.git' '/root/bin'

# Add once addon root .bashrc
grep -q hubbitus /root/.bashrc || echo '[ -f /root/.bashrc.hubbitus ] && . /root/.bashrc.hubbitus' >> /root/.bashrc

%files
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.screenrc
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.screenrc-remote
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.toprc
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.rpmmacros
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.bash_profile
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.bashrc
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/.rsync_shared_options
%attr(-,pasha,pasha) %config(noreplace) /home/pasha/bin
%config(noreplace) /root/.screenrc
%config(noreplace) /root/.toprc
%config(noreplace) /root/.bashrc.hubbitus
%config(noreplace) /root/bin
%dir %attr(0700,pasha,pasha) %config(noreplace) /home/pasha/.ssh
%attr(0600,pasha,pasha) %config(noreplace) /home/pasha/.ssh/authorized_keys
%attr(0600,root,root) %config(noreplace) /root/.ssh/authorized_keys
/home/_SHARED_

%files gui

%changelog
* Sat Mar 28 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1.25
- Cleanup root.bashrc file.

* Sat Mar 28 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1.24
- /root/.bashrc present in rootfiles package, so, deploy addon instead of conflict

* Sat Mar 28 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1-23
- Include root.bashrc.
- Add R trafshow, the_silver_searcher(ag) and php.
- Remove R subversion (but leave in Requires(post))
- Move glances R from -gui sub-package to main.
- Update authorized_keys to mention more my servers (ansible will come to replacee it).

* Thu Mar 26 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1-22
- In .bashrc conditionaly include /opt/grails/grails_autocomplete only if it exists.

* Fri Mar 06 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1-21
- Change check of svn to just dir .svn presence, to do not play with its versions and upgrades

* Fri Mar 06 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1-20
- Update git-up function with workaround to handle old 1.8 git on epel, which has not known -C option.

* Fri Mar 06 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1-19
- Add R telnet, elmon

* Tue Dec 16 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-18
- Add R nethogs.

* Fri Oct 24 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-17
- Add R psmisc.

* Fri Sep 12 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-16
- Disable as it is not awailable for epel7:
# https://bugzilla.redhat.com/show_bug.cgi?id=1141182
#Requires:	bmon
# https://bugzilla.redhat.com/show_bug.cgi?id=1141199
#Requires:	atop
- Add R darkstat.

* Wed Apr 16 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-15.2
- Add -C option in git, add --strategy=recursive option.

* Tue Apr 15 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-15.1
- Migrate also bin-scripts from private svn to github git repository. Unify root and not-root.
- Drop svn repos support.

* Mon Apr 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-14
- Migrate HuPHP framework from private svn to git repo on github.
- Bump version to 1-14

* Tue Oct 4 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-12
- Add .rsync_shared_options

* Mon Oct 3 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-11
- Add strace to dep.

* Sun Oct 2 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-10
- Correct files owner (pasha).
- Remove httpd-itk dependency.

* Wed Jun 15 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-9
- Add .screenrc-remote

* Tue Jun 7 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-8
- Add R atop, iotop

* Mon Jun 6 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-7
- Add R sshfs

* Fri May 6 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-6
- Add R grin

* Fri Mar 11 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-5
- Add R ferm
- Add R in gui - java-1.6.0-openjdk-plugin
- Add wireshark and wireshark-gnome in appropriate packages.

* Tue Mar 8 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-4
- Add R moreutils.
- Add Requires: firefox, thunderbird, gajim, meld into GUI subpackage.
- Add empty "%%files gui" section to generate subpackage.

* Tue Mar 8 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-3
- Silence user add if they exists.

* Tue Mar 8 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1-2
- Add pasha .bash_profile and .bashrc
- Update svn repos if they checkouted.

* Thu Sep 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1-1
- Initial release.
