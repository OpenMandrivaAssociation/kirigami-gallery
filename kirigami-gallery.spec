%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name: kirigami-gallery
Version: 25.12.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0:        https://invent.kde.org/sdk/%{name}/-/archive/master/%{name}-master.tar.bz2
%else
Source0:        https://download.kde.org/%{stable}/release-service/%{version}/src/%{name}-%{version}.tar.xz
%endif
Summary: Kirigami component gallery application
URL: https://github.com/kirigami-gallery/kirigami-gallery
License: GPL
Group: Development/Tools
BuildRequires: cmake ninja
BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(KF6ItemModels)

%description
Kirigami component gallery application

%prep
%autosetup -p1
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build
TOP=$(pwd)
cd %{buildroot}
find .%{_datadir}/locale -name "*.qm" |while read r; do
	echo "%%lang($(echo $r|cut -d/ -f5)) $(echo $r |cut -b2-)" >>$TOP/qm.lang
done

%files -f qm.lang
%{_bindir}/kirigami2gallery
%{_datadir}/applications/org.kde.kirigami2.gallery.desktop
%{_datadir}/metainfo/org.kde.kirigami2.gallery.appdata.xml
