Name:		Hubbitus-config
Version:		1
Release:		12
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

BuildArch:	noarch
Requires:		Hubbitus-release
Requires:		screen, mc, bash-completion, colorize, subversion, git
Requires:		moreutils, ferm, wireshark, grin, sshfs, atop, iotop, strace
Requires(pre):	/usr/sbin/useradd
Requires(post):subversion

%description
My initially settings of new system.
Mostly it contain Requires of useful packages and some settings.
Also creates pasha user without password but with access by keys.
THIS PACKAGE DOES NOT INTENDED FOR FOREIGN USE, but may be good idea to start
customize it fo own needs.

%description -l ru
Мои основные настройки новой системы.
Прежде всего пакет содержит зависимости к другим пакетам, которые я считаю
необходимыми, но также ещё некоторые настройки и скрипты.
ПАКЕТ НЕ ПРЕДНАЗНАЧЕН ДЛЯ ВНЕШНЕГО ИСПОЛЬЗОВАНИЯ, но моет быть хорошим стартом
для создания подобного для себя.

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
customize it fo own needs.

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


%clean
rm -rf %{buildroot}

%pre
# Add the "pasha" user
/usr/sbin/useradd pasha 2>/dev/null || :

%post
# $1 - svn URL
# $2 - svn local dir
function svn_up(){
	if svn info "$2" &>/dev/null ; then
	svn up "$2"
	else
	svn co "$1" "$2"
	fi
}

# Checkout ~/bin
svn_up "svn+ssh://pasha@x-www.info/svn/scripts/trunk" "/home/pasha/bin"
svn_up "svn+ssh://pasha@x-www.info/svn/scripts/trunk/root" "/root/bin"
svn_up "svn+ssh://pasha@x-www.info/svn/_SHARED_/trunk" "/home/_SHARED_"

%files
%defattr(-,root,root,-)
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
%config(noreplace) /root/bin
%attr(0600,pasha,pasha) %config(noreplace) /home/pasha/.ssh/authorized_keys
%attr(0600,root,root) %config(noreplace) /root/.ssh/authorized_keys
/home/_SHARED_

%files gui

%changelog
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