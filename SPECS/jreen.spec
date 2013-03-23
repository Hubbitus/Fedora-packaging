%define snap 20110826

Name:    jreen
Summary: Qt XMPP Library
Version: 0.1.0
Release: 0.3.%{snap}%{?dist}

License: GPLv2+
URL:     http://gitorious.org/jreen
# git clone git://github.com/euroelessar/jreen.git
# git archive --prefix=jreen-0.1.0/ master | bzip2 > ../jreen-0.1.0-20110816.tar.bz2
Source0: jreen-%{version}-%{snap}.tar.bz2

BuildRequires: cmake
BuildRequires: qca2-devel
BuildRequires: qt4-devel

%description
%{summary}.
 
%package devel
Summary:  Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.
 
 
%prep
%setup -q -n jreen-%{version}
 
%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc GPL
%{_libdir}/libjreen.so.0*

%files devel
%{_libdir}/libjreen.so
%{_includedir}/jreen/
%{_libdir}/pkgconfig/lib%{name}.pc

%changelog
* Fri Aug 26 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 0.1.0-0.3.20110826
- 20110826 snapshot
- Add %%{_libdir}/pkgconfig/lib%%{name}.pc

* Tue Aug 16 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-0.2.20110816
- 20110816 snapshot

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-0.1.20010602
- first try, 0.1.0 20010602 git snapshot

