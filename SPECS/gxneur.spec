%global SVN	859

Summary:		GTK front-end for X Neural Switcher (xneur)
Name:		gxneur
Version:		0.12.0
Release:		2%{?SVN:.svn%{SVN}}%{?dist}

Group:		User Interface/Desktops
License:		GPLv2+
URL:			http://www.xneur.ru
# In case of SVN build tarball generated with tese set of commands:
# svn export svn://xneur.ru:3690/xneur/%%{name} %%{name}-%%{version}
# tar -jcf %%{name}-%%{version}-svn%%{SVN} %%{name}-%%{version}
Source:		http://dists.xneur.ru/release-%{version}/tgz/%{name}-%{version}%{?SVN:-svn%{SVN}}.tar.bz2
Source1:		gxneur.desktop

# For EL5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	desktop-file-utils, pcre-devel, libglade2-devel, enchant-devel
BuildRequires:	gettext-devel, gtk2-devel, GConf2-devel
BuildRequires:	xneur-devel = %{version}
%if 0%{SVN}
BuildRequires:	libtool
%endif

# Requirex explicit full versioned requires because not only labriry used. gxneur only GUI to xneur config daemon and relies on
# concrete xneur futures, including svn revision fixes if that svn build.
Requires:		xneur = %{version}-%{release}

%description
GTK front-end for X Neural Switcher (xneur).

%description -l ru
GTK интерфейс для Интеллектуального переключателя клавиатурных раскладок (xneur)

%prep
%setup -q


%build
%if 0%{SVN}
./autogen.sh
%endif

export XNEUR_LIBS="-lxnconfig -lpcre -lX11 -ldl"
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications	\
	%{SOURCE1}

%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
	if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
	fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ABOUT-NLS COPYING ChangeLog NEWS
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*

%changelog
* Sat Feb 5 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.12.0-2.svn859
- Rebuild svn revision 859. See update info for xneur for more details.

* Wed Feb 2 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.12.0-1
- New version 0.12.0

* Fri Jan 28 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.11.1-2.svn844
- Build postrelease 0.11.1-svn844 in hope it fix Shift + Tab problem.

* Tue Nov 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.11.1-1
- New 0.11.1 version.
- BR aspell-devel replaced by enchant-devel.

* Thu Nov 18 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.10.0-4
- Remove empty README and TODO files by insistence of Martin Gieseking.

* Wed Nov 17 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.10.0-3
- Changes inspired by comments in review request.
- License changed to GPLv2+ from GPLv2
- In .desktop file removed icon extension (.png)
- Removed BRs: autoconf, automake, autoheader, libtool as configure script does not rebuilding in packaging process.
- More precise in file including.
- Add BR GConf2-devel

* Fri Oct 8 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.10.0-2
- New 0.10.0 version.

* Wed Aug 11 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.9-1
- Import from http://mirror.yandex.ru/fedora/russianfedora/russianfedora/free/fedora/releases/13/Everything/source/SRPMS/gxneur-0.9.9-1.fc13.src.rpm
	and fully rewrite.