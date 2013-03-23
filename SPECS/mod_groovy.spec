Name:		mod_groovy
Version:		1
Release:		1.alpha%{?dist}
Summary:		Apache module to run groovy outside of traditional J2EE containers

License:		GPLv2+
URL:			http://code.google.com/p/mod-groovy/
Source0:		http://mod-groovy.googlecode.com/files/mod-groovy-alpha-1.tar.gz

BuildRequires:	httpd-devel
Requires:		groovy

%description
mod_groovy can run your Java/Groovy code under Apache. No messing around with
Tomcat / JBoss / WebSphere or anything like that. Put your index.gr file onto
your hard drive, hit the URL, and it's compiled and ran. Think of it as mod_php
for groovy.

This project is for people who:

want to try new languages like groovy, but don't want to be tied to JXEE
and friends like PHP, but are afraid that php6 is going nowhere can't
run a 600 Mb JVM on their server like Java but also like Virtual Hosts
like Java but also like putting their applications onto the URL
whichever whay they want w/o editing XML files and stopping/starting the
server. don't like 3 min server start-up times :( This project needs
help from people who know Gnu make utilities, or who are willing to move
the build system to ant/maven/et al.

%prep
%setup -q -n mod-groovy-alpha-1

exit 101

%build
aclocal
libtoolize
# automake threat such files as required and ends with error
touch NEWS AUTHORS
automake --add-missing --force-missing --gnu
autoconf
%configure
make %{?_smp_mflags}
apxs -i -a -n groovy libmodgroovy.la

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%files
%doc



%changelog
* Sat Mar 24 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1-1.alpha
- Initial spec
