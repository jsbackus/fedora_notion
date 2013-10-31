Name:           notion
Version:        
Release:        1%{?dist}
Summary:        

License:        
URL:            
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
