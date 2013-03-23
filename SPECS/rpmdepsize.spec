# rpmdepsize.spec.  Generated from rpmdepsize.spec.in by configure.

Name:           rpmdepsize
Version:        1.0
Release:        1%{?dist}
Summary:        Visualize RPM dependencies

Group:          Development/Libraries
License:        GPLv2+
URL:            http://et.redhat.com/~rjones/rpmdepsize/
Source0:        http://et.redhat.com/~rjones/rpmdepsize/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-sexplib-devel
BuildRequires:  ocaml-lablgtk-devel >= 2.10.1
BuildRequires:  ocaml-camlp4-devel

# The program embeds a python script, which has these requirements:
Requires:       python
Requires:       yum >= 3.2.21


%description
rpmdepsize is an interactive graphical tool for visualizing the size
of RPM dependencies.

It's useful for shaming RPMs that have too many dependencies or pull
in large amounts of data because of indirect dependencies.


%prep
%setup -q


%build
%{configure}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/rpmdepsize


%changelog
* Fri Mar 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0-1
- Initial RPM release.
