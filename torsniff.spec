%define debug_package %{nil}

%define  uid   torsniff 
%define  gid   torsniff 
%define  nuid  980
%define  ngid  980



Name:     torsniff 
Version:  0.1.1
Release:  4%{?dist}
Summary:  Bittorrent Spider Written in GoLang
Epoch:    1
Packager: idcm <idcm@live.cn>
License:  AGPLv3
Group:    System Environment/Daemons
URL:      https://github.com/idcm/torsniff/tags
Source0:  https://github.com/idcm/torsniff/archive/%{version}.tar.gz
Source1:  torsniff.service
Source2:  torsniff.sysconfig

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:     golang
BuildRequires:     git
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd



%description
Torsniff an opensource Bittorrent Spider written in GoLang.

%prep
%setup -q -n %{name}-%{version}

%build
go build -o %{name} -ldflags "-s -w -X main.VERSION=%{version}"


%install
rm -rf %{buildroot}
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/torrents

# install binary
install -p -D -m 0755 %{_builddir}/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/torsniff.service

# install configuration
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/sysconfig/torsniff

%clean
rm -rf %{buildroot}

%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -s /sbin/nologin -u %{nuid} -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -s /sbin/nologin -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi

%post
%systemd_post torsniff.service

%preun
%systemd_preun torsniff.service

%postun
%systemd_postun_with_restart torsniff.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/torsniff
%{_unitdir}/torsniff.service
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/torrents

%changelog
* Tue Jan 07 2020 IDCM <idcm@live.cn>
