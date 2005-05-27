Summary:	A small audio/video editing software for Linux
Summary(pl):	Ma³y edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.0.40
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://download.berlios.de/avidemux/%{name}-%{version}.tar.gz
# Source0-md5:	eed30487a2ae62f927c8a84dbc889e6d
Source1:	%{name}.desktop
Patch0:		%{name}-autoconf.patch
URL:		http://fixounet.free.fr/avidemux/
BuildRequires:	SDL-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel
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
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	xvid-devel >= 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl
Ma³y edytor audio/wideo dla Linuksa.

%prep
%setup -q
%patch0 -p1

%{__perl} -pi -e 's/-g|-O2//g' adm_lavcodec/Makefile
%{__perl} -pi -e 's/charset=Unicode/charset=UTF-8/' po/ru.po

%build
cp /usr/share/automake/config.sub admin
%{__gettextize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure
%{__make} \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
#%files
%defattr(644,root,root,755)
%doc AUTHORS History
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
