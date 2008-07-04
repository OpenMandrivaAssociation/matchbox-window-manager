%define name 	matchbox-window-manager
%define version 1.2

%define enable_drakx_version 0

Summary: 	Window manager for the Matchbox Desktop
Name: 		%name
Version: 	%version
Release: 	%mkrel 2
Url: 		http://projects.o-hand.com/matchbox/
License: 	GPL
Group: 		Graphical desktop/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: 	http://projects.o-hand.com/matchbox/sources/%name/%version/%{name}-%{version}.tar.bz2
#specific theme for installer
Source1:	matchbox-ia_ora.tar.bz2
# (fc) 1.2-2mdv various bug fixes from SVN
Patch0:		matchbox-window-manager-1.2-svnfixes.patch
# (fc) 1.2-2mdv various customizations for DrakX
Patch1:		matchbox-window-manager-1.2-drakx.patch

BuildRequires:	pkgconfig libmatchbox-devel expat-devel 
%if !%enable_drakx_version
BuildRequires:	startup-notification-devel libXsettings-client-devel
BuildRequires:	libGConf2-devel
%if %mdkversion <= 200900
Requires(post):	GConf2
%endif
Requires(preun):GConf2
%endif

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%prep
%setup -q
%patch0 -p1 -b .svnfixes
%if %{enable_drakx_version}
%patch1 -p1 -b .drakx-version
%endif

%build
%configure2_5x --enable-expat --enable-composite \
%if %{enable_drakx_version}
--disable-session --disable-keyboard --disable-ping-protocol --disable-xrm --disable-gconf
%else
--enable-gconf --enable-startup-notification
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#this file is ignored 
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/matchbox/kbdconfig

%if %{enable_drakx_version}
tar -x -C $RPM_BUILD_ROOT -f %{SOURCE1}
%endif

%define schemas matchbox

%if %mdkversion < 200900
%if !%{enable_drakx_version}
%post
%post_install_gconf_schemas %{schemas}
%endif
%endif

%if !%{enable_drakx_version}
%preun
%preun_uninstall_gconf_schemas %{schemas}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS README ChangeLog
%_bindir/*
%if !%{enable_drakx_version}
%_sysconfdir/gconf/schemas/matchbox.schemas
%endif
%_datadir/matchbox/*
%_datadir/themes/*
