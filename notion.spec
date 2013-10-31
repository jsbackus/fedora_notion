Name:           notion
Version:        3.2013030200
Release:        1%{?dist}
Summary:        Tabbed tiling window manager. Fork of Ion3.

License:        
URL:            http://notion.sourceforge.net
Source0:        

BuildRequires:  
Requires:       

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
