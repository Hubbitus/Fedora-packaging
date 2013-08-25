Name:           ulatencyd
Version:        0.5.0
Release:        1
Summary:        Daemon to minimize latency on a Linux system using cgroups
Summary(ru):    Демон для минимизации задержек на Linux системе используя cgroups
URL:            https://github.com/poelzi/ulatencyd

Group:          System Environment/Base
License:        GPLv3+
Source0:        https://github.com/poelzi/%{name}/archive/%{version}.tar.gz

BuildRequires:  cmake glib2-devel dbus-glib-devel dbus-python-devel PyQt4 polkit-devel libxcb-devel
BuildRequires:  lua-devel lua-posix doxygen perl-Moose pandoc libcgroup-devel libXau-devel
Requires:       dbus-python systemd lua lua-posix
BuildRequires:  systemd

%description
== What is ulatency ==
Ulatency is a daemon that controls how the Linux kernel will spend it's
resources on the running processes. It uses dynamic cgroups to give the kernel
hints and limitations on processes.

It strongly supports the lua scripting language for writing rules and the
scheduler code.

== What tries it to fix ==
The Linux scheduler does a pretty good job to give the available resources to
all processes, but this may not be the best user experience in the desktop case.
It monitors the system and categorizes the running processes into cgroups.
Processes that run wild to slow down the system by causing massive swapping will
be isolated.

%description -l ru
== Что из себя представляет ulatency ==
Прежде всего это демон контролирующий как ядро Linux распределяет ресурсы между
выполняющимися процессами. Он использует динамические cgroups политики для
предоставления ядру подсказок и ограничений.

Использует язык lua для написания правил.

== Что пытается исправить ==
Планировщик ядра Linux делает весьма хорошую работу по распределению ресурсов
между процессами, но это может работать не лучшим образом по ожиданиям
пользователей при использовании его в качестве desktop системы.

Ulatencyd отслеживает процессы в системе и распределяет их по группам cgroups.
Процессы которые требуют слишком много ресурсов и приводящие к замедлению
системы, использованию swap изолируются динамически.

Это позволяет иметь всегда отзывчивую систему, даже если в фоне выполняется
какой-то процесс который может длиться весьма продолжительное время.

%prep
%setup -q

# Remove bundled libs
#rm -rf src/{bc,coreutils,proc}/*

# Correct hardcoded pathes
sed -i.sed 's#SET(SYSTEMD_DIR "/lib/systemd/system" CACHE STRING#SET(SYSTEMD_DIR "%{_unitdir}" CACHE STRING#' CMakeLists.txt
sed -i.sed 's#DESTINATION ${CMAKE_INSTALL_PREFIX}/man/#DESTINATION ${CMAKE_INSTALL_PREFIX}/share/man/#' docs/CMakeLists.txt

%build
cmake \
  -DLIBCGROUPS=0 \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DENABLE_DBUS=1 \
  -DLUA_JIT=0 \
  .

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.quamquam.%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/simple.d/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/scheduler/*.lua
%config(noreplace) %{_sysconfdir}/%{name}/rules/*.lua
%{_unitdir}/%{name}.service
%{_bindir}/run-game
%{_bindir}/run-single-task
%{_bindir}/ulatency
%{_bindir}/ulatency-gui
%{_sbindir}/%{name}
%{_libdir}/../lib/%{name}/*.lua
%{_libdir}/../lib/%{name}/modules/simplerules.so
%{_libdir}/../lib/%{name}/modules/xwatch.so
%{_datadir}/man/man1/run-game.1*
%{_datadir}/man/man1/ulatency.1*
%{_datadir}/man/man1/run-single-task.1*
%{_datadir}/man/man1/ulatency-gui.1*
%{_datadir}/man/man8/%{name}.8*
%{_datadir}/polkit-1/actions/org.quamquam.%{name}.policy

%changelog
* Sun Aug 25 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.5.0-1
- Import package from ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/home%3A/awk2007%3A/scm/Fedora_17/src/ulatencyd-9999-9.1.src.rpm
  was created Tue May 03 2011 with version 9999-9.1 by Anonymous (for the infor and clear useless changelog entry).
- Rework to prepare for Fedora.
