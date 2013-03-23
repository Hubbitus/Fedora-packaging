%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:		sk1libs
Version:		0.9.1
Release:		2%{?dist}
Summary:		Universal vector graphics translator

Group:		Applications/Multimedia
License:		LGPLv2+
URL:			http://sk1project.org/modules.php?name=Products&product=uniconvertor
Source0:		http://uniconvertor.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:	python-devel, lcms-devel, zlib-devel, libjpeg-turbo-devel
BuildRequires:	freetype-devel
Requires:		python-imaging
Requires:		python-reportlab

%description
sk1libs is a universal vector graphics library for Python.

%prep
%setup -q

# Remove forbidden content
rm -rf src/ft2engine/fallback_fonts/*.ttf
# src/imaging/* src/libpdf/* src/pycms/*
find src/imaging/ src/libpdf/ src/pycms/ -type f -not -name __init__.py -delete

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Fix permissions
chmod a+x %{buildroot}%{python_sitearch}/sk1libs/__init__.py

# Don't duplicate documentation
rm -f %{buildroot}%{python_sitearch}/sk1libs/GNU_LGPL_v2

%files
%doc README
%doc GNU_LGPL_v2
%{python_sitearch}/*


%changelog
* Mon Dec 12 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-2
- Add neccasary BR.

* Sat Dec 3 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.9.1-1
- Import package from http://sailer.fedorapeople.org/sk1libs-0.9.1-1.fc16.src.rpm

* Sun Nov 13 2011 Thomas Sailer <t.sailer@alumni.ethz.ch> - 0.9.1-1
- initial package
