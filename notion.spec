%global majorver 3
%global datever  2013030200

Name:           notion
Version:        %{majorver}.%{datever}
Release:        3%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/%{name}-%{majorver}-%{datever}-src.tar.bz2
Source1:        https://fedorahosted.org/released/%{name}/%{name}-doc-%{majorver}-%{datever}.tar.bz2
Source2:        https://fedorahosted.org/released/%{name}/%{name}.desktop

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
# Patch submitted to upstream via e-mail on 11/26/2013
Patch5:         %{name}-%{majorver}.%{datever}.p05-fix_orphaned_statusd.patch

BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  desktop-file-utils
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
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

%package -n libextl-devel
Summary:        Small library for very easily extending programs with Lua
License:        LGPLv2+

%description -n libextl-devel
Libextl supports exporting functions that operate on basic data types (int,
bool, double, [const] char*) and references to Lua tables and functions
(ExtlTab, ExtlFn) simply by prefixing the function definition with the
keywords EXTL_EXPORT, EXTL_EXPORT_AS or EXTL_EXPORT_MEMBER. More complex
data must, however, either be proxied libtu objects (or objects of some
other object system with the appropriate macros redefined), or Lua tables.
The binding glue is, however, generated as painlessly as for functions that
operate on basic data types with all pointers to a type with a name that
begins with an uppercase letter considered as such objects. Libextl also
provides functions to manipulate Lua tables through references to these, and
ways to call and load Lua code.

%package -n libmainloop-devel
Summary:        Support library for the Notion window manager

%description -n libmainloop-devel
This package contains a support library necessary for extending and 
customizing Notion.

%package -n libtu-devel
Summary:        Support library for the Notion window manager

%description -n libtu-devel
This package contains a support library necessary for extending and 
customizing Notion.

%package devel
Summary:        Development files for the Notion window manager
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libextl-devel = %{version}-%{release}
Requires:       libmainloop-devel = %{version}-%{release}
Requires:       libtu-devel = %{version}-%{release}

%description devel
This package contains the development files necessary for extending and 
customizing Notion.

%prep
%setup -q -n %{name}-%{majorver}-%{datever}

# Decompress doc pkg
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

# Installing docs to a temporary directory so that we can pick them up with 
# doc macro later.
mkdir _docs_staging

%build
make %{?_smp_mflags} DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging

# Note: -doc won't build w/ ?_smp_mflags.
cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc
make DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging TOPDIR=.. all

%install
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_pkgdocdir}

%find_lang %{name} --with-man

# Install and verify desktop file
desktop-file-install --dir=%{buildroot}/%{_datadir}/xsessions %{SOURCE2}
desktop-file-validate %{buildroot}/%{_datadir}/xsessions/%{name}.desktop

# libextl subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libextl
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libextl/*.h $RPM_BUILD_ROOT%{_includedir}/libextl/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_includedir}/libextl/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl.a $RPM_BUILD_ROOT%{_libdir}/

# libmainloop subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libmainloop
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/*.h $RPM_BUILD_ROOT%{_includedir}/libmainloop/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/rx.mk $RPM_BUILD_ROOT%{_includedir}/libmainloop/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/libmainloop.a $RPM_BUILD_ROOT%{_libdir}/

# libtu subpackage
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libtu
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libtu/*.h $RPM_BUILD_ROOT%{_includedir}/libtu/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libtu/libtu.a $RPM_BUILD_ROOT%{_libdir}/

# notion-devel subpackage
for i in de ioncore mod_dock mod_menu mod_query mod_sm mod_sp mod_statusbar mod_tiling mod_xinerama mod_xkbevents mod_xrandr utils/ion-statusd; do
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
  ln -s "../$i" $RPM_BUILD_ROOT%{_includedir}/%{name}/$i
done

# contrib subpackage
for i in keybindings scripts statusbar statusd styles; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i/* $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
done

# Doc subpackage
cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc
make install DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging TOPDIR=..

%files -f %{name}.lang
%doc README LICENSE ChangeLog RELNOTES
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%lang(fi) %{_datadir}/%{name}/welcome.fi.txt
%lang(cs) %{_datadir}/%{name}/welcome.cs.txt
%{_datadir}/%{name}
%{_datadir}/xsessions/%{name}.desktop

%files contrib
%doc README LICENSE
%{_datadir}/%{name}/contrib

%files doc
%doc _docs_staging/*

%files -n libextl-devel
%doc libextl/README libextl/LICENSE
%{_includedir}/libextl
%{_libdir}/libextl.a

%files -n libmainloop-devel
%doc README LICENSE
%{_includedir}/libmainloop
%{_libdir}/libmainloop.a

%files -n libtu-devel
%doc README LICENSE
%{_includedir}/libtu
%{_libdir}/libtu.a

%files devel
%doc README LICENSE
%{_includedir}/%{name}

%changelog
* Sun Nov  24 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-3
- Added patch for ion-statusd bug.
- Removed URLs for patches.
- Updated URLs for source1 and source2.
- Switched to all references to package version to use variables.
- Switched to find_lang from lang.
- Switched to desktop-file-install and added desktop-file-validate.
- Changed files section such that package owns whole directory instead of 
  just individual files.
- Moved libextl, libmainloop, and libtu into their own packages to conform
  to Fedora guidelines.
- Switched all documentation references in files section to using doc macro.
- Removed BuildRequires: lua
- Added optflags to build.
- Updated notion.desktop.

* Wed Nov  13 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-2
- Modified devel to place all files in /usr/include
- Added sed statment to alter X11_LIBS= in system-autodetect.mk to use pkgconfig.
- Patched fonts in styles scripts to use valid 100dpi fonts.

* Fri Nov  1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.
