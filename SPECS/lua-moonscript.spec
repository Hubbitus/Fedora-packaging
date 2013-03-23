%global luaver 5.1
%global luapkgdir %{_datadir}/lua/%{luaver}

Name:           lua-moonscript
Version:        0.1.0
Release:        2%{?dist}
Summary:        A little language that compiles to Lua

License:        MIT
URL:            http://moonscript.org/
# Source only available from Git; instructions below
# git clone git://github.com/leafo/moonscript.git
# git archive --format=tar --prefix=%%{name}-%%{version}/ v%%{version} \
# | xz - > %%{name}-%%{version}.tar.xz
Source0:        moonscript-%{version}.tar.xz

BuildArch:      noarch
BuildRequires:  lua >= %{luaver}
BuildRequires:  lua-alt-getopt >= 0.7
BuildRequires:  lua-filesystem >= 1.5
BuildRequires:  lua-lpeg >= 0.10
Requires:       lua >= %{luaver}
Requires:       lua-alt-getopt >= 0.7
Requires:       lua-filesystem >= 1.5
Requires:       lua-lpeg >= 0.10
# lua-inotify is recommended, but not required

%description
MoonScript is a dynamic scripting language that compiles into Lua. It
gives you the power of Lua combined with a rich set of features.

MoonScript can either be compiled into Lua and run at a later time, or
it can be dynamically compiled and run using the moonloader. It’s as
simple as require "moonscript" in order to have Lua understand how to
load and run any MoonScript file.

Because it compiles right into Lua code, it is completely compatible
with alternative Lua implementations like LuaJIT, and it is also
compatible with all existing Lua code and libraries.

The command line tools also let you run MoonScript directly from the
command line, like any first-class scripting language.


%prep
%setup -q -n moonscript-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p moon moonc $RPM_BUILD_ROOT%{_bindir}/
install -p dump $RPM_BUILD_ROOT%{_bindir}/moon-dump
mkdir -p $RPM_BUILD_ROOT%{luapkgdir}
cp -pr moonscript $RPM_BUILD_ROOT%{luapkgdir}/


%check
lua test.lua


%files
%doc README.md docs todo
%{_bindir}/moon
%{_bindir}/moonc
%{_bindir}/moon-dump
%{luapkgdir}/moonscript


%changelog
* Thu Sep  8 2011 Michel Salim <salimma@fedoraproject.org> - 0.1.0-2
- Clean up spec file
- Add explicit checkout instructions

* Tue Aug 16 2011 Michel Salim <salimma@fedoraproject.org> - 0.1.0-1
- Initial package
