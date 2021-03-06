%define debug_package %{nil}

# end of distribution specific definitions

Summary:    Cryptography and SSL/TLS Toolkit
Name:       ulyaoth-openssl1.1.0
Version:    1.1.0i
Release:    1%{?dist}
BuildArch: x86_64
License:    OpenSSL
Group:      System Environment/Libraries
URL:        https://www.openssl.org/
Vendor:     OpenSSL
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com>
%if 0%{?fedora}  == 19
Source0:    http://www.openssl.org/source/openssl-%{version}.tar.gz
%else
Source0:    https://www.openssl.org/source/openssl-%{version}.tar.gz
%endif
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SOURCES/ulyaoth-openssl1.1.0.conf
BuildRoot:  %{_tmppath}/openssl-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora}  == 19
BuildRequires: perl-Pod-MinimumVersion
%endif

Requires: ulyaoth-openssl1.1.0-libs

Provides: ulyaoth-openssl1.1.0
Provides: ulyaoth-openssl1.1.0i

%description
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library. The project is managed by a worldwide community of volunteers that use the Internet to communicate, plan, and develop the OpenSSL toolkit and its related documentation.
OpenSSL is based on the excellent SSLeay library developed by Eric Young and Tim Hudson. The OpenSSL toolkit is licensed under an Apache-style license, which basically means that you are free to get and use it for commercial and non-commercial purposes subject to some simple license conditions.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Provides: ulyaoth-openssl1.1.0-libs
%description libs
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-libs package contains the libraries that are used by various applications which support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl1.1.0-libs
Provides: ulyaoth-openssl1.1.0-devel
%description devel
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-devel package contains include files needed to develop applications which support various cryptographic algorithms and protocols.

%package static
Summary: Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: ulyaoth-openssl1.1.0-devel
Provides: ulyaoth-openssl1.1.0-static
%description static
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-static package contains static libraries needed for static linking of applications which support various cryptographic algorithms and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: ulyaoth-openssl1.1.0
%description perl
The OpenSSL Project is a collaborative effort to develop a robust, commercial-grade, full-featured, and Open Source toolkit implementing the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols as well as a full-strength general purpose cryptography library.
The openssl-perl package provides Perl scripts for converting certificates and keys from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n openssl-%{version}

%build
export C_INCLUDE_PATH=/usr/local/ulyaoth/openssl1.1.0/include
export LIBRARY_PATH=/usr/local/ulyaoth/openssl1.1.0/lib
export LD_RUN_PATH=/usr/local/ulyaoth/openssl1.1.0/lib

%ifarch i386 i486 i586 i686
./Configure -Wl,-rpath=/usr/local/ulyaoth/openssl1.1.0/lib --prefix=/usr/local/ulyaoth/openssl1.1.0 --openssldir=/usr/local/ulyaoth/openssl1.1.0 linux-elf shared
%endif
%ifarch x86_64
./Configure -Wl,-rpath=/usr/local/ulyaoth/openssl1.1.0/lib --prefix=/usr/local/ulyaoth/openssl1.1.0 --openssldir=/usr/local/ulyaoth//openssl1.1.0 linux-x86_64 shared
%endif

make depend
make all
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0
mkdir -p $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/man

make MANDIR=/usr/local/ulyaoth/openssl1.1.0/man MANSUFFIX=ssl DESTDIR="$RPM_BUILD_ROOT" install

mv $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/share/doc $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/
mv $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/misc/* $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/bin/
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/share
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/certs
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/private
rm -rf $RPM_BUILD_ROOT/usr/local/ulyaoth/openssl1.1.0/misc

%{__mkdir} -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT/etc/ld.so.conf.d/ulyaoth-openssl1.1.0.conf

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%files
%defattr(-,root,root,-)
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.1.0
/usr/local/ulyaoth/openssl1.1.0/bin/openssl
%doc /usr/local/ulyaoth/openssl1.1.0/man/man1*/*
%doc /usr/local/ulyaoth/openssl1.1.0/man/man5*/*
%doc /usr/local/ulyaoth/openssl1.1.0/man/man7*/*
/usr/local/ulyaoth/openssl1.1.0/doc/*
%doc /usr/local/ulyaoth/openssl1.1.0/man/*
%exclude /usr/local/ulyaoth/openssl1.1.0/man/man1*/*.pl*
%exclude /usr/local/ulyaoth/openssl1.1.0/man/man1*/c_rehash*
%exclude /usr/local/ulyaoth/openssl1.1.0/man/man1*/tsget*


%files libs
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.1.0
/usr/local/ulyaoth/openssl1.1.0/openssl.cnf.dist
%config(noreplace) /usr/local/ulyaoth/openssl1.1.0/openssl.cnf
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.1.0/lib/libcrypto.so.1.1
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.1.0/lib/libssl.so.1.1
%attr(0755,root,root) /usr/local/ulyaoth/openssl1.1.0/lib/engines-1.1/*
/etc/ld.so.conf.d/ulyaoth-openssl1.1.0.conf

%files devel
%dir /usr/local/ulyaoth
%dir /usr/local/ulyaoth/openssl1.1.0
%dir /usr/local/ulyaoth/openssl1.1.0/lib/pkgconfig
/usr/local/ulyaoth/openssl1.1.0/lib/*.so
/usr/local/ulyaoth/openssl1.1.0/include/*
%doc /usr/local/ulyaoth/openssl1.1.0/man/man3*/*
/usr/local/ulyaoth/openssl1.1.0/lib/pkgconfig/*.pc

%files static
/usr/local/ulyaoth/openssl1.1.0/lib/*.a

%files perl
/usr/local/ulyaoth/openssl1.1.0/bin/c_rehash
/usr/local/ulyaoth/openssl1.1.0/bin/CA.pl
/usr/local/ulyaoth/openssl1.1.0/bin/tsget
%doc /usr/local/ulyaoth/openssl1.1.0/man/man1*/*.pl*
%doc /usr/local/ulyaoth/openssl1.1.0/man/man1*/c_rehash*
%doc /usr/local/ulyaoth/openssl1.1.0/man/man1*/tsget*

%post
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.1.0!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%post libs
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.1.0-libs!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%post devel
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.1.0-devel!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%post static
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.1.0-static!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%post perl
/sbin/ldconfig
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-openssl1.1.0-perl!

Please find the official documentation for OpenSSL here:
* https://www.openssl.org

For any additional information or help regarding this rpm:
Website: https://ulyaoth.com
Forum: https://community.ulyaoth.com

----------------------------------------------------------------------
BANNER

%postun -p /sbin/ldconfig

%changelog
* Fri Nov 9 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> 1.1.0i-1
- Updated to OpenSSL 1.1.0i.

* Wed May 23 2018 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.1.0h-1
- Updated to OpenSSL 1.1.0h.

* Sun Nov 12 2017 Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.net> 1.1.0g-1
- Updated to OpenSSL 1.1.0g.

* Fri May 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0f-1
- Updated to OpenSSL 1.1.0f.

* Sun Mar 26 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0e-2
- Changed directory structure.
- ld fixes.
- split into sub packages, perl, static, libs, devel.

* Wed Feb 22 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0e-1
- Updated to OpenSSL 1.1.0e.

* Sun Feb 5 2017 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0d-1
- Updated to OpenSSL 1.1.0d.

* Sun Nov 13 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0c-1
- Updated to OpenSSL 1.1.0c.

* Mon Oct 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0b-2
- Added ldd fixes.

* Mon Sep 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0b-1
- Updated to OpenSSL 1.1.0b.

* Mon Sep 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0a-1
- Updated to OpenSSL 1.1.0a.

* Sat Aug 27 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-1
- Updated to OpenSSL 1.1.0.

* Sat Aug 6 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.6.pre6
- Updated to OpenSSL 1.1.0 Beta 3.

* Sun May 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.5.pre5
- Updated to OpenSSL 1.1.0 Beta 2.

* Sat Mar 19 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.4.pre4
- Updated to OpenSSL 1.1.0 Beta 1.

* Thu Jan 14 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.3.pre2
- Updated to OpenSSL 1.1.0 Alpha 2.

* Mon Jan 11 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.2.pre1
- added "shared" to compile options.

* Sun Jan 10 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 1.1.0-0.1.pre1
- Initial release with openssl 1.1.0-pre1.
