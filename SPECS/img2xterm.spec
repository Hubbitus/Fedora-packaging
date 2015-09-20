Name:           img2xterm
Version:        1.0.0
Release:        1%{?dist}
Summary:        Tool to display images on the terminal

License:        Public Domain
URL:            https://github.com/rossy/img2xterm
Source0:        https://github.com/rossy/img2xterm/archive/v1.0.0.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  ImageMagick-devel, ncurses-devel

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
%setup -qn %{name}-%{version}

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
* Sun Sep 20 2015 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.0-1
- License issue https://github.com/rossy/img2xterm/issues/7 resolved - 1.0.0 relased.

* Sat Jul 25 2015 Pavel Alexeev (aka Pahan-Hubbitus) <Pahan@Hubbitus.info> - 0-1.git.e24d136
- Initial release