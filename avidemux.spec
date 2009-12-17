# TODO:
# - create aften.spec (aften.sf.net) and use it
# - needs some cmake magican to fixup the bconds
# - use external seamonkey (cmake fix needed): Checking for SpiderMonkey -- Skipping check and using bundled version.
# - sync or use .desktop from sources
# - subpackages per ui engine
# - uses patched ffmpeg
# - the bconds don't work with cmake, all gets enabled if BR found
# - Could not find Gettext -- libintl not required for gettext support
#
# Conditional build:
%bcond_without	esd	# disable EsounD sound support
%bcond_without	arts	# without arts audio output
%bcond_with	amr	# enable 3GPP Adaptive Multi Rate (AMR) speech codec support
%bcond_without	qt4	# build qt4-base interface
%bcond_with	ssse3	# use SSSE3 instructions

%define		qt4_version	4.2

%ifarch pentium4 %{x8664}
%define		with_sse3	1
%endif

Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.5.1
Release:	0.8
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	081db3af87f1f93c7b4e5d5975e07e40
Source1:	%{name}.desktop
Patch0:		gcc44.patch
Patch1:		types.patch
Patch2:		qtlocale.patch
Patch3:		link-libs.patch
Patch4:		libdir.patch
#Patch1:	%{name}-dts_internal.patch
#Patch2:	%{name}-sparc64.patch
URL:		http://fixounet.free.fr/avidemux/
%{?with_qt4:BuildRequires:	QtGui-devel >= %{qt4_version}}
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0
%{?with_amr:BuildRequires:	amrnb-devel}
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	cmake >= 2.6.2
%{?with_esd:BuildRequires:	esound-devel}
BuildRequires:	faac-devel
BuildRequires:	faad2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 1:2.6.0
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	js-devel(threads)
BuildRequires:	lame-libs-devel
#BuildRequires:	libdca-devel
BuildRequires:	libdts-devel
BuildRequires:	libmad-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libpng-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	libx264-devel
BuildRequires:	libxml2-devel
BuildRequires:	nasm >= 0.98.32
BuildRequires:	pkgconfig
%{?with_qt4:BuildRequires:	qt4-build >= %{qt4_version}}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-proto-xextproto-devel
BuildRequires:	xvid-devel >= 1:1.0
BuildRequires:	xvidcore-devel
BuildRequires:	zlib-devel
Requires:	js(threads)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl.UTF-8
Mały edytor audio/wideo dla Linuksa.

%prep
%setup -q -n %{name}_%{version}
find '(' -name '*.js' -o -name '*.cpp' -o -name '*.h' -o -name '*.cmake' -o -name '*.txt' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

echo 'pt_BR' >> po/LINGUAS

# libdir fix
grep -rl 'DESTINATION lib' . | xargs sed -i -e's,DESTINATION lib,DESTINATION lib${LIB_SUFFIX},g'
sed -i -e's,FFMPEG_INSTALL_DIR lib,FFMPEG_INSTALL_DIR lib${LIB_SUFFIX},' cmake/admFFmpegBuild.cmake
sed -i -e's,"lib","%{_lib}",' avidemux/main.cpp avidemux/ADM_core/src/ADM_fileio.cpp

%build
TOP=$PWD
# main
install -d build plugin-build
cd build
%cmake \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:Release} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DAVIDEMUX_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..
%{__make}
cd ..

# plugins
cd plugin-build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DAVIDEMUX_INSTALL_PREFIX=%{_prefix} \
	-DAVIDEMUX_SOURCE_DIR=$TOP/  \
	-DAVIDEMUX_CORECONFIG_DIR=$TOP/build/config \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../plugins

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_bindir},%{_mandir}/man1}
#install -d $RPM_BUILD_ROOT%{_libdir}/ADM_plugins/{audioDecoder,videoFilter,audioDevices,audioEncoders}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C plugin-build install \
	DESTDIR=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

cp -a man/avidemux.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a avidemux_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png
install -p build/avidemux/avidemux2_gtk $RPM_BUILD_ROOT%{_bindir}/avidemux2_gtk

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/avidemux2_cli
%attr(755,root,root) %{_bindir}/avidemux2_gtk
%{?with_qt4:%attr(755,root,root) %{_bindir}/avidemux2_qt4}
%attr(755,root,root) %{_libdir}/libADM5avcodec.so.52
%attr(755,root,root) %{_libdir}/libADM5avformat.so.52
%attr(755,root,root) %{_libdir}/libADM5avutil.so.50
%attr(755,root,root) %{_libdir}/libADM5postproc.so.51
%attr(755,root,root) %{_libdir}/libADM5swscale.so.0
%attr(755,root,root) %{_libdir}/libADM_UICli.so
%attr(755,root,root) %{_libdir}/libADM_UIGtk.so
%{?with_qt4:%attr(755,root,root) %{_libdir}/libADM_UIQT4.so}
%attr(755,root,root) %{_libdir}/libADM_core.so
%attr(755,root,root) %{_libdir}/libADM_coreAudio.so
%attr(755,root,root) %{_libdir}/libADM_coreImage.so
%attr(755,root,root) %{_libdir}/libADM_coreUI.so
%attr(755,root,root) %{_libdir}/libADM_render_cli.so
%attr(755,root,root) %{_libdir}/libADM_render_gtk.so
%{?with_qt4:%attr(755,root,root) %{_libdir}/libADM_render_qt4.so}
%attr(755,root,root) %{_libdir}/libADM_smjs.so

%dir %{_libdir}/ADM_plugins
%dir %{_libdir}/ADM_plugins/audioDecoder
%dir %{_libdir}/ADM_plugins/videoFilter
%dir %{_libdir}/ADM_plugins/audioDevices
%dir %{_libdir}/ADM_plugins/audioEncoders

%{_datadir}/ADM_scripts

%dir %{_datadir}/%{name}
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

%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
