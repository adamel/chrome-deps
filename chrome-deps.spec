# Spec file from https://github.com/adamel/chrome-deps

# Library versions.
%define glibcver	2.14.1
%define glibcrel	6
%define stdcxxver	6.0.16
%define libstdcxxver	4.6.3-2.fc15
%define glib2ver	2.28.8-1.fc15
%define glib2libver	2800.8
%define gtk2ver		2.24.7-3.fc15
%define gtk2libver	2400.7
%define gdkpixbuf2ver 2.23.3-2.fc15
%define gdkpixbuf2libver 2300.3
%define libgnomekeyringver 3.4.1-2.fc17
%define libgnomekeyringlibver 2.0
%define fedoramirror	http://archives.fedoraproject.org/pub/archive/fedora/linux/updates/15/%{_arch}
%define f17_os_mirror	http://archives.fedoraproject.org/pub/archive/fedora/linux/releases/17/Everything/%{_arch}/os/Packages/l/

%define chromedir	/opt/google/chrome
%define instdir		%{chromedir}/lib

# For modify_wrapper script.
%define wrapper_mod_version	1.01
%define chrome_wrapper		%{chromedir}/google-chrome
%define chrome_defaults		/etc/default/google-chrome

%ifarch x86_64
%define ld_linux	ld-linux-x86-64
%else
%define ld_linux	ld-linux
%endif

Name:		chrome-deps
Version:	1.3
Release:	1%{?dist}
Summary:	Fedora libraries for running chrome on EL6
Group:		System Environment/Libraries
License:	LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and BSD
URL:		https://github.com/adamel/chrome-deps
Source:		%{name}-%{version}.tar.gz
Source1:	%{fedoramirror}/glibc-%{glibcver}-%{glibcrel}.%{_target_cpu}.rpm
Source2:	%{fedoramirror}/libstdc++-%{libstdcxxver}.%{_target_cpu}.rpm
Source3:	%{fedoramirror}/glib2-%{glib2ver}.%{_target_cpu}.rpm
Source4:	%{fedoramirror}/gtk2-%{gtk2ver}.%{_target_cpu}.rpm
Source5:	%{fedoramirror}/gdk-pixbuf2-%{gdkpixbuf2ver}.%{_target_cpu}.rpm
Source6:	%{f17_os_mirror}/libgnome-keyring-%{libgnomekeyringver}.%{_target_cpu}.rpm
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
Libraries (glibc, libstdc++, glib2, gtk2) taken from Fedora 15, in
order to be able to run latest Google Chrome on EL6 and derivates.

%prep
%setup -q
# Extract required libraries.
rpm2cpio %{SOURCE1} | cpio -vid ./%{_lib}/libc-%{glibcver}.so ./%{_lib}/ld-%{glibcver}.so
rpm2cpio %{SOURCE2} | cpio -vid .%{_libdir}/libstdc++.so.%{stdcxxver}
rpm2cpio %{SOURCE3} | cpio -vid ./%{_lib}/libglib-2.0.so.0.%{glib2libver}
rpm2cpio %{SOURCE4} | cpio -vid .%{_libdir}/libgtk-x11-2.0.so.0.%{gtk2libver} .%{_libdir}/libgdk-x11-2.0.so.0.%{gtk2libver}
rpm2cpio %{SOURCE5} | cpio -vid .%{_libdir}/libgdk_pixbuf-2.0.so.0.%{gdkpixbuf2libver}
rpm2cpio %{SOURCE6} | cpio -vid .%{_libdir}/libgnome-keyring.so.0.%{libgnomekeyringlibver}

%build
# Build preload module.
make -C src OPTFLAGS="$RPM_OPT_FLAGS"
# Patch glibc to reference the local copy of ld-linux.
sed -e "s/%{ld_linux}.so.2/%{ld_linux}.so.0/g" < ./%{_lib}/libc-%{glibcver}.so > ./%{_lib}/libc-%{glibcver}.so.patched
# Patch the identity of ld-linux itself to get RPM provides right.
sed -e "s/%{ld_linux}.so.2/%{ld_linux}.so.0/g" < ./%{_lib}/ld-%{glibcver}.so > ./%{_lib}/ld-%{glibcver}.so.patched


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{instdir}
# Install preload module.
install -m 0755 ./src/unset_var.so $RPM_BUILD_ROOT%{instdir}/
# Install patched libraries.
install -m 0755 ./%{_lib}/ld-%{glibcver}.so.patched $RPM_BUILD_ROOT%{instdir}/ld-%{glibcver}.so
ln -s ld-%{glibcver}.so $RPM_BUILD_ROOT%{instdir}/%{ld_linux}.so.0
install -m 0755 ./%{_lib}/libc-%{glibcver}.so.patched $RPM_BUILD_ROOT%{instdir}/libc-%{glibcver}.so
ln -s libc-%{glibcver}.so $RPM_BUILD_ROOT%{instdir}/libc.so.6
install -m 0755 .%{_libdir}/libstdc++.so.%{stdcxxver} $RPM_BUILD_ROOT%{instdir}/
ln -s libstdc++.so.%{stdcxxver} $RPM_BUILD_ROOT%{instdir}/libstdc++.so.6
install -m 0755 ./%{_lib}/libglib-2.0.so.0.%{glib2libver} $RPM_BUILD_ROOT%{instdir}/
ln -s libglib-2.0.so.0.%{glib2libver} $RPM_BUILD_ROOT%{instdir}/libglib-2.0.so.0
install -m 0755 .%{_libdir}/libgdk-x11-2.0.so.0.%{gtk2libver} $RPM_BUILD_ROOT%{instdir}/
ln -s libgdk-x11-2.0.so.0.%{gtk2libver} $RPM_BUILD_ROOT%{instdir}/libgdk-x11-2.0.so.0
install -m 0755 .%{_libdir}/libgtk-x11-2.0.so.0.%{gtk2libver} $RPM_BUILD_ROOT%{instdir}/
ln -s libgtk-x11-2.0.so.0.%{gtk2libver} $RPM_BUILD_ROOT%{instdir}/libgtk-x11-2.0.so.0
install -m 0755 .%{_libdir}/libgdk_pixbuf-2.0.so.0.%{gdkpixbuf2libver} $RPM_BUILD_ROOT%{instdir}/
ln -s libgdk_pixbuf-2.0.so.0.%{gdkpixbuf2libver} $RPM_BUILD_ROOT%{instdir}/libgdk_pixbuf-2.0.so.0
install -m 0755 .%{_libdir}/libgnome-keyring.so.0.%{libgnomekeyringlibver} $RPM_BUILD_ROOT%{instdir}/
ln -s libgnome-keyring.so.0.%{libgnomekeyringlibver} $RPM_BUILD_ROOT%{instdir}/libgnome-keyring.so.0
# Install chrome wrapper script modification script.
cat src/modify_wrapper | sed \
   -e "s#@MODIFY_WRAPPER@#modify_wrapper#g" \
   -e "s#@WRAPPER_MOD_VERSION@#%{wrapper_mod_version}#g" \
   -e "s#@SCRIPTNAME@#install_chrome.sh#g" \
   -e "s#@DEPS_NAME@#%{name}#g" \
   -e "s#@CHROME_DEFAULTS@#%{chrome_defaults}#g" \
   -e "s#@UNSETLIB@#%{instdir}/unset_var.so#g" \
   -e "s#@CHROME_WRAPPER@#%{chrome_wrapper}#g" \
> $RPM_BUILD_ROOT%{chromedir}/modify_wrapper
chmod 0755 $RPM_BUILD_ROOT%{chromedir}/modify_wrapper

%clean
rm -rf $RPM_BUILD_ROOT


%post
%{chromedir}/modify_wrapper


%files
%defattr(-,root,root,-)
%{chromedir}/modify_wrapper
%{instdir}/ld-%{glibcver}.so
%{instdir}/%{ld_linux}.so.0
%{instdir}/libc-%{glibcver}.so
%{instdir}/libc.so.6
%{instdir}/libstdc++.so.%{stdcxxver}
%{instdir}/libstdc++.so.6
%{instdir}/libglib-2.0.so.0.%{glib2libver}
%{instdir}/libglib-2.0.so.0
%{instdir}/libgdk-x11-2.0.so.0.%{gtk2libver}
%{instdir}/libgdk-x11-2.0.so.0
%{instdir}/libgtk-x11-2.0.so.0.%{gtk2libver}
%{instdir}/libgtk-x11-2.0.so.0
%{instdir}/libgdk_pixbuf-2.0.so.0.%{gdkpixbuf2libver}
%{instdir}/libgdk_pixbuf-2.0.so.0
%{instdir}/libgnome-keyring.so.0.%{libgnomekeyringlibver}
%{instdir}/libgnome-keyring.so.0
%{instdir}/unset_var.so


%changelog
* Wed May 07 2014 Matthew Gyurgyik <gyurgyikms@ornl.gov> - 1.3-1
- Include gdk-pixbuf2 and libgnome-keyring dependencies.

* Thu Sep 26 2013 Marcus Sundberg <marcus.sundberg@aptilo.com> - 1.2-1
- Intercept system() function as well.

* Thu Sep 19 2013 Marcus Sundberg <marcus.sundberg@aptilo.com> - 1.1-1
- Add unset_var preload wrapper from Richard K. Lloyd. This fixes
  the crashes when chrome tries to execute external programs.

* Mon Jul 22 2013 Marcus Sundberg <marcus.sundberg@aptilo.com> - 1.0-1
- Initial version - concept based on install_chrome.sh from
  http://chrome.richardlloyd.org.uk/
- Things done different compared to install_chrome.sh 3.00:
  * Dynamic linker gets version 0 instead of 3 - we won't see the
    version number of the system linker increase anytime soon, but a
    never used version is better than a version that may be used in
    the future.
  * Dynamic linker version gets replaced in the linker itself, not
    just in libc. This makes RPMs automatic dependency generation work
    properly.
  * The chrome repo file and cron job are not removed - with this
    package installed chrome can be installed and upgraded with yum
    just like any package.
  * The libraries are installed using their real filenames, and then
    symlinks with the names expected by the dynamic linker are
    created.
