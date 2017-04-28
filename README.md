# This is no longer maintained

  RHEL 7/CentOS 7 was released 3 years ago, so just upgrade to that if
  you want to use Chrome.

This spec file was inspired by the install_chrome.sh script by Richard
K. Lloyd, as found on http://chrome.richardlloyd.org.uk/

The end result is more or less the same, but with the chrome-deps
packagage it is possible to use normal package management tools like
rpm/yum to install and upgrade the google-chrome package.

- Main differences from version 3.00 of install_chrome.sh
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

- In order to build an x86_64 (64-bit) version you need to download the
  following files to ~/rpmbuild/SOURCES/

  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/x86_64/gdk-pixbuf2-2.23.3-2.fc15.x86_64.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/x86_64/glib2-2.28.8-1.fc15.x86_64.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/x86_64/glibc-2.14.1-6.x86_64.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/x86_64/gtk2-2.24.7-3.fc15.x86_64.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/x86_64/libstdc++-4.6.3-2.fc15.x86_64.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/releases/17/Fedora/x86_64/os/Packages/l/libgnome-keyring-3.4.1-2.fc17.x86_64.rpm

- In order to build an i686 (32-bit) version you need to download the
  following files to ~/rpmbuild/SOURCES/

  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/i386/gdk-pixbuf2-2.23.3-2.fc15.i686.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/i386/glib2-2.28.8-1.fc15.i686.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/i386/glibc-2.14.1-6.i686.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/i386/gtk2-2.24.7-3.fc15.i686.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/updates/15/i386/libstdc++-4.6.3-2.fc15.i686.rpm
  * http://dl.fedoraproject.org/pub/archive/fedora/linux/releases/17/Fedora/i386/os/Packages/l/libgnome-keyring-3.4.1-2.fc17.i686.rpm

- To build the chrome-deps RPM you use:
  rpmbuild -bb chrome-deps.spec
