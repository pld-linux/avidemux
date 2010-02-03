# TODO:
# - create aften.spec (aften.sf.net) and use it -D USE_AFTEN=1
# - -ui-cli subpackage?
# - use external spidermonkey (cmake fix needed): Checking for SpiderMonkey -- Skipping check and using bundled version.
# - uses patched ffmpeg
# - don't force -O3 optimization
#
# Conditional build:
%bcond_without	esd	# disable EsounD sound support
%bcond_without	arts	# without arts audio output
%bcond_without	amr	# disable Adaptive Multi Rate (AMR) speech codec support
%bcond_without	qt4	# build qt4 interface
%bcond_without	gtk	# build gtk interface

%define		qt4_version	4.2

Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.5.2
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	9027e1324c06e833e6c3c22298503cc7
Source1:	%{name}.desktop
Source2:	%{name}-qt4.desktop
Patch0:		gcc44.patch
Patch1:		types.patch
Patch2:		qtlocale.patch
#Patch1:	%{name}-dts_internal.patch
#Patch2:	%{name}-sparc64.patch
URL:		http://fixounet.free.fr/avidemux/
%{?with_qt4:BuildRequires:	QtGui-devel >= %{qt4_version}}
BuildRequires:	SDL-devel
#BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	cmake >= 2.6.2
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	faac-devel
BuildRequires:	faad2-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gettext-devel
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

%description ui-gtk
GTK+2 UI for Avidemux

%package ui-qt4
Summary:	Qt4 UI for Avidemux
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description ui-qt4
Qt4 UI for Avidemux

%prep
%setup -q -n %{name}_%{version}
find '(' -name '*.js' -o -name '*.cpp' -o -name '*.h' -o -name '*.cmake' -o -name '*.txt' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1
%patch1 -p1
%patch2 -p1

echo 'pt_BR' >> po/LINGUAS

# libdir fix
sed -i -e's,"lib","%{_lib}",' avidemux/main.cpp avidemux/ADM_core/src/ADM_fileio.cpp

%build
TOP=$PWD

# main
install -d build/%{_lib} plugins/build
cd build

export QTDIR=%{_libdir}/qt4
%cmake \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:Release} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DAVIDEMUX_INSTALL_PREFIX=%{_prefix} \
	%{!?with_gtk:-DGTK=0} \
	%{!?with_qt4:-DQT4=0} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..

%{__make}

# plugin build expects libraries to be already installed; we fake a prefix
# in build/ by symlinking all libraries to build/lib/
cd %{_lib}
find ../avidemux -name '*.so*' | xargs ln -sft .
cd ../..

# plugins
cd plugins/build
%cmake \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:Release} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DAVIDEMUX_INSTALL_PREFIX=$TOP/build \
	-DAVIDEMUX_SOURCE_DIR=$TOP/  \
	-DAVIDEMUX_CORECONFIG_DIR=$TOP/build/config \
	%{!?with_arts:-DARTS=0} \
	%{!?with_esd:-DESD=0} \
	%{!?with_amr:-DOPENCORE_AMRNB=0 -DOPENCORE_AMRWB=0} \
	%{!?with_gtk:-DGTK=0} \
	%{!?with_qt4:-DQT4=0} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_bindir},%{_mandir}/man1}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C plugins/build install \
	DESTDIR=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

mv $RPM_BUILD_ROOT%{_bindir}/avidemux2{_cli,}
cp -a man/avidemux.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-gtk.desktop
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-qt4.desktop
cp -a avidemux_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/avidemux2
%attr(755,root,root) %{_libdir}/libADM5avcodec.so.52
%attr(755,root,root) %{_libdir}/libADM5avformat.so.52
%attr(755,root,root) %{_libdir}/libADM5avutil.so.50
%attr(755,root,root) %{_libdir}/libADM5postproc.so.51
%attr(755,root,root) %{_libdir}/libADM5swscale.so.0
%attr(755,root,root) %{_libdir}/libADM_UICli.so
%attr(755,root,root) %{_libdir}/libADM_core.so
%attr(755,root,root) %{_libdir}/libADM_coreAudio.so
%attr(755,root,root) %{_libdir}/libADM_coreImage.so
%attr(755,root,root) %{_libdir}/libADM_coreUI.so
%attr(755,root,root) %{_libdir}/libADM_render_cli.so
%attr(755,root,root) %{_libdir}/libADM_smjs.so

%dir %{_libdir}/ADM_plugins
%dir %{_libdir}/ADM_plugins/audioDecoder
%dir %{_libdir}/ADM_plugins/audioDevices
%dir %{_libdir}/ADM_plugins/audioEncoders
%dir %{_libdir}/ADM_plugins/videoEncoder
%dir %{_libdir}/ADM_plugins/videoEncoder/avcodec
%dir %{_libdir}/ADM_plugins/videoEncoder/x264
%dir %{_libdir}/ADM_plugins/videoEncoder/xvid
%dir %{_libdir}/ADM_plugins/videoFilter

%{_libdir}/ADM_plugins/videoEncoder/avcodec/Mpeg1Param.xsd
%{_libdir}/ADM_plugins/videoEncoder/xvid/XvidParam.xsd
%{_libdir}/ADM_plugins/videoEncoder/x264/Apple*.xml
%{_libdir}/ADM_plugins/videoEncoder/x264/Microsoft*.xml
%{_libdir}/ADM_plugins/videoEncoder/x264/Sony*.xml
%{_libdir}/ADM_plugins/videoEncoder/x264/x264Param.xsd

%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_Mad.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_a52.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_faad.so
%if %{with amr}
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_opencore_amrnb.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_opencore_amrwb.so
%endif

%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_alsa.so
%{?with_arts:%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_arts.so}
%{?with_esd:%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_esd.so}
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_jack.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_oss.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_pulseAudioSimple.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDevices/libADM_av_sdl.so

%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_faac.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_lame.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_lav_ac3.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_lav_mp2.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_pcm.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_twolame.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioEncoders/libADM_ae_vorbis.so

%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/libADM_vidEnc_avcodec.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/libADM_vidEnc_xvid.so

%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_addborders.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_asharp_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_avisynthResize_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_blackenBorders.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_blendDgBob.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_blendRemoval.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_chromashift_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_cnr2_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_colorYUV_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_contrast_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_crop_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_decimate.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Deinterlace.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Delta.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_denoise3dhq.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_denoise3d.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Denoise.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_dropOut.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_eq2_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_equalizer_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_fade.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_fastconvolutiongauss.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_fastconvolutionmean.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_fastconvolutionmedian.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_fastconvolutionsharpen.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_FluxSmooth.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_forcedPP.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Hue_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_hzStackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_keepEvenField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_keepOddField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_kernelDeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_largemedian.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_lavDeinterlace.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_lumaonly.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mcdeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mergeField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Mosaic.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mpdelogo_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mplayerResize_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mSharpen.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mSmooth.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_palShift.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Pulldown.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_resampleFps.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_reverse.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_rotate.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_separateField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_smartPalShift.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_smartSwapField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_soften.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_ssa.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Stabilize.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_stackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_sub_cli.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_swapField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_swapuv.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_tdeint.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_telecide.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Tisophote.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_unstackField.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_vflip.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_vlad.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Whirl.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_yadif.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vidChromaU.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vidChromaV.so
%{_mandir}/man1/avidemux.1*
%{_pixmapsdir}/*.png

%{_datadir}/ADM_scripts

%dir %{_datadir}/%{name}

%if %{with gtk}
%files ui-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux2_gtk
%{_desktopdir}/%{name}-gtk.desktop
%attr(755,root,root) %{_libdir}/libADM_UIGtk.so
%attr(755,root,root) %{_libdir}/libADM_render_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/x264/libADM_vidEnc_x264_Gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/xvid/libADM_vidEnc_Xvid_Gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_asharp_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_avisynthResize_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_chromaShift_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_cnr2_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_colorYUV_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_contrast_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_Crop_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_eq2_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_equalizer_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_hue_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mpdelogo_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mplayerResize_gtk.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_sub_gtk.so
%endif

%if %{with qt4}
%files ui-qt4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/avidemux2_qt4
%{_desktopdir}/%{name}-qt4.desktop
%attr(755,root,root) %{_libdir}/libADM_UIQT4.so
%attr(755,root,root) %{_libdir}/libADM_render_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/audioDecoder/libADM_ad_vorbis.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/libADM_vidEnc_x264.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/x264/libADM_vidEnc_x264_Qt.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoEncoder/xvid/libADM_vidEnc_Xvid_Qt.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_asharp_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_avisynthResize_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_chromaShift_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_cnr2_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_colorYUV_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_contrast_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_crop_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_curveEditor_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_eq2_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_equalizer_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_hue_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mpdelogo_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_mplayerResize_qt4.so
%attr(755,root,root) %{_libdir}/ADM_plugins/videoFilter/libADM_vf_sub_qt4.so

%dir %{_datadir}/%{name}/i18n
%lang(ca) %{_datadir}/%{name}/i18n/*_ca.qm
%lang(cs) %{_datadir}/%{name}/i18n/*_cs.qm
%lang(de) %{_datadir}/%{name}/i18n/*_de.qm
%lang(el) %{_datadir}/%{name}/i18n/*_el.qm
%lang(es) %{_datadir}/%{name}/i18n/*_es.qm
%lang(fr) %{_datadir}/%{name}/i18n/*_fr.qm
%lang(it) %{_datadir}/%{name}/i18n/*_it.qm
%lang(ja) %{_datadir}/%{name}/i18n/*_ja.qm
%lang(pt_BR) %{_datadir}/%{name}/i18n/*_pt_BR.qm
%lang(ru) %{_datadir}/%{name}/i18n/*_ru.qm
%lang(sr) %{_datadir}/%{name}/i18n/*_sr.qm
%lang(sr@latin) %{_datadir}/%{name}/i18n/*_sr@latin.qm
%lang(tr) %{_datadir}/%{name}/i18n/*_tr.qm
%lang(zh_TW) %{_datadir}/%{name}/i18n/*_zh_TW.qm
%endif
