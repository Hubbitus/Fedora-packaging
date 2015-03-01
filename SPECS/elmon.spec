Name:           elmon
Version:        13b1
Release:        1%{?dist}
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
	- 2 or 3 columns worth of data will be displayed if your terminal is wide
	- Allows you to see more information and reduces wasted screen space
o Interactive Help Menu
	- Supports using the arrow keys to highlight options.  Press Enter to
	  enable/disable the option
	- If your terminal supports the mouse, you can click on items in the menu
	  to enable/disable them
o Stat sections are displayed in the order that the user enables them
	- This allows the user to control the layout of the screen and determine
	  the order of the displayed statistics
o Long term CPU graph will use up the entire width of the screen instead of
being limited to 72 columns
	- This allows you see longer CPU history and better use available screen
	  space.
o Supports subsecond screen refreshes
	- You can set elmon to refresh the screen as often as every 0.1 seconds.
	- However, the more often the screen is refreshed the more CPU cycles elmon
	  will take.
o New Memory/Swap graph
	- The graph shows how much memory and swap space are currently being used
o Multiple bug fixes (including several bug fixes supplied by David Baril on
nmon forum).


%prep
%setup -q -c %{name}-%{version}


%build
make %{?_smp_mflags} elmon_x86_rhel52


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
install elmon_x86_rhel52 %{buildroot}/%{_bindir}/%{name}

%files
%doc change_log.txt
%license license.txt
%{_bindir}/%{name}


%changelog
* Sun Mar  1 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 13b1-1
- Initial spec
