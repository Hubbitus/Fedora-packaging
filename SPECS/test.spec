Name:		test
Version:		1
Release:		2%{?dist}
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

%triggerun -- test < 1-2
echo "[triggerun -- test < 1-2] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%triggerun -- test > 1-1
echo "[triggerun -- test > 1-1] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%triggerin -- test < 1-2
echo "[triggerin -- test < 1-2] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%triggerin -- test > 1-1
echo "[triggerin -- test > 1-1] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%triggerpostun -- test < 1-2
echo "[triggerpostun -- test < 1-2] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%triggerpostun -- test > 1-1
echo "[triggerpostun -- test > 1-1] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%pre
echo "[pre] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%preun
echo "[preun] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%post
echo "[post] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2

%postun
echo "[postun] \$0=[$0]; \$1=[$1]; \$2=[$2]; \$3=[$3]; \$4=[$4]; \$5=[$5]" 1>&2


%files
%defattr(-,root,root,-)


%changelog
* Mon Apr 14 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 1-2
- Test triggers:
	http://rpm.org/api/4.4.2.2/triggers.html
	http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch10s02.html

* Sun May 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1-1
- Initial spec.