%global apiversion   0.2
%global spaversion   0.1
%global systemd      1
%global multilib_archs x86_64

Name:           pipewire
Version:        0.2.7
Release:        1
Summary:        Multimedia processing graphs
License:        LGPLv2+
URL:            https://pipewire.org/
Source0:        https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  meson gcc pkgconf-pkg-config dbus-devel glib2-devel
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel systemd-devel
BuildRequires:  alsa-lib-devel libv4l-devel doxygen xmltoman graphviz sbc-devel

Requires(pre):  shadow-utils
Requires:       systemd >= 184 rtkit

Provides:       %{name}-libs  %{name}-utils
Obsoletes:      %{name}-libs  %{name}-utils

%description
%{name} is a server and user space API to deal with multimedia
pipelines,contains command line utilities. 

%package          devel
Summary:          includes development files for %{name} client development
License:          LGPLv2+
Requires:         %{name} = %{version}-%{release}

%description      devel
Files needed for building applications,such as static libraries,
header files that can communicate with a %{name} media server.

%package_help

%prep
%autosetup -T -b0 -n %{name}-%{version} -p1

%build
%meson -D docs=true -D man=true -D gstreamer=enabled -D systemd=true
%meson_build

%install
%meson_install

mkdir %{buildroot}%{_userunitdir}/sockets.target.wants
ln -s ../pipewire.socket %{buildroot}%{_userunitdir}/sockets.target.wants/pipewire.socket

%check
%meson_test

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE GPL LGPL
%{_libdir}/spa/*
%{_libdir}/pipewire-%{apiversion}/*
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/gstreamer-1.0/libgstpipewire.*
%{_bindir}/pipewire*
%{_bindir}/spa-*
%{_userunitdir}/pipewire.*
%{_userunitdir}/sockets.target.wants/pipewire.socket
%dir %{_sysconfdir}/pipewire/
%{_sysconfdir}/pipewire/*

%files devel
%defattr(-,root,root)
%{_includedir}/pipewire/*
%{_includedir}/spa/*
%{_libdir}/libpipewire-%{apiversion}.so
%{_libdir}/pkgconfig/*.pc

%files help
%defattr(-,root,root)
%doc README
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/doc/pipewire/html/*

%changelog
* Thu Jan 9 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.2.7-1
- update to 0.2.7

* Sat Nov 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.2.2-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:change build requires of v4l-utils-deve to libv4l-devel

* Thu Nov 14 2019 shenyangyang<shenyangyang4@huawei.com> - 0.2.2-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change build requires of libv4l-devel to v4l-utils-devel

* Thu Aug 29 2018 openEuler Buildteam <buildteam@openeuler.org> - 0.2.2-2
- Package init
