jenkins.md

# j0 system

http://p10-ts-dev-ansible.bris.cdi.com:8080/jenkins/

# Documentation

Jenkins under Tomcat
  https://wiki.jenkins-ci.org/display/JENKINS/Tomcat

Download war file
  https://updates.jenkins-ci.org/download/war/

Jenkins under python
  https://www.cloudbees.com/jenkins/juc-2015/presentations/JUC-2015-Europe-Orchestrating-Your-Bhattacharya.pdf

Pipeline
  https://jenkins.io/doc/pipeline/

Set jenkins home directory
  export CATALINA_OPTS="-DJENKINS_HOME=/path/to/jenkins_home/ -Xmx512m"

Add user
  <role rolename="admin"/>
  <user username="jenkins-admin" password="secret" roles="admin"/>


chown -R relmanager:common /usr/local/tomcat8/webapps
chown -R relmanager:common /usr/local/tomcat8/work
chown -R relmanager:common /usr/local/tomcat8/temp

Admin account
  admin / admin

Port excepption to:
  http://updates.jenkins-ci.org
  http://mirrors.jenkins-ci.org

  resolves to:
    ec2-52-202-51-185.compute-1.amazonaws.com

  SD Ticket considerations
    It wasn't the URL filter in this case, but Jenkins traffic was specifically being identified at L7 as 'jenkins' and not web browsing and 'jenkins' as an application wasn't being allowed.


Upgrade Jenkins
  https://wiki.jenkins-ci.org/display/JENKINS/Automated+Upgrade

# plugins

Pipeline plugin
pipeline stage view plugin
git plugin

# jenkins2 plugins

Name ↓
Active Directory plugin This plugin enables authentication through Active Directory on Windows environment.
Ant PluginThis plugin adds Apache Ant support to Jenkins.
Artifactory Plugin This plugin allows deploying maven artifacts and build info to Artifactory.
CVS Plug-in Integrates Jenkins with CVS version control system using a modified version of the Netbeans cvsclient.

Copy Artifact Plugin Adds a build step to copy artifacts from another project.
Email Extension Plugin This plugin is a replacement for Jenkins's email publisher
Mailer PluginThis plugin allows you to configure email notifications for build results. This is a break-out of the original core based email component.
Git client pluginShared library plugin for other Git related Jenkins plugins.
GIT plugin This plugin integrates GIT with Jenkins.

Build Name Setter Plugin This plug-in sets the display name of a build to something other than #1, #2, #3, ...
Credentials Plugin This plugin allows you to store credentials in Jenkins.
Environment Injector Plugin This plugin makes it possible to set an environment for the builds.
Extended Choice Parameter Plug-In Adds extended functionality to Choice parameter
Job Import Plugin The Job Import Plugin lets you import jobs from another Jenkins instance.
Mask Passwords Plugin This plugin allows masking passwords that may appear in the console.
Matrix Authorization Strategy Plugin Offers matrix-based security authorization strategies (global and per-project).
Matrix Project PluginMulti-configuration (matrix) project type.
Maven Integration pluginJenkins plugin for building Maven 2/3 jobs via a special project type.
Multiple SCMs plugin This plugin enables the selection of multiple source code management systems for a build. For example, it enables checking out the source code from one SCM while checking out legacy or third-party code from another.
Parameterized Trigger pluginThis plugin lets you trigger new builds when your build has completed, with various ways of specifying parameters for the new build.
Publish Over SSH Send build artifacts over SSH

External Monitor Job Type PluginAdds the ability to monitor the result of externally executed jobs.
Javadoc PluginThis plugin adds Javadoc support to Jenkins.
jQuery plugin This allows other plugins to use jQuery in UI.
LDAP PluginAdds LDAP authentication to Jenkins

MapDB API Plugin This plugin provides a shared dependency on the MapDB library so that other plugins can co-operate when using this library.
OWASP Markup Formatter Plugin Uses OWASP AntiSamy to allow safe-seeming HTML markup to be entered in project descriptions and the like.
PAM Authentication pluginAdds Unix Pluggable Authentication Module (PAM) support to Jenkins.
Subversion Plug-inThis plugin adds the Subversion support (via SVNKit) to Jenkins.
Token Macro Plugin This plug-in adds reusable macro expansion capability for other plug-ins to use.
Translation Assistance pluginThis plugin adds an additional dialog box in every page, which enables people to contribute localizations for the messages they are seeing in the current page.
user build vars plugin This plugin is used to set user build variables: jenkins user name and id.
Windows Slaves Plugin Allows you to connect to Windows machines and start slave agents on them.

Role-based Authorization Strategy Enables authorization using a role-based strategy.
SCM API Plugin This plugin provides a new enhanced API for interacting with SCM systems.
SSH Credentials PluginThis plugin allows you to store SSH credentials in Jenkins.
SSH plugin This plugin executes shell commands remotely using SSH protocol.
SSH Slaves pluginThis plugin allows you to manage slaves running on \*nix machines over SSH.
Validating String Parameter Plugin Adds a new parameter type called Validating String Parameter which supports regular expression validation of a user entered parameter.
Workspace Cleanup Plugin This plugin deletes the project workspace after a build is finished.


# p10-ts-dev-ansible

ansible-playbook jenkins.yml
sudo chown relmanager /usr/local/tomcat8/logs
change tomcat => relmanager in /etc/init.d/tomcat8


# Jenkins latest

## Tomcat setup

/usr/local/tomcat/Catalina/localhost/funding.xml

Location of war file
  /usr/local/twinspires/swslib/funding/deploy

### server.xml

Fix connector

```xml
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443"
               URIEncoding="UTF-8"
               />
```

Add user

```xml
<role rolename="manager-gui"/>
  <role rolename="admin-gui"/>
  <user name="admin"
    password="mypassword"
    roles="admin-gui, manager-gui, manager-script, admin-script"
    />
```


# Jenkins3
## Tomcat setup

Jenkins RPM
  rpm -ql jenkins
    /etc/init.d/jenkins
    /etc/logrotate.d/jenkins
    /etc/sysconfig/jenkins
    /etc/yum.repos.d/jenkins.repo
      not usable
    /usr/lib/jenkins
    /usr/lib/jenkins/jenkins.war
      -rw-r--r--  1 root       root    67185354 Jan 20 09:19 jenkins.war
    /usr/sbin/rcjenkins
      /usr/sbin/rcjenkins -> ../../etc/init.d/jenkins
    /var/cache/jenkins
      war -- expanded war file
    /var/lib/jenkins
      jenkins home directory -- not used
      Configured home
        /backup/10.20.1.26/jenkins/jenkins_home
    /var/log/jenkins
      jenkins.log

/usr/share/tomcat6
/usr/share/tomcat6/webapps


/usr/share/tomcat6/work


drwxr-xr-x.   2 root root   4096 Apr  2  2014 bin
lrwxrwxrwx.   1 root tomcat   12 Apr  2  2014 conf -> /etc/tomcat6
lrwxrwxrwx.   1 root root     23 Apr  2  2014 lib -> /usr/share/java/tomcat6
lrwxrwxrwx.   1 root root     16 Apr  2  2014 logs -> /var/log/tomcat6
lrwxrwxrwx.   1 root root     23 Apr  2  2014 temp -> /var/cache/tomcat6/temp
lrwxrwxrwx.   1 root root     24 Apr  2  2014 webapps -> /var/lib/tomcat6/webapps
lrwxrwxrwx.   1 root root     23 Apr  2  2014 work -> /var/cache/tomcat6/work

/etc/tomcat6

drwxrwxr-x.   3 root tomcat  4096 Apr  2  2014 Catalina
-rw-rw-r--.   1 root root    8945 Sep 11  2013 catalina.policy
-rw-rw-r--.   1 root root    3713 Sep 11  2013 catalina.properties
-rw-rw-r--.   1 root root    1395 Sep 11  2013 context.xml
-rw-rw-r--.   1 root root     547 Sep 11  2013 log4j.properties
-rw-rw-r--.   1 root root    3257 Sep 11  2013 logging.properties
-rw-rw-r--.   1 root root    6639 Apr  2  2014 server.xml
-rw-rw-r--.   1 root root    1809 Apr  2  2014 tomcat6.conf
-rw-rw-r--.   1 root tomcat  1383 Sep 11  2013 tomcat-users.xml
-rw-rw-r--.   1 root root   50475 Sep 11  2013 web.xml

/etc/tomcat6/localhost
    empty

/etc/tomcat6/context.xml
    <Context>
            <WatchedResource>WEB-INF/web.xml</WatchedResource>
    </Context>

/etc/tomcat6/server.xml


#Jenkins02

JENKINS_HOME
    /backup/10.20.1.21/jenkins/jenkins_home

JOB XML FILE
    File that contains contents of job configuration
    $JENKINS_HOME/jobs/NAME/config.xml
      NAME is job name in the UI

##Legacy ITE configuration

###p10-in-dev-jenk02:/etc/yum.repos.d/business_services.repo

[ite_business_services]
name= Churchill Downs Business Services Applications
baseurl=http://jenkins2.bris.cdi.com/business_services_repo/
enabled=1
gpgcheck=0
failovermethod=priority

[business_services]
name=CDI Business Services Applications - ITE
baseurl=http://jenkins2.bris.cdi.com/business_services_repo/
enabled=1
gpgcheck=0
failovermethod=priority
metadata_expire=2m


###/etc/httpd/sites.d/repos.conf

```
<Directory /backup/ite_install/business_services/>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
</Directory>

<Directory /backup/ite_install/mobile/>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
</Directory>

<Directory /backup/ite_install/rpm/>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
</Directory>

<Directory /backup/ite_install/tux/>
      AllowOverride All
      Options Indexes FollowSymLinks
      Order allow,deny
      Allow from all
</Directory>
```

# Jenkins Ryan KT

Jenkins 1 (QA):
  url: https://jenkins1.bris.cdi.com/jenkins/

There are two kinds of tests that get executed
  1.) UI - Selenium
  2.) Web Services - Soap UI

Selenium:
  The grid runs at: 10.20.1.22

Start the selenium process with the follow command:
su -c "find /home/relmanager/10.20.1.22/tools/selenium -name 'launchhub.sh' -exec sh -c 'nohup {} &' \;" -s /bin/bash relmanager

These processes have been set to start at bootup via /etc/rc.local

The selenium grid/SoapUI nodes are windows machines:
  10.20.1.{27,28,29,30,31,32,33,34,35,36,37}

  and can be accessed via RDP and wrelmanager/10FwQhCWF1o

  To start the selenium process and connect the node to the grid, execute the .bat file in C:\Node

There is a scheduled task on 10.20.1.37 that run at 6am everyday to convert testng reports into the jelly bean reports. This executes a java program that is owned by the QA team

the Jelly bean reports can be accessed at:
  http://10.20.1.37:8080/ReportGenerate/


Jenkins 2 (ITE):
  Maven settings.xml file:
    File is located at: /opt/maven/conf/settings.xml. It is rare that this will ever need updated, but if you need to point to a new artifact repository, it will be done here.

  Versioning:
    Versions are derived from the timestamp of the most recent commit for the job in question. The jenkins job will determine the version with the following
    command: VERSION=$(git show -s --format=%at). This will derive a unix timestamp version like 1446041589 and the rpm spec file will use this version when building the rpm

Jenkins 3 (STE):
  Versioning:
    Versions are derived from the tag being built. So, if the Jenkins job is building tag 3.18.1, the rpm versioning will be 3.18.1.

  Release tasks:
    1. execute create branch job (http://jenkins3.bris.cdi.com/jenkins/view/RELEASE-BRANCH/job/create-branch/) on all repos being released. from_branch will typically be master and branch_name should be of the form release-<version> (release-3.18)
    2. execute the bump-pom-and-tag jobs to update POM files and create a git tag for all repos. from_branch should be the name of the branch created in step 1. tag_version should be an incrementing tag version, like 3.18.1
    3. repeat step 2, bumping the minor version, for all subsequent hotfix releases.

  The branching and release strategy is documented in detail: https://github.cdinteractive.com/devops/branch-release-strategy

Jenkins issues:
  The most common issue that arises is maven caching old versions of artifacts. When this happens, a developer will reach out and tell you that an old artifact is being cached. To fix this, login to jenkin2 and navigate to /backup/10.20.1.19/.m2 maven caching directory.
  you can then delete the directory for the artifact in question. So, if the issue is occurring on com.twinspires.cam, deleting the /backup/10.20.1.19/.m2/com/twinspires/cam directory and rebuilding will cause jenkins to generate a new, uncached artifact.

  It's rare, but sometimes a jenkins job will get into a weird state. Typically, clearing out the jobs workspace will fix the issue. So, if job GIT-TWS-RPM-TUX-BUILD is having trouble, login to jenkins2 and delete the directory: /backup/10.20.1.21/jenkins/jenkins_home/workspace/GIT-TWS-RPM-TUX-BUILD and rerun the build.

  The other common task is giving users permissions to the jenkins instance. the following page can be used to add them: https://jenkins2.bris.cdi.com/jenkins/role-strategy/assign-roles. Enter the users AD account like (john.smith) in the 	User/group to add field and then click the Add button
