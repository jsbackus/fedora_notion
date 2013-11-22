%global majorver 3
%global datever  2013030200

Name:           notion
Version:        %{majorver}.%{datever}
Release:        3%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/notion-%{majorver}-%{datever}-src.tar.bz2
#Source1:        git://notion.git.sourceforge.net/gitroot/notion/notion-doc
Source1:        https://www.dropbox.com/sh/n1icl72l63dy9tr/jFYmjjqH-f/notion-doc-%{majorver}-%{datever}.tar.bz2
# notion.desktop can also be found in git repo https://github.com/jsbackus/fedora_notion.git
Source2:        https://www.dropbox.com/sh/n1icl72l63dy9tr/Qurc5REVFy/notion.desktop

# Patch submitted to upstream via e-mail on 11/3/2013
Patch0:         notion-%{majorver}.%{datever}.p00-man-utf8.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch1:         notion-%{majorver}.%{datever}.p01-fsf_addr.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch2:         notion-doc-%{majorver}.%{datever}.p02-css_newline.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch3:         notion-%{majorver}.%{datever}.p03-ChangeLog_update.patch
# Patch submitted to upstream via e-mail on 11/16/2013
Patch4:         notion-%{majorver}.%{datever}.p04-fonts.patch
Patch5:         notion-%{majorver}.%{datever}.p05-fix_orphaned_statusd.patch

BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
#BuildRequires:  lua
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
License:        GPLv3 and Public Domain and GPLv2+ and Artistic clarified and LGPLv2+ and GPL+ and GPLv2 and BSD
BuildArch:      noarch

Requires:       terminus-fonts

%description contrib
This package contains a number of scripts from third parties for Notion, 
such as:
* Alternative keybindings
* Miscellaneous support scripts
* Status monitors for the status bar
* Additional styles

Scripts are installed into %{_datadir}/%{name}/contrib. To use,
copy/link the script(s) you want into ~/.notion and restart Notion.

%package doc
Summary:        Documentation for the Notion window manager
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
%setup -q -n %{name}-%{majorver}-%{datever}
tar -xvf %SOURCE1

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

sed -e 's|^\(PREFIX=\).*$|\1%{_prefix}|' \
    -e 's|^\(ETCDIR=\).*$|\1%{_sysconfdir}/%{name}|' \
    -e 's|^\(LUA_DIR=\).*$|\1%{_prefix}|' \
    -e 's|^\(X11_PREFIX=\).*$|\1%{_prefix}|' \
    -e 's|^\(X11_LIBS=\).*$|\1`pkg-config --libs x11 xext`|' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

cd $RPM_BUILD_DIR/%{buildsubdir}/notion-doc
make TOPDIR=.. all

%install
make install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_defaultdocdir}/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%find_lang %{name}

# Install and verify desktop file
desktop-file-install --dir=%{buildroot}/%{_datadir}/xsessions/%{name}.desktop %{SOURCE2}
desktop-file-validate %{buildroot}/%{_datadir}/xsessions/%{name}.desktop

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
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/config.h $RPM_BUILD_ROOT%{_includedir}/notion/

mkdir -p $RPM_BUILD_ROOT%{_includedir}/notion/libextl
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_includedir}/notion/libextl/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/install-sh $RPM_BUILD_ROOT%{_includedir}/notion/

mkdir -p $RPM_BUILD_ROOT%{_includedir}/notion/libmainloop
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/rx.mk $RPM_BUILD_ROOT%{_includedir}/notion/libmainloop/

mkdir -p $RPM_BUILD_ROOT%{_includedir}/notion/build
for i in rules.mk system-inc.mk; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/$i $RPM_BUILD_ROOT%{_includedir}/notion/build/
done

mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
for i in LICENSE README; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
done

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_libdir}/%{name}
#%lang(cs) %{_mandir}/cs/*
#%lang(fi) %{_mandir}/fi/*
%{_mandir}/man1/*
#%lang(cs) %{_datadir}/locale/cs/*
#%lang(de) %{_datadir}/locale/de/*
#%lang(fi) %{_datadir}/locale/fi/*
#%lang(fr) %{_datadir}/locale/fr/*
%{_datadir}/%{name}
#%lang(fi) %{_datadir}/%{name}/welcome.fi.txt
#%lang(cs) %{_datadir}/%{name}/welcome.cs.txt
%{_defaultdocdir}/%{name}-%{version}/README
%{_defaultdocdir}/%{name}-%{version}/LICENSE
%{_defaultdocdir}/%{name}-%{version}/ChangeLog
%{_defaultdocdir}/%{name}-%{version}/RELNOTES
#%attr(0644, root, root) %{_datadir}/xsessions/%{name}.desktop

%files contrib
%{_datadir}/%{name}/contrib
%{_defaultdocdir}/%{name}-contrib-%{version}/*

%files doc
%{_defaultdocdir}/%{name}-doc-%{version}/*

%files devel
%{_defaultdocdir}/%{name}-devel-%{version}/*
%{_includedir}/%{name}/*

%changelog
* Sun Nov  24 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-3
- Added patch for ion-statusd bug.
- Removed URLs for patches, as per review.
- Added missing libmainloop/rx.mk to -devel.
- Switched to all references to package version to use variables.
- Switched to find_lang from lang
- Switched to desktop-file-install and added desktop-file-validate.
- Changed files section such that package owns whole directory instead of 
  just individual files.

* Wed Nov  13 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-2
- Modified devel to place all files in /usr/include
- Added sed statment to alter X11_LIBS= in system-autodetect.mk to use pkgconfig.
- Patched fonts in styles scripts to use valid 100dpi fonts.

* Fri Nov  1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.
