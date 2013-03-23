Summary:		VNC server for the current X11 session
Summary(ru):	VNC-сервер для текущей сессии X11
Name:		x11vnc
Version:		0.9.8
Release:		14%{?dist}
License:		GPLv2
Group:		User Interface/X
URL:			http://www.karlrunge.com/x11vnc/
Source0:		http://downloads.sourceforge.net/libvncserver/%{name}-%{version}.tar.gz

BuildRequires:	libjpeg-devel, zlib-devel, openssl-devel
BuildRequires:	xorg-x11-proto-devel, libXext-devel, libXtst-devel
BuildRequires:	libXfixes-devel, libvncserver-devel

BuildRequires:	java-1.6.0-openjdk-devel

# In Fedora 12 /usr/include/X11/extensions/XInput.h in libXi-devel but in
# previous versions in xorg-x11-proto-devel /usr/include/X11/extensions/shmproto.h
# placed in libXext-devel in F12 and in xorg-x11-proto-devel early.
%if 0%{?fedora} > 11
BuildRequires:	libXi-devel libXext-devel
%else
BuildRequires:	xorg-x11-proto-devel
%endif
Requires:		Xvfb

# Fedora don't want hardcoded rpaths.
Patch1:		x11vnc-0.9.8-disableRpath.patch
# According to new paths add new include to build. I think it is Fedora-related.
Patch2:		x11vnc-0.9.8-XShm-explicit-include.patch

# Package intended to EL-5 too, so we still need define BuildRoot
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
What WinVNC is to Windows x11vnc is to X Window System, i.e. a server
which serves the current X Window System desktop via RFB (VNC)
protocol to the user.

Based on the ideas of x0rfbserver and on LibVNCServer it has evolved into a
versatile and productive while still easy to use program.

%description -l ru
Это подобно VNC-серверу под Windows - VNC-сервер, который предоставля-
ет доступ к текущей X-сессии пользователя по протоколу (VNC).
Таким образом, Вы всегда можете вернуться к работе удаленно, даже если
сессия была стандартно запущена локально. Более того, доступ к Логин-
менеджеру также может быть осуществлена (GDM, KDM, XDM etc)

Базируется на идее x0rfbserver и LibVNCServer x11vnc эволюционировал
в гибкий и производительный инструмент, который, однако, остается
просто в использовании.

%package		javaviewers
Version:		%{version}
Summary:		VNC clients (browser java applets)
Summary(ru):	VNC-клиенты в виде java-аплетов для браузеров
Requires:		%{name} = %{version}-%{release}
License:		GPLv2+
Group:		User Interface/X
BuildArch:	noarch
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	jpackage-utils


%description	javaviewers
The package contains the corresponding java clients for %{name}. They
can be used with any java-enabled browser and provide an easy access to
the server without the need to install software on the client machine.

%description -l ru	javaviewers
Java-клиенты для использования совместно с %{name} прямо из браузера
без необходимости ставить какой бы то ни было софт.

Должно по идее работать с любым современным браузером, где есть
поддержка Java

%prep
%setup -q
%patch1 -p0 -b .rpath

%if 0%{?fedora} > 11
%patch2 -p0 -b .XShm
%endif

# fix source perms for the -debuginfo package rpmlint warnings
find -name "*.c" -o -name "*.h" -exec %{__chmod} 0644 {} \;

for file in README AUTHORS; do
	# ISO-8859-1 is my assumption.
	iconv -f ISO-8859-1 -t UTF-8 "$file" > "$file.new"
	touch --reference "$file" "$file.new"
	%{__mv} "$file.new" "$file"
done

# Delete prebuilt binaries
find -name '*.jar' -exec rm {} \;

%build
%configure --with-system-libvncserver --without-tightvnc-filetransfer

# First rebuild jars, what have been removed in %%prep.
pushd classes/ssl/src
%{__make} %{?_smp_mflags}
	# Alternative to patch Makefiles.
	for jarfile in *.jar; do
	%{__ln_s} src/$jarfile ../;
	%{__ln_s} ssl/src/$jarfile ../../;
	done
popd

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

# And Java viewers
pushd classes/ssl
%{__make} install DESTDIR="%{buildroot}"
popd

# Rename README file to avoid name bump
%{__mv} classes/ssl/src/tight/README classes/ssl/src/tight/README.tight
%{__mv} classes/ssl/src/ultra/README classes/ssl/src/ultra/README.ultra

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_mandir}/man1/x11vnc.1*
%{_bindir}/x11vnc
%{_datadir}/applications/x11vnc.desktop

%files javaviewers
%defattr(-,root,root,-)
%doc classes/ssl/README classes/ssl/src/tight/README.tight classes/ssl/src/ultra/README.ultra
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/classes/ssl/README

%changelog
* Tue Oct 6 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-14
- Make -javaviewers subpackage noarch.

* Sun Oct 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-13
- Small fis requires release.
- Rename README file to avoid name bump

* Fri Sep 25 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-12
- Own %%{_datadir}/%%{name} instead of %%{_datadir}/%%{name}/classes
- Add Requires: %%{name} = %%{version}-%%{release} in subpackage.
- Change summary and description for javaviewers subpackage.
- Remove %%doc marker from man-page.
- %%defattr(-,root,root,0755) -> %%defattr(-,root,root,-)
- Add classes/ssl/src/tight/README classes/ssl/src/ultra/README files into
	javaviewers subpackage %%doc (thank you Orcan Ogetbil)
- ln -s replaced by %%{__ln_s}
- Set License: GPLv2+ for javaviewers subpackage (Thanks Spot)

* Mon Aug 31 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-11
- Remove all prebuilt *.jar-files in %%prep section and try build it from source.
- Add BR java-1.6.0-openjdk-devel
- Introduce new subpackage x11vnc-javaviewers.
- Add separate build java-viewers.
- Add Russian localized versions of Summary and descrioptions.

* Wed Aug 26 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-10
- Fix some spelling, change some cosmetic things.
- Delete Patch0 and hacks to link with system lzo package - it is not needed
	anymore as we link it with systel libvncserver instead.
- Delete BR lzo-devel
- Remiove empty directory %%{_datadir}/%%{name}/

* Sun Aug 9 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-9
- Add Requires: Xvfb

* Fri Aug 7 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-8
- Link to shared lzo instead of minilzo for all (not only EL-5).
- Add BuildRequires: /usr/include/X11/extensions/XShm.h
- Patch2: x11vnc-0.9.8-XShm-explicit-include.patch
- Step to conditional BR for Fedora 12, add
	Patch2: x11vnc-0.9.8-XShm-explicit-include.patch to build on it.

* Tue Aug 4 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-7
- Change license to GPLv2 without plus according to x11vnc.c
	source (thanks to Christian Krause).
- For consistency macros usage replace "ln -s" by %%{__ln_s},
	mv by %%{__mv} and similar (chmod, sed).
- Change find call to avoid using xargs in chmod sources command.

* Wed Jul 29 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-6
- Build with openssl unconditionally.
- Add Patch1: x11vnc-0.9.8-disableRpath.patch
- fix source perms for the -debuginfo package rpmlint warnings

* Tue Jul 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-5
- Try use lzo instead of minilzo in EL-5 (minilzo is not bundled in it).
- Try use system libvncserver library (--with-system-libvncserver
	configure option) instead of bundled one.
- System libvncserver built without tightvnc-filetransfer support.
	Now disable it there (--without-filetransfer)
	And according to it change License to only GPLv2+
	./configure --help misleading, using --without-tightvnc-filetransfer

* Tue Jul 21 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-4
- All changes inspired by started Fedora Review (thank you to Christian Krause).
- README and AUTHORS files converted into UTF-8.
- Explicit mention previous author in changelog and delet old entries of it.
- Source renamed to Source0.
- Source0 URL changed to long (correct) variant:
	http://downloads.sourceforge.net/libvncserver/%%{name}-%%{version}.tar.gz
	was http://dl.sf.net/libvncserver/x11vnc-%%{version}.tar.gz
- Add BR: /usr/include/X11/extensions/XInput.h; In F12 it is located in
	libXi-devel but in previous versions in xorg-x11-proto-devel
	so, to do not make conditional requires, require explicit file.
- Remove prebuild binaries clients.
- Remove Requires: minilzo it will be automatically propogated.
- Add BR: libvncserver-devel

* Fri Jul 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-3
- Add BR openssl-devel to provide SSL capability (thanks Manuel Wolfshant).
- Requires: minilzo, BR lzo-devel and Patch0: 
	11vnc-0.9.8-use-system-minilzo.patch to use system version of library.
- Add "and GPLv2" to License. See comment above why.
- Add BuildRequires: libXfixes-devel

* Fri Jul 10 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.8-2
- Import http://packages.sw.be/x11vnc/x11vnc-0.9.7-1.rf.src.rpm to maintain it in fedora:
	Packager: Dag Wieers <dag@wieers.com>
	Vendor: Dag Apt Repository, http://dag.wieers.com/apt/
- Step to version 0.9.8
- Reformat spec with tabs.
- Comment out (leave for history) Packager and Vendor tags
- Remove defines of several macros like dtag, conditional _without_modxorg
- Remove all stuff around conditional build _without_modxorg
- Add -%%(%%{__id_u} -n) part into buildroot.
- Make setup quiet.
- Remove "rf" Release suffix and replace it by %%{?dist}
- License from GPL changed to GPLv2+
