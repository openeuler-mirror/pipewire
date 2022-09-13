%global apiversion   0.3
%global spaversion   0.2
%global systemd      1
%global minorversion 3
%global microversion 38
%global soversion    0
%global multilib_archs x86_64
%global libversion   %{soversion}.%(bash -c '((intversion = (%{minorversion} * 100) + %{microversion})); echo ${intversion}').0
%global enable_alsa 1

%global enable_jack   0
%global enable_pulse  0
%global enable_vulkan 0

Name:           pipewire
Version:        0.3.38
Release:        2
Summary:        Multimedia processing graphs
License:        LGPLv2+
URL:            https://pipewire.org/
Source0:        https://github.com/pipewire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz
Patch01:	fix-bug-of-build-fails-on-16-17-test-support.patch
Patch02:	fix-missing-NAME-define-under-arm.patch

BuildRequires:  meson gcc g++ pkgconf-pkg-config libudev-devel dbus-devel glib2-devel pipewire-gstreamer
BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel systemd-devel vulkan-loader-devel
BuildRequires:  alsa-lib-devel libv4l-devel doxygen xmltoman graphviz sbc-devel libsndfile-devel
BuildRequires:  bluez-devel SDL2-devel jack-audio-connection-kit-devel python3-docutils
BuildRequires:  webrtc-audio-processing-devel libldac-devel libusbx-devel
#remove rpath
BuildRequires:	chrpath

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
%meson \
    -D docs=enabled -D man=enabled -D gstreamer=enabled -D systemd=enabled	\
    -D jack=disabled -D pipewire-jack=disabled 					\
    -D vulkan=disabled -D gstreamer-device-provider=disabled -D sdl2=disabled 	\
    -D audiotestsrc=disabled -D videotestsrc=disabled				\
    -D volume=disabled -D bluez5-codec-aptx=disabled -D roc=disabled		\
    -D libcamera=disabled -D jack-devel=true -D pipewire-alsa=disabled		\
    -D bluez5-codec-aac=disabled -D echo-cancel-webrtc=disabled
%meson_build

%install
%meson_install

#remove rpath
chrpath -d %{buildroot}%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so

%if 0%{?enable_jack}
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir}/pipewire-%{apiversion}/jack/ > %{buildroot}%{_sysconfdir}/ld.so.conf.d/pipewire-jack-%{_arch}.conf
%else
rm %{buildroot}%{_datadir}/pipewire/jack.conf
rm %{buildroot}%{_datadir}/pipewire/media-session.d/with-jack
%endif

# If the PulseAudio replacement isn't being offered, delete the files
rm %{buildroot}%{_bindir}/pipewire-pulse
rm %{buildroot}%{_userunitdir}/pipewire-pulse.*
rm %{buildroot}%{_datadir}/pipewire/media-session.d/with-pulseaudio
rm %{buildroot}%{_datadir}/pipewire/pipewire-pulse.conf

# rm media_session related
rm %{buildroot}%{_datadir}/pipewire/media-session.d/alsa-monitor.conf
rm %{buildroot}%{_datadir}/pipewire/media-session.d/bluez-monitor.conf
rm %{buildroot}%{_datadir}/pipewire/media-session.d/media-session.conf
rm %{buildroot}%{_datadir}/pipewire/media-session.d/v4l2-monitor.conf
rm %{buildroot}%{_datadir}/spa-0.2/bluez5/bluez-hardware.conf

# We don't start the media session with systemd yet
rm %{buildroot}%{_userunitdir}/pipewire-media-session.*

%find_lang %{name}

# upstream should use udev.pc
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d


%check
%meson_test || TESTS_ERROR=$?
if [ "${TESTS_ERROR}" != "" ]; then
echo "test failed"
%{!?tests_nonfatal:exit $TESTS_ERROR}
fi

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%post
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%triggerun -- %{name} < 0.3.6-2
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pipewire.socket >/dev/null 2>&1 || :

%if 0%{?enable_pulse}
%post pulseaudio
%systemd_user_post pipewire-pulse.service
%systemd_user_post pipewire-pulse.socket
%endif

%files
%defattr(-,root,root)
%license LICENSE COPYING
%{_libdir}/alsa-lib/libasound_module_*
%{_bindir}/pipewire	
%{_bindir}/pipewire-media-session
%{_userunitdir}/pipewire.*
%{_datadir}/pipewire/pipewire.conf
%{_datadir}/pipewire/filter-chain/*.conf

%files libs -f %{name}.lang
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
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf

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
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*
%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-monitor
%{_bindir}/spa-resample
%{_bindir}/pw-dsdplay
%{_bindir}/pw-dump
%{_bindir}/pw-link
%{_bindir}/pw-loopback
%{_bindir}/spa-json-dump

%if 0%{?enable_alsa}
%files alsa
%defattr(-,root,root)
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
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
* Tue Sep 13 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 0.3.38-2
- fix rpath compile option

* Mon Jun 20 2022 wenlong ding <wenlong.ding@turbolinux.com.cn> - 0.3.38-1
- Update version to 0.3.38

* Wed Apr 13 2022 liuyumeng <liuyumeng5@h-partners.comm> - 0.3.15-6
- delete redundant buildrequires

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
