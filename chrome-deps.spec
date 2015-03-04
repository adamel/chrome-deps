# Spec file from https://github.com/adamel/chrome-deps
%define debug_package %{nil}

# Library versions.
%define gccver          4.9.2
%define stdcxxver       6.0.20

%define chromedir   /opt/google/chrome
%define instdir    %{chromedir}/lib

# For modify_wrapper script.
%define wrapper_mod_version 2.10
%define chrome_wrapper      %{chromedir}/google-chrome
%define chrome_defaults     /etc/default/google-chrome


Name:       chrome-deps
Version:    3.11
Release:    1%{?dist}
Summary:    Dependencies required for running Google Chrome on EL6
Group:      System Environment/Libraries
License:    LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and BSD
URL:        https://github.com/adamel/chrome-deps
Provides:   /opt/google/chrome/lib/link-to-libgnome-keyring.so.0


Source:     %{name}-%{version}.tar.gz
Source1:    http://mirrors.concertpass.com/gcc/releases/gcc-4.9.2/gcc-%{gccver}.tar.bz2
#Source1:    libstdc++.so.6.0.20
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc gmp-devel mpfr-devel libmpc-devel

%description
Includes an later libstdc++ Library, a shared library (libgnome-keyring.so.0)
and a soft-link to load in the original libgnome-keyring.so.0 system library.
Also modifies Google Chrome's wrapper script to allow Google Crhome to run on
RHEL/CentOS 6 derivatives.

%prep
%setup -q

# extract gcc source
tar xvf %{SOURCE1}


%build
# Build gnomekeyring module.
make -C src OPTFLAGS="$RPM_OPT_FLAGS"

# build gcc for libstdc++
# http://chrome.richardlloyd.org.uk/build_library.html
mkdir -p objdir
cd objdir
../gcc-%{gccver}/configure --enable-languages=c++ --disable-multilib
make %{?_smp_mflags} BOOT_CFLAGS='-O' bootstrap

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{instdir}

# Install libraries.
install -m 0755 ./objdir/prev-x86_64-unknown-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.%{stdcxxver} %{buildroot}/%{instdir}/libstdc++.so.%{stdcxxver}
ln -s libstdc++.so.%{stdcxxver} $RPM_BUILD_ROOT%{instdir}/libstdc++.so.6

install -m 0755 ./src/libgnome-keyring.so $RPM_BUILD_ROOT%{instdir}/libgnome-keyring.so.0
ln -sf /usr/lib64/libgnome-keyring.so.0 %{buildroot}/%{instdir}/link-to-libgnome-keyring.so.0

# Install chrome wrapper script modification script.
cat src/modify_wrapper | sed \
   -e "s#@MODIFY_WRAPPER@#modify_wrapper#g" \
   -e "s#@WRAPPER_MOD_VERSION@#%{wrapper_mod_version}#g" \
   -e "s#@SCRIPTNAME@#install_chrome.sh#g" \
   -e "s#@DEPS_NAME@#%{name}#g" \
   -e "s#@CHROME_DEFAULTS@#%{chrome_defaults}#g" \
   -e "s#@DEPS_NAME@#chrome-deps#g" \
   -e "s#@CUSTOMLIB@#%/opt/google/chrome/lib/libgnome-keyring.so.0#g" \
> $RPM_BUILD_ROOT%{chromedir}/modify_wrapper
chmod 0755 $RPM_BUILD_ROOT%{chromedir}/modify_wrapper

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{chromedir}/modify_wrapper

%files
%defattr(-,root,root,-)
%{chromedir}/modify_wrapper
%{chromedir}/lib/libstdc++.so.6
%{chromedir}/lib/libstdc++.so.%{stdcxxver}
%{chromedir}/lib/libgnome-keyring.so.0
%{chromedir}/lib/link-to-libgnome-keyring.so.0


%changelog
* Wed Mar 4 2015 Matthew Gyurgyik <matthew@pyther.net> - 3.11-1
- With RHEL 6.6 and newer Chrome just needs a more recent version of libstdc++.
  Unfortantly we must compile a newer version.
- Provide libgnome-keyring.so that includes a "missing" function
  (gnome_keyring_attribute_list_new)
- removed Dynamic Linker and Fedora libraries
- All changes were based on install_chrome.sh 7.11
  http://chrome.richardlloyd.org.uk/
  http://chrome.richardlloyd.org.uk/build_library.html

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
