Summary:	A small audio/video editing software for Linux
Summary(pl):	Ma³y edytor audio/wideo dla Linuksa
Name:		avidemux
Version:	2.0.18
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://fixounet.free.fr/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	5236a00d4a56b25df2c5f28fa8a40ce8
URL:		http://fixounet.free.fr/avidemux/
BuildRequires:	a52dec-libs-devel
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README AUTHORS TODO
%attr(755,root,root) %{_bindir}/*
