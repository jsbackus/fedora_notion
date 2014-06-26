%global majorver 3
%global datever  2014052800

Name:           notion
Version:        %{majorver}.%{datever}
Release:        1%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

# Notion is distributed under a modified LGPLv2.1. As of 1/20/2014 this 
# license was considered to be to restrictive to be included in the
# official Fedora repositories.
License:        Redistributable, modified LGPLv2.1
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/%{name}-%{majorver}-%{datever}-src.tar.bz2
Source1:        https://fedorahosted.org/released/%{name}/%{name}.desktop

BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  lua-devel
BuildRequires:  libXext-devel
BuildRequires:  libSM-devel

Requires:       xterm
Requires:       xorg-x11-utils
Requires:       xorg-x11-fonts-ISO8859-1-75dpi

%description
Notion is a tabbed, tiling window manager for the X windows system.

Features include:
* Workspaces: each work space has its own tiling.
* Multiheaded
* RandR support
* Extensible via Lua scripts.

%package contrib
Summary:        3rd party scripts for the Notion window manager
License:        GPLv3 and Public Domain and GPLv2+ and Artistic clarified and LGPLv2+ and GPL+ and GPLv2 and BSD
BuildArch:      noarch
Requires:       terminus-fonts
Requires:       %{name} = %{version}-%{release}

%description contrib
This package contains a number of scripts from third parties for Notion, 
such as:
* Alternative keybindings
* Miscellaneous support scripts
* Status monitors for the status bar
* Additional styles

Scripts are installed into %{_datadir}/%{name}/contrib. To use,
copy/link the script(s) you want into ~/.notion and restart Notion.

%prep
%setup -q -n %{name}-%{majorver}-%{datever}

sed -e 's|^\(PREFIX\s*?=\s*\).*$|\1%{_prefix}|' \
    -e 's|^\(ETCDIR\s*?=\s*\).*$|\1%{_sysconfdir}/%{name}|' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -e 's|\(CFLAGS *+*= *\)\(-Os\)|\1 $(RPM_OPT_FLAGS) \2|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_pkgdocdir}

%find_lang %{name} --with-man

# Install and verify desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT/%{_datadir}/xsessions %{SOURCE1}

# contrib subpackage
for i in keybindings scripts scripts/legacy statusbar statusbar/legacy statusd statusd/legacy styles; do
  install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i
  install -pm 0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i/*.lua $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
done

%files -f %{name}.lang
%doc README CHANGELOG LICENSE
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%dir %{_datadir}/%{name}
%lang(fi) %{_datadir}/%{name}/welcome.fi.txt
%lang(cs) %{_datadir}/%{name}/welcome.cs.txt
%{_datadir}/%{name}/ion-completeman
%{_datadir}/%{name}/ion-runinxterm
%{_datadir}/%{name}/notion-lock
%{_datadir}/%{name}/welcome.txt
%{_datadir}/xsessions/%{name}.desktop

%files contrib
%doc README LICENSE
%{_datadir}/%{name}/contrib

%changelog
* Wed Jun 25 2014 Jeff Backus <jeff.backus@gmail.com> - 3.2014052800-1
- Initial RPMFusion Release
