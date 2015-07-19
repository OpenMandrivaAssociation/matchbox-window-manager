Summary:	Window manager for the Matchbox Desktop
Name:		matchbox-window-manager
Version:	1.2
Release:	26
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://projects.o-hand.com/matchbox/
Source0:	http://projects.o-hand.com/matchbox/sources/%name/%version/%{name}-%{version}.tar.bz2
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

BuildRequires:	Xsettings-client-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gconf-2.0) GConf2
BuildRequires:	pkgconfig(libmb)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
Requires(preun):GConf2

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%package -n	drakx-installer-matchbox
Summary:	Customized version of Matchbox for DrakX installer
Group:		Graphical desktop/Other

%description -n	drakx-installer-matchbox
Customized version of Matchbox Window Manager for DrakX installer

%prep
%setup -q
%apply_patches

%build
CONFIGURE_TOP="$PWD"
LDFLAGS="%{ldflags} -lm"
mkdir -p standard
pushd standard
%configure2_5x \
	--enable-expat \
	--disable-composite \
	--enable-gconf \
	--enable-startup-notification
%make
popd

mkdir -p drakx
pushd drakx
CFLAGS="%{optflags} -DDRAKX_VERSION -Os" \
%configure2_5x \
	--enable-expat	\
	--enable-composite \
	--disable-session \
	--disable-keyboard \
	--disable-ping-protocol \
	--disable-xrm \
	--disable-gconf \
	--disable-startup-notification \
	--disable-xsettings
%make
popd

%install
%makeinstall_std -C standard

#this file is ignored 
rm %{buildroot}%{_sysconfdir}/matchbox/kbdconfig

mkdir -p %{buildroot}%{_sysconfdir}/X11/xsetup.d/

install -m755 %{SOURCE2} %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xsetup.d/

tar -x -C %{buildroot} -f %{SOURCE1}

install -m755 drakx/src/matchbox-window-manager -D %{buildroot}%{_bindir}/drakx-matchbox-window-manager

%files
%doc AUTHORS README ChangeLog
%{_sysconfdir}/gconf/schemas/matchbox.schemas
%{_bindir}/matchbox*
%{_datadir}/themes/*
%exclude %{_datadir}/themes/Ia*Ora*Smooth

%files -n drakx-installer-matchbox
%{_sysconfdir}/X11/xsetup.d/*.xsetup
%{_bindir}/drakx-matchbox-window-manager
%{_datadir}/themes/Ia*Ora*Smooth
%{_datadir}/matchbox/mbnoapp.xpm

