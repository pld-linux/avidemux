# TODO:
# - create aften.spec (aften.sf.net) and use it
# - needs some cmake magican to fixup the bconds
# - use external seamonkey (cmake fix needed): Checking for SpiderMonkey -- Skipping check and using bundled version.
# - sync or use .desktop from sources
# - subpackages per ui engine
# - uses patched ffmpeg
# - the bconds don't work with cmake, all gets enabled if BR found
# - Could not find Gettext -- libintl not required for gettext support
# - fix lib64 libdir install
# - i18n in /usr/bin/i18n
# - fix plugin scan dir: Scanning directory /usr/lib/ADM_plugins/audioDecoder/
#
# Conditional build:
%bcond_without	esd	# disable EsounD sound support
%bcond_without	arts	# without arts audio output
%bcond_with	amr	# enable 3GPP Adaptive Multi Rate (AMR) speech codec support
%bcond_without	qt4	# build qt4-base interface
%bcond_with	ssse3	# use SSSE3 instructions

%ifarch pentium4 %{x8664}
%define		with_sse3	1
%endif

%define		qt4_version	4.2

Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.5.1
Release:	0.2
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	081db3af87f1f93c7b4e5d5975e07e40
Source1:	%{name}.desktop
Patch0:		gcc44.patch
Patch1:		types.patch
#Patch0:	%{name}-autoconf.patch
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
BuildRequires:	faad2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 1:2.6.0
BuildRequires:	js-devel(threads)
BuildRequires:	lame-libs-devel
BuildRequires:	libdts-devel
BuildRequires:	libmad-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	libx264-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
%{?with_qt4:BuildRequires:	qt4-build >= %{qt4_version}}
BuildRequires:	sed >= 4.0
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-proto-xextproto-devel
BuildRequires:	xvid-devel >= 1:1.0
BuildRequires:	zlib-devel
Requires:	js(threads)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl.UTF-8
Mały edytor audio/wideo dla Linuksa.

%prep
%setup -q -n %{name}_%{version}
#%patch0 -p1
#%patch1 -p0
#%patch2 -p1

find '(' -name '*.js' -o -name '*.cpp' -o -name '*.h' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch0 -p1
%patch1 -p1

echo 'pt_BR' >> po/LINGUAS

%build
install -d build
cd build
%cmake \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:Release} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	..
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_bindir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if "%{_lib}" != "lib"
mv $RPM_BUILD_ROOT{%{_prefix}/lib,%{_libdir}}
%endif

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

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
%attr(755,root,root) %{_libdir}/libADM_UIQT4.so
%attr(755,root,root) %{_libdir}/libADM_core.so
%attr(755,root,root) %{_libdir}/libADM_coreAudio.so
%attr(755,root,root) %{_libdir}/libADM_coreImage.so
%attr(755,root,root) %{_libdir}/libADM_coreUI.so
%attr(755,root,root) %{_libdir}/libADM_render_cli.so
%attr(755,root,root) %{_libdir}/libADM_render_gtk.so
%{?with_qt4:%attr(755,root,root) %{_libdir}/libADM_render_qt4.so}
%attr(755,root,root) %{_libdir}/libADM_smjs.so
%{_datadir}/ADM_scripts
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
