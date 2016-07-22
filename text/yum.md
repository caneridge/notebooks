# yum.md

## Cookbook

List files installed by RPM
  rpm -ql NAME

## Other

Copy jenkins3 to STE
  ssh p10-in-dev-jenk03.bris.cdi.com
  sudo su - relmanager
  scp /backup/ste_install/rpm/ts-sitecode-3.18.12-1.el6.x86_64.rpm repos01:/repos/cdirelease/EL6/ste/RPMS
  ssh repos01 createrepo --update /repos/cdirelease/EL6/ste

Copy STE to PROD
  ssh bjones@repos.twinspires.com
  sudo -s
  cd /repos/cdirelease/EL6/production
  scp CHURCHILL\\brian.jones@10.20.1.201:/repos/cdirelease/EL6/ste/RPMS/ts-sitecode-3.18.12-1.el6.x86_64.rpm .
  createrepo --update /repos/cdirelease/EL6/production


Search specific repository for something
```
  yum --disablerepo "*" --enablerepo "rpmforge" list available
```

ITE
  http://jenkins2.bris.cdi.com/business_services_repo/

STE
  ftp://release-snaps.bris.cdi.com/

Base for STE legacy repo location
  scp p10-in-dev-jenk03.bris.cdi.com:/backup/ste_install/

  Example
  scp p10-in-dev-jenk03.bris.cdi.com:/backup/ste_install/mobile/ts-mobile-3.18.8-1.el6.noarch.rpm DEST


List repos
  yum repolist

RUNDECK - james set it up
  p10-in-dev-rundeck01.bris.cdi.com

CREATE YUM REPOSITORY
=====================

##Documentation

http://man7.org/linux/man-pages/man1/yum-config-manager.1.html

       pkcon (1)
       yum.conf (5)
       yum-updatesd (8)
       package-cleanup (1)
       repoquery (1)
       yum-complete-transaction (1)
       yumdownloader (1)
       yum-utils (1)
       yum-security (8)

##Create directory structure

```
repos.dev.twinspires.com:
    /repos/cdirelease/EL6
        ite <-- future YUM REPO at or below here
          /RPMS
        ste <-- YUM REPO
          /RPMS
            ts-funding-3.18.1.rpm
```

##Repo host

10.20.1.201
p10-in-dev-repos01
repos.dev.twinspires.com:

##Make directory

sudo mkdir -p /repos/cdirelease/EL6/ste/RPMS

##Create repo

createrepo /repos/cdirelease/EL6/ste

##Repo file

/etc/yum.repos.d/cdirelease-ste.conf

[cdirelease-ste]
name = “Twinspires product releases to STE RHEL 6 - x86_64”
baseurl=http://repos.dev.twinspires.com/cdirelease/EL6/ste
enabled=1
failovermethod=priority
metadata_expire=1m

##Jenkins 3 access

from jenk03 su to relmanager and:

ssh ste-packager@10.20.1.201

login, no password
also, I put that users home directory in /usr/home/ste-packager so that it would *not* be on the NFS /home share

### ~/.ssh/config:
```
    # Identity to r/w RPMs
    Host repos01
    HostName p10-in-dev-repos01.bris.cdi.com
    User ste-packager
    PreferredAuthentications publickey
```

```

##Setup document root

```
    <Directory /repos>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
    </Directory>
```

##Create repo file

Let’s assume your http/repository server is named super.software.biz. Your resulting repo file (/etc/yum.repos.d/super_software.repo on the target machines) should look something like:

```
# begin repo
[twinspires]
name=Twinspires Custom Packages for Enterprise Linux 6 - x86_64
baseurl=http://repos.dev.twinspires.com/twinspires/EL6/
enabled=1
gpgcheck=1
gpgkey=http://repos.dev.twinspires.com/twinspires/EL6/RPM-GPG-KEY-Twinspires
failovermethod=priority
metadata_expire=10m


# begin repo
[cdirelease-ste]
name = “Twinspires product releases to STE”
baseurl=“http://repos.dev.twinspires.com/tsrelease/EL6/cdirelease-ste“
enabled=1
failovermethod=priority
metadata_expire=1m
priority=20

----
# Note, if you enable whizbang-beta veryify that whizbang is also enabled
[whizbang-beta]
name = “WhizBang Beta”
baseurl=“http://super.software.biz/whizbang/EL6/whizbang-beta“
enabled=0
failovermethod=priority
metadata_expire=1m

# Note, if you enable whizbang-beta veryify that whizbang and whizbang beta are also enabled
[whizbang-testing]
name = “WhizBang Testing”
baseurl=“http://super.software.biz/whizbang/EL6/whizbang-testing“
enabled=0
failovermethod=priority
metadata_expire=1m
# end repo
```

###Example: twinspires.repo

/etc/yum.repos.d/twinspires.repo:

[twinspires]
name=Twinspires Custom Packages for Enterprise Linux 6 - x86_64
baseurl=http://repos.dev.twinspires.com/twinspires/EL6/
enabled=1
gpgcheck=1
gpgkey=http://repos.dev.twinspires.com/twinspires/EL6/RPM-GPG-KEY-Twinspires
failovermethod=priority
metadata_expire=10m

10.20.1.201: p10-in-dev-repos01



Brian;

Below are the steps to quickly create a YUM repository as we had discussed. You will have to adjust naming accordingly of course.

1). Create a directory structure:

mkdir -p /repos/whizbang/EL6/whizbang/RPMS /repos/whizbang/EL6/whizbang-testing/RPMS /repos/whizbang/EL6/whizbang-beta/RPMS

2). Drop your rpms in the appropriate RPMS directories. Keep in mind that the “production” repository is standalone. In other words the other repositories may (probably) rely on it for some packages (old, stable packages).

3). Create metadata:

createrepo /repos/whizbang/EL6/whizbang
createrepo /repos/whizbang/EL6/whizbang-testing
createrepo /repos/whizbang/EL6/whizbang-beta

4). Set up access to the repository via http. I would suggest using the /repos/ as the DocumentRoot and it won’t be in the path. You will also have to add a directory definition to allow directory traversal:

/etc/httpd/sites.d/repos.conf

    <Directory /repos>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
    </Directory>

5). Create the repo file

Let’s assume your http/repository server is named super.software.biz. Your resulting repo file (/etc/yum.repos.d/super_software.repo on the target machines) should look something like:

```
# begin repo
[whizbang]
name = “WhizBang”
baseurl=“http://super.software.biz/whizbang/EL6/whizbang“
enabled=1
failovermethod=priority
metadata_expire=1m

# Note, if you enable whizbang-beta veryify that whizbang is also enabled
[whizbang-beta]
name = “WhizBang Beta”
baseurl=“http://super.software.biz/whizbang/EL6/whizbang-beta“
enabled=0
failovermethod=priority
metadata_expire=1m

# Note, if you enable whizbang-beta veryify that whizbang and whizbang beta are also enabled
[whizbang-testing]
name = “WhizBang Testing”
baseurl=“http://super.software.biz/whizbang/EL6/whizbang-testing“
enabled=0
failovermethod=priority
metadata_expire=1m
# end repo
```


Jay Fougere, MCSE
Linux/UNIX/Microsoft Systems Administrator
Twinspires.com – A Churchill Downs Company

jay.fougere@twinspires.com

Phone:
(859) 223-4444 ext 4656
Direct Dial:
(859) 219-4656
Cell Phone:
(859) 629-2392
