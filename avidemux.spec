# TODO:
# - create aften.spec (aften.sf.net) and use it -D USE_AFTEN=1
# - -ui-cli subpackage?
# - use external spidermonkey (cmake fix needed): Checking for SpiderMonkey -- Skipping check and using bundled version.
# - uses patched ffmpeg
# - don't force -O3 optimization
# - get rid of gcc-bug-mmx-x86 patch
#
# Conditional build:
%bcond_with	esd	# disable EsounD sound support
%bcond_with	arts	# with arts audio output
%bcond_without	amr	# disable Adaptive Multi Rate (AMR) speech codec support
%bcond_without	qt4	# build qt4 interface
%bcond_without	gtk	# build gtk interface

%define		qt4_version	4.2

Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.6.4
Release:	3
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	adb9110ab230fe13a8e9799f547f2f57
Source1:	%{name}.desktop
Source2:	%{name}-qt4.desktop
Patch0:		build.patch
Patch1:		no-qt-in-gtk.patch
URL:		http://fixounet.free.fr/avidemux/
%{?with_qt4:BuildRequires:	QtGui-devel >= %{qt4_version}}
BuildRequires:	SDL-devel
#BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0
BuildRequires:	bash
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	cmake >= 2.6.2
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	faac-devel
BuildRequires:	faad2-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gettext-tools
%{?with_gtk:BuildRequires:	gtk+2-devel >= 1:2.6.0}
BuildRequires:	jack-audio-connection-kit-devel
#BuildRequires:	js-devel(threads)
BuildRequires:	lame-libs-devel
#BuildRequires:	libdca-devel
#BuildRequires:	libdts-devel
#BuildRequires:	libmad-devel
#BuildRequires:	libmpeg3-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libx264-devel
BuildRequires:	libxml2-devel
%{?with_qt4:BuildRequires:	libxslt-progs}
%ifarch %{ix86}
BuildRequires:	nasm >= 0.98.32
%endif
%{?with_amr:BuildRequires:	opencore-amr-devel}
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
%{?with_qt4:BuildRequires:	qt4-build >= %{qt4_version}}
%{?with_qt4:BuildRequires:	qt4-linguist}
%{?with_qt4:BuildRequires:	qt4-qmake >= %{qt4_version}}
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-proto-xextproto-devel
BuildRequires:	xvid-devel >= 1:1.0
BuildRequires:	xvidcore-devel
BuildRequires:	zlib-devel
#Requires:	js(threads)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl.UTF-8
Mały edytor audio/wideo dla Linuksa.

%package ui-gtk
Summary:	GTK+2 UI for Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	desktop-file-utils

%description ui-gtk
GTK+2 UI for Avidemux

%package ui-qt4
Summary:	Qt4 UI for Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	desktop-file-utils

%description ui-qt4
Qt4 UI for Avidemux

%prep
%setup -q -n %{name}_%{version}
find '(' -name '*.js' -o -name '*.cpp' -o -name '*.h' -o -name '*.cmake' -o -name '*.txt' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1
%patch1 -p1

echo 'pt_BR' >> po/LINGUAS

# libdir fix
%{__sed} -i -e's,"lib","%{_lib}",' avidemux/common/main.cpp avidemux_core/ADM_core/src/ADM_fileio.cpp

%build
bash ./bootStrap.bash \
	--with-core \
	--with-cli \
	--with-gtk \
	--with-qt4 \
	--with-plugins

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_bindir},%{_mandir}/man1}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -a install/* $RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

mv $RPM_BUILD_ROOT%{_bindir}/avidemux3{_cli,}
cp -a man/avidemux.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-gtk.desktop
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-qt4.desktop
cp -a avidemux_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{__rm} -r $RPM_BUILD_ROOT%{_includedir}

#find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post ui-gtk
%update_desktop_database

%post ui-qt4
%update_desktop_database

#files -f %{name}.lang
%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/avidemux3
%attr(755,root,root) %{_libdir}/libADM6avcodec.so.54
%attr(755,root,root) %{_libdir}/libADM6avformat.so.54
%attr(755,root,root) %{_libdir}/libADM6avutil.so.52
%attr(755,root,root) %{_libdir}/libADM6postproc.so.52
%attr(755,root,root) %{_libdir}/libADM6swscale.so.2
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
%attr(755,root,root) %{_libdir}/libADM_coreMuxer6.so
%attr(755,root,root) %{_libdir}/libADM_coreScript.so
%attr(755,root,root) %{_libdir}/libADM_coreSocket6.so
%attr(755,root,root) %{_libdir}/libADM_coreSqlLight3.so
%attr(755,root,root) %{_libdir}/libADM_coreUtils6.so
%attr(755,root,root) %{_libdir}/libADM_coreVDPAU6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoCodec6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoEncoder6.so
%attr(755,root,root) %{_libdir}/libADM_coreVideoFilter6.so

%dir %{_libdir}/ADM_plugins6
%dir %{_libdir}/ADM_plugins6/audioDecoder
%dir %{_libdir}/ADM_plugins6/audioDevices
%dir %{_libdir}/ADM_plugins6/audioEncoders
%dir %{_libdir}/ADM_plugins6/videoDecoders
%dir %{_libdir}/ADM_plugins6/videoEncoders
%dir %{_libdir}/ADM_plugins6/videoFilters
%dir %{_libdir}/ADM_plugins6/autoScripts
%dir %{_libdir}/ADM_plugins6/autoScripts/lib
%dir %{_libdir}/ADM_plugins6/demuxers
%dir %{_libdir}/ADM_plugins6/muxers
%dir %{_libdir}/ADM_plugins6/pluginSettings
%dir %{_libdir}/ADM_plugins6/pluginSettings/x264
%dir %{_libdir}/ADM_plugins6/pluginSettings/x264/1
%dir %{_libdir}/ADM_plugins6/scriptEngines

%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_Mad.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_a52.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_faad.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_vorbis.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_dca.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ima_adpcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_lav.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ms_adpcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_ulaw.so
%if %{with amr}
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_opencore_amrnb.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDecoder/libADM_ad_opencore_amrwb.so
%endif

%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaDMix.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaDefault.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_alsaHw.so
%{?with_arts:%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_arts.so}
%{?with_esd:%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_esd.so}
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_jack.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_oss.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_pulseAudioSimple.so
#%attr(755,root,root) %{_libdir}/ADM_plugins6/audioDevices/libADM_av_sdl.so

%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_faac.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lame.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_ac3.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_mp2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_pcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_twolame.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_vorbis.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/audioEncoders/libADM_ae_lav_aac.so

%attr(755,root,root) %{_libdir}/ADM_plugins6/videoDecoders/libADM_vd_vpx.so

%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_x264_other.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_xvid4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffFlv1.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffMpeg2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_ffMpeg4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_huff.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_jpeg.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_null.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_png.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_yv12.so

%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_addBorders.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_avsfilter.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_blackenBorders.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_DgBob.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_chromaShiftCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_colorYuv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_contrastCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_decimate.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_denoise3dhq.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_denoise3d.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_eq2Cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_fadeToBlack.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_gauss.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mean.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_median.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_sharpen.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_FluxSmooth.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_HueCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_hzstackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_kernelDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_largeMedian.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_lavDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_logo.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_lumaOnly.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mergeField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mpdelogoCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_resampleFps.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_rotate.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_separateField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_ssa.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_stackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_swapUV.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_telecide.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_unstackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vflip.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_yadif.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_hf_hflip.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_CropCli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_changeFps.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_dummy.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_msharpen.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_printInfo.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_removePlane.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_swscaleResize_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vdpauFilter.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_vdpauFilterDeint.so

%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/720p.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/PSP.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/check24fps.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/dvd.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/lib/ADM_image.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/lib/ADM_imageInfo.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/svcd.py
%attr(755,root,root) %{_libdir}/ADM_plugins6/autoScripts/vcd.py
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
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_Mkv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_avi.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_dummy.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_ffPS.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_ffTS.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_flv.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_mp4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_mp4v2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/muxers/libADM_mx_raw.so
%{_libdir}/ADM_plugins6/pluginSettings/x264/1/PSP.json
%{_libdir}/ADM_plugins6/pluginSettings/x264/1/iPhone.json
%attr(755,root,root) %{_libdir}/ADM_plugins6/scriptEngines/libADM_script_spiderMonkey.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/scriptEngines/libADM_script_tinyPy.so

%dir %{_datadir}/ADM6_addons
%dir %{_datadir}/ADM6_addons/avsfilter
%{_datadir}/ADM6_addons/avsfilter/avsload.exe
%{_datadir}/ADM6_addons/avsfilter/pipe_source.dll

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
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_asharpGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_chromaShiftGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_contrastGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_cropGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_eq2Gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_HueGtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_swscaleResize_gtk.so
%{_libdir}/ADM_glade
%endif

%if %{with qt4}
%files ui-qt4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux3_jobs
%attr(755,root,root) %{_bindir}/avidemux3_qt4
%{_desktopdir}/%{name}-qt4.desktop
%attr(755,root,root) %{_libdir}/libADM_UIQT46.so
%attr(755,root,root) %{_libdir}/libADM_render6_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoEncoders/libADM_ve_x264_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_asharpQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_chromaShiftQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_contrastQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_cropQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_eq2Qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_HueQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_swscaleResize_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_mpdelogoQt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_glBenchmark.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_glResize.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_rotateGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_sampleGlFrag2.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/videoFilters/libADM_vf_sampleGlVertex.so
%attr(755,root,root) %{_libdir}/ADM_plugins6/scriptEngines/libADM_script_qt.so

%dir %{_datadir}/%{name}6
%{_datadir}/%{name}6/help

%dir %{_datadir}/%{name}6/i18n
%lang(ca) %{_datadir}/%{name}6/i18n/*_ca.qm
%lang(cs) %{_datadir}/%{name}6/i18n/*_cs.qm
%lang(de) %{_datadir}/%{name}6/i18n/*_de.qm
%lang(el) %{_datadir}/%{name}6/i18n/*_el.qm
%{_datadir}/%{name}6/i18n/*_en.qm
%lang(es) %{_datadir}/%{name}6/i18n/*_es.qm
%lang(eu) %{_datadir}/%{name}6/i18n/*_eu.qm
%lang(fr) %{_datadir}/%{name}6/i18n/*_fr.qm
%lang(it) %{_datadir}/%{name}6/i18n/*_it.qm
%lang(ja) %{_datadir}/%{name}6/i18n/*_ja.qm
%lang(pl) %{_datadir}/%{name}6/i18n/*_pl.qm
%lang(pt_BR) %{_datadir}/%{name}6/i18n/*_pt_BR.qm
%lang(ru) %{_datadir}/%{name}6/i18n/*_ru.qm
%lang(sr) %{_datadir}/%{name}6/i18n/*_sr.qm
%lang(sr@latin) %{_datadir}/%{name}6/i18n/*_sr@latin.qm
%lang(tr) %{_datadir}/%{name}6/i18n/*_tr.qm
%lang(zh_TW) %{_datadir}/%{name}6/i18n/*_zh_TW.qm
%endif
