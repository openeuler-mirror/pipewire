%global apiversion   0.2

Name:             pipewire
Version:          0.2.2
Release:          2
Summary:          Multimedia processing graphs
License:          LGPLv2+
URL:              https://pipewire.org/
Source0:          https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz


BuildRequires:    meson gcc pkgconf-pkg-config dbus-devel glib2-devel gstreamer1-devel gstreamer1-plugins-base-devel
BuildRequires:    systemd-devel alsa-lib-devel libv4l-devel doxygen xmltoman graphviz sbc-devel git 

Requires(pre):    shadow-utils
Requires:         systemd >= 184 rtkit

Provides:         %{name}-libs  %{name}-utils
Obsoletes:        %{name}-libs  %{name}-utils

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
%autosetup -T -b0 -n %{name}-%{version} -p1 -S git

%build
%meson -D enable_docs=true -D enable_man=true -D enable_gstreamer=true
%meson_build

%install
%meson_install

%check
%meson_test

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d /var/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE GPL LGPL
%{_libdir}/pipewire-%{apiversion}/*
%{_libdir}/libpipewire-%{apiversion}.so*
%{_libdir}/libspa-lib.so*
%{_libdir}/gstreamer-1.0/libgstpipewire.*
%{_libdir}/spa/*
%{_bindir}/pipewire*
%{_bindir}/spa-*
%{_userunitdir}/pipewire.*
%{_sysconfdir}/pipewire/*

%files devel
%defattr(-,root,root)
%{_includedir}/pipewire/*
%{_includedir}/spa/*
%{_libdir}/pkgconfig/*

%files help
%defattr(-,root,root)
%doc README
%{_mandir}/man1/*
%{_datadir}/doc/pipewire/html/*

%changelog
* Thu Aug 29 2018 openEuler Buildteam <buildteam@openeuler.org> - 0.2.2-2
- Package init
