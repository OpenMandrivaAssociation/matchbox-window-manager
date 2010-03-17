%define name 	matchbox-window-manager
%define version 1.2

%define enable_drakx_version 0

%{?_with_drakx: %global enable_drakx_version 1}

Summary: 	Window manager for the Matchbox Desktop
Name: 		%name
Version: 	%version
Release: 	%mkrel 14
Url: 		http://projects.o-hand.com/matchbox/
License: 	GPL
Group: 		Graphical desktop/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: 	http://projects.o-hand.com/matchbox/sources/%name/%version/%{name}-%{version}.tar.bz2
#specific theme for installer
Source1:	matchbox-ia_ora.tar.bz2
Source2:	30-start-matchbox.xsetup
Source3:	80-stop-matchbox.xsetup
# (fc) 1.2-2mdv various bug fixes from SVN
Patch0:		matchbox-window-manager-1.2-svnfixes.patch
# (fc) 1.2-2mdv various customizations for DrakX
Patch1:		matchbox-window-manager-1.2-drakx.patch
# (fc) 1.2-3mdv extend theme for separate decorations for modal dialogs
Patch2:		matchbox-window-manager-1.2-modal.patch

BuildRequires:	pkgconfig libmatchbox-devel expat-devel 
BuildRequires:	startup-notification-devel libXsettings-client-devel
BuildRequires:	libGConf2-devel
BuildRequires:  libxcomposite-devel
BuildRequires:  libxdamage-devel
%if %mdkversion <= 200900
Requires(post):	GConf2
%endif
Requires(preun):GConf2

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%package -n drakx-installer-matchbox
Summary:	Customized version of Matchbox for DrakX installer
Group:		Graphical desktop/Other

%description -n drakx-installer-matchbox
Customized version of Matchbox Window Manager for DrakX installer

%prep
%setup -q
%patch0 -p1 -b .svnfixes
%patch1 -p1 -b .drakx-version
%patch2 -p1 -b .modal

%build
[ -d standard ] || mkdir standard
cd standard
CONFIGURE_TOP=.. \
%configure2_5x --enable-expat --disable-composite \
--enable-gconf --enable-startup-notification

%make
cd -

[ -d drakx ] || mkdir drakx
cd drakx
CONFIGURE_TOP=.. \
CFLAGS="%optflags -DDRAKX_VERSION" %configure2_5x --enable-expat --enable-composite \
--disable-session --disable-keyboard --disable-ping-protocol --disable-xrm --disable-gconf --disable-startup-notification --disable-xsettings

%make
cd -

%install
rm -rf $RPM_BUILD_ROOT
cd standard
%makeinstall_std
cd -

#this file is ignored 
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/matchbox/kbdconfig

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xsetup.d/

install -m755 %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xsetup.d/

tar -x -C $RPM_BUILD_ROOT -f %{SOURCE1}

install -m 755 drakx/src/matchbox-window-manager $RPM_BUILD_ROOT%{_bindir}/drakx-matchbox-window-manager

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
%_sysconfdir/gconf/schemas/matchbox.schemas
%_bindir/matchbox*
%_datadir/matchbox/*
%_datadir/themes/*
%exclude %_datadir/themes/Ia*Ora*Smooth

%files -n drakx-installer-matchbox
%defattr(-,root,root)
%_sysconfdir/X11/xsetup.d/*.xsetup
%_bindir/drakx-matchbox-window-manager
%_datadir/themes/Ia*Ora*Smooth
%_datadir/matchbox/*
