#%%if 0%%{?rhel} || 0%%{?suse_version} == 1110 || 0%%{?suse_version} == 1315
%bcond_without python2
#%%else
#%%bcond_with python2
#%%endif

%if 0%{?with_python2}
%global PYVER 2
%define noarch 0
%else
%global PYVER 3
%define noarch 1
%endif

%global pyXsuf %{PYVER}
%global pyXcmd python%{PYVER}

%define pyX_sitelib %(%{pyXcmd} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:           bareos-fuse
Version:        0.2
Release:        1%{?dist}
Summary:        Backup Archiving REcovery Open Sourced - FUSE
Group:          Productivity/Archiving/Backup
License:        AGPL-3.0
URL:            https://github.com/bareos/bareos-fuse/
Vendor:         The Bareos Team
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-root
%global debug_package %{nil}
%if %{with python2}
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-dateutil
%endif
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-dateutil
%endif
%if %noarch
BuildArch:      noarch
%endif
%{?python_provide:%python_provide python-%{srcname}}
BuildRequires:  rsync
# for directory /etc/bareos/bareos-dir.d/
BuildRequires:  bareos-common
# required for restoring.
# Recommends would be enough, but not supported by all distributions.
Requires:       bareos-filedaemon >= 15.2.1
# fusermount
Requires:       fuse
Requires:       python-fuse
Requires:       python-bareos >= 0.4

%description
Bareos - Backup Archiving Recovery Open Sourced - FUSE

bareos-fuse allows you to display the information of a Bareos Backup System in your filesystem.



%prep
%setup -q

%build
%{pyXcmd} setup.py build

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%{pyXcmd} setup.py install --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}/bin %{buildroot}/etc  %{buildroot}/%{_sbindir}
#rsync -av bin/.  %{buildroot}/bin/.
rsync -av etc/.  %{buildroot}/etc/.
rsync -av sbin/. %{buildroot}/%{_sbindir}/.


%check
# does not work, as it tries to download other packages from pip
#%%{__python2} setup.py test
#%%{pyXcmd} setup.py -q test

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files
%defattr(-,root,root,-)
%doc README.rst
%{pyX_sitelib}/*
%{_bindir}/*
%{_sbindir}/*
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/console/bareosfs.conf.example
%config(noreplace) %attr(644,root,root) /etc/bareos/bareos-dir.d/profile/bareosfs-all.conf

%changelog
