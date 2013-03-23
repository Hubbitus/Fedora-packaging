%define contentdir /var/www
%define mmn 20051115
%define mpms worker event

Summary:		MPM Itk for Apache HTTP Server
Name:		httpd-itk
Version:		2.2.22
Release:		4%{?dist}
URL:			http://mpm-itk.sesse.net/
License:		ASL 2.0
Group:		System Environment/Daemons
# It still needed as it targedted for EL5 too
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Source0:		http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
# In 2.2.19 introduced new mpm winnt, delete it for backward capability
Patch99:		httpd-2.2.19-build.patch
# It main Patch, actually as second upstream source for this package in patch form distribution!
Patch100:		http://mpm-itk.sesse.net/apache2.2-mpm-itk-2.2.17-01.patch

Source1:		README.Fedora

# Other patches (greather than 200) from main httpd package. Unfortunately I can't gone it there
# to do not miss something urgent (see comment and links in first changelog entry)!!
# Comment was leaved filled about that to httpd maintainer: https://bugzilla.redhat.com/show_bug.cgi?id=225891#c3
Patch201:		httpd-2.1.10-apctl.patch
Patch202:		httpd-2.1.10-apxs.patch
Patch203:		httpd-2.2.9-deplibs.patch
Patch204:		httpd-2.1.10-disablemods.patch
Patch205:		httpd-2.1.10-layout.patch
Patch220:		httpd-2.0.48-release.patch
Patch222:		httpd-2.1.10-pod.patch
Patch223:		httpd-2.0.45-export.patch
Patch224:		httpd-2.2.11-corelimit.patch
Patch225:		httpd-2.2.11-selinux.patch
Patch226:		httpd-2.2.9-suenable.patch
Patch227:		httpd-2.2.22-pcre830.patch


BuildRequires:	autoconf, perl, pkgconfig
BuildRequires:	zlib-devel, libselinux-devel
BuildRequires:	apr-devel >= 1.3.0, apr-util-devel >= 1.3.0, pcre-devel >= 5.0
Requires:		initscripts >= 8.36, /etc/mime.types, system-logos >= 7.92.1-1
Provides:		webserver
Conflicts:	pcre < 4.0
# There no required strict equal httpd version, just not older, because from it
# used only environment, but package provide fully independent binary file.
Requires:		httpd >= %{version}

%description
The Apache HTTP Server is a powerful, efficient, and extensible web server.

This package contain mpm-itk which is an MPM (Multi-Processing Module) for the
Apache web server. Mpm-itk allows you to run each of your vhost under a separate
uid and gid — in short, the scripts and configuration files for one vhost no
longer have to be readable for all the other vhosts.

In summary it is Apache module (opposite CGI solutions like suexec), fast and
allow safely use non-thread-aware code software (like many PHP extensions f.e.)

%prep
%setup -q -n httpd-%{version}
%patch99 -p1 -b .pre-itk
%patch100 -p1 -b .itk

%patch201 -p1 -b .apctl
%patch202 -p1 -b .apxs
%patch203 -p1 -b .deplibs
%patch204 -p1 -b .disablemods
%patch205 -p1 -b .layout
%patch220 -p1 -b .fedora
%patch222 -p1 -b .pod
%patch223 -p1 -b .export
%patch224 -p1 -b .corelimit
%patch225 -p1 -b .selinux
%patch226 -p1 -b .suenable
%patch227 -p1 -b .pcre830

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
	: Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}.
	: Update the mmn macro and rebuild.
	exit 1
fi
: Building with MMN %{mmn}

# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

%build
# regenerate configure scripts
autoheader && autoconf || exit 1

function mpmbuild(){
mpm=$1; shift
mkdir $mpm;
pushd $mpm;
ln -s ../configure
%configure \
	--prefix=%{_sysconfdir}/httpd \
	--exec-prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
	--with-installbuilddir=%{_libdir}/httpd/build \
	--with-mpm=$mpm \
	--with-apr=%{_prefix} \
	--with-apr-util=%{_prefix} \
	--enable-pie \
	--with-pcre \
	$*

make %{?_smp_mflags}
popd
}

# Only one build
mpmbuild itk --enable-modules=none

%install
rm -rf %{buildroot}

install -Dm 755 itk/httpd %{buildroot}%{_sbindir}/httpd.itk
install -m 600 %{SOURCE1} .

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.Fedora
%{_sbindir}/httpd.itk

%changelog
* Wed Mar 7 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-4
- Port pcre patch from httpd.
- Up apr and upr-utils required BR to 1.3 (http://centos.org/modules/newbb/print.php?form=1&topic_id=35915&forum=37&order=ASC&start=0).

* Thu Mar 1 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-3
- Add source1 - README.Fedora.

* Thu Feb 23 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-2
- Some minor fixes due to Fedora Review. Thanks to Nikos Roussos.

* Sat Feb 18 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.22-1
- Version 2.2.22
- Move content fo README.Fedora in separate file instead of store in SPEC.

* Tue Sep 13 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.21-1
- New version

* Sat Sep 10 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.20-1
- Security upstream update

* Wed Jul 6 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.19-1
- Update to 2.2.19 version follow to upstream.
- Drop outdated patch httpd-2.2.0-authnoprov.patch

* Wed Mar 23 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.17-4
- Follow the main httpd package:
	o Drop merged upstream Patch21: httpd-2.2.11-xfsz.patch
	o Update httpd-2.2.11-corelimit.patch and httpd-2.2.11-selinux.patch.

* Sat Oct 30 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.17-3
- Follow upstream new version 2.2.17 - https://admin.fedoraproject.org/updates/httpd-2.2.17-1.fc13.1

* Wed Jul 28 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.16-2
- Update to Apache 2.2.16 version.

* Sun Apr 04 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 2.2.15-1
- Initial spec. Based on httpd.spec in Fedora rawhide. Joe Orton has asked
	initially add MPM-ITK support into main httpd package (BUG#479575) -
	he dismiss enhancment request. After that he was asked (with proposed
	patch) to provide httpd-source package he also dismiss it (BUG#597772).
	Pride is a mortal sin. But I can not get it to do something.
	So, instead just base on always current version of Fedora httpd, I have to
	do it again from begining and doubling... I'll try it do as best as
	possible in this situation.
