Name:           SocketW
Version:        031026
Release:        3%{?dist}
Summary:        Streaming socket C++ library designed to be easy to use
License:        LGPLv2+
Group:          System Environment/Libraries
Source0:        http://www.digitalfanatics.org/cal/socketw/files/%{name}%{version}.tar.gz
Patch0:         SocketW031026-path.patch
# Reported upstream by mail. Did not found open bugtracker.
Patch1:         SocketW031026-include.patch
# Fedora specific
Patch2:         SocketW031026.honor-Fedora-flags.patch
Url:            http://www.digitalfanatics.org/cal/socketw/
BuildRequires:  openssl-devel, dos2unix

%description
It supports Unix sockets and TCP/IP sockets with optional SSL/TLS (OpenSSL)
support. It allows you to write portable and secure network applications quickly
without needing to spend time learning low-level system functions or reading
OpenSSL manuals.

%package devel
Summary:        Files for compiling software that uses %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}%{version}

%patch0 -p1 -b .path
%patch1 -d src -p0 -b .include
%patch2 -p1 -b .fedora-flags

%build
make %{?_smp_mflags} shared CXXFLAGS="$RPM_OPT_FLAGS"

%install
make DESTDIR=%{buildroot} PREFIX=%{buildroot}%{_prefix} PREFIX_H=%{buildroot}%{_includedir}/%{name} PREFIX_L=%{buildroot}%{_libdir} install

# Remove static
rm %{buildroot}%{_libdir}/*.a

# correct README encoding
iconv -f ISO-8859-1 -t UTF-8 README > README.new
touch --reference README README.new
mv README.new README

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE README WhatsNew Todo examples docs
%{_libdir}/libSocketW.so.0
%{_libdir}/libSocketW.so.0.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/libSocketW.so

%changelog
* Sat Feb 9 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 031026-3
- Change group and small adjust -devel summary (thanks to Michael Schwendt).

* Mon Nov 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 031026-2
- Changes inspired by Volker Fröhlich review comments. Thanks.
- For devel requirement add %%{?_isa}.
- Correct README encoding
- Remove %%defattr
- Add to docs Todo file and examples docs dirs.
- Drop the "It is a" from the summary.
- Mail about forgotten include (Patch1: SocketW031026-include.patch) to upstream
    author. Add patch comment.
- Try honnor Fedora compile flags. Add patch2.

* Sun Aug 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 031026-1
- Spec imported from https://build.opensuse.org/package/view_file?file=SocketW.spec&package=SocketW&project=devel%3Alibraries%3Ac_c%2B%2B
    and reworked.
- Mailed to author request to update FSF address in license.
