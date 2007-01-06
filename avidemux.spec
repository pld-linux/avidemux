Summary:	A small audio/video editing software for Linux
Summary(pl):	Ma³y edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.3.0
Release:	0.1
License:	GPL v2
Group:		X11/Applications/Multimedia
Source0:	http://download2.berlios.de/avidemux/%{name}_%{version}.tar.gz
# Source0-md5:	14c58c14fc9757d36e4d72498431da42
Source1:	%{name}.desktop
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-dts_internal.patch
URL:		http://fixounet.free.fr/avidemux/
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 1.0
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
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xvid-devel >= 1:1.0
Requires:	js(threads)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl
Ma³y edytor audio/wideo dla Linuksa.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1
%patch1 -p0

%{__sed} -i 's/charset=Unicode/charset=UTF-8/' po/ru.po
%{__sed} -i 's/klingon/de\npt_BR/' po/LINGUAS

%build
cp /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common
#%{__gettextize}
#%{__aclocal} -I m4
#%{__autoheader}
#%{__automake}
#%{__autoconf}

%configure \
%ifarch ppc
	--enable-altivec \
%endif
	--with-newfaad \
	--with-jsapi-include=%{_includedir}/js \
	--disable-static

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
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
