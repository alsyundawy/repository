#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm
%define nginx_version 1.9.5

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?fedora} >= 18
Group: System Environment/Daemons
Requires: systemd
BuildRequires: systemd
%define with_spdy 1
%endif

# end of distribution specific definitions

Summary: High performance web server / Phusion Passenger web & app
Name: ulyaoth-nginx-mainline-passenger5
Version: 5.0.21
Release: 1%{?dist}
BuildArch: x86_64
Vendor: nginx inc. / Phusion
URL: https://www.phusionpassenger.com/
Packager: Sjir Bagmeijer <sbagmeijer@ulyaoth.net>

Source0: http://nginx.org/download/nginx-%{nginx_version}.tar.gz
Source1: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/logrotate
Source2: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.init
Source3: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.sysconf
Source4: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.conf
Source5: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.vh.default.conf
Source6: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.vh.example_ssl.conf
Source7: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.suse.init
Source8: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.service
Source9: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.upgrade.sh
Source10: https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SOURCES/nginx.vh.passenger5.conf
Source11: passenger.tar.gz

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/nginx-%{nginx_version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: curl-devel
BuildRequires: rubygem-rake
BuildRequires: GeoIP
BuildRequires: GeoIP-devel

Requires: openssl
Requires: ruby
Requires: GeoIP

Provides: webserver
Provides: nginx
Provides: nginx-mainline
Provides: nginx-passenger
Provides: nginx-passenger5
Provides: nginx-mainline-passenger
Provides: nginx-mainline-passenger5
Provides: passenger
Provides: passenger5
Provides: ulyaoth-nginx
Provides: ulyaoth-nginx-passenger
Provides: ulyaoth-nginx-passenger5
Provides: ulyaoth-nginx-mainline
Provides: ulyaoth-nginx-mainline-passenger
Provides: ulyaoth-nginx-mainline-passenger5

%description
nginx [engine x] is an HTTP and reverse proxy server, as well asa mail proxy server.
Phusion Passenger is a multi-language (Ruby, Python, Node) web & app server which can integrate into Apache and Nginx

%package debug
Summary: debug version of nginx with passenger
Group: System Environment/Daemons
Requires: ulyaoth-nginx-mainline-passenger5
%description debug
Not stripped version of nginx and passenger built with the debugging log support.

%prep
%setup -q -n nginx-%{nginx_version}

%build
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-http_geoip_module \
        --with-threads \
        --with-stream \
        --with-stream_ssl_module \
		--add-module=/etc/nginx/modules/passenger/src/nginx_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        --with-http_v2_module \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/nginx-%{nginx_version}/objs/nginx \
        %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
		--with-http_geoip_module \
        --with-threads \
        --with-stream \
        --with-stream_ssl_module \
		--add-module=/etc/nginx/modules/passenger/src/nginx_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-http_v2_module \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/passenger
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx/passenger_temp

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf
%{__install} -m 644 -p %{SOURCE10} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/passenger.conf
   
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-enabled

# Install Passenger
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules
tar xvf %{SOURCE11} -C $RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules/

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version} == 1110
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%if 0%{?suse_version}
%{__install} -m 644 -p %{SOURCE10} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%else
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%endif

%{__install} -m644 %{_builddir}/nginx-%{nginx_version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/sites-available
%dir %{_sysconfdir}/nginx/sites-enabled
%dir %{_sysconfdir}/nginx/modules
%{_sysconfdir}/nginx/modules/*

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/passenger.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx/passenger_temp
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/passenger

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using ulyaoth-nginx-mainline-passenger5!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

Please find the official documentation or the enterprise version for passenger here:
* https://www.phusionpassenger.com/ 

For any additional help please visit my forum at:
* https://www.ulyaoth.net

----------------------------------------------------------------------
BANNER

    # Touch and set permissions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%changelog
* Sat Oct 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.21-1
- Updated to Passenger 5.0.21.

* Sat Oct 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.20-1
- Updated to Passenger 5.0.20.
- Update to Nginx Mainline 1.9.5.
- Changed spdy to http_v2_module.

* Sat Sep 12 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.18-1
- Updated to Passenger 5.0.18.

* Mon Aug 24 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.16-1
- Updated to Passenger 5.0.16.

* Fri Aug 21 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.net> 5.0.15-2
- Update to Nginx Mainline 1.9.4.

* Thu Jul 30 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.15-1
- Updated to Passenger 5.0.15.

* Thu Jul 16 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.14-1
- Updated to Passenger 5.0.14.
- Updated to Nginx Mainline 1.9.3.

* Sun Jul 5 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.13-1
- Updated to Passenger 5.0.13.

* Fri Jun 26 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.11-1
- Updated to Passenger 5.0.11.

* Thu Jun 18 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.10-2
- Updated to Nginx 1.9.2.

* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.10-1
- Updated to Passenger 5.0.10.

* Sun Jun 14 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.9-1
- Updated to Passenger 5.0.9.

* Wed Jun 3 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.8-2
- Update to Nginx Mainline 1.9.1.

* Wed May 20 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.8-1
- Updated to Passenger 5.0.8.

* Tue Apr 28 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.7-1
- Updated to Nginx 1.9.0.
- Updated to Passenger 5.0.7.

* Wed Apr 8 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-2
- Updated to Nginx 1.7.12.

* Mon Apr 6 2015 Sjir Bagmeijer <sbagmeijer@ulyaoth.co.kr> 5.0.6-1
- Initial Release.
- Spec file taken from nginx.com
- Compiled with Mainline Nginx version 1.7.11