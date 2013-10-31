Name:           notion
Version:        3.2013030200
Release:        1%{?dist}
Summary:        Tabbed, tiling window manager. Fork of Ion3.

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/notion-3-2013030200-src.tar.bz2

BuildRequires:  pkgconfig
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
#BuildRequires:  glib2-devel
BuildRequires:  lua
BuildRequires:  libXext-devel
BuildRequires:  libSM-devel

Requires:       glib2
Requires:       gettext
Requires:       lua
Requires:       libXext
Requires:       libSM
#Requires:       libXinerama
#Requires:       libXrandr

Provides:       libtu
Provides:       libextl

%description
Notion is a tabbed, tiling window manager for the X windows system. Features include:
* Workspaces: each workspace has its own tiling.
* Multiheaded
* RandR support
* Extensible via Lua scripts.

%prep
%setup -q -n notion-3-2013030200

sed -e 's/^\(PREFIX=\).*$/\1\/usr/' \
    -e 's/^\(ETCDIR=\).*$/\1\/etc\/notion/' \
    -e 's/^\(LUA_DIR=\).*$/\1\/usr/' \
    -e 's/^\(X11_PREFIX=\).*/\1\/usr/' \
    -e 's|^\(LIBDIR=\).*|\1%{_libdir}|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

%check
#make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc README LICENSE
# to do


%changelog

