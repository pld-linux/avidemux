# TODO:
# - split (at least some) plugins
# - -ui-cli subpackage?
# - use external spidermonkey (cmake fix needed): Checking for SpiderMonkey -- Skipping check and using bundled version.
# - use patched ffmpeg
# - nvenc (on bcond)?
#
# Conditional build:
%bcond_with	arts		# aRts audio output
%bcond_with	esd		# EsounD audio output
%bcond_without	amr		# Adaptive Multi Rate (AMR) speech codec support
%bcond_without	qt4		# Qt 4 interface
%bcond_without	qt5		# Qt 5 interface
%bcond_without	system_liba52	# system liba52 library
%bcond_without	system_libass	# system libass library
%bcond_without	system_libmad	# system libmad library
%bcond_without	system_mp4v2	# system mp4v2 library
%bcond_with	gtk		# GTK+ interface

%define		qt4_version	4.6
%define		qt5_version	5.3

Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.7.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	e3510c858c9371283551b1b4b67d288b
Source1:	%{name}.desktop
Source2:	%{name}-qt4.desktop
Source3:	%{name}-qt5.desktop
Patch0:		build.patch
Patch1:		no-qt-in-gtk.patch
Patch2:		%{name}-ffmpeg-make.patch
Patch3:		%{name}-x32.patch
URL:		http://fixounet.free.fr/avidemux/
%{?with_qt5:BuildRequires:	Qt5Core-devel >= %{qt5_version}}
%{?with_qt5:BuildRequires:	Qt5Gui-devel >= %{qt5_version}}
%{?with_qt5:BuildRequires:	Qt5OpenGL-devel >= %{qt5_version}}
%{?with_qt5:BuildRequires:	Qt5Script-devel >= %{qt5_version}}
%{?with_qt5:BuildRequires:	Qt5Widgets-devel >= %{qt5_version}}
%{?with_qt4:BuildRequires:	QtCore-devel >= %{qt4_version}}
%{?with_qt4:BuildRequires:	QtGui-devel >= %{qt4_version}}
%{?with_qt4:BuildRequires:	QtOpenGL-devel >= %{qt4_version}}
%{?with_qt4:BuildRequires:	QtScript-devel >= %{qt4_version}}
BuildRequires:	SDL2-devel >= 2
%{?with_system_liba52:BuildRequires:	a52dec-libs-devel}
BuildRequires:	aften-devel >= 0.0.8
BuildRequires:	alsa-lib-devel >= 1.0
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	bash
BuildRequires:	cmake >= 3.0
BuildRequires:	dcaenc-devel
BuildRequires:	doxygen
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	faac-devel
BuildRequires:	faad2-devel >= 2
BuildRequires:	fdk-aac-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	fribidi-devel >= 0.19
%{?with_gtk:BuildRequires:	gdk-pixbuf2-devel >= 2.0}
BuildRequires:	gettext-tools
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	gtk+3-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	lame-libs-devel
%{?with_system_libass:BuildRequires:	libass-devel}
BuildRequires:	libdts-devel >= 0.0.5
%{?with_system_libmad:BuildRequires:	libmad-devel}
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libva-devel
BuildRequires:	libva-x11-devel
BuildRequires:	libvdpau-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libvpx-devel
# ABI >= 67
BuildRequires:	libx264-devel
# ABI >= 9
BuildRequires:	libx265-devel
BuildRequires:	libxml2-devel
%{?with_qt4:BuildRequires:	libxslt-progs}
%{?with_system_mp4v2:BuildRequires:	mp4v2-devel}
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm >= 0.98.32
BuildRequires:	yasm
%endif
%{?with_amr:BuildRequires:	opencore-amr-devel}
BuildRequires:	opus-devel
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
%{?with_qt4:BuildRequires:	qt4-build >= %{qt4_version}}
%{?with_qt4:BuildRequires:	qt4-linguist >= %{qt4_version}}
%{?with_qt4:BuildRequires:	QtNetwork-devel >= %{qt4_version}}
%{?with_qt4:BuildRequires:	qt4-qmake >= %{qt4_version}}
%{?with_qt5:BuildRequires:	qt5-build >= %{qt5_version}}
%{?with_qt5:BuildRequires:	qt5-linguist >= %{qt5_version}}
%{?with_qt5:BuildRequires:	Qt5Network-devel >= %{qt5_version}}
%{?with_qt5:BuildRequires:	qt5-qmake >= %{qt5_version}}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	twolame-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-proto-xextproto-devel
BuildRequires:	xvid-devel >= 1:1.0
BuildRequires:	zlib-devel
# see cmake/admDetermineSystem.cmake
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl.UTF-8
Mały edytor audio/wideo dla Linuksa.

%package ui-gtk
Summary:	GTK+ 2 UI for Avidemux
Summary(pl.UTF-8):	Interfejs użytkownika GTK+ 2 do edytora Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	desktop-file-utils

%description ui-gtk
GTK+ 2 UI for Avidemux.

%description ui-gtk -l pl.UTF-8
Interfejs użytkownika GTK+ 2 do edytora Avidemux.

%package ui-qt4
Summary:	Qt 4 UI for Avidemux
Summary(pl.UTF-8):	Interfejs użytkownika Qt 4 do edytora Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	desktop-file-utils

%description ui-qt4
Qt 4 UI for Avidemux.

%description ui-qt4 -l pl.UTF-9
Interfejs użytkownika Qt 4 do edytora Avidemux.

%package ui-qt5
Summary:	Qt 5 UI for Avidemux
Summary(pl.UTF-8):	Interfejs użytkownika Qt 5 do edytora Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	desktop-file-utils

%description ui-qt5
Qt 5 UI for Avidemux.

%description ui-qt5 -l pl.UTF-8
Interfejs użytkownika Qt 5 do edytora Avidemux.

%prep
%setup -q -n %{name}_%{version}
find '(' -name '*.js' -o -name '*.cpp' -o -name '*.h' -o -name '*.cmake' -o -name '*.txt' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch2 -p1

%build
install -d buildCore buildCli buildQt4 buildQt5 buildGtk buildPluginsCommon buildPluginsCLI buildPluginsSettings buildPluginsQt4 buildPluginsQt5 buildPluginsGtk

FAKEROOT_DIR=$(pwd)/install
AVIDEMUX_SOURCE_DIR=$(pwd)

cd buildCore
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
%ifarch x32
	-DFF_FLAGS="--disable-asm" \
%endif
	../avidemux_core
%{__make} -j1
%{__make} install DESTDIR=$FAKEROOT_DIR
cd ..
cd buildCli
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	../avidemux/cli
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsCommon
%cmake \
	%{!?with_arts:-DARTS=OFF} \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	%{!?with_esd:-DESD=OFF} \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=COMMON \
	%{?with_system_liba52:-DUSE_EXTERNAL_LIBA52=ON} \
	%{?with_system_libass:-DUSE_EXTERNAL_LIBASS=ON} \
	%{?with_system_libmad:-DUSE_EXTERNAL_LIBMAD=ON} \
	%{?with_system_mp4v2:-DUSE_EXTERNAL_MP4V2=ON} \
	../avidemux_plugins
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsCLI
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=CLI \
	../avidemux_plugins
%{__make}
%{__make} install DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsSettings
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=SETTINGS \
	../avidemux_plugins
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..

%if %{with qt4}
cd buildQt4
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	../avidemux/qt4
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsQt4
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=QT4 \
	../avidemux_plugins
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
%endif

%if %{with qt5}
cd buildQt5
%cmake \
	-DENABLE_QT5=True \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	../avidemux/qt4
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsQt5
%cmake \
	-DENABLE_QT5=True \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=QT4 \
	../avidemux_plugins
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
%endif

%if %{with gtk}
cd buildGtk
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	../avidemux/gtk
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
cd buildPluginsGtk
%cmake \
	-DAVIDEMUX_SOURCE_DIR=$AVIDEMUX_SOURCE_DIR \
	-DFAKEROOT=$FAKEROOT_DIR \
	-DPLUGIN_UI=GTK \
	../avidemux_plugins
%{__make}
%{__make} install \
	DESTDIR=$FAKEROOT_DIR
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_bindir},%{_mandir}/man1}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a install/* $RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

%{__mv} $RPM_BUILD_ROOT%{_bindir}/avidemux3{_cli,}
cp -a man/avidemux.1 $RPM_BUILD_ROOT%{_mandir}/man1
%{?with_gtk:cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-gtk.desktop}
%{?with_qt4:cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-qt4.desktop}
%{?with_qt5:cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-qt5.desktop}
cp -a avidemux_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{__rm} -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post ui-gtk
%update_desktop_database

%post ui-qt4
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc AUTHORS License.txt README
%attr(755,root,root) %{_bindir}/avidemux3
%attr(755,root,root) %{_libdir}/libADM6avcodec.so.57
%attr(755,root,root) %{_libdir}/libADM6avformat.so.57
%attr(755,root,root) %{_libdir}/libADM6avutil.so.55
%attr(755,root,root) %{_libdir}/libADM6postproc.so.54
%attr(755,root,root) %{_libdir}/libADM6swscale.so.4
%attr(755,root,root) %{_libdir}/libADM_UI_Cli6.so
%attr(755,root,root) %{_libdir}/libADM_core6.so
%attr(755,root,root) %{_libdir}/libADM_coreAudio6.so
%attr(755,root,root) %{_libdir}/libADM_coreImage6.so
%attr(755,root,root) %{_libdir}/libADM_coreUI6.so
%attr(755,root,root) %{_libdir}/libADM_render6_cli.so
%attr(755,root,root) %{_libdir}/libADM_audioParser6.so
%attr(755,root,root) %{_libdir}/libADM_coreAudioDevice6.so
%attr(755,root,root) %{_libdir}/libADM_coreAudioEncoder6.so
%attr(755,root,root) %{_libdir}/libADM_coreAudioFilterAPI6.so
%attr(755,root,root) %{_libdir}/libADM_coreDemuxer6.so
%attr(755,root,root) %{_libdir}/libADM_coreDemuxerMpeg6.so
%attr(755,root,root) %{_libdir}/libADM_coreImageLoader6.so
%attr(755,root,root) %{_libdir}/libADM_coreJobs.so
%attr(755,root,root) %{_libdir}/libADM_coreLibVA6.so
%attr(755,root,root) %{_libdir}/libADM_coreLibVAEnc6.so
%attr(755,root,root) %{_libdir}/libADM_coreMuxer6.so
%attr(755,root,root) %{_libdir}/libADM_coreScript.so
%attr(755,root,root) %{_libdir}/libADM_coreSocket6.so
%attr(755,root,root) %{_libdir}/libADM_coreSqlLight3.so
%attr(755,root,root) %{_libdir}/libADM_coreSubtitle.so
%attr(755,root,root) %{_libdir}/libADM_coreUtils6.so
%attr(755,root,root) %{_libdir}/libADM_coreVDPAU6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoCodec6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoEncoder6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoFilter6.so

%dir %{_libdir}/ADM_plugins6

%dir %{_libdir}/ADM_plugins6/audioDecoder
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_Mad.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_a52.so
# R: libdts
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_dca.so
# R: faad2-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_faad.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ima_adpcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_lav.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ms_adpcm.so
%if %{with amr}
# R: opencore-amr
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_opencore_amrnb.so
# R: opencore-amr
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_opencore_amrwb.so
%endif
# R: opus
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_opus.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ulaw.so
# R: libvorbis
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_vorbis.so

%dir %{_libdir}/ADM_plugins6/audioDevices
# R: alsa-lib
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaDMix.so
# R: alsa-lib
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaDefault.so
# R: alsa-lib
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaHw.so
# R: artsc
%{?with_arts:%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_arts.so}
# R: esound
%{?with_esd:%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_esd.so}
# R: audio-connection-kit-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_jack.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_oss.so
# R: pulseaudio-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_pulseAudioSimple.so

%dir %{_libdir}/ADM_plugins6/audioEncoders
# R: aften
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_aften.so
# R: dcaenc
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_dcaenc.so
# R: faac-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_faac.so
# R: fdk-aac
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_fdk_aac.so
# R: lame-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lame.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_aac.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_ac3.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_mp2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_pcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_opus.so
# R: twolame-libs
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_twolame.so
# R: libvorbis
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_vorbis.so

#%dir %{_libdir}/ADM_plugins6/videoDecoders
# R: libvpx [2.7.0: disabled in CMakeLists.txt]
#%attr(755,root,root) %{_libdir}/ADM_plugins6/videoDecoders/libADM_vd_vpx.so

%dir %{_libdir}/ADM_plugins6/videoEncoders
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffDv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffFlv1.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffMpeg2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffMpeg4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_huff.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_jpeg.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_libva.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_null.so
# R: libx264
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_x264_other.so
# R: libx265
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_x265_other.so
# R: xvid
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_xvid4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_yv12.so

%dir %{_libdir}/ADM_plugins6/videoFilters
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_addBorders.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_admIvtc.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_ascii.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_avsfilter.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_black.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_changeFps.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_colorYuv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_denoise3dhq.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_denoise3d.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_DgBob.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_dummy.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_fadeToBlack.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_fadeTo.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_FluxSmooth.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_gauss.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_hflip.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_hzstackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_ivtcDupeRemover.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_kernelDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_largeMedian.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_lavDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_lumaOnly.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mean.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_median.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mergeField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_printInfo.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_removePlane.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_resampleFps.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_rotate.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_separateField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_sharpen.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_ssa.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_stackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_stillimage.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_swapUV.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_telecide.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_unstackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vaapiFilter.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vdpauFilterDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vdpauFilter.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vflip.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_yadif.so
%dir %{_libdir}/ADM_plugins6/videoFilters/cli
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_blackenBordersCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_chromaShiftCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_contrastCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_CropCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_eq2Cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_HueCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_logoCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_mpdelogoCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_msharpenCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/cli/libADM_vf_swscaleResize_cli.so

%dir %{_libdir}/ADM_plugins6/autoScripts
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/720p.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/PSP.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/check24fps.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/dvd.py
%dir %{_libdir}/ADM_plugins6/autoScripts/lib
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/lib/ADM_image.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/lib/ADM_imageInfo.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/svcd.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/vcd.py

%dir %{_libdir}/ADM_plugins6/demuxers
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_asf.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_avsproxy.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_flv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_matroska.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_mp4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_mxf.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_opendml.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_pic.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_ps.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/demuxers/libADM_dm_ts.so

%dir %{_libdir}/ADM_plugins6/muxers
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_Mkv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_Webm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_avi.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_dummy.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_ffPS.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_ffTS.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_flv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_mp4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_mp4v2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_raw.so

%dir %{_libdir}/ADM_plugins6/pluginSettings
%dir %{_libdir}/ADM_plugins6/pluginSettings/x264
%dir %{_libdir}/ADM_plugins6/pluginSettings/x264/3
%{_libdir}/ADM_plugins6/pluginSettings/x264/3/PSP.json
%{_libdir}/ADM_plugins6/pluginSettings/x264/3/fast.json
%{_libdir}/ADM_plugins6/pluginSettings/x264/3/iPhone.json
%{_libdir}/ADM_plugins6/pluginSettings/x264/3/ultraFast.json
%{_libdir}/ADM_plugins6/pluginSettings/x264/3/veryFast.json

%dir %{_libdir}/ADM_plugins6/scriptEngines
%attr(755,root,root) %{_libdir}/ADM_plugins6/scriptEngines/libADM_script_tinyPy.so

%dir %{_libdir}/ADM_plugins6/shaderDemo
%dir %{_libdir}/ADM_plugins6/shaderDemo/1
%{_libdir}/ADM_plugins6/shaderDemo/1/bump.shader
%{_libdir}/ADM_plugins6/shaderDemo/1/lightning.shader
%{_libdir}/ADM_plugins6/shaderDemo/1/ripple.shader
%{_libdir}/ADM_plugins6/shaderDemo/1/zigzag.shader

%dir %{_datadir}/ADM6_addons
%dir %{_datadir}/ADM6_addons/avsfilter
%{_datadir}/ADM6_addons/avsfilter/avsload.exe
%{_datadir}/ADM6_addons/avsfilter/pipe_source.dll

%dir %{_datadir}/%{name}6

%{_mandir}/man1/avidemux.1*
%{_pixmapsdir}/*.png

%dir %{_datadir}/%{name}

%if %{with gtk}
%files ui-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux3_gtk
%{_desktopdir}/%{name}-gtk.desktop
%attr(755,root,root) %{_libdir}/libADM_UIGtk6.so
%attr(755,root,root) %{_libdir}/libADM_render6_gtk.so
%attr(755,root,root) %{_libdir}/libADM_toolkitGtk.so
%{_libdir}/ADM_glade

%dir %{_libdir}/ADM_plugins6/videoFilters/gtk
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_asharpGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_chromaShiftGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_contrastGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_cropGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_eq2Gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_HueGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/gtk/libADM_vf_swscaleResize_gtk.so
%endif

%if %{with qt4}
%files ui-qt4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux3_jobs_qt4
%attr(755,root,root) %{_bindir}/avidemux3_qt4
%{_desktopdir}/%{name}-qt4.desktop
%attr(755,root,root) %{_libdir}/libADM_UIQT46.so
%attr(755,root,root) %{_libdir}/libADM_openGLQT46.so
%attr(755,root,root) %{_libdir}/libADM_render6_QT4.so

%dir %{_libdir}/ADM_plugins6/videoEncoders/qt4
# R: libx264
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/qt4/libADM_ve_x264_QT4.so
# R: libx265
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/qt4/libADM_ve_x265_QT4.so

%dir %{_libdir}/ADM_plugins6/videoFilters/qt4
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_asharpQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_blackenBordersQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_chromaShiftQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_contrastQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_cropQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_eq2QT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_glBenchmark.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_glResize.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_HueQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_logoQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_mpdelogoQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_msharpenQT4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_rotateGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_sampleGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_sampleGlVertex.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_shaderLoaderGl.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt4/libADM_vf_swscaleResizeQT4.so

%dir %{_datadir}/%{name}6/qt4
%dir %{_datadir}/%{name}6/qt4/i18n
%lang(ca) %{_datadir}/%{name}6/qt4/i18n/*_ca.qm
%lang(cs) %{_datadir}/%{name}6/qt4/i18n/*_cs.qm
%lang(da) %{_datadir}/%{name}6/qt4/i18n/*_da.qm
%lang(de) %{_datadir}/%{name}6/qt4/i18n/*_de.qm
%lang(el) %{_datadir}/%{name}6/qt4/i18n/*_el.qm
%{_datadir}/%{name}6/qt4/i18n/*_en.qm
%lang(es) %{_datadir}/%{name}6/qt4/i18n/*_es.qm
%lang(eu) %{_datadir}/%{name}6/qt4/i18n/*_eu.qm
%lang(fr) %{_datadir}/%{name}6/qt4/i18n/*_fr.qm
%lang(hu) %{_datadir}/%{name}6/qt4/i18n/*_hu.qm
%lang(it) %{_datadir}/%{name}6/qt4/i18n/*_it.qm
%lang(ja) %{_datadir}/%{name}6/qt4/i18n/*_ja.qm
%lang(ko) %{_datadir}/%{name}6/qt4/i18n/*_ko.qm
%lang(pl) %{_datadir}/%{name}6/qt4/i18n/*_pl.qm
%lang(pt) %{_datadir}/%{name}6/qt4/i18n/*_pt.qm
%lang(pt_BR) %{_datadir}/%{name}6/qt4/i18n/*_pt_BR.qm
%lang(ru) %{_datadir}/%{name}6/qt4/i18n/*_ru.qm
%lang(sr) %{_datadir}/%{name}6/qt4/i18n/*_sr.qm
%lang(sr@latin) %{_datadir}/%{name}6/qt4/i18n/*_sr@latin.qm
%lang(tr) %{_datadir}/%{name}6/qt4/i18n/*_tr.qm
%lang(zh_CN) %{_datadir}/%{name}6/qt4/i18n/*_zh_CN.qm
%lang(zh_TW) %{_datadir}/%{name}6/qt4/i18n/*_zh_TW.qm
%endif

%if %{with qt5}
%files ui-qt5
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux3_jobs_qt5
%attr(755,root,root) %{_bindir}/avidemux3_qt5
%{_desktopdir}/%{name}-qt5.desktop
%attr(755,root,root) %{_libdir}/libADM_UIQT56.so
%attr(755,root,root) %{_libdir}/libADM_openGLQT56.so
%attr(755,root,root) %{_libdir}/libADM_render6_QT5.so

%dir %{_libdir}/ADM_plugins6/videoEncoders/qt5
# R: libx264
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/qt5/libADM_ve_x264_QT5.so
# R: libx265
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/qt5/libADM_ve_x265_QT5.so

%dir %{_libdir}/ADM_plugins6/videoFilters/qt5
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_asharpQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_blackenBordersQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_chromaShiftQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_contrastQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_cropQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_eq2QT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_glBenchmark.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_glResize.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_HueQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_logoQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_mpdelogoQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_msharpenQT5.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_rotateGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_sampleGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_sampleGlVertex.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_shaderLoaderGl.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/qt5/libADM_vf_swscaleResizeQT5.so

%dir %{_datadir}/%{name}6/qt5
%dir %{_datadir}/%{name}6/qt5/i18n
%lang(ca) %{_datadir}/%{name}6/qt5/i18n/*_ca.qm
%lang(cs) %{_datadir}/%{name}6/qt5/i18n/*_cs.qm
%lang(da) %{_datadir}/%{name}6/qt5/i18n/*_da.qm
%lang(de) %{_datadir}/%{name}6/qt5/i18n/*_de.qm
%lang(el) %{_datadir}/%{name}6/qt5/i18n/*_el.qm
%{_datadir}/%{name}6/qt5/i18n/*_en.qm
%lang(es) %{_datadir}/%{name}6/qt5/i18n/*_es.qm
%lang(eu) %{_datadir}/%{name}6/qt5/i18n/*_eu.qm
%lang(fi) %{_datadir}/%{name}6/qt5/i18n/*_fi.qm
%lang(fr) %{_datadir}/%{name}6/qt5/i18n/*_fr.qm
%lang(he) %{_datadir}/%{name}6/qt5/i18n/*_he.qm
%lang(hu) %{_datadir}/%{name}6/qt5/i18n/*_hu.qm
%lang(it) %{_datadir}/%{name}6/qt5/i18n/*_it.qm
%lang(ja) %{_datadir}/%{name}6/qt5/i18n/*_ja.qm
%lang(ko) %{_datadir}/%{name}6/qt5/i18n/*_ko.qm
%lang(lv) %{_datadir}/%{name}6/qt5/i18n/*_lv.qm
%lang(pl) %{_datadir}/%{name}6/qt5/i18n/*_pl.qm
%lang(pt_BR) %{_datadir}/%{name}6/qt5/i18n/*_pt_BR.qm
%lang(ru) %{_datadir}/%{name}6/qt5/i18n/*_ru.qm
%lang(sk) %{_datadir}/%{name}6/qt5/i18n/*_sk.qm
%lang(sr) %{_datadir}/%{name}6/qt5/i18n/*_sr.qm
%lang(sr@latin) %{_datadir}/%{name}6/qt5/i18n/*_sr@latin.qm
%lang(tr) %{_datadir}/%{name}6/qt5/i18n/*_tr.qm
%lang(uk) %{_datadir}/%{name}6/qt5/i18n/*_uk.qm
%lang(zh_CN) %{_datadir}/%{name}6/qt5/i18n/*_zh_CN.qm
%lang(zh_TW) %{_datadir}/%{name}6/qt5/i18n/*_zh_TW.qm
%endif
