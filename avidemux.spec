# TODO:
#	- create aften.spec (aften.sf.net) and use it
#
# Conditional build:
%bcond_with	amr	# enable 3GPP Adaptive Multi Rate (AMR) speech codec support
%bcond_with	qt	# build qt4-base interface
#
Summary:	A small audio/video editing software for Linux
Summary(pl.UTF-8):	Mały edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.4.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://download2.berlios.de/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	2d972f6b8795c891dd6e0ebe5035852a
Source1:	%{name}.desktop
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-dts_internal.patch
Patch2:		%{name}-sparc64.patch
URL:		http://fixounet.free.fr/avidemux/
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0
%{?with_amr:BuildRequires:	amrnb-devel}
BuildRequires:	artsc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel
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
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	libx264-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
%{?with_qt:BuildRequires:	QtGui-devel}
%{?with_qt:BuildRequires:	qt4-build}
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xvid-devel >= 1:1.0
Requires:	js(threads)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl.UTF-8
Mały edytor audio/wideo dla Linuksa.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1

echo 'pt_BR' >> po/LINGUAS

%build
export kde_htmldir=%{_kdedocdir}
export kde_libs_htmldir=%{_kdedocdir}
%{__make} -f admin/Makefile.common cvs
%{__libtoolize}
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%configure \
	%{!?with_amr:ac_cv_header_amrnb_interf_dec_h=no} \
	--disable-static \
%ifarch ppc
	--enable-altivec \
%endif
	--with-jsapi-include=%{_includedir}/js \
%if %{with qt}
	--with-qt-dir=%{_prefix} \
	--with-qt-include=%{_includedir}/qt4 \
	--with-qt-lib=%{_libdir}
%endif

%{__make} -j1 -C po
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install avidemux_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS History
%attr(755,root,root) %{_bindir}/avidemux2_cli
%attr(755,root,root) %{_bindir}/avidemux2_gtk
%{?with_qt:%attr(755,root,root) %{_bindir}/avidemux2_qt4}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
