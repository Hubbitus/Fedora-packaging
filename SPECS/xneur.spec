Summary:		X Neural Switcher
Name:		xneur
Version:		0.9.9
Release:		2%{?dist}

License:		GPLv2+
Group:		User Interface/Desktops
URL:			http://www.xneur.ru
Source:		http://dists.xneur.ru/release-%{version}/tgz/%{name}-%{version}.tar.bz2

# It is needed fo build to EL-5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	fontconfig-devel, freetype-devel, glib2-devel, pcre-devel
BuildRequires:	libX11-devel, gstreamer-devel, freealut-devel >= 1.0.1
BuildRequires:	aspell-devel, libXpm-devel, imlib2-devel, xosd-devel
BuildRequires:	gettext-devel, libnotify-devel >= 0.4.0, gtk2-devel

# El5 http://fedoraproject.org/wiki/EPEL/GuidelinesAndPolicies#Distribution_specific_guidelines
Requires:		pkgconfig

%description
X Neural Switcher is a program for automatic (intelligent) keyboard layout
changing in the X Window System. It is mainly used to change between Russian
and English, but also supports Armenian, Belorussian, Bolgarian, Czech,
Georgian, German, Greek, Estonian, French, Kazakh, Lithuanian, Latvian, Polish,
Moldovan (Romanian), Spanish, Ukrainian and Uzbek.

%description -l ru
X Neural Switcher это программа для автоматического (интеллектуального)
переключения раскладок клавиатуры в X Window. Прежде всего он предназначен
для смены русской и английской раскладок, но также поддерживаются армянский,
белорусский, болгарский, чешский, грузинский, немецкий, греческий, эстонский,
французский, казахский, литовский, латвийский (латышский), польский, молдавский
(румынский), испанский, украинский и узбекский языки.

%package		devel
Summary:		Development files for %{name}
Group:		Development/Libraries
Requires:		%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
# Extra parameters needs to build on Fedora > 13. See https://bugzilla.gnome.org/show_bug.cgi?id=622550
%configure LIBNOTIFY_CFLAGS="%( pkg-config --cflags "libnotify >= 0.4.0" gtk+-2.0 )" LIBNOTIFY_LIBS="%( pkg-config --libs "libnotify >= 0.4.0" gtk+-2.0 )"

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

# remove static
rm %{buildroot}/%{_libdir}/{,%{name}}/*.{a,la}

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ABOUT-NLS TODO ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/%{name}/xneurrc*
%{_bindir}/%{name}
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/*.so.*
%{_libdir}/*.so.*
%{_mandir}/man?/*
%{_datadir}/%{name}


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/xneur/*.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/*


%changelog
* Wed Sep 22 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.9-2
- All changes inspired by Fedora review, thanks to Damian Wrobel and Martin Gieseking.
- Changed description to do not mention comparation (suggested Wikipedia variant
	with full languages list).
- Change license to GPLv2+ instead of GPLv2.
- Own %%{_libdir}/xneur/
- Explicit mention %%{_bindir}/%%{name}
- %%{_libdir}/xneur/*.so.* replaced by macros variant: %%{_libdir}/%%{name}/*.so.*
- Remove unneeded BR autoconf, automake, libtool
- Add BR gtk2-devel to build on Fedora 14+.
- Add extraparameters LIBNOTIFY_LIBS and LIBNOTIFY_CFLAGS to fix build on Fedora > 13.
    Please see commment above for more info.

* Wed Aug 11 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.9-1
- Import from http://mirror.yandex.ru/fedora/russianfedora/russianfedora/free/fedora/releases/13/Everything/source/SRPMS/xneur-0.9.9-1.fc13.src.rpm
	and fully revisited.