Name:		test
Version:		1
Release:		1%{?dist}
Summary:		For tests RPM build things

Group:		System Environment/Libraries
License:		GPLv2+
#URL:			local
Source0:		test.macros
BuildArch:	noarch

%description
Spec for tests.

%prep

%include %{SOURCE0}
%{testmacros}

%build


%install
rm -rf %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)


%changelog
* Sun May 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1-1
- Initial spec.