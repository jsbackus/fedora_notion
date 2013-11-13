Name:           notion
Version:        3.2013030200
Release:        1%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/notion-3-2013030200-src.tar.bz2
#Source1:        git://notion.git.sourceforge.net/gitroot/notion/notion-doc
# The doc package was pulled from upstream's git repo. Use the following command:
# 
Source1:        https://www.dropbox.com/sh/n1icl72l63dy9tr/jFYmjjqH-f/notion-doc-3-2013030200.tar.bz2
#
Source2:        https://www.dropbox.com/sh/n1icl72l63dy9tr/Qurc5REVFy/notion.desktop

Patch0:         https://www.dropbox.com/sh/n1icl72l63dy9tr/QlpDOhk8Vc/notion-3.2013030200.p00-man-utf8.patch
Patch1:         https://www.dropbox.com/sh/n1icl72l63dy9tr/Pc9uyH5Boo/notion-3.2013030200.p01-fsf_addr.patch
Patch2:         https://www.dropbox.com/sh/n1icl72l63dy9tr/dwIWWPddTE/notion-doc-3.2013030200.p02-css_newline.patch
Patch3:         https://www.dropbox.com/sh/n1icl72l63dy9tr/_4wS0oLCEX/notion-3.2013030200.p03-ChangeLog_update.patch

BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  lua
BuildRequires:  lua-devel
BuildRequires:  libXext-devel
BuildRequires:  libSM-devel

BuildRequires:  rubber
BuildRequires:  latex2html
BuildRequires:  texlive-collection-htmlxml
BuildRequires:  texlive-collection-latexextra

Requires:       xterm
Requires:       xorg-x11-utils
# This package provides Helvetica 12px.
#Requires:       xorg-x11-fonts-75dpi

%description
Notion is a tabbed, tiling window manager for the X windows system.

Features include:
* Workspaces: each work space has its own tiling.
* Multiheaded
* RandR support
* Extensible via Lua scripts.

%package contrib
Summary:        3rd party scripts for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        GPLv3 and Public Domain and GPLv2+ and Artistic clarified and LGPLv2+ and GPL+ and GPLv2 and BSD and 
BuildArch:      noarch

Requires:       terminus-fonts
#Requires:       bitstream-vera-sans-fonts
#Requires:       artwiz-aleczapka-snap-fonts

%description contrib
This package contains a number of scripts from third parties for Notion, 
such as:
* Alternative keybindings
* Miscellaneous support scripts
* Status monitors for the status bar
* Additional styles

Scripts are installed into /usr/share/notion/contrib. To use,
copy/link the script(s) you want into ~/.notion and restart Notion.

%package doc
Summary:        Documentation for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        GFDL
BuildArch:      noarch
%description doc
This package contains the documentation for extending and customizing 
Notion.

%package devel
Summary:        Development files for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
This package contains the development files necessary for extending and 
customizing Notion.

%prep
%setup -q -n notion-3-2013030200
tar -xvf %SOURCE1

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -e 's|^\(PREFIX=\).*$|\1/usr|' \
    -e 's|^\(ETCDIR=\).*$|\1/etc/X11/notion|' \
    -e 's|^\(LUA_DIR=\).*$|\1/usr|' \
    -e 's|^\(X11_PREFIX=\).*$|\1/usr|' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

cd $RPM_BUILD_DIR/%{buildsubdir}/notion-doc
make TOPDIR=.. all

#%check
#make test

%install
#rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_defaultdocdir}/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

# Install and verify desktop file
install -Dm0644 %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/xsessions/%{name}.desktop

# contrib subpackage
for i in keybindings scripts statusbar statusd styles; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/contrib/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i/* $RPM_BUILD_ROOT%{_datadir}/notion/contrib/$i/
done

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}
for i in LICENSE README; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}/
done

# Doc subpackage
cd $RPM_BUILD_DIR/%{buildsubdir}/notion-doc
make install DOCDIR=$RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-doc-%{version} TOPDIR=..
for i in LICENSE README; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-doc-%{version}/
done

# Dev subpackage
for i in de ioncore libextl libmainloop libtu mod_dock mod_menu mod_query mod_sm mod_sp mod_statusbar mod_tiling mod_xinerama mod_xkbevents mod_xrandr utils/ion-statusd; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/notion/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i/*.h $RPM_BUILD_ROOT%{_includedir}/notion/$i/
done

mkdir -p $RPM_BUILD_ROOT%{_includedir}/notion/build
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/*.mk $RPM_BUILD_ROOT%{_includedir}/notion/build/ 

install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/system-autodetect.mk $RPM_BUILD_ROOT%{_includedir}/notion/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/version.h $RPM_BUILD_ROOT%{_includedir}/notion/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/config.h $RPM_BUILD_ROOT%{_datadir}/notion/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_includedir}/notion/libextl/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/install-sh $RPM_BUILD_ROOT%{_includedir}/notion/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/build
mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/libextl

#install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/libs.mk $RPM_BUILD_ROOT%{_datadir}/notion/build/
#install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/config.h $RPM_BUILD_ROOT%{_datadir}/notion/
#install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/install-sh $RPM_BUILD_ROOT%{_datadir}/notion/
#install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_datadir}/notion/libextl/
#install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/system-autodetect.mk $RPM_BUILD_ROOT%{_datadir}/notion/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/build
for i in rules.mk system-inc.mk; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/$i $RPM_BUILD_ROOT%{_datadir}/notion/build/
done

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
for i in LICENSE README; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
done

%files
%config(noreplace) %{_sysconfdir}/X11/%{name}/*
%{_bindir}/*
%{_libdir}/%{name}/bin/*
%{_libdir}/%{name}/lc/*
%{_libdir}/%{name}/mod/*
%{_libdir}/%{name}/libextl/*
%lang(cs) %{_mandir}/cs/*
%lang(fi) %{_mandir}/fi/*
%{_mandir}/man1/*
%lang(cs) %{_datadir}/locale/cs/*
%lang(de) %{_datadir}/locale/de/*
%lang(fi) %{_datadir}/locale/fi/*
%lang(fr) %{_datadir}/locale/fr/*
%{_datadir}/%{name}/ion-completeman
%{_datadir}/%{name}/ion-runinxterm
%{_datadir}/%{name}/notion-lock
%{_datadir}/%{name}/welcome.txt
%lang(fi) %{_datadir}/%{name}/welcome.fi.txt
%lang(cs) %{_datadir}/%{name}/welcome.cs.txt
%{_defaultdocdir}/%{name}-%{version}/README
%{_defaultdocdir}/%{name}-%{version}/LICENSE
%{_defaultdocdir}/%{name}-%{version}/ChangeLog
%{_defaultdocdir}/%{name}-%{version}/RELNOTES
%attr(0644, root, root) %{_datadir}/xsessions/%{name}.desktop

%files contrib
%{_datadir}/%{name}/contrib
%{_defaultdocdir}/%{name}-contrib-%{version}/*

%files doc
%{_defaultdocdir}/%{name}-doc-%{version}/*

%files devel
%{_defaultdocdir}/%{name}-devel-%{version}/*
%{_includedir}/%{name}/*
#%{_libdir}/%{name}/build/libs.mk
#%{_libdir}/%{name}/config.h
#%{_libdir}/%{name}/install-sh
#%{_libdir}/%{name}/libextl/libextl-mkexports
#%{_libdir}/%{name}/system-autodetect.mk
#%{_datadir}/%{name}/build/rules.mk
#%{_datadir}/%{name}/build/system-inc.mk

%changelog
* Fri Nov  1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.

