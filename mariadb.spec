%global pkg_name %{name}
%global pkgnamepatch mariadb
%{!?runselftest:%global runselftest 1}
%global ignore_testsuite_result 0
%global last_tested_version 10.5.10
%global force_run_testsuite 0
%global require_mysql_selinux 1

%global _pkgdocdirname %{pkg_name}%{!?_pkgdocdir:-%{version}}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{pkg_name}-%{version}}

%global _default_patch_flags --no-backup-if-mismatch

%ifarch x86_64
%bcond_with mroonga
%bcond_with rocksdb
%endif
%ifarch aarch64
%bcond_without mroonga
%bcond_without rocksdb
%endif

%bcond_without oqgraph
%bcond_without pam

# S3 storage engine
%bcond_with cracklib
%bcond_with connect
%bcond_with sphinx
%bcond_with s3
%bcond_with clibrary

%bcond_without gssapi
%bcond_without embedded
%bcond_without devel
%bcond_without client
%bcond_without common
%bcond_without errmsg
%bcond_without test
%bcond_without galera
%bcond_without backup

%bcond_without config

%bcond_with    debug
%bcond_without lz4

%bcond_without unbundled_pcre

%global python_path /usr/bin/python3

# Include systemd files
%global daemon_name %{name}
%global daemon_no_prefix %{pkg_name}
%global mysqld_pid_dir mariadb

# We define some system's well known locations here so we can use them easily
# later when building to another location (like SCL)
%global logrotateddir %{_sysconfdir}/logrotate.d
%global logfiledir %{_localstatedir}/log/%{daemon_name}
%global logfile %{logfiledir}/%{daemon_name}.log
# Directory for storing pid file
%global pidfiledir %{_rundir}/%{mysqld_pid_dir}
# Defining where database data live
%global dbdatadir %{_localstatedir}/lib/mysql
# Home directory of mysql user should be same for all packages that create it
%global mysqluserhome /var/lib/mysql

%bcond_with    mysql_names


# Make long macros shorter
%global sameevr   %{epoch}:%{version}-%{release}

Name:             mariadb
Version:          10.5.10
Release:          2
Epoch:            4

Summary:          A very fast and robust SQL database server
URL:              http://mariadb.org
License:          GPLv2 and LGPLv2

Source0:          https://downloads.mariadb.org/interstitial/mariadb-%{version}/source/mariadb-%{version}.tar.gz

Source2:          mysql_config_multilib.sh
Source3:          my.cnf.in
Source6:          README.mariadb-docs
Source10:         mariadb.tmpfiles.d.in
Source11:         mysql.service.in
Source12:         mariadb-prepare-db-dir.sh
Source14:         mariadb-check-socket.sh
Source15:         mariadb-scripts-common.sh
Source16:         mariadb-check-upgrade.sh
Source18:         mysql@.service.in
Source50:         skipped-tests-base.list
Source51:         skipped-tests-arm.list

Source70:         clustercheck.sh
Source71:         LICENSE.clustercheck

Source72:         mariadb-server-galera.te
#   Patch4: yum distributions specific logrotate fix
#   it would be big unexpected change, if we start shipping it now. Better wait for MariaDB 10.2
Patch4:           %{pkgnamepatch}-logrotate.patch
#   Patch7: add to the CMake file all files where we want macros to be expanded
Patch7:           %{pkgnamepatch}-scripts.patch
#   Patch9: pre-configure to comply with guidelines
Patch9:           %{pkgnamepatch}-ownsetup.patch
#   Patch10: Fix cipher name in the SSL Cipher name test
Patch10:          %{pkgnamepatch}-ssl-cipher-tests.patch
#   Patch11: Use PCDIR CMake option, if configured
Patch11:          %{pkgnamepatch}-pcdir.patch
#   Patch15:  Add option to edit groonga's and groonga-normalizer-mysql install path
Patch15:          %{pkgnamepatch}-groonga.patch

BuildRequires:    make
BuildRequires:    cmake gcc-c++
BuildRequires:    multilib-rpm-config
BuildRequires:    selinux-policy-devel
BuildRequires:    systemd systemd-devel

# Page compression algorithms for InnoDB & XtraDB
BuildRequires:    zlib-devel
%{?with_lz4:BuildRequires:    lz4-devel}

# asynchornous operations stuff; needed also for wsrep API
BuildRequires:    libaio-devel
# commands history features
BuildRequires:    libedit-devel
# CLI graphic; needed also for wsrep API
BuildRequires:    ncurses-devel
# debugging stuff
BuildRequires:    systemtap-sdt-devel
# Bison SQL parser; needed also for wsrep API
BuildRequires:    bison bison-devel

%{?with_debug:BuildRequires:    valgrind-devel}

# use either new enough version of pcre2 or provide bundles(pcre2)
%{?with_unbundled_pcre:BuildRequires: pcre2-devel pkgconf}
%{!?with_unbundled_pcre:Provides: bundled(pcre2) = %{pcre_bundled_version}}
# Few utilities needs Perl
BuildRequires:    perl-interpreter
BuildRequires:    perl-generators
# Some tests requires python
BuildRequires:    python3
# Tests requires time and ps and some perl modules
BuildRequires:    procps
BuildRequires:    time
BuildRequires:    perl(base)
BuildRequires:    perl(Cwd)
BuildRequires:    perl(Data::Dumper)
BuildRequires:    perl(English)
BuildRequires:    perl(Env)
BuildRequires:    perl(Errno)
BuildRequires:    perl(Exporter)
BuildRequires:    perl(Fcntl)
BuildRequires:    perl(File::Basename)
BuildRequires:    perl(File::Copy)
BuildRequires:    perl(File::Find)
BuildRequires:    perl(File::Spec)
BuildRequires:    perl(File::Spec::Functions)
BuildRequires:    perl(File::Temp)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IO::File)
BuildRequires:    perl(IO::Handle)
BuildRequires:    perl(IO::Select)
BuildRequires:    perl(IO::Socket)
BuildRequires:    perl(IO::Socket::INET)
BuildRequires:    perl(IPC::Open3)
BuildRequires:    perl(lib)
BuildRequires:    perl(Memoize)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(Socket)
BuildRequires:    perl(strict)
BuildRequires:    perl(Symbol)
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Term::ANSIColor)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(Time::HiRes)
BuildRequires:    perl(Time::localtime)
BuildRequires:    perl(warnings)
# for running some openssl tests rhbz#1189180
BuildRequires:    openssl openssl-devel

%if %{with debug}
BuildRequires:    valgrind-devel
%endif

Requires:         bash coreutils grep

Requires:         %{name}-common%{?_isa} = %{sameevr}

%if %{with clibrary}
# Explicit EVR requirement for -libs is needed for RHBZ#1406320
Requires:         %{name}-libs%{?_isa} = %{sameevr}
%else
# If not built with client library in this package, use connector-c
Requires:         mariadb-connector-c >= 3.0
%endif

%if %{with mysql_names}
Provides:         mysql = %{sameevr}
Provides:         mysql%{?_isa} = %{sameevr}
Provides:         mysql-compat-client = %{sameevr}
Provides:         mysql-compat-client%{?_isa} = %{sameevr}
%endif

Suggests:         %{name}-server%{?_isa} = %{sameevr}

Conflicts:        community-mysql

%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::|wsrep)
%global __provides_exclude_from ^(%{_datadir}/(mysql|mysql-test)/.*|%{_libdir}/%{pkg_name}/plugin/.*\\.so)$

%{!?_licensedir:%global license %doc}

%description
MariaDB is a community developed fork from MySQL - a multi-user, multi-threaded
SQL database server. It is a client/server implementation consisting of
a server daemon (mariadbd) and many different client programs and libraries.
The base package contains the standard MariaDB/MySQL client programs and
utilities.


%if %{with clibrary}
%package          libs
Summary:          The shared libraries required for MariaDB/MySQL clients
Requires:         %{name}-common%{?_isa} = %{sameevr}
%if %{with mysql_names}
Provides:         mysql-libs = %{sameevr}
Provides:         mysql-libs%{?_isa} = %{sameevr}
%endif

%description      libs
The mariadb-libs package provides the essential shared libraries for any
MariaDB/MySQL client program or interface. You will need to install this
package to use any other MariaDB package or any clients that need to connect
to a MariaDB/MySQL server.
%endif


# At least main config file /etc/my.cnf is shared for client and server part
# Since we want to support combination of different client and server
# implementations (e.g. mariadb library and community-mysql server),
# we need the config file(s) to be in a separate package, so no extra packages
# are pulled, because these would likely conflict.
# More specifically, the dependency on the main configuration file (/etc/my.cnf)
# is supposed to be defined as Requires: /etc/my.cnf rather than requiring
# a specific package, so installer app can choose whatever package fits to
# the transaction.
%if %{with config}
%package          config
Summary:          The config files required by server and client

%description      config
The package provides the config file my.cnf and my.cnf.d directory used by any
MariaDB or MySQL program. You will need to install this package to use any
other MariaDB or MySQL package if the config files are not provided in the
package itself.
%endif


%if %{with common}
%package          common
Summary:          The shared files required by server and client
Requires:         %{_sysconfdir}/my.cnf


%if %{without clibrary}
Obsoletes: %{name}-libs <= %{sameevr}
%endif

%description      common
The package provides the essential shared files for any MariaDB program.
You will need to install this package to use any other MariaDB package.
%endif


%if %{with errmsg}
%package          errmsg
Summary:          The error messages files required by server and embedded
Requires:         %{name}-common%{?_isa} = %{sameevr}

%description      errmsg
The package provides error messages files for the MariaDB daemon and the
embedded server. You will need to install this package to use any of those
MariaDB packages.
%endif


%if %{with galera}
%package          server-galera
Summary:          The configuration files and scripts for galera replication
Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{name}-server%{?_isa} = %{sameevr}
Requires:         galera >= 25.3.3
Requires(post):   libselinux-utils
Requires(post):   policycoreutils-python-utils
# wsrep requirements
Requires:         lsof
# Default wsrep_sst_method
Requires:         rsync

%description      server-galera
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mariadbd)
and many different client programs and libraries. This package contains
added files to allow MariaDB server to operate as a Galera cluster
member. MariaDB is a community developed fork originally from MySQL.
%endif


%package          server
Summary:          The MariaDB server and related files

# note: no version here = %%{version}-%%{release}
%if %{with mysql_names}
Requires:         mysql-compat-client%{?_isa}
Requires:         mysql%{?_isa}
Recommends:       %{name}%{?_isa}
%else
Requires:         %{name}%{?_isa}
%endif
Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{name}-errmsg%{?_isa} = %{sameevr}
Recommends:       %{name}-server-utils%{?_isa} = %{sameevr}
Recommends:       %{name}-backup%{?_isa} = %{sameevr}
%{?with_cracklib:Recommends:   %{name}-cracklib-password-check%{?_isa} = %{sameevr}}
%{?with_gssapi:Recommends:     %{name}-gssapi-server%{?_isa} = %{sameevr}}
%{?with_rocksdb:Suggests:      %{name}-rocksdb-engine%{?_isa} = %{sameevr}}
%{?with_sphinx:Suggests:       %{name}-sphinx-engine%{?_isa} = %{sameevr}}
%{?with_oqgraph:Suggests:      %{name}-oqgraph-engine%{?_isa} = %{sameevr}}
%{?with_connect:Suggests:      %{name}-connect-engine%{?_isa} = %{sameevr}}
%{?with_pam:Suggests:          %{name}-pam%{?_isa} = %{sameevr}}

Suggests:         mytop
Suggests:         logrotate

Requires:         %{_sysconfdir}/my.cnf
Requires:         %{_sysconfdir}/my.cnf.d

%if %require_mysql_selinux
Requires:         (mysql-selinux if selinux-policy-targeted)
%endif

# for fuser in mysql-check-socket
Requires:         psmisc

Requires:         coreutils
Requires(pre):    /usr/sbin/useradd
# We require this to be present for %%{_tmpfilesdir}
Requires:         systemd
# Make sure it's there when scriptlets run, too
%{?systemd_requires}
# RHBZ#1496131; use 'iproute' instead of 'net-tools'
Requires:         iproute
%if %{with mysql_names}
Provides:         mysql-server = %{sameevr}
Provides:         mysql-server%{?_isa} = %{sameevr}
Provides:         mysql-compat-server = %{sameevr}
Provides:         mysql-compat-server%{?_isa} = %{sameevr}
%endif
Conflicts:        community-mysql-server

# Bench subpackage has been deprecated in F32
Obsoletes: %{name}-bench <= %{sameevr}

Obsoletes:      %{name}-tokudb-engine <= %{sameevr}

%description      server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mariadbd)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed fork from MySQL.


%if %{with oqgraph}
%package          oqgraph-engine
Summary:          The Open Query GRAPH engine for MariaDB
Requires:         %{name}-server%{?_isa} = %{sameevr}
# boost and Judy required for oograph
BuildRequires:    boost-devel Judy-devel

%description      oqgraph-engine
The package provides Open Query GRAPH engine (OQGRAPH) as plugin for MariaDB
database server. OQGRAPH is a computation engine allowing hierarchies and more
complex graph structures to be handled in a relational fashion. In a nutshell,
tree structures and friend-of-a-friend style searches can now be done using
standard SQL syntax, and results joined onto other tables.
%endif


%if %{with connect}
%package          connect-engine
Summary:          The CONNECT storage engine for MariaDB
Requires:         %{name}-server%{?_isa} = %{sameevr}

# As per https://jira.mariadb.org/browse/MDEV-21450
BuildRequires:    libxml2-devel

%description      connect-engine
The CONNECT storage engine enables MariaDB to access external local or
remote data (MED). This is done by defining tables based on different data
types, in particular files in various formats, data extracted from other DBMS
or products (such as Excel), or data retrieved from the environment
(for example DIR, WMI, and MAC tables).
%endif


%if %{with backup}
%package          backup
Summary:          The mariabackup tool for physical online backups
Requires:         %{name}-server%{?_isa} = %{sameevr}
BuildRequires:    libarchive-devel

%description      backup
MariaDB Backup is an open source tool provided by MariaDB for performing
physical online backups of InnoDB, Aria and MyISAM tables.
For InnoDB, "hot online" backups are possible.
%endif


%if %{with rocksdb}
%package          rocksdb-engine
Summary:          The RocksDB storage engine for MariaDB
Requires:         %{name}-server%{?_isa} = %{sameevr}
Provides:         bundled(rocksdb)

%description      rocksdb-engine
The RocksDB storage engine is used for high performance servers on SSD drives.
%endif


%if %{with cracklib}
%package          cracklib-password-check
Summary:          The password strength checking plugin
Requires:         %{name}-server%{?_isa} = %{sameevr}
BuildRequires:    cracklib-dicts cracklib-devel
Requires:         cracklib-dicts

%description      cracklib-password-check
CrackLib is a password strength checking library. It is installed by default
in many Linux distributions and is invoked automatically (by pam_cracklib.so)
whenever the user login password is modified.
Now, with the cracklib_password_check password validation plugin, one can
also use it to check MariaDB account passwords.
%endif


%if %{with gssapi}
%package          gssapi-server
Summary:          GSSAPI authentication plugin for server
Requires:         %{name}-server%{?_isa} = %{sameevr}
BuildRequires:    krb5-devel

%description      gssapi-server
GSSAPI authentication server-side plugin for MariaDB for passwordless login.
This plugin includes support for Kerberos on Unix.
%endif


%if %{with pam}
%package          pam
Summary:          PAM authentication plugin for the MariaDB server

Requires:         %{name}-server%{?_isa} = %{sameevr}
# This subpackage NEED the 'mysql' user/group (created during mariadb-server %%pre) to be available prior installation
Requires(pre):    %{name}-server%{?_isa} = %{sameevr}

BuildRequires:    pam-devel

%description      pam
PAM authentication server-side plugin for MariaDB.
%endif


%if %{with sphinx}
%package          sphinx-engine
Summary:          The Sphinx storage engine for MariaDB
Requires:         %{name}-server%{?_isa} = %{sameevr}
BuildRequires:    sphinx libsphinxclient libsphinxclient-devel
Requires:         sphinx libsphinxclient

%description      sphinx-engine
The Sphinx storage engine for MariaDB.
%endif


%if %{with s3}
%package          s3-engine
Summary:          The S3 storage engine for MariaDB
Requires:         %{name}-server%{?_isa} = %{sameevr}

BuildRequires:    curl-devel

%description      s3-engine
The S3 read only storage engine allows archiving MariaDB tables in Amazon S3,
or any third-party public or private cloud that implements S3 API,
but still have them accessible for reading in MariaDB.
%endif


%package          server-utils
Summary:          Non-essential server utilities for MariaDB/MySQL applications
Requires:         %{name}-server%{?_isa} = %{sameevr}
%if %{with mysql_names}
Provides:         mysql-perl = %{sameevr}
%endif
Conflicts:        community-mysql-server
# mysqlhotcopy needs DBI/DBD support
Requires:         perl(DBI) perl(DBD::MariaDB)

%description      server-utils
This package contains all non-essential server utilities and scripts for
managing databases. It also contains all utilities requiring Perl and it is
the only MariaDB sub-package, except test subpackage, that depends on Perl.


%if %{with devel}
%package          devel
Summary:          Files for development of MariaDB/MySQL applications
%{?with_clibrary:Requires:         %{name}-libs%{?_isa} = %{sameevr}}
Requires:         openssl-devel
%if %{without clibrary}
Requires:         mariadb-connector-c-devel >= 3.0
%endif
%if %{with mysql_names}
Provides:         mysql-devel = %{sameevr}
Provides:         mysql-devel%{?_isa} = %{sameevr}
%endif
Conflicts:        community-mysql-devel

%description      devel
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed branch of MySQL.
%if %{with clibrary}
This package contains everything needed for developing MariaDB/MySQL client
and server plugins and applications.
%else
This package contains everything needed for developing MariaDB/MySQL server
plugins and applications. For developing client applications, use
mariadb-connector-c package.
%endif
%endif


%if %{with embedded}
%package          embedded
Summary:          MariaDB as an embeddable library
Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{name}-errmsg%{?_isa} = %{sameevr}
%if %{with mysql_names}
Provides:         mysql-embedded = %{sameevr}
Provides:         mysql-embedded%{?_isa} = %{sameevr}
%endif

%description      embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed fork from MySQL.


%package          embedded-devel
Summary:          Development files for MariaDB as an embeddable library
Requires:         %{name}-embedded%{?_isa} = %{sameevr}
Requires:         %{name}-devel%{?_isa} = %{sameevr}
# embedded-devel should require libaio-devel (rhbz#1290517)
Requires:         libaio-devel
%if %{with mysql_names}
Provides:         mysql-embedded-devel = %{sameevr}
Provides:         mysql-embedded-devel%{?_isa} = %{sameevr}
%endif
Conflicts:        community-mysql-embedded-devel

%description      embedded-devel
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed fork from MySQL.
This package contains files needed for developing and testing with
the embedded version of the MariaDB server.
%endif


%if %{with test}
%package          test
Summary:          The test suite distributed with MariaDB
Requires:         %{name}%{?_isa} = %{sameevr}
Requires:         %{name}-common%{?_isa} = %{sameevr}
Requires:         %{name}-server%{?_isa} = %{sameevr}
Requires:         patch
Requires:         perl(Env)
Requires:         perl(Exporter)
Requires:         perl(Fcntl)
Requires:         perl(File::Temp)
Requires:         perl(Data::Dumper)
Requires:         perl(Getopt::Long)
Requires:         perl(IPC::Open3)
Requires:         perl(Socket)
Requires:         perl(Sys::Hostname)
Requires:         perl(Test::More)
Requires:         perl(Time::HiRes)
Conflicts:        %{?fedora:community-}mysql-test
%if %{with mysql_names}
Provides:         mysql-test = %{sameevr}
Provides:         mysql-test%{?_isa} = %{sameevr}
%endif

%description      test
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed fork from MySQL.
This package contains the regression test suite distributed with the MariaDB
sources.
%endif


%prep
%setup -q -n mariadb-%{version}

# Remove JAR files that upstream puts into tarball
find . -name "*.jar" -type f -exec rm --verbose -f {} \;
# Remove testsuite for the mariadb-connector-c
rm -rf libmariadb/unittest
%if %{without rocksdb}
rm -r storage/rocksdb/
%endif

%patch4 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch15 -p1

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE50} | tee -a mysql-test/unstable-tests

# disable some tests failing on different architectures
%ifarch %{arm} aarch64
cat %{SOURCE51} | tee -a mysql-test/unstable-tests
%endif

cp %{SOURCE2} %{SOURCE3} %{SOURCE10} %{SOURCE11} %{SOURCE12} \
   %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE18} %{SOURCE70} scripts

%if %{with galera}
mkdir selinux
sed 's/mariadb-server-galera/%{name}-server-galera/' %{SOURCE72} > selinux/%{name}-server-galera.te
%endif


# Get version of PCRE, that upstream use
pcre_version=`grep -e "ftp.pcre.org/pub/pcre/pcre2" cmake/pcre.cmake | sed -r "s;[^0123456789]*2-([[:digit:]]+\.[[:digit:]]+)\.[^0123456789]*;\1;"`

# Check if the PCRE version in macro 'pcre_bundled_version', used in Provides: bundled(...), is the same version as upstream actually bundles
%if %{without unbundled_pcre}
if [ %{pcre_bundled_version} != "$pcre_version" ] ; then
  echo "\n Error: Bundled PCRE version is not correct. \n\tBundled version number:%{pcre_bundled_version} \n\tUpstream version number: $pcre_version\n"
  exit 1
fi
%else
# Check if the PCRE version that upstream use, is the same as the one present in system
pcre_system_version=`pkgconf %{_libdir}/pkgconfig/libpcre2-*.pc --modversion 2>/dev/null | head -n 1`

if [ "$pcre_system_version" != "$pcre_version" ] ; then
  echo "\n Warning: Error: Bundled PCRE version is not correct. \n\tSystem version number:$pcre_system_version \n\tUpstream version number: $pcre_version\n"
fi
%endif



%build
# This package has static probe points which do not currently
# work with LTO and result in undefined symbols at link time.
# This is being worked on in upstream GCC
%define _lto_cflags %{nil}

# fail quickly and obviously if user tries to build as root
%if %runselftest
    if [ x"$(id -u)" = "x0" ]; then
        echo "mysql's regression tests fail if run as root."
        echo "If you really need to build the RPM as root, use"
        echo "--nocheck to skip the regression tests."
        exit 1
    fi
%endif

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.
%cmake . \
         -DBUILD_CONFIG=mysql_release \
         -DFEATURE_SET="community" \
         -DINSTALL_LAYOUT=RPM \
         -DDAEMON_NAME="%{daemon_name}" \
         -DDAEMON_NO_PREFIX="%{daemon_no_prefix}" \
         -DLOG_LOCATION="%{logfile}" \
         -DPID_FILE_DIR="%{pidfiledir}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DRPM="openeuler1" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
         -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
         -DINSTALL_DOCDIR="share/doc/%{_pkgdocdirname}" \
         -DINSTALL_DOCREADMEDIR="share/doc/%{_pkgdocdirname}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_INFODIR=share/info \
         -DINSTALL_LIBDIR="%{_lib}" \
         -DINSTALL_MANDIR=share/man \
         -DINSTALL_MYSQLSHAREDIR=share/%{pkg_name} \
         -DINSTALL_MYSQLTESTDIR=%{?with_test:share/mysql-test}%{!?with_test:} \
         -DINSTALL_PLUGINDIR="%{_lib}/%{pkg_name}/plugin" \
         -DINSTALL_SBINDIR=libexec \
         -DINSTALL_SCRIPTDIR=bin \
         -DINSTALL_SUPPORTFILESDIR=share/%{pkg_name} \
         -DINSTALL_PCDIR=%{_lib}/pkgconfig \
         -DMYSQL_DATADIR="%{dbdatadir}" \
         -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
         -DTMPDIR=/var/tmp \
         -DGRN_DATA_DIR=share/%{name}-server/groonga \
         -DGROONGA_NORMALIZER_MYSQL_PROJECT_NAME=%{name}-server/groonga-normalizer-mysql \
         -DENABLED_LOCAL_INFILE=ON \
         -DENABLE_DTRACE=ON \
         -DSECURITY_HARDENED=ON \
         -DWITH_WSREP=%{?with_galera:ON}%{!?with_galera:OFF} \
         -DWITH_INNODB_DISALLOW_WRITES=%{?with_galera:ON}%{!?with_galera:OFF} \
         -DWITH_EMBEDDED_SERVER=%{?with_embedded:ON}%{!?with_embedded:OFF} \
         -DWITH_MARIABACKUP=%{?with_backup:ON}%{!?with_backup:NO} \
         -DWITH_UNIT_TESTS=%{?with_test:ON}%{!?with_test:NO} \
         -DCONC_WITH_SSL=%{?with_clibrary:ON}%{!?with_clibrary:NO} \
         -DWITH_SSL=system \
         -DWITH_ZLIB=system \
         -DLZ4_LIBS=%{_libdir}/liblz4.so \
         -DLZ4_LIBS=%{?with_lz4:%{_libdir}/liblz4.so}%{!?with_lz4:} \
         -DWITH_INNODB_LZ4=%{?with_lz4:ON}%{!?with_lz4:OFF} \
         -DWITH_ROCKSDB_LZ4=%{?with_lz4:ON}%{!?with_lz4:OFF} \
         -DPLUGIN_MROONGA=%{?with_mroonga:DYNAMIC}%{!?with_mroonga:NO} \
         -DPLUGIN_OQGRAPH=%{?with_oqgraph:DYNAMIC}%{!?with_oqgraph:NO} \
         -DPLUGIN_CRACKLIB_PASSWORD_CHECK=%{?with_cracklib:DYNAMIC}%{!?with_cracklib:NO} \
         -DPLUGIN_ROCKSDB=%{?with_rocksdb:DYNAMIC}%{!?with_rocksdb:NO} \
         -DPLUGIN_SPHINX=%{?with_sphinx:DYNAMIC}%{!?with_sphinx:NO} \
         -DPLUGIN_CONNECT=%{?with_connect:DYNAMIC}%{!?with_connect:NO} \
         -DPLUGIN_S3=%{?with_s3:DYNAMIC}%{!?with_s3:NO} \
         -DPLUGIN_COLUMNSTORE=NO \
         -DPLUGIN_CLIENT_ED25519=OFF \
         -DPYTHON_SHEBANG=%{python_path} \
         -DPLUGIN_CACHING_SHA2_PASSWORD=%{?with_clibrary:DYNAMIC}%{!?with_clibrary:OFF} \
         -DPLUGIN_AWS_KEY_MANAGEMENT=NO \
         -DCONNECT_WITH_MONGO=OFF \
         -DCONNECT_WITH_JDBC=OFF \
%{?with_debug: -DCMAKE_BUILD_TYPE=Debug -DWITH_ASAN=OFF -DWITH_INNODB_EXTRA_DEBUG=ON -DWITH_VALGRIND=ON}


CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"

%if %{with debug}
# Override all optimization flags when making a debug build
# -D_FORTIFY_SOURCE requires optimizations enabled. Disable the fortify.
CFLAGS=`echo "$CFLAGS" | sed -r 's/-D_FORTIFY_SOURCE=[012]/-D_FORTIFY_SOURCE=0/'`
CFLAGS=`echo "$CFLAGS" | sed -r 's/-O[0123]//'`

CFLAGS="$CFLAGS -O0 -g -D_FORTIFY_SOURCE=0"
%endif # debug

CXXFLAGS="$CFLAGS"
CPPFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS CPPFLAGS

%make_build -j7

# build selinux policy
%if %{with galera}
pushd selinux
make -f /usr/share/selinux/devel/Makefile %{name}-server-galera.pp
%endif



%install
%make_install

# multilib header support #1625157
for header in mysql/server/my_config.h mysql/server/private/config.h; do
%multilib_fix_c_header --file %{_includedir}/$header
done

ln -s mysql_config.1.gz %{buildroot}%{_mandir}/man1/mariadb_config.1.gz

# multilib support for shell scripts
# we only apply this to known Red Hat multilib arches, per bug #181335
if [ %multilib_capable ]
then
mv %{buildroot}%{_bindir}/mysql_config %{buildroot}%{_bindir}/mysql_config-%{__isa_bits}
install -p -m 0755 %{_builddir}/mariadb-%{version}/scripts/mysql_config_multilib %{buildroot}%{_bindir}/mysql_config
# Copy manual page for multilib mysql_config; https://jira.mariadb.org/browse/MDEV-11961
ln -s mysql_config.1 %{buildroot}%{_mandir}/man1/mysql_config-%{__isa_bits}.1
fi

%if %{without clibrary}
# Client part should be included in package 'mariadb-connector-c'
rm %{buildroot}%{_libdir}/pkgconfig/libmariadb.pc
%endif

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also %%{name}-file-contents.patch)
install -p -m 644 %{_builddir}/mariadb-%{version}/Docs/INFO_SRC %{buildroot}%{_libdir}/%{pkg_name}/
install -p -m 644 %{_builddir}/mariadb-%{version}/Docs/INFO_BIN %{buildroot}%{_libdir}/%{pkg_name}/
rm -r %{buildroot}%{_datadir}/doc/%{_pkgdocdirname}/MariaDB-server-%{version}/

# Logfile creation
mkdir -p %{buildroot}%{logfiledir}
chmod 0750 %{buildroot}%{logfiledir}
touch %{buildroot}%{logfile}

# current setting in my.cnf is to use /var/run/mariadb for creating pid file,
# however since my.cnf is not updated by RPM if changed, we need to create mysqld
# as well because users can have odd settings in their /etc/my.cnf
mkdir -p %{buildroot}%{pidfiledir}
install -p -m 0755 -d %{buildroot}%{dbdatadir}

%if %{with config}
install -D -p -m 0644 %{_builddir}/mariadb-%{version}/scripts/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
%else
rm %{_builddir}/mariadb-%{version}/scripts/my.cnf
%endif

# use different config file name for each variant of server (mariadb / mysql)
mv %{buildroot}%{_sysconfdir}/my.cnf.d/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf

# Remove upstream SysV init script and a symlink to that, we use systemd
rm %{buildroot}%{_libexecdir}/rcmysql
# Remove upstream Systemd service files
rm -r %{buildroot}%{_datadir}/%{pkg_name}/systemd
# Our downstream Systemd service file have set aliases to the "mysql" names in the [Install] section.
# They can be enabled / disabled by "systemctl enable / diable <service_name>"
rm %{buildroot}%{_unitdir}/{mysql,mysqld}.service

# install systemd unit files and scripts for handling server startup
install -D -p -m 644 %{_builddir}/mariadb-%{version}/scripts/mysql.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 644 %{_builddir}/mariadb-%{version}/scripts/mysql@.service %{buildroot}%{_unitdir}/%{daemon_name}@.service

# helper scripts for service starting
install -p -m 755 %{_builddir}/mariadb-%{version}/scripts/mariadb-prepare-db-dir %{buildroot}%{_libexecdir}/mariadb-prepare-db-dir
install -p -m 755 %{_builddir}/mariadb-%{version}/scripts/mariadb-check-socket %{buildroot}%{_libexecdir}/mariadb-check-socket
install -p -m 755 %{_builddir}/mariadb-%{version}/scripts/mariadb-check-upgrade %{buildroot}%{_libexecdir}/mariadb-check-upgrade
install -p -m 644 %{_builddir}/mariadb-%{version}/scripts/mariadb-scripts-common %{buildroot}%{_libexecdir}/mariadb-scripts-common

# Install downstream version of tmpfiles
install -D -p -m 0644 %{_builddir}/mariadb-%{version}/scripts/mariadb.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{name}.conf
%if 0%{?mysqld_pid_dir:1}
echo "d %{pidfiledir} 0755 mysql mysql -" >>%{buildroot}%{_tmpfilesdir}/%{name}.conf
%endif

# install additional galera selinux policy
%if %{with galera}
install -p -m 644 -D selinux/%{name}-server-galera.pp %{buildroot}%{_datadir}/selinux/packages/%{name}/%{name}-server-galera.pp
%endif

%if %{with test}
# mysql-test includes one executable that doesn't belong under /usr/share, so move it and provide a symlink
mv %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir}
ln -s ../../../../../bin/my_safe_process %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process
# Provide symlink expected by RH QA tests
ln -s unstable-tests %{buildroot}%{_datadir}/mysql-test/rh-skipped-tests.list
%endif


# Client that uses libmysqld embedded server.
# Pretty much like normal mysql command line client, but it doesn't require a running mariadb server.
%{?with_embedded:rm %{buildroot}%{_bindir}/{mariadb-,mysql_}embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_,mariadb-}embedded.1*
# Static libraries
rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_datadir}/%{pkg_name}/binary-configure
rm %{buildroot}%{_datadir}/%{pkg_name}/magic
rm %{buildroot}%{_datadir}/%{pkg_name}/mysql.server
rm %{buildroot}%{_datadir}/%{pkg_name}/mysqld_multi.server

# Binary for monitoring MySQL performance
# Shipped as a standalone package in Fedora
rm %{buildroot}%{_bindir}/mytop
rm %{buildroot}%{_mandir}/man1/mytop.1*

# Should be shipped with mariadb-connector-c
rm %{buildroot}%{_mandir}/man1/mariadb_config.1*

# put logrotate script where it needs to be
mkdir -p %{buildroot}%{logrotateddir}
mv %{buildroot}%{_datadir}/%{pkg_name}/mysql-log-rotate %{buildroot}%{logrotateddir}/%{daemon_name}
chmod 644 %{buildroot}%{logrotateddir}/%{daemon_name}

# for compatibility with upstream RPMs, create mysqld symlink in sbin
mkdir -p %{buildroot}%{_sbindir}
ln -s %{_libexecdir}/mysqld %{buildroot}%{_sbindir}/mysqld
ln -s %{_libexecdir}/mariadbd %{buildroot}%{_sbindir}/mariadbd

# copy additional docs into build tree so %%doc will find them
install -p -m 0644 %{SOURCE6} %{basename:%{SOURCE6}}
install -p -m 0644 %{SOURCE16} %{basename:%{SOURCE16}}
install -p -m 0644 %{SOURCE71} %{basename:%{SOURCE71}}

# install galera config file
%if %{with galera}
sed -i -r 's|^wsrep_provider=none|wsrep_provider=%{_libdir}/galera/libgalera_smm.so|' %{_builddir}/mariadb-%{version}/support-files/wsrep.cnf
install -p -m 0644 %{_builddir}/mariadb-%{version}/support-files/wsrep.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/galera.cnf
%endif
# install the clustercheck script
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/sysconfig/clustercheck
install -p -m 0755 %{_builddir}/mariadb-%{version}/scripts/clustercheck %{buildroot}%{_bindir}/clustercheck

# remove duplicate logrotate script
rm %{buildroot}%{logrotateddir}/mysql
# Remove AppArmor files
rm -r %{buildroot}%{_datadir}/%{pkg_name}/policy/apparmor

# Buildroot does not have symlink /lib64 --> /usr/lib64
mv %{buildroot}/%{_lib}/security %{buildroot}%{_libdir}

# Disable plugins
%if %{with gssapi}
sed -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%endif
%if %{with cracklib}
sed -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%endif

# Fix Galera Replication config file
#   The replication requires cluster address upon startup (which is end-user specific).
#   Disable it entirely, rather than have it failing out-of-the-box.
%if %{with galera}
sed -i 's/^wsrep_on=1/wsrep_on=0/' %{buildroot}%{_sysconfdir}/my.cnf.d/galera.cnf
%endif

%if %{without embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
%endif


%if %{without clibrary}
rm %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
# Client library and links
rm %{buildroot}%{_libdir}/libmariadb.so.*
unlink %{buildroot}%{_libdir}/libmysqlclient.so
unlink %{buildroot}%{_libdir}/libmysqlclient_r.so
unlink %{buildroot}%{_libdir}/libmariadb.so
# Client plugins
rm %{buildroot}%{_libdir}/%{pkg_name}/plugin/{dialog.so,mysql_clear_password.so,sha256_password.so}
%if %{with gssapi}
rm %{buildroot}%{_libdir}/%{pkg_name}/plugin/auth_gssapi_client.so
%endif
%endif

%if %{without clibrary} || %{without devel}
rm %{buildroot}%{_bindir}/mysql_config*
rm %{buildroot}%{_bindir}/mariadb_config
rm %{buildroot}%{_bindir}/mariadb-config
rm %{buildroot}%{_mandir}/man1/mysql_config*.1*
%endif

%if %{without clibrary} && %{with devel}
# This files are already included in mariadb-connector-c
rm %{buildroot}%{_includedir}/mysql/mysql_version.h
rm %{buildroot}%{_includedir}/mysql/{errmsg.h,ma_list.h,ma_pvio.h,mariadb_com.h,\
mariadb_ctype.h,mariadb_dyncol.h,mariadb_stmt.h,mariadb_version.h,ma_tls.h,mysqld_error.h,mysql.h,mariadb_rpl.h}
rm -r %{buildroot}%{_includedir}/mysql/{mariadb,mysql}
%endif

%if %{without devel}
rm -r %{buildroot}%{_includedir}/mysql
rm %{buildroot}%{_datadir}/aclocal/mysql.m4
rm %{buildroot}%{_libdir}/pkgconfig/mariadb.pc
%if %{with clibrary}
rm %{buildroot}%{_libdir}/libmariadb*.so
unlink %{buildroot}%{_libdir}/libmysqlclient.so
unlink %{buildroot}%{_libdir}/libmysqlclient_r.so
%endif
%endif

%if %{without client}
rm %{buildroot}%{_bindir}/msql2mysql
rm %{buildroot}%{_bindir}/{mysql,mariadb}
rm %{buildroot}%{_bindir}/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}
rm %{buildroot}%{_bindir}/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}

rm %{buildroot}%{_mandir}/man1/msql2mysql.1*
rm %{buildroot}%{_mandir}/man1/{mysql,mariadb}.1*
rm %{buildroot}%{_mandir}/man1/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}.1*
rm %{buildroot}%{_mandir}/man1/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}.1*
%endif

%if %{without config}
rm %{buildroot}%{_sysconfdir}/my.cnf
%endif

%if %{without common}
rm -r %{buildroot}%{_datadir}/%{pkg_name}/charsets
%endif

%if %{without errmsg}
rm %{buildroot}%{_datadir}/%{pkg_name}/errmsg-utf8.txt
rm -r %{buildroot}%{_datadir}/%{pkg_name}/{english,czech,danish,dutch,estonian,\
french,german,greek,hungarian,italian,japanese,korean,norwegian,norwegian-ny,\
polish,portuguese,romanian,russian,serbian,slovak,spanish,swedish,ukrainian,hindi}
%endif

%if %{without test}
%if %{with embedded}
rm %{buildroot}%{_bindir}/{mysql_client_test_embedded,mysqltest_embedded}
rm %{buildroot}%{_bindir}/{mariadb-client-test-embedded,mariadb-test-embedded}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
%endif # embedded
rm %{buildroot}%{_bindir}/{mysql_client_test,mysqltest}
rm %{buildroot}%{_bindir}/{mariadb-client-test,mariadb-test}
rm %{buildroot}%{_mandir}/man1/{mysql_client_test,mysqltest,my_safe_process}.1*
rm %{buildroot}%{_mandir}/man1/{mariadb-client-test,mariadb-test}.1*
rm %{buildroot}%{_mandir}/man1/{mysql-test-run,mysql-stress-test}.pl.1*
rm %{buildroot}/suite/plugins/pam/mariadb_mtr
rm %{buildroot}/suite/plugins/pam/pam_mariadb_mtr.so
%endif

%if %{without galera}
rm %{buildroot}%{_sysconfdir}/sysconfig/clustercheck
rm %{buildroot}%{_bindir}/{clustercheck,galera_new_cluster}
rm %{buildroot}%{_bindir}/galera_recovery
rm %{buildroot}%{_datadir}/%{pkg_name}/systemd/use_galera_new_cluster.conf
%endif

%if %{without rocksdb}
rm %{buildroot}%{_mandir}/man1/{mysql_,mariadb-}ldb.1*
rm %{buildroot}%{_mandir}/man1/myrocks_hotbackup.1*
%endif

%if %{without backup}
rm %{buildroot}%{_mandir}/man1/maria{,db-}backup.1*
rm %{buildroot}%{_mandir}/man1/mbstream.1*
%endif

%if %{without s3}
rm %{buildroot}%{_mandir}/man1/aria_s3_copy.1*
%endif

%check
%if %{with test}
%if %runselftest
# hack to let 32- and 64-bit tests run concurrently on same build machine
export MTR_PARALLEL=1
export MTR_BUILD_THREAD=$(( $(date +%s) % 1100 ))

(
  set -ex
  cd %{buildroot}%{_datadir}/mysql-test

  export common_testsuite_arguments=" --parallel=auto --force --retry=2 --suite-timeout=900 --testcase-timeout=30 --mysqld=--binlog-format=mixed --force-restart --shutdown-timeout=60 --max-test-fail=5 "

  # If full testsuite has already been run on this version and we don't explicitly want the full testsuite to be run
  if [[ "%{last_tested_version}" == "%{version}" ]] && [[ %{force_run_testsuite} -eq 0 ]]
  then
    # in further rebuilds only run the basic "main" suite (~800 tests)
    echo "running only base testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments --ssl --suite=main --mem --skip-test-list=unstable-tests
  fi

  # If either this version wasn't marked as tested yet or I explicitly want to run the testsuite, run everything we have (~4000 test)
  if [[ "%{last_tested_version}" != "%{version}" ]] || [[ %{force_run_testsuite} -ne 0 ]]
  then
    echo "running advanced testsuite"
    perl ./mysql-test-run.pl $common_testsuite_arguments --ssl --big-test --skip-test=spider \
    %if %{ignore_testsuite_result}
      --max-test-fail=9999 || :
    %else
      --skip-test-list=unstable-tests
    %endif
    # Second run for the SPIDER suites that fail with SCA (ssl self signed certificate)
    perl ./mysql-test-run.pl $common_testsuite_arguments --skip-ssl --big-test --mem --suite=spider,spider/bg,spider/bugfix,spider/handler \
    %if %{ignore_testsuite_result}
      --max-test-fail=999 || :
    %endif
  # blank line
  fi

  # There might be a dangling symlink left from the testing, remove it to not be installed
  rm -rf ./var
)

# NOTE: the Spider SE has 2 more hidden testsuites "oracle" and "oracle2".
#       however, all of the tests fail with: "failed: 12521: Can't use wrapper 'oracle' for SQL connection"

%endif
%endif



%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{mysqluserhome} -s /sbin/nologin \
  -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :

%if %{with galera}
%post server-galera
# Allow ports needed for the replication:
# https://mariadb.com/kb/en/library/configuring-mariadb-galera-cluster/#network-ports
#   Galera Replication Port
semanage port -a -t mysqld_port_t -p tcp 4567 >/dev/null 2>&1 || :
semanage port -a -t mysqld_port_t -p udp 4567 >/dev/null 2>&1 || :
#   IST Port
semanage port -a -t mysqld_port_t -p tcp 4568 >/dev/null 2>&1 || :
#   SST Port
semanage port -a -t mysqld_port_t -p tcp 4444 >/dev/null 2>&1 || :

semodule -i %{_datadir}/selinux/packages/%{name}/%{name}-server-galera.pp >/dev/null 2>&1 || :
%endif

%post server
%systemd_post %{daemon_name}.service

%preun server
%systemd_preun %{daemon_name}.service

%if %{with galera}
%postun server-galera
if [ $1 -eq 0 ]; then
    semodule -r %{name}-server-galera 2>/dev/null || :
fi
%endif

%postun server
%systemd_postun_with_restart %{daemon_name}.service



%if %{with client}
%files
%{_bindir}/msql2mysql
%{_bindir}/{mysql,mariadb}
%{_bindir}/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}
%{_bindir}/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/{mysql,mariadb}.1*
%{_mandir}/man1/mysql{access,admin,binlog,check,dump,_find_rows,import,_plugin,show,slap,_waitpid}.1*
%{_mandir}/man1/mariadb-{access,admin,binlog,check,dump,find-rows,import,plugin,show,slap,waitpid}.1*

%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%endif

%if %{with clibrary}
%files libs
%exclude %{_libdir}/{libmysqlclient.so.18,libmariadb.so,libmysqlclient.so,libmysqlclient_r.so}
%{_libdir}/libmariadb.so*
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%endif

%if %{with config}
%files config
# although the default my.cnf contains only server settings, we put it in the
# common package because it can be used for client settings too.
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%endif

%if %{with common}
%files common
%doc %{_datadir}/doc/%{_pkgdocdirname}
%dir %{_datadir}/%{pkg_name}
%{_datadir}/%{pkg_name}/charsets
%if %{with clibrary}
%{_libdir}/%{pkg_name}/plugin/dialog.so
%{_libdir}/%{pkg_name}/plugin/mysql_clear_password.so
%endif
%endif

%if %{with errmsg}
%files errmsg
%{_datadir}/%{pkg_name}/errmsg-utf8.txt
%{_datadir}/%{pkg_name}/english
%lang(cs) %{_datadir}/%{pkg_name}/czech
%lang(da) %{_datadir}/%{pkg_name}/danish
%lang(nl) %{_datadir}/%{pkg_name}/dutch
%lang(et) %{_datadir}/%{pkg_name}/estonian
%lang(fr) %{_datadir}/%{pkg_name}/french
%lang(de) %{_datadir}/%{pkg_name}/german
%lang(el) %{_datadir}/%{pkg_name}/greek
%lang(hi) %{_datadir}/%{pkg_name}/hindi
%lang(hu) %{_datadir}/%{pkg_name}/hungarian
%lang(it) %{_datadir}/%{pkg_name}/italian
%lang(ja) %{_datadir}/%{pkg_name}/japanese
%lang(ko) %{_datadir}/%{pkg_name}/korean
%lang(no) %{_datadir}/%{pkg_name}/norwegian
%lang(no) %{_datadir}/%{pkg_name}/norwegian-ny
%lang(pl) %{_datadir}/%{pkg_name}/polish
%lang(pt) %{_datadir}/%{pkg_name}/portuguese
%lang(ro) %{_datadir}/%{pkg_name}/romanian
%lang(ru) %{_datadir}/%{pkg_name}/russian
%lang(sr) %{_datadir}/%{pkg_name}/serbian
%lang(sk) %{_datadir}/%{pkg_name}/slovak
%lang(es) %{_datadir}/%{pkg_name}/spanish
%lang(sv) %{_datadir}/%{pkg_name}/swedish
%lang(uk) %{_datadir}/%{pkg_name}/ukrainian
%endif

%if %{with galera}
%files server-galera
%doc Docs/README-wsrep
%license LICENSE.clustercheck
%{_bindir}/clustercheck
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%config(noreplace) %{_sysconfdir}/my.cnf.d/galera.cnf
%attr(0640,root,root) %ghost %config(noreplace) %{_sysconfdir}/sysconfig/clustercheck
%{_datadir}/selinux/packages/%{name}/%{name}-server-galera.pp
%endif

%files server

%{_bindir}/aria_{chk,dump_log,ftdump,pack,read_log}
%{_bindir}/mariadb-service-convert
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/my_print_defaults

%{_bindir}/mariadb-conv

%{_bindir}/mysql_{install_db,secure_installation,tzinfo_to_sql}
%{_bindir}/mariadb-{install-db,secure-installation,tzinfo-to-sql}
%{_bindir}/{mysqld_,mariadbd-}safe
%{_bindir}/{mysqld_safe_helper,mariadbd-safe-helper}

%{_bindir}/innochecksum
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%if %{with galera}
# wsrep_sst_common should be moved to /usr/share/mariadb: https://jira.mariadb.org/browse/MDEV-14296
%{_bindir}/wsrep_*
%endif

%config(noreplace) %{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset
%config(noreplace) %{_sysconfdir}/my.cnf.d/spider.cnf

%{_sbindir}/mysqld
%{_sbindir}/mariadbd
%{_libexecdir}/{mysqld,mariadbd}

%{_libdir}/%{pkg_name}/INFO_SRC
%{_libdir}/%{pkg_name}/INFO_BIN
%if %{without common}
%dir %{_datadir}/%{pkg_name}
%endif

%dir %{_libdir}/%{pkg_name}
%dir %{_libdir}/%{pkg_name}/plugin

%{_libdir}/%{pkg_name}/plugin/*
%{?with_oqgraph:%exclude %{_libdir}/%{pkg_name}/plugin/ha_oqgraph.so}
%{?with_connect:%exclude %{_libdir}/%{pkg_name}/plugin/ha_connect.so}
%{?with_cracklib:%exclude %{_libdir}/%{pkg_name}/plugin/cracklib_password_check.so}
%{?with_rocksdb:%exclude %{_libdir}/%{pkg_name}/plugin/ha_rocksdb.so}
%{?with_gssapi:%exclude %{_libdir}/%{pkg_name}/plugin/auth_gssapi.so}
%{?with_sphinx:%exclude %{_libdir}/%{pkg_name}/plugin/ha_sphinx.so}
%{?with_s3:%exclude %{_libdir}/%{pkg_name}/plugin/ha_s3.so}
%if %{with clibrary}
%exclude %{_libdir}/%{pkg_name}/plugin/dialog.so
%exclude %{_libdir}/%{pkg_name}/plugin/mysql_clear_password.so
%endif

# PAM plugin; moved to a standalone sub-package
%exclude %{_libdir}/%{pkg_name}/plugin/{auth_pam_v1.so,auth_pam.so}
%exclude %dir %{_libdir}/%{pkg_name}/plugin/auth_pam_tool_dir
%exclude %{_libdir}/%{pkg_name}/plugin/auth_pam_tool_dir/auth_pam_tool

%{_mandir}/man1/aria_{chk,dump_log,ftdump,pack,read_log}.1*
%{_mandir}/man1/galera_new_cluster.1*
%{_mandir}/man1/galera_recovery.1*
%{_mandir}/man1/mariadb-service-convert.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/my_print_defaults.1*

%{_mandir}/man1/mariadb-conv.1*

%{_mandir}/man1/mysql_{install_db,secure_installation,tzinfo_to_sql}.1*
%{_mandir}/man1/mariadb-{install-db,secure-installation,tzinfo-to-sql}.1*
%{_mandir}/man1/{mysqld_,mariadbd-}safe.1*
%{_mandir}/man1/{mysqld_safe_helper,mariadbd-safe-helper}.1*

%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man8/{mysqld,mariadbd}.8*
%{_mandir}/man1/wsrep_*.1*

%{_mandir}/man1/mysql.server.1*

%{_datadir}/%{pkg_name}/fill_help_tables.sql
%{_datadir}/%{pkg_name}/maria_add_gis_sp.sql
%{_datadir}/%{pkg_name}/maria_add_gis_sp_bootstrap.sql
%{_datadir}/%{pkg_name}/mysql_system_tables.sql
%{_datadir}/%{pkg_name}/mysql_system_tables_data.sql
%{_datadir}/%{pkg_name}/mysql_test_data_timezone.sql
%{_datadir}/%{pkg_name}/mysql_performance_tables.sql
%{_datadir}/%{pkg_name}/mysql_test_db.sql
%if %{with mroonga}
%{_datadir}/%{pkg_name}/mroonga/install.sql
%{_datadir}/%{pkg_name}/mroonga/uninstall.sql
%license %{_datadir}/%{pkg_name}/mroonga/COPYING
%license %{_datadir}/%{pkg_name}/mroonga/AUTHORS
%license %{_datadir}/%{name}-server/groonga-normalizer-mysql/lgpl-2.0.txt
%license %{_datadir}/%{name}-server/groonga/COPYING
%doc %{_datadir}/%{name}-server/groonga-normalizer-mysql/README.md
%doc %{_datadir}/%{name}-server/groonga/README.md
%endif
%if %{with galera}
%{_datadir}/%{pkg_name}/wsrep.cnf
%endif
%{_datadir}/%{pkg_name}/wsrep_notify
%dir %{_datadir}/%{pkg_name}/policy
%dir %{_datadir}/%{pkg_name}/policy/selinux
%{_datadir}/%{pkg_name}/policy/selinux/README
%{_datadir}/%{pkg_name}/policy/selinux/mariadb-server.*
%{_datadir}/%{pkg_name}/policy/selinux/mariadb.*

%{_unitdir}/%{daemon_name}*

%{_libexecdir}/mariadb-prepare-db-dir
%{_libexecdir}/mariadb-check-socket
%{_libexecdir}/mariadb-check-upgrade
%{_libexecdir}/mariadb-scripts-common

%attr(0755,mysql,mysql) %dir %{pidfiledir}
%attr(0755,mysql,mysql) %dir %{dbdatadir}
%attr(0750,mysql,mysql) %dir %{logfiledir}
%attr(0660,mysql,mysql) %config %ghost %verify(not md5 size mtime) %{logfile}
%config(noreplace) %{logrotateddir}/%{daemon_name}

%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf

%if %{with cracklib}
%files cracklib-password-check
%config(noreplace) %{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%{_libdir}/%{pkg_name}/plugin/cracklib_password_check.so
%endif

%if %{with backup}
%files backup
%{_bindir}/maria{,db-}backup
%{_bindir}/mbstream
%{_mandir}/man1/maria{,db-}backup.1*
%{_mandir}/man1/mbstream.1*
%endif

%if %{with rocksdb}
%files rocksdb-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/rocksdb.cnf
%{_bindir}/myrocks_hotbackup
%{_bindir}/{mysql_,mariadb-}ldb
%{_bindir}/sst_dump
%{_libdir}/%{pkg_name}/plugin/ha_rocksdb.so
%{_mandir}/man1/{mysql_,mariadb-}ldb.1*
%{_mandir}/man1/myrocks_hotbackup.1*
%endif

%if %{with gssapi}
%files gssapi-server
%{_libdir}/%{pkg_name}/plugin/auth_gssapi.so
%config(noreplace) %{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%endif

%if %{with pam}
%files pam
%{_libdir}/%{pkg_name}/plugin/{auth_pam_v1.so,auth_pam.so}
%attr(0755,root,root) %dir %{_libdir}/%{pkg_name}/plugin/auth_pam_tool_dir
# SUID-to-root binary. Access MUST be restricted (https://jira.mariadb.org/browse/MDEV-25126)
%attr(4750,root,mysql) %{_libdir}/%{pkg_name}/plugin/auth_pam_tool_dir/auth_pam_tool
%{_libdir}/security/pam_user_map.so
%{_sysconfdir}/security/user_map.conf
%endif

%if %{with sphinx}
%files sphinx-engine
%{_libdir}/%{pkg_name}/plugin/ha_sphinx.so
%endif

%if %{with oqgraph}
%files oqgraph-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/oqgraph.cnf
%{_libdir}/%{pkg_name}/plugin/ha_oqgraph.so
%endif

%if %{with connect}
%files connect-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/connect.cnf
%{_libdir}/%{pkg_name}/plugin/ha_connect.so
%endif

%if %{with s3}
%files s3-engine
%{_bindir}/aria_s3_copy
%{_mandir}/man1/aria_s3_copy.1*
%config(noreplace) %{_sysconfdir}/my.cnf.d/s3.cnf
%{_libdir}/%{pkg_name}/plugin/ha_s3.so
%endif

%files server-utils
# Perl utilities
%{_bindir}/mysql{_convert_table_format,dumpslow,_fix_extensions,hotcopy,_setpermission}
%{_bindir}/mariadb-{convert-table-format,dumpslow,fix-extensions,hotcopy,setpermission}
%{_bindir}/{mysqld_,mariadbd-}multi

%{_mandir}/man1/mysql{_convert_table_format,dumpslow,_fix_extensions,hotcopy,_setpermission}.1*
%{_mandir}/man1/mariadb-{convert-table-format,dumpslow,fix-extensions,hotcopy,setpermission}.1*
%{_mandir}/man1/{mysqld_,mariadbd-}multi.1*
# Utilities that can be used remotely
%{_bindir}/{mysql_,mariadb-}upgrade
%{_bindir}/perror
%{_mandir}/man1/{mysql_,mariadb-}upgrade.1*
%{_mandir}/man1/perror.1*

%if %{with devel}
%files devel
%{_includedir}/*
%{_datadir}/aclocal/mysql.m4
%{_libdir}/pkgconfig/*mariadb.pc
%if %{with clibrary}
%{_libdir}/{libmysqlclient.so.18,libmariadb.so,libmysqlclient.so,libmysqlclient_r.so}
%{_bindir}/mysql_config*
%{_bindir}/mariadb_config*
%{_bindir}/mariadb-config
%{_libdir}/libmariadb.so
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlclient_r.so
%{_mandir}/man1/mysql_config*
%endif
%endif

%if %{with embedded}
%files embedded
%{_libdir}/libmariadbd.so.*

%files embedded-devel
%{_libdir}/libmysqld.so
%{_libdir}/libmariadbd.so
%endif

%if %{with test}
%files test
%if %{with embedded}
%{_bindir}/test-connect-t
%{_bindir}/{mysql_client_test_embedded,mysqltest_embedded}
%{_bindir}/{mariadb-client-test-embedded,mariadb-test-embedded}
%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1*
%{_mandir}/man1/{mariadb-client-test-embedded,mariadb-test-embedded}.1*
%endif
%{_bindir}/{mysql_client_test,mysqltest,mariadb-client-test,mariadb-test}
%{_bindir}/my_safe_process
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%{_mandir}/man1/{mysql_client_test,mysqltest,mariadb-client-test,mariadb-test}.1*
%{_mandir}/man1/my_safe_process.1*
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*
%endif

%changelog
* Fri Jul 23 2021 zhouwenpei<zhouwenpei1@gmail.com> -4:10.5.10-2
- remove unnecessary build require.

* Wed Jun 16 2021 bzhaoop<bzhaojyathousandy@gmail.com> -4:10.5.10-1
- Package init for new version 10.5.10

* Tue Sep 8 2020 lihaotian<lihaotian9@huawei.com> -3:10.3.9-11
- Update the source0 url

* Fri Jul 10 2020 volcanodragon<linfeilong@huawei.com> -3:10.3.9-10
- Rename patch names

* Fri Jul 3 2020 jinzhimin<jinzhimin2@huawei.com> -3:10.3.9-9
- Add conflict between mysql

* Mon Mar 2 2020 steven <steven_ygui@163.com> - 3:10.3.9-8
- Add requires exclude for perls and skip some test cases

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 3:10.3.9-7
- Add mysql_install_db command in service file

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 3:10.3.9-6
- Add my.cnf file

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 3:10.3.9-5
- Repackaged

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 3:10.3.9-4
- Package rewrap and update the release number

* Wed Sep 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 3:10.3.9-3
- Package init

