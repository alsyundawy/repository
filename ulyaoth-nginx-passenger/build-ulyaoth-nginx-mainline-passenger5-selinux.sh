arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf install -y policycoreutils-python checkpolicy selinux-policy-devel
else
yum install -y policycoreutils-python checkpolicy selinux-policy-devel
fi

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SELinux/ulyaoth-nginx-mainline-passenger5.txt"
su ulyaoth -c "audit2allow -M ulyaoth-nginx-mainline-passenger5 < ulyaoth-nginx-mainline-passenger5.txt"
su ulyaoth -c "mv ulyaoth-nginx-mainline-passenger5.pp /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SPECS/ulyaoth-nginx-mainline-passenger5-selinux.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-passenger5-selinux.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-selinux.spec
elif grep -q -i "release 23" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-selinux.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-selinux.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-mainline-passenger5-selinux.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /home/ulyaoth/ulyaoth-*
rm -rf /root/build-ulyaoth-nginx-mainline-passenger5-selinux.sh