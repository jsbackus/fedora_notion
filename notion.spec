Name:           notion
Version:        3.2013030200
Release:        1%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

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

%prep
%setup -q -n notion-3-2013030200

sed -e 's/^\(PREFIX=\).*$/\1\/usr/' \
    -e 's/^\(ETCDIR=\).*$/\1\/etc\/notion/' \
    -e 's/^\(LUA_DIR=\).*$/\1\/usr/' \
    -e 's/^\(X11_PREFIX=\).*$/\1\/usr/' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}
find $RPM_BUILD_DIR/%{buildsubdir}/man -iname '*.1' -exec iconv -f LATIN1 -t utf8 -o '{}' '{}' \;

%check
#make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cp -r $RPM_BUILD_ROOT%{_sysconfdir}/notion $RPM_BUILD_ROOT%{_datadir}/notion/etc
mv $RPM_BUILD_ROOT%{_defaultdocdir}/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/notion/contrib
for i in keybindings scripts statusd styles; do
  cp -r $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_datadir}/notion/contrib/
done

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}
for i in LICENSE README; do
  cp -r $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}/
done

%files
%config(noreplace) %{_sysconfdir}/*
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
%{_defaultdocdir}/%{name}-%{version}/*

%files contrib
%{_datadir}/notion/contrib
%{_defaultdocdir}/%{name}-contrib-%{version}/*

%changelog
* Fri Nov  1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.

