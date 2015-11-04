arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y http://ftp.acc.umu.se/mirror/fedora/epel/6/$arch/epel-release-6-8.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y http://ftp.acc.umu.se/mirror/fedora/epel/6/$arch/epel-release-6-8.noarch.rpm
elif grep -q -i "release 7" /etc/oracle-release
then
yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm
else
echo yeah Fedora!
fi

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modsecurity/SPECS/ulyaoth-nginx-modsecurity.spec"
mkdir -p /etc/nginx/modules
cd /etc/nginx/modules
wget https://www.modsecurity.org/tarball/2.9.0/modsecurity-2.9.0.tar.gz
tar xvf modsecurity-2.9.0.tar.gz
mv modsecurity-2.9.0 modsecurity
rm -rf modsecurity-2.9.0.tar.gz
cd modsecurity
./autogen.sh
./configure --enable-standalone-module
make
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /etc/nginx/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-modsecurity.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-nginx-modsecurity.spec
elif grep -q -i "release 23" /etc/fedora-release
then
dnf builddep -y ulyaoth-nginx-modsecurity.spec
else
yum-builddep -y ulyaoth-nginx-modsecurity.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-modsecurity -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-modsecurity.spec"
rm -rf /home/ulyaoth/rpmbuild/BUILD/*
rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*
rm -rf /home/ulyaoth/rpmbuild/RPMS/*
rm -rf /home/ulyaoth/rpmbuild/SOURCES/modsecurity.tar.gz
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-modsecurity.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/