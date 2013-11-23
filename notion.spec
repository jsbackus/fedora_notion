%global majorver 3
%global datever  2013030200

#TODO: Try removing this and running Koji
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           notion
Version:        %{majorver}.%{datever}
Release:        3%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/%{name}-%{majorver}-%{datever}-src.tar.bz2
#TODO: Consider putting up a fork of this repo on GitHub and specifying a "release link"
#Source1:        git://notion.git.sourceforge.net/gitroot/notion/notion-doc
Source1:        https://www.dropbox.com/sh/n1icl72l63dy9tr/jFYmjjqH-f/%{name}-doc-%{majorver}-%{datever}.tar.bz2
Source2:        https://raw.github.com/jsbackus/fedora_notion/master/%{name}.desktop

# Patch submitted to upstream via e-mail on 11/3/2013
Patch0:         %{name}-%{majorver}.%{datever}.p00-man-utf8.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch1:         %{name}-%{majorver}.%{datever}.p01-fsf_addr.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch2:         %{name}-doc-%{majorver}.%{datever}.p02-css_newline.patch
# Patch submitted to upstream via e-mail on 11/3/2013
Patch3:         %{name}-%{majorver}.%{datever}.p03-ChangeLog_update.patch
# Patch submitted to upstream via e-mail on 11/16/2013
Patch4:         %{name}-%{majorver}.%{datever}.p04-fonts.patch
Patch5:         %{name}-%{majorver}.%{datever}.p05-fix_orphaned_statusd.patch

BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
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

%package libextl
Summary:        TODO
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description libextl
TODO
This package contains the development files necessary for extending and 
customizing Notion.

%package libmainloop
Summary:        TODO
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description libmainloop
TODO
This package contains the development files necessary for extending and 
customizing Notion.

%package libtu
Summary:        TODO
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description libtu
TODO
This package contains the development files necessary for extending and 
customizing Notion.

%package devel
Summary:        Development files for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libextl%{?_isa} = %{version}-%{release}
Requires:       libmainloop%{?_isa} = %{version}-%{release}
Requires:       libtu%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files necessary for extending and 
customizing Notion.

%prep
#tar -xvf %SOURCE1
#%patch2 -p1

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
    -e 's|\(CFLAGS *+*= *\)\(-Os\)|\1 $(RPM_OPT_FLAGS) \2|' \
    -i system-autodetect.mk

%build
make %{?_smp_mflags}

cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc
make TOPDIR=.. all 

# Note: -doc won't build w/ ?_smp_mflags.
#cd $RPM_BUILD_DIR/%{name}-doc
#make TOPDIR=$RPM_BUILD_DIR/%{buildsubdir} all 

%install

make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_pkgdocdir}
#mv $RPM_BUILD_ROOT%{_defaultdocdir}/%{name} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%find_lang %{name}

# Install and verify desktop file
desktop-file-install --dir=%{buildroot}/%{_datadir}/xsessions %{SOURCE2}
desktop-file-validate %{buildroot}/%{_datadir}/xsessions/%{name}.desktop

# libextl subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libextl
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libextl/*.h $RPM_BUILD_ROOT%{_includedir}/libextl/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_includedir}/libextl/

# libmainloop subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libmainloop
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/*.h $RPM_BUILD_ROOT%{_includedir}/libmainloop/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/rx.mk $RPM_BUILD_ROOT%{_includedir}/%{name}/libmainloop/

# libtu subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libtu
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libtu/*.h $RPM_BUILD_ROOT%{_includedir}/libtu/

# Dev subpackage
for i in de ioncore libextl libmainloop libtu mod_dock mod_menu mod_query mod_sm mod_sp mod_statusbar mod_tiling mod_xinerama mod_xkbevents mod_xrandr utils/ion-statusd; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/$i/
done

mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/build
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/*.mk $RPM_BUILD_ROOT%{_includedir}/%{name}/build/ 

install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/system-autodetect.mk $RPM_BUILD_ROOT%{_includedir}/%{name}/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/version.h $RPM_BUILD_ROOT%{_includedir}/%{name}/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/config.h $RPM_BUILD_ROOT%{_includedir}/%{name}/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/install-sh $RPM_BUILD_ROOT%{_includedir}/%{name}/

mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/build
for i in rules.mk system-inc.mk; do
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/build/$i $RPM_BUILD_ROOT%{_includedir}/%{name}/build/
done

# Most parts of Notion actually expect these "libraries" to be in the 
# notion TOPDIR, so we'll create links to keep them happy.
for i in libextl libmainloop libtu; do
  ln -s $RPM_BUILD_ROOT%{_includedir}/$i $RPM_BUILD_ROOT%{_includedir}/%{name}/$i
done

#mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
#for i in LICENSE README; do
#  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-devel-%{version}/
#done

# contrib subpackage
for i in keybindings scripts statusbar statusd styles; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i/* $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
done

#mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}
#for i in LICENSE README; do
#  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-contrib-%{version}/
#done

#mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}
#for i in LICENSE README; do
#  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i $RPM_BUILD_ROOT%{_pkgdocdir}/$i
#done

# Doc subpackage
%pre doc
cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc
#make install DOCDIR=$RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-doc-%{version} TOPDIR=..
#for i in LICENSE README; do
#  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-doc-%{version}/
#done
make install DOCDIR=%{_pkgdocdir} TOPDIR=..
#for i in LICENSE README; do
#  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/$i $RPM_BUILD_ROOT%{_pkgdocdir}/
#done

%files -f %{name}.lang
%doc README LICENSE ChangeLog RELNOTES
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_libdir}/%{name}
%lang(cs) %{_mandir}/cs/*
%lang(fi) %{_mandir}/fi/*
%{_mandir}/man1/*
#%lang(cs) %{_datadir}/locale/cs/*
#%lang(de) %{_datadir}/locale/de/*
#%lang(fi) %{_datadir}/locale/fi/*
#%lang(fr) %{_datadir}/locale/fr/*
%{_datadir}/%{name}
#%lang(fi) %{_datadir}/%{name}/welcome.fi.txt
#%lang(cs) %{_datadir}/%{name}/welcome.cs.txt
#%{_defaultdocdir}/%{name}-%{version}/README
#%{_defaultdocdir}/%{name}-%{version}/LICENSE
#%{_defaultdocdir}/%{name}-%{version}/ChangeLog
#%{_defaultdocdir}/%{name}-%{version}/RELNOTES

%{_datadir}/xsessions/%{name}.desktop

%files contrib
%doc README LICENSE
%{_datadir}/%{name}/contrib

%files doc
%doc %{_pkgdocdir}
#%{_defaultdocdir}/%{name}-doc-%{version}/*

%files libextl
%doc README LICENSE
%{_includedir}/libextl

%files libmainloop
%doc README LICENSE
%{_includedir}/libmainloop

%files libtu
%doc README LICENSE
%{_includedir}/libtu

%files devel
%doc README LICENSE
%{_includedir}/%{name}

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
