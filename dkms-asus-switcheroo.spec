%global module_name asus-switcheroo
%global _srcdir %{_prefix}/src
%global git_author awilliam
%global git_date 20120105
%global git_commit bf9951b

Name:           dkms-%{module_name}
Version:        0.1
Release:        1.%{git_date}git%{git_commit}%{?dist}.R
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

#build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_srcdir}
mkdir -p $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
cp -r Makefile *.c $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/
install -D -m 0644 dkms.conf $RPM_BUILD_ROOT%{_srcdir}/%{module_name}-%{version}/dkms.conf
install -D -m 0755 %{module_name}-pm $RPM_BUILD_ROOT%{_sysconfdir}/pm/sleep.d/75-%{module_name}-pm
install -D -m 0644 %{module_name}.conf-modprobe.d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{module_name}.conf
install -D -m 0644 %{module_name}.conf-dracut $RPM_BUILD_ROOT%{_sysconfdir}/dracut.conf.d/%{module_name}.conf


%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc COPYING README
%defattr(-,root,root,-)
%{_srcdir}/%{module_name}-%{version}
%{_sysconfdir}/pm/sleep.d/75-%{module_name}-pm
%{_sysconfdir}/modprobe.d/%{module_name}.conf
%{_sysconfdir}/dracut.conf.d/%{module_name}.conf

%post
/usr/sbin/dkms add -m %{module_name} -v %{version}

%preun
/usr/sbin/dkms remove -m %{module_name} -v %{version} --all

%changelog
* Thu Jan 05 2012 Alexey Torkhov <atorkhov@gmail.com> - 3.1.0-1.R
- Initial package

