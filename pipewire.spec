%global apiversion   0.3
%global spaversion   0.2
%global systemd      1
%global minorversion 3
%global microversion 15
%global soversion    0
%global multilib_archs x86_64
%global libversion   %{soversion}.%(bash -c '((intversion = (%{minorversion} * 100) + %{microversion})); echo ${intversion}').0
%global enable_alsa 1

%global enable_jack   0
%global enable_pulse  0
%global enable_vulkan 0


Name:           pipewire
Version:        0.3.15
Release:        5
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
	
%package libs
Summary:        Libraries for PipeWire clients
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-libpulse < %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package gstreamer
Summary:        GStreamer elements for PipeWire
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
 
%description gstreamer
This package contains GStreamer elements to interface with a
PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
 
%description utils
This package contains command line utilities for the PipeWire media server.
	
%if 0%{?enable_alsa}
%package alsa
Summary:        PipeWire media server ALSA support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
 
%description alsa
This package contains an ALSA plugin for the PipeWire media server.
%endif

%if 0%{?enable_jack}
%package libjack
Summary:        PipeWire libjack library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
Conflicts:      jack-audio-connection-kit
Conflicts:      jack-audio-connection-kit-dbus
Obsoletes:      pipewire-jack < 0.2.96-2
Conflicts:      %{name}-libjack < 0.3.13-6
Conflicts:      %{name}-jack-audio-connection-kit < 0.3.13-6
Obsoletes:      %{name}-jack-audio-connection-kit < 0.3.13-6
 
%description libjack
This package contains a PipeWire replacement for JACK audio connection kit
"libjack" library.
 
%package jack-audio-connection-kit
Summary:        PipeWire JACK implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libjack%{?_isa} = %{version}-%{release}
BuildRequires:  jack-audio-connection-kit-devel >= 1.9.10
Conflicts:      jack-audio-connection-kit
Conflicts:      jack-audio-connection-kit-dbus
Conflicts:      %{name}-libjack < 0.3.13-6
Conflicts:      %{name}-jack-audio-connection-kit < 0.3.13-6
 
%description jack-audio-connection-kit
This package provides a JACK implementation based on PipeWire
 
%package plugin-jack
Summary:        PipeWire media server JACK support
License:        MIT
BuildRequires:  jack-audio-connection-kit-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       jack-audio-connection-kit
 
%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.
%endif

%package          devel
Summary:          includes development files for %{name} client development
License:          LGPLv2+
Requires:         %{name} = %{version}-%{release}

%description      devel
Files needed for building applications,such as static libraries,
header files that can communicate with a %{name} media server.

%if 0%{?enable_pulse}
%package libpulse
Summary:        PipeWire libpulse library
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
Conflicts:      pulseaudio-libs
Conflicts:      pulseaudio-libs-glib2
Obsoletes:      pipewire-pulseaudio < 0.2.96-2
Conflicts:      %{name}-libpulse < 0.3.13-6
Conflicts:      %{name}-pulseaudio < 0.3.13-6
Obsoletes:      %{name}-pulseaudio < 0.3.13-6
 
%description libpulse
This package contains a PipeWire replacement for PulseAudio "libpulse" library.
 
%package pulseaudio
Summary:        PipeWire PulseAudio implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libpulse%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs-devel
Conflicts:      %{name}-libpulse < 0.3.13-6
Conflicts:      %{name}-pulseaudio < 0.3.13-6
 
%description pulseaudio
This package provides a PulseAudio implementation based on PipeWire
%endif

%package_help

%prep
%autosetup -T -b0 -n %{name}-%{version} -p1

%build
%meson -D docs=true -D man=true -D gstreamer=true -D systemd=true \
        -D jack=false -D pipewire-jack=false	  \
    	-D pipewire-pulseaudio=false			  \
        -D vulkan=false
%meson_build

%install
%meson_install

%if 0%{?enable_jack}
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjack.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libjack.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjack.so.%{libversion}
ln -s libjack.so.%{libversion} %{buildroot}%{_libdir}/libjack.so.0.1.0
ln -s libjack.so.0.1.0 %{buildroot}%{_libdir}/libjack.so.0
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libjackserver.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so.%{libversion}
ln -s libjackserver.so.%{libversion} %{buildroot}%{_libdir}/libjackserver.so.0.1.0
ln -s libjackserver.so.0.1.0 %{buildroot}%{_libdir}/libjackserver.so.0
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libjacknet.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so.%{libversion}
ln -s libjacknet.so.%{libversion} %{buildroot}%{_libdir}/libjacknet.so.0.1.0
ln -s libjacknet.so.0.1.0 %{buildroot}%{_libdir}/libjacknet.so.0
%endif
	
%if 0%{?enable_pulse}
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libpulse.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse.so.%{libversion}
ln -s libpulse.so.%{libversion} %{buildroot}%{_libdir}/libpulse.so.0
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-simple.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libpulse-simple.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-simple.so.%{libversion}
ln -s libpulse-simple.so.%{libversion} %{buildroot}%{_libdir}/libpulse-simple.so.0
mv %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so.%{libversion} %{buildroot}%{_libdir}
ln -sr %{buildroot}%{_libdir}/libpulse-mainloop-glib.so.%{libversion} %{buildroot}%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so.%{libversion}
ln -s libpulse-mainloop-glib.so.%{libversion} %{buildroot}%{_libdir}/libpulse-mainloop-glib.so.0
%endif

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
%{_libdir}/alsa-lib/libasound_module_*
%{_bindir}/pipewire	
%{_bindir}/pipewire-media-session
%{_userunitdir}/pipewire.*
%{_userunitdir}/sockets.target.wants/pipewire.socket
%dir %{_sysconfdir}/pipewire/
%{_sysconfdir}/pipewire/*
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf

%files libs
%defattr(-,root,root)	
%license LICENSE COPYING
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%dir %{_libdir}/spa-%{spaversion}
%{_libdir}/spa-%{spaversion}/alsa/
%{_libdir}/spa-%{spaversion}/audioconvert/
%{_libdir}/spa-%{spaversion}/audiomixer/
%{_libdir}/spa-%{spaversion}/bluez5/
%{_libdir}/spa-%{spaversion}/control/
%{_libdir}/spa-%{spaversion}/support/
%{_libdir}/spa-%{spaversion}/v4l2/
%{_libdir}/spa-%{spaversion}/videoconvert/	
%if 0%{?enable_vulkan}
%{_libdir}/spa-%{spaversion}/vulkan/
%endif

%files gstreamer
%defattr(-,root,root)
%{_libdir}/gstreamer-1.0/libgstpipewire.*

%files utils
%defattr(-,root,root)
%{_bindir}/pw-mon
%{_bindir}/pw-metadata
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*
%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-monitor
%{_bindir}/spa-resample

%if 0%{?enable_alsa}
%files alsa
%defattr(-,root,root)
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%if 0%{?enable_jack}
%files jack-audio-connection-kit
%defattr(-,root,root)
%{_bindir}/pw-jack
%{_mandir}/man1/pw-jack.1*
%{_libdir}/pipewire-%{apiversion}/jack/libjack.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so*
%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so*
 
%files libjack
%defattr(-,root,root)
%{_libdir}/libjack.so.*
%{_libdir}/libjackserver.so.*
%{_libdir}/libjacknet.so.*
 
%files plugin-jack
%defattr(-,root,root)
%{_libdir}/spa-%{spaversion}/jack/
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/pipewire-%{apiversion}/*
%{_includedir}/spa-%{spaversion}/*
%{_libdir}/libpipewire-%{apiversion}.so
%{_libdir}/pkgconfig/*.pc

%if 0%{?enable_pulse}
%files pulseaudio
%defattr(-,root,root)
%{_bindir}/pw-pulse
%{_mandir}/man1/pw-pulse.1*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-simple.so*
%{_libdir}/pipewire-%{apiversion}/pulse/libpulse-mainloop-glib.so*
 
%files libpulse
%defattr(-,root,root)
%{_libdir}/libpulse.so.*
%{_libdir}/libpulse-simple.so.*
%{_libdir}/libpulse-mainloop-glib.so.*
%endif

%files help
%defattr(-,root,root)
%doc README.md
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/doc/pipewire/html/*

%changelog
* Mon Aug 2 2021 wangkerong <wangkerong@huawei.com> - 0.3.15-5
- disable jack pulse vulkan subpackages

* Sat Jul 31 2021 wangkerong <wangkerong@huawei.com> - 0.3.15-4
- add alsa,gstreamer,libjack,libpulse... subpackages

* Thu Jul 29 2021 wangkerong <wangkerong@huawei.com> - 0.3.15-3
- add lib package

* Mon May 31 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 0.3.15-2
- Update stage 'build', add disable configuration to pipewire-pulseaudio

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
