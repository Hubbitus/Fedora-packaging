Name:	rigsofrods
Version:	0.4.0.4
Release:	2%{?dist}
Summary:	Vehicle simulator based on soft-body physics

License:	GPLv3
URL:		http://www.rigsofrods.com/
Source0:	http://sourceforge.net/projects/rigsofrods/files/rigsofrods/0.4-dev/%{name}-source-%{version}.zip

# Content-pack last for 0.37 version (http://www.rigsofrods.com/wiki/pages/Starting_RoR_under_Linux)
# Not neccesary?
# Source1:	http://sourceforge.net/projects/rigsofrods/files/rigsofrods/0.37/content-pack-0.37.zip

BuildRequires:	wxGTK-devel, ois-devel, ogre-devel >= 1.8.1, ogre-pagedgeometry-devel, openal-devel, mygui-devel
BuildRequires:	cmake, dos2unix
# Due to the bug http://redmine.rigsofrods.org/issues/1015 it strongly required
BuildRequires:	caelum
Patch0:	rigsofrods-0.39.4-dl.patch
# Pathes of libraries. I think it Fedora-specific
Patch1:	rigsofrods-0.4.0.4-paths-libs.patch

# It also strongly required: http://redmine.rigsofrods.com/issues/1033
# Also old fixed version: http://redmine.rigsofrods.com/issues/956
BuildRequires:	angelscript-devel <= 2.22.1
Patch2:	rigsofrods-0.4.0.4-angelscript-required.patch

# http://redmine.rigsofrods.com/issues/964
Patch3:	rigsofrods-0.4.0.4-gcc4.7.patch

%description
Rigs of Rods is an open source vehicle simulator licensed under the GNU General
Public License version 3. What makes Rigs of Rods different to most simulators
is its unique soft-body physics: vehicles, machines, objects, etc. are simulated
in real-time as flexible soft-body objects, giving the simulation an extremely
accurate behavior which entirely depends on the physical construction of the
vehicles or objects you create.
Features
 - Soft-body physics. Objects according to their weight distribution,
	construction, and/or suspension (in the case of vehicles).
 - Advanced flight model based on blade element theory. It allows the accurate
	simulation of any airplane, based entirely on its physical dimensions and
	wing airfoils, similar to X-Plane.
 - Accurate buoyancy model based on elemental pressure gradients, enabling boats
	with complex hulls to move realistically in the swell.
 - Basic support for dual-core processing. More multithreading and CUDA support
	is planned.
 - Basic support for scripting using AngelScript.
 - Based on the OGRE Graphics Engine.

%prep
%setup -qn %{name}-source-%{version}
%patch0 -p0 -b .dl
%patch1 -p1 -b .includes
%patch2 -p1 -b .angelscript
%patch3 -p1 -b .gcc4.7

# Convert lineendings
dos2unix --keepdate readme.txt COPYING LICENSE.txt

find . -type d -exec chmod 0755 {} \;

cmake \
	-DROR_USE_MYGUI="TRUE" \
	-DROR_USE_OPENAL="TRUE" \
	-DROR_USE_PAGED="TRUE" \
	-DROR_USE_CAELUM="TRUE" \
	-DROR_USE_ANGELSCRIPT="TRUE" \
	-DROR_USE_SOCKETW="TRUE" \
	-DSOCKETW_INCLUDE_DIRS:PATH="/usr/include" \
	-DPAGED_INCLUDE_DIRS:PATH="/usr/include/OGRE" \
	-DPAGED_LIBRARY_DIRS:PATH="/usr/lib64/OGRE" \
	-DPAGED_LIBRARIES=/usr/lib64/OGRE/libPagedGeometry.so \
	-DCMAKE_BUILD_TYPE=Debug \
	-DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} .

# Hack! I do not known how to fix it properly. To report upstream.
sed -ir 's/;-lMyGUI.Ogr//g;s/;MyGUI.Ogr$//g' CMakeCache.txt
sed -i 's/ -lMyGUI.Ogr / /g' ./source/main/main_sim/CMakeFiles/RoR.dir/link.txt

%build
make %{?_smp_mflags}

%install
install -Dm 0755 bin/RoR %{buildroot}%{_bindir}/RoR
install -Dm 0755 bin/RoRConfig %{buildroot}%{_bindir}/RoRConfig
mkdir -p %{buildroot}%{_datarootdir}/%{name}
cp -pr bin/resources/* %{buildroot}%{_datarootdir}/%{name}/

%files
%doc readme.txt COPYING LICENSE.txt
%{_bindir}/RoR
%{_bindir}/RoRConfig
%{_datarootdir}/%{name}

%changelog
* Sun Nov 25 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.0.4-2
- Fix RoRconfig file.
- Add resources.

* Sat Sep 22 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.4.0.4-1
- New version.
- Remade paths libs patch: rigsofrods-0.4.0.4-paths-libs.patch
- Add patches 2 and 3.

* Sun Jun 24 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 0.39.4-1
- Initial spec version.
