# Review Request: https://bugzilla.redhat.com/show_bug.cgi?id=1197517

Name:           elmon
Version:        13b1
Release:        3%{?dist}
Summary:        Performance monitoring tool

License:        GPLv3
URL:            http://elmon.sourceforge.net/
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}_%{version}.tar

BuildRequires:  ncurses-devel

%description
elmon is a performance monitoring tool for Linux. It provides an ncurses
interface as well as the ability to save the data to a CSV file. elmon is based
on nmon by Nigel Griffiths and the CSV output is compatible with nmon processing
tools.

elmon provides performance information on CPU, memory, network, disk, file
system usage, etc.

If you are familiar with nmon, here are the additional features that elmon
supports:
o Multi-column output.
o Interactive Help Menu
o Stat sections are displayed in the order that the user enables them
o Long term CPU graph will use up the entire width of the screen
o Supports subsecond screen refreshes
o New Memory/Swap graph
o Multiple bug fixes (including several bug fixes supplied by David Baril on
nmon forum).


%prep
%setup -q -c %{name}-%{version}


%build
%{make_build} elmon_x86_rhel52


%install
mkdir -p %{buildroot}/%{_bindir}
install elmon_x86_rhel52 %{buildroot}/%{_bindir}/%{name}

%files
%doc change_log.txt
%license license.txt
%{_bindir}/%{name}


%changelog
* Wed Oct 26 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 13b1-3
- Drop BR gcc

* Tue Sep 13 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 13b1-2
- Shorter description.
- Cleanup.
- Add BR gcc
- Use make_build macros.

* Sun Mar  1 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 13b1-1
- Initial spec
