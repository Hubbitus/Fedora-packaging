%global commit0 e24d13686c10c25f79f7a2841d8bb95c5571d261
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           img2xterm
Version:        0
Release:        1%{?shortcommit0:.git.%{shortcommit0}}%{?dist}
Summary:        Tool to display images on the terminal

License:        ???
URL:            https://github.com/rossy/img2xterm
Source0:        https://github.com/rossy/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  ImageMagick-devel, ncurses-devel
#Requires:

%description
img2xterm is a program that can display bitmap images on 256-colour terminals by
converting them into Unicode block characters and xterm compatible control
sequences. Based on software by lachs0r and Xebec for creating colourful
cowfiles, img2xterm improves on the colour selection and block printing logic,
providing cleaner output on terminals with nice bitmap fonts.

img2xterm uses a modified version of the algorithm used in xterm256-conv
in order to have an accurate representation of the upper 240 colours used
in xterm. Modification was needed in order to fix the range of the grey
ramp.

%prep
%setup -qn %{name}-%{commit0}

%build
make %{?_smp_mflags}


%install
%make_install PREFIX="%{buildroot}%{_prefix}"

rm -rf %{buildroot}{%{_bindir}/img2cow,%{_mandir}/man6/img2cow.6*}

%files
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man6/%{name}.6*

%changelog
* Sat Jul 25 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0-1.git.e24d136
- Initial release