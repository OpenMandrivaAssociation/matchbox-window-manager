Summary: 	Window manager for the Matchbox Desktop
Name: 		matchbox-window-manager
Version: 	1.2
Release: 	17
Url: 		http://projects.o-hand.com/matchbox/
License: 	GPLv2+
Group: 		Graphical desktop/Other
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

BuildRequires:	pkgconfig pkgconfig(libmb) pkgconfig(expat)
BuildRequires:	pkgconfig(libstartup-notification-1.0) libXsettings-client-devel
BuildRequires:	pkgconfig(gconf-2.0) GConf2
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
Requires(preun):GConf2

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%package -n	drakx-installer-matchbox
Summary:	Customized version of Matchbox for DrakX installer
Group:		Graphical desktop/Other

%description -n drakx-installer-matchbox
Customized version of Matchbox Window Manager for DrakX installer

%prep
%setup -q
%patch0 -p1 -b .svnfixes~
%patch1 -p1 -b .drakx-version~
%patch2 -p1 -b .modal~

%build
CONFIGURE_TOP="$PWD"
LDFLAGS="%{ldflags} -lm"
mkdir -p standard
pushd standard
%configure2_5x	--enable-expat \
		--disable-composite \
		--enable-gconf \
		--enable-startup-notification
%make
popd

mkdir -p drakx
pushd drakx
CFLAGS="%{optflags} -DDRAKX_VERSION -Os" \
%configure2_5x	--enable-expat	\
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
%{_datadir}/matchbox/*
%{_datadir}/themes/*
%exclude %{_datadir}/themes/Ia*Ora*Smooth
%exclude %{_datadir}/matchbox/mbnoapp.xpm

%files -n drakx-installer-matchbox
%{_sysconfdir}/X11/xsetup.d/*.xsetup
%{_bindir}/drakx-matchbox-window-manager
%{_datadir}/themes/Ia*Ora*Smooth
%{_datadir}/matchbox/*

%changelog
* Tue Dec 11 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.2-17
- use pkgconfig(foo) deps for buildrequires
- compile drakx build with -Os
- cleanups

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 1.2-16mdv2011.0
+ Revision: 669809
- add br

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-15mdv2011.0
+ Revision: 606629
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-14mdv2010.1
+ Revision: 523285
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.2-13mdv2010.0
+ Revision: 426076
- rebuild

* Mon Apr 20 2009 Frederic Crozat <fcrozat@mandriva.com> 1.2-12mdv2009.1
+ Revision: 368420
- Update default background color in patch1

* Fri Mar 20 2009 Frederic Crozat <fcrozat@mandriva.com> 1.2-11mdv2009.1
+ Revision: 359154
- Regenerate patch 2
- Disable composite for standard build (Mdv bug #48982)

* Tue Nov 18 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-10mdv2009.1
+ Revision: 304212
- Stop matchbox a little later, needed for draklive-resize

* Tue Sep 30 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-9mdv2009.0
+ Revision: 290158
- Update patch1 to render root window not as black but with Mandriva blue (fix black squares in finish-install)

* Wed Sep 17 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-8mdv2009.0
+ Revision: 285474
- Add xsetup scripts to start / stop drakx matchbox, for usage with finish-install / draklive-install  / drakfirsttime

* Tue Aug 19 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-7mdv2009.0
+ Revision: 273801
- Remove alpha transparency on Ia Ora window corners (not handled by Matchbox)
- Update patch1 to not use lowlight on override windows (menu popup)

* Thu Jul 31 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-6mdv2009.0
+ Revision: 258270
- Update patch1 to force all modal dialogs to be super modal

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Jul 24 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-4mdv2009.0
+ Revision: 245572
- Reorganise specfile and patches to build both standard and drakx version of matchbox at the same time
- Update theme description
- put drakx version of matchbox and Ia Ora Smooth in separate subpackage

* Tue Jul 22 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2-3mdv2009.0
+ Revision: 240111
- Add xdamage-devel to buildrequires
- Fix buildrequires
- Patch2: extend theme for separate decorations for modal dialogs
- Update patch1 to include default for drakx version
- Update Ia Ora Smooth theme with modal decorations
- Patch0: add various bug fixes from SVN
- Patch1 + source0: various customizations for drakx usage

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 1.2-1mdv2008.1
+ Revision: 168083
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Wed Sep 05 2007 Jérôme Soyer <saispo@mandriva.org> 1.2-1mdv2008.0
+ Revision: 80239
- New version 1.2


* Thu Jan 25 2007 Jérôme Soyer <saispo@mandriva.org> 1.1-1mdv2007.0
+ Revision: 113080
- New release 1.1
- Import matchbox-window-manager

* Thu Mar 23 2006 Austin Acton <austin@mandriva.org> 1.0-1mdk
- New release 1.0

* Fri Aug 26 2005 Austin Acton <austin@mandriva.org> 0.9.5-1mdk
- New release 0.9.5

* Fri May 13 2005 Austin Acton <austin@mandriva.org> 0.9.4-1mdk
- 0.9.4
- new URLs

* Mon Jan 24 2005 Austin Acton <austin@mandrake.org> 0.9.2-1mdk
- 0.9.2

* Mon Jan 10 2005 Austin Acton <austin@mandrake.org> 0.9-1mdk
- 0.9

* Thu Sep 30 2004 Austin Acton <austin@mandrake.org> 0.8.4-1mdk
- 0.8.4

* Tue Aug 24 2004 Austin Acton <austin@mandrake.org> 0.8.3-2mdk
- fix schemas

* Tue Aug 24 2004 Austin Acton <austin@mandrake.org> 0.8.3-1mdk
- 0.8.3

* Wed Aug 11 2004 Austin Acton <austin@mandrake.org> 0.8.2-3mdk
- buildrequires xsettings

* Wed Jul 28 2004 Austin Acton <austin@mandrake.org> 0.8.2-1mdk
- enable startup-notification

* Wed Jul 21 2004 Austin Acton <austin@mandrake.org> 0.8.2-1mdk
- 0.8.2

