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

%define fedoramirror	http://mirrors.kernel.org/fedora/updates/15/%{_arch}

%define instdir		/opt/google/chrome/lib

%ifarch x86_64
%define ld_linux	ld-linux-x86-64
%else
%define ld_linux	ld-linux
%endif

Name:		chrome-deps
Version:	1.0
Release:	1%{?dist}
Summary:	Fedora libraries for running chrome on EL6
Group:		System Environment/Libraries
License:	LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and BSD
URL:		https://github.com/adamel/chrome-deps
Source0:	%{fedoramirror}/glibc-%{glibcver}-%{glibcrel}.%{_target_cpu}.rpm
Source1:	%{fedoramirror}/libstdc++-%{libstdcxxver}.%{_target_cpu}.rpm
Source2:	%{fedoramirror}/glib2-%{glib2ver}.%{_target_cpu}.rpm
Source3:	%{fedoramirror}/gtk2-%{gtk2ver}.%{_target_cpu}.rpm
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
Libraries (glibc, libstdc++, glib2, gtk2) taken from Fedora 15, in
order to be able to run latest Google Chrome on EL6 and derivates.

%prep
%setup -q -c %{name}-%{version} -T
# Extract required libraries.
rpm2cpio %{SOURCE0} | cpio -vid ./%{_lib}/libc-%{glibcver}.so ./%{_lib}/ld-%{glibcver}.so
rpm2cpio %{SOURCE1} | cpio -vid .%{_libdir}/libstdc++.so.%{stdcxxver}
rpm2cpio %{SOURCE2} | cpio -vid ./%{_lib}/libglib-2.0.so.0.%{glib2libver}
rpm2cpio %{SOURCE3} | cpio -vid .%{_libdir}/libgtk-x11-2.0.so.0.%{gtk2libver} .%{_libdir}/libgdk-x11-2.0.so.0.%{gtk2libver}

%build
# Patch glibc to reference the local copy of ld-linux.
sed -e "s/%{ld_linux}.so.2/%{ld_linux}.so.0/g" < ./%{_lib}/libc-%{glibcver}.so > ./%{_lib}/libc-%{glibcver}.so.patched
# Patch the identity of ld-linux itself to get RPM provides right.
sed -e "s/%{ld_linux}.so.2/%{ld_linux}.so.0/g" < ./%{_lib}/ld-%{glibcver}.so > ./%{_lib}/ld-%{glibcver}.so.patched


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{instdir}
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


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
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

%changelog
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
