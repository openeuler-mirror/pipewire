%global apiversion   0.3
%global spaversion   0.2
%global systemd      1
%global multilib_archs x86_64

Name:           pipewire
Version:        0.3.15
Release:        1
Summary:        Multimedia processing graphs
License:        LGPLv2+
URL:            https://pipewire.org/
Source0:        https://github.com/pipewire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         0001-protocol-native-do-version-check-on-HELLO.patch

BuildRequires:  meson gcc pkgconf-pkg-config libudev-devel dbus-devel glib2-devel gstreamer-devel
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel systemd-devel vulkan-loader-devel
BuildRequires:  alsa-lib-devel libv4l-devel doxygen xmltoman graphviz sbc-devel libsndfile-devel
BuildRequires:  bluez-devel SDL2-devel jack-audio-connection-kit-devel

Requires(pre):  shadow-utils
Requires:       systemd >= 184 rtkit

Provides:       %{name}-libs  %{name}-utils
Obsoletes:      %{name}-libs < %{version}-%{release} %{name}-utils < %{version}-%{release}

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
%meson -D docs=true -D man=true -D gstreamer=true -D systemd=true
%meson_build

%install
%meson_install

mkdir %{buildroot}%{_userunitdir}/sockets.target.wants
ln -s ../pipewire.socket %{buildroot}%{_userunitdir}/sockets.target.wants/pipewire.socket

mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d


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
%license LICENSE COPYING
%{_libdir}/spa-0.2/*
%{_libdir}/pipewire-%{apiversion}/*
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/gstreamer-1.0/libgstpipewire.*
%{_libdir}/alsa-lib/libasound_module_*
%{_bindir}/pipewire*
%{_bindir}/pw-*
%{_bindir}/spa-*
%{_userunitdir}/pipewire.*
%{_userunitdir}/sockets.target.wants/pipewire.socket
%dir %{_sysconfdir}/pipewire/
%{_sysconfdir}/pipewire/*
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules

%files devel
%defattr(-,root,root)
%{_includedir}/pipewire-%{apiversion}/*
%{_includedir}/spa-%{spaversion}/*
%{_libdir}/libpipewire-%{apiversion}.so
%{_libdir}/pkgconfig/*.pc

%files help
%defattr(-,root,root)
%doc README.md
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/doc/pipewire/html/*
%{_datadir}/alsa-card-profile/*

%changelog
* Mon May 31 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 0.3.15-1
- Upgrade to 0.3.15
- Update Version, Source0, BuildRequires, Obsoletes
- Update stage 'build', 'install' and 'files'
- Correct uncorrect date, add one patch

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

* Wed Aug 29 2018 openEuler Buildteam <buildteam@openeuler.org> - 0.2.2-2
- Package init
