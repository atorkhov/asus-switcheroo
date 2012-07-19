%global module_name asus-switcheroo
%global git_author awilliam
%global git_date 20120119
%global git_commit 6c7da8e
%global quiet -q

Name:           dkms-%{module_name}
Version:        0.1
Release:        2.%{git_date}git%{git_commit}%{?dist}.R
Summary:        Kernel module for switcheroo support on ASUS laptops

Group:          System Environment/Kernel
License:        GPLv2
URL:            https://github.com/awilliam/asus-switcheroo.git
Source0:        %{git_author}-%{module_name}-%{git_commit}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:       dkms kernel-devel gcc
BuildArch:      noarch

%description
Kernel module source for switcheroo support on ASUS laptops.

%prep
%setup -q -n %{git_author}-%{module_name}-%{git_commit}
echo 'AUTOINSTALL="yes"' >> dkms.conf

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_usrsrc}
mkdir -p $RPM_BUILD_ROOT%{_usrsrc}/%{module_name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
cp -r Makefile *.c $RPM_BUILD_ROOT%{_usrsrc}/%{module_name}-%{version}/
install -D -m 0644 dkms.conf $RPM_BUILD_ROOT%{_usrsrc}/%{module_name}-%{version}/dkms.conf
install -D -m 0755 %{module_name}-pm $RPM_BUILD_ROOT%{_sysconfdir}/pm/sleep.d/75-%{module_name}-pm
install -D -m 0644 %{module_name}.conf-modprobe.d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{module_name}.conf
install -D -m 0644 %{module_name}.conf-dracut $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/%{module_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc COPYING README
%defattr(-,root,root,-)
%{_usrsrc}/%{module_name}-%{version}
%{_sysconfdir}/pm/sleep.d/75-%{module_name}-pm
%{_sysconfdir}/modprobe.d/%{module_name}.conf
%{_sysconfdir}/dracut.conf.d/%{module_name}.conf

%post
if [ $1 == 1 ] ; then
    # Add to DKMS registry on install
    dkms add -m %{module_name} -v %{version} %{?quiet} || :
    # Rebuild and make available for the currenty running kernel
    dkms build -m %{module_name} -v %{version} %{?quiet} || :
    dkms install -m %{module_name} -v %{version} %{?quiet} --force || :
fi

%preun
if [ $1 == 0 ] ; then
    # Remove all versions from DKMS registry on uninstall
    dkms remove -m %{module_name} -v %{version} %{?quiet} --all || :
fi

%changelog
* Thu Jan 10 2012 Alexey Torkhov <atorkhov@gmail.com> - 0.1-2.20120105gitbf9951b
- Add autoinstall directive to dkms config
- Fixing install and uninstall scriptlets

* Thu Jan 05 2012 Alexey Torkhov <atorkhov@gmail.com> - 0.1-1.20120105gitbf9951b
- Initial package

