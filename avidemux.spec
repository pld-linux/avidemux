# TODO
# - buold errors on ppc:
#postprocess_template.c: In function `vertX1Filter_altivec_template':
#postprocess_template.c:516: error: can't convert between vector values of different size
#make[3]: *** [postprocess.o] Error 1
#
Summary:	A small audio/video editing software for Linux
Summary(pl):	Ma³y edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.0.42
Release:	1
License:	GPL v2
Group:		X11/Applications/Multimedia
Source0:	http://download.berlios.de/avidemux/%{name}-%{version}.tar.gz
# Source0-md5:	d30f1bb981767bca793d78067bcfe084
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-autoconf.patch
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
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	lame-libs-devel
BuildRequires:	libmad-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xvid-devel >= 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl
Ma³y edytor audio/wideo dla Linuksa.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's/charset=Unicode/charset=UTF-8/' po/ru.po
%{__sed} -i 's/klingon//' po/LINGUAS

%build
cp /usr/share/automake/config.sub admin
%{__gettextize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
%ifarch ppc
	--enable-altivec \
%endif
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS History
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
