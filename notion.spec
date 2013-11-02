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
Source1:        notion-doc-3-2013030200.tar.bz2
Source2:        notion.desktop

Patch0:         p00-man_utf8.patch
Patch1:         p01-fsf_addr.patch

BuildRequires:  pkgconfig
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
#BuildRequires:  glib2-devel
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
License:        GPLv3
%description contrib
This package contains a number of scripts from third parties for Notion, 
such as:
* Alternative keybindings
* Miscellaneous support scripts
* Status monitors for the statusbar
* Additional styles

%package doc
Summary:        Documentation for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        GFDL
%description doc
This package contains the documentation for extending and customizing 
Notion.

%prep
%setup -q -n notion-3-2013030200
tar -xvf %SOURCE1

%patch0 -p1
%patch1 -p1

sed -e 's|^\(PREFIX=\).*$|\1/usr|' \
    -e 's|^\(ETCDIR=\).*$|\1/etc/X11/notion|' \
    -e 's|^\(LUA_DIR=\).*$|\1/usr|' \
    -e 's|^\(X11_PREFIX=\).*$|\1/usr|' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

#cd $RPM_BUILD_DIR/notion-doc
cd notion-doc
make %{?_smp_mflags} TOPDIR=..

%check
#make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cp -r $RPM_BUILD_ROOT%{_sysconfdir}/X11/notion $RPM_BUILD_ROOT%{_datadir}/notion/etc
mv $RPM_BUILD_ROOT%{_defaultdocdir}/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/contrib
for i in keybindings scripts statusbar statusd styles; do
  cp -r $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_datadir}/notion/contrib/
done

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}
for i in LICENSE README; do
  cp -r $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}/
done

cd $RPM_BUILD_DIR/%{buildsubdir}/notion-doc
make install DOCDIR=$RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version} TOPDIR=..

mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions
cp %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/xsessions/

%files
%config(noreplace) %{_sysconfdir}/X11/notion*
%{_bindir}/*
%{_libdir}/*
%lang(cs) %{_mandir}/cs/*
%lang(fi) %{_mandir}/fi/*
%{_mandir}/man1/*
%lang(cs) %{_datadir}/locale/cs/*
%lang(de) %{_datadir}/locale/de/*
%lang(fi) %{_datadir}/locale/fi/*
%lang(fr) %{_datadir}/locale/fr/*
%{_datadir}/notion/etc
%{_datadir}/notion/ion-completeman
%{_datadir}/notion/ion-runinxterm
%{_datadir}/notion/notion-lock
%{_datadir}/notion/welcome.txt
%lang(fi) %{_datadir}/notion/welcome.fi.txt
%lang(cs) %{_datadir}/notion/welcome.cs.txt
%{_defaultdocdir}/%{name}-%{version}/README
%{_defaultdocdir}/%{name}-%{version}/LICENSE
%{_defaultdocdir}/%{name}-%{version}/ChangeLog
%{_defaultdocdir}/%{name}-%{version}/RELNOTES
%{_datadir}/xsessions/notion.desktop

%files contrib
%{_datadir}/notion/contrib
%{_defaultdocdir}/%{name}-contrib-%{version}/*

%files doc
%{_defaultdocdir}/%{name}-%{version}/*

%changelog
* Fri Nov  1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.

