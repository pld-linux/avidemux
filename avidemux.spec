Summary:	A small audio/video editing software for Linux
Summary(pl):	Ma³y edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.0.16
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://fixounet.free.fr/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	89e4ac8f832328e8761a7c3035d4d4bc
URL:		http://fixounet.free.fr/avidemux/
Patch0:		%{name}-lameh.patch
BuildRequires:	a52dec-libs-devel
#BuildRequires:	divx4linux-devel
BuildRequires:	esound-devel
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	libxml2-devel
BuildRequires:	xvid-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	libmad-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libvorbis-devel
BuildRequires:	mad-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small audio/video editing software for Linux.

%description -l pl
Ma³y edytor audio/wideo dla Linuksa.

%prep
%setup -q
#%patch0 -p1

%build
#CPPFLAGS="-I/usr/include/divx -I/usr/include/libmpeg3"

# dirty hack, so we are avoiding ac/am madness
echo timestamp > stamp-h.in

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README AUTHORS TODO
%attr(755,root,root) %{_bindir}/*
