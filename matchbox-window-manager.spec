%define name 	matchbox-window-manager
%define version 1.2

Summary: 	Window manager for the Matchbox Desktop
Name: 		%name
Version: 	%version
Release: 	%mkrel 1
Url: 		http://projects.o-hand.com/matchbox/
License: 	GPL
Group: 		Graphical desktop/Other
Source: 	http://projects.o-hand.com/matchbox/sources/%name/%version/%{name}-%{version}.tar.bz2

Buildroot: 	%_tmppath/%name-%version-buildroot
BuildRequires:	pkgconfig libmatchbox-devel expat-devel libGConf2-devel
BuildRequires:	startup-notification-devel libXsettings-client-devel
Requires(pre):	GConf2

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%prep
%setup -q

%build
%configure2_5x --enable-gconf --enable-expat --enable-message-wins --enable-startup-notification
%make

%install
rm -rf $RPM_BUILD_ROOT
perl -p -i -e 's|install-data-local:|||g' data/schemas/Makefile
%makeinstall

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/matchbox.schemas > /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS README ChangeLog
%_bindir/*
%config(noreplace) %{_sysconfdir}/matchbox/kbdconfig
%_sysconfdir/gconf/schemas/matchbox.schemas
%_datadir/matchbox/*
%_datadir/themes/*


