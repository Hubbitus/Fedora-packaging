#% global HGrev 1032

Summary:       KDE frontend for X Neural Switcher (xneur)
Summary(ru):   KDE интерфейс для X Neural Switcher (xneur)
Name:          kdeneur
Version:       0.17.0
Release:       1%{?HGrev:.hg%{HGrev}}%{?dist}

Group:         User Interface/Desktops
License:       GPLv2+
URL:           http://www.xneur.ru
%if 0%{?HGrev}
# Sources now in mercurial. Tarball from author to fix last deprecated error.
Source:        kdeneur-%{version}+hg%{HGrev}.orig.tar.gz
%else
Source:        https://launchpad.net/~andrew-crew-kuznetsov/+archive/xneur-stable/+files/%{name}_%{version}.orig.tar.gz
%endif
Source1:       kdeneur.desktop

BuildRequires: desktop-file-utils, pcre-devel, qt-devel, kdelibs-devel
BuildRequires: xneur-devel = %{version}
%if 0%{?HGrev}
BuildRequires: libtool
%endif

# Require explicit full versione because not only labriry used. This is only GUI to xneur config daemon and relies on
# concrete xneur futures, including concrete revision fixes if that SCM build.
Requires:      xneur = %{version}-%{release}

%description
KDE front-end for X Neural Switcher (xneur).

%description -l ru
KDE интерфейс для Интеллектуального переключателя клавиатурных раскладок (xneur)

%prep
%setup -q

# rpmlint happy on W: spurious-executable-perm /usr/src/debug/kdeneur-0.17.0/src/tabbar.h
find -iname '*.h' -exec chmod -x {} \;

%build
%if 0%{?HGrev}
./autogen.sh
%endif

#export XNEUR_LIBS="-lxnconfig -lpcre -lX11 -ldl"
#export XNEUR_LIBS="-lxnconfig -lpcre"

%configure
make %{?_smp_mflags} CXXFLAGS=" -I%{_kde4_includedir}/ -L%{_kde4_libdir}/kde4/devel/ -lkdecore %{optflags}"


%install
make DESTDIR=%{buildroot} install

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%find_lang %{name} --with-qt --with-kde

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ABOUT-NLS COPYING ChangeLog NEWS
%{_bindir}/%{name}
%{_datadir}/%{name}
# To do not list files twice it must be listed by find_lang helper
%exclude %{_datadir}/%{name}/i18n/*.qm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*

%changelog
* Mon Dec 2 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.17.0-1
- Initial attempt package new frontend for xneur
