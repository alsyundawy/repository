
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat

Summary:    Apache Servlet/JSP Engine
Name:       ulyaoth-tomcat7-docs
Version:    7.0.73
Release:    1%{?dist}
BuildArch: x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        http://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sbagmeijer@ulyaoth.net>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-7/v%{version}/bin/apache-tomcat-%{version}.tar.gz
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: ulyaoth-tomcat7

Provides: tomcat-docs
Provides: apache-tomcat-docs
Provides: ulyaoth-tomcat-docs
Provides: ulyaoth-tomcat7-docs

%description
The package contains the official Apache Tomcat "webapps/docs" directory.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Delete all files except webapp docs
%{__rm} -rf %{buildroot}/%{tomcat_home}/bin
%{__rm} -rf %{buildroot}/%{tomcat_home}/conf
%{__rm} -rf %{buildroot}/%{tomcat_home}/lib
%{__rm} -rf %{buildroot}/%{tomcat_home}/LICENSE
%{__rm} -rf %{buildroot}/%{tomcat_home}/NOTICE
%{__rm} -rf %{buildroot}/%{tomcat_home}/RELEASE-NOTES
%{__rm} -rf %{buildroot}/%{tomcat_home}/RUNNING.txt
%{__rm} -rf %{buildroot}/%{tomcat_home}/temp
%{__rm} -rf %{buildroot}/%{tomcat_home}/work
%{__rm} -rf %{buildroot}/%{tomcat_home}/logs
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/examples
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/ROOT
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/host-manager
%{__rm} -rf %{buildroot}/%{tomcat_home}/webapps/manager

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%dir %{tomcat_home}/webapps/docs
%{tomcat_home}/webapps/docs/*

%post
cat <<BANNER
----------------------------------------------------------------------

Thank you for using ulyaoth-tomcat7-docs!

Please find the official documentation for tomcat here:
* http://tomcat.apache.org/

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

%changelog
* Sat Nov 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.73-1
- Updated to Tomcat 7.0.73.

* Sat Oct 1 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.72-1
- Updated to Tomcat 7.0.72.

* Wed Jun 22 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.70-1
- Updated to Tomcat 7.0.70.

* Tue Apr 26 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.69-1
- Updated to Tomcat 7.0.69.

* Sat Apr 9 2016 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.68-1
- Updated to Tomcat 7.0.68.

* Sun Dec 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.67-1
- Updated to Tomcat 7.0.67.

* Sat Oct 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 7.0.65-1
- Updated to Tomcat 7.0.65.

* Thu Jul 9 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.63-1
- Updated to Tomcat 7.0.63.

* Fri May 15 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.62-1
- Updated to Tomcat 7.0.62.

* Sat Apr 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.61-1
- Updated to Tomcat 7.0.61.

* Fri Mar 13 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-3
- Support for Oracle Linux 6 & 7.

* Wed Mar 11 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-2
- Removal of some things from spec file.
- Support for Fedora 22 and CentOS 6 & 7.
- i386 Support.

* Fri Feb 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.59-1
- Update to tomcat 7.0.59.

* Tue Nov 18 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.57-1
- Update to tomcat 7.0.57.

* Mon Nov 17 2014 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 7.0.56-1
- Creating separate package for the documentation.