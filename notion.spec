%global majorver 3
%global datever  2014010900

Name:           notion
Version:        %{majorver}.%{datever}
Release:        3%{?dist}
Summary:        Tabbed, tiling window manager forked from Ion3

License:        LGPLv2 with exceptions
URL:            http://notion.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/notion/%{name}-%{majorver}-%{datever}-src.tar.bz2
# Source https://github.com/jsbackus/notion-doc/archive/3-2014010505.tar.gz
Source1:        https://fedorahosted.org/released/%{name}/%{name}-doc-%{majorver}-%{datever}.tar.gz
Source2:        https://fedorahosted.org/released/%{name}/%{name}.desktop

#Patch0:         %{name}-%{majorver}.%{datever}.p00-ChangeLog_update.patch
Patch1:         %{name}-%{majorver}.%{datever}.p01-man_utf8.patch
Patch2:         %{name}-%{majorver}.%{datever}.p02-x11_prefix.patch

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

%package doc
Summary:        Documentation for the Notion window manager
License:        GFDL
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

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

# Decompress doc pkg
tar -xvf %SOURCE1

#%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -e 's|^\(PREFIX\s*?=\s*\).*$|\1%{_prefix}|' \
    -e 's|^\(ETCDIR\s*?=\s*\).*$|\1%{_sysconfdir}/%{name}|' \
    -e 's|^\(LIBDIR=\).*$|\1%{_libdir}|' \
    -e 's|\(CFLAGS *+*= *\)\(-Os\)|\1 $(RPM_OPT_FLAGS) \2|' \
    -i system-autodetect.mk



%build
# Installing docs to a temporary directory so that we can pick them up with 
# doc macro later.
mkdir $RPM_BUILD_DIR/%{buildsubdir}/_docs_staging

make %{?_smp_mflags} DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging

# Note: -doc won't build w/ ?_smp_mflags. Shouldn't be a problem as there are
# no executables.
cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc-%{majorver}-%{datever}
make DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging TOPDIR=.. all

%check
make test

%install
make install DESTDIR=$RPM_BUILD_ROOT DOCDIR=%{_pkgdocdir}

%find_lang %{name} --with-man

# Install and verify desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT/%{_datadir}/xsessions %{SOURCE2}
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/xsessions/%{name}.desktop

# notion-devel subpackage
# libextl header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/libextl
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libextl/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/libextl/
install -Dm0755 $RPM_BUILD_DIR/%{buildsubdir}/libextl/libextl-mkexports $RPM_BUILD_ROOT%{_includedir}/%{name}/libextl/

# libmainloop header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/libmainloop
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/libmainloop/
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libmainloop/rx.mk $RPM_BUILD_ROOT%{_includedir}/%{name}/libmainloop/

# libtu header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/libtu
install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/libtu/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/libtu/

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

# contrib subpackage
for i in keybindings scripts scripts/legacy statusbar statusbar/legacy statusd statusd/legacy styles; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
  install -Dm0644 $RPM_BUILD_DIR/%{buildsubdir}/contrib/$i/*.lua $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/$i/
done

# Doc subpackage
cd $RPM_BUILD_DIR/%{buildsubdir}/%{name}-doc-%{majorver}-%{datever}
make install DOCDIR=$RPM_BUILD_DIR/%{buildsubdir}/_docs_staging TOPDIR=..

%files -f %{name}.lang
%doc README ChangeLog LICENSE RELNOTES
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

%files doc
%doc _docs_staging/*

%files devel
%doc README LICENSE
%{_includedir}/%{name}
#%{_includedir}/%{name}/libextl
#%{_includedir}/%{name}/libmainloop
#%{_includedir}/%{name}/libtu

%changelog
* Sun Jan 19 2014 Jeff Backus <jeff.backus@gmail.com> - 3.2014010900-3
- Changed method of correcting manpage text encoding to something upstream can
  apply to source.

* Sat Jan 18 2014 Jeff Backus <jeff.backus@gmail.com> - 3.2014010900-2
- Fixed a typo in required font package name.

* Sun Jan 12 2014 Jeff Backus <jeff.backus@gmail.com> - 3.2014010900-1
- New upstream release.
- Fixed issue where contrib files where getting picked up by main package.

* Sun Nov 24 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-3
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

* Wed Nov 13 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-2
- Modified devel to place all files in /usr/include
- Added sed statment to alter X11_LIBS= in system-autodetect.mk to use pkgconfig.
- Patched fonts in styles scripts to use valid 100dpi fonts.

* Fri Nov 1 2013 Jeff Backus <jeff.backus@gmail.com> - 3.2013030200-1
- Initial addition to Fedora.
