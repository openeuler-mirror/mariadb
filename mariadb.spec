%global runtest 1

Name:             mariadb
Version:          10.3.9
Release:          9
Epoch:            3
Summary:          One of the most popular database servers
License:          GPLv2 with exceptions and LGPLv2 and BSD
URL:              http://mariadb.org

Source0:          https://downloads.mariadb.org/interstitial/mariadb-%{version}/source/mariadb-%{version}.tar.gz

Patch0001:        disable-some-unstable-testcases.patch
Patch0002:        add-install-db-command.patch
Patch0003:        disable-some-unstable-testcases-2.patch

BuildRequires:    selinux-policy-devel, cmake, gcc-c++
BuildRequires:    systemd, systemd-devel
BuildRequires:    zlib-devel, lz4-devel, libaio-devel, libedit-devel, ncurses-devel
BuildRequires:    systemtap-sdt-devel, bison, bison-devel, pam-devel
BuildRequires:    pcre-devel >= 8.35 pkgconf
BuildRequires:    perl-interpreter, perl-generators
BuildRequires:    python3, time, procps
BuildRequires:    openssl openssl-devel
BuildRequires:    perl(File::Temp), perl(Data::Dumper), perl(Getopt::Long)
BuildRequires:    perl(Env), perl(Exporter), perl(Fcntl)
BuildRequires:    perl(IPC::Open3), perl(Memoize), perl(Socket)
BuildRequires:    perl(Sys::Hostname), perl(Test::More), perl(Time::HiRes), perl(Symbol)


Requires:         grep, bash, coreutils
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         mariadb-connector-c >= 3.0
Suggests:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Provides:         mariadb-galera = %{epoch}:%{version}-%{release}

%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::)

%description
MariaDB turns data into structured information in a wide array of applications,
ranging from banking to websites. It is an enhanced, drop-in replacement for MySQL.
MariaDB is used because it is fast, scalable and robust, with a rich ecosystem of storage
engines, plugins and many other tools make it very versatile for a wide variety of use cases.

%package          common
Summary:          It including share config files used by client and server
Provides:         mariadb-galera-common = %{epoch}:%{version}-%{release}
Obsoletes:        %{name}-libs <= %{epoch}:%{version}-%{release}

%description      common
It including share config files used by client and server,
It must install first.

%package          errmessage
Summary:          It including the error messages files
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Provides:         errmsg errmsg%{?_isa}
Obsoletes:        errmsg

%description      errmessage
The package provides error messages files for other packages.


%package          server
Summary:          The MariaDB server
Requires:         %{name}%{?_isa}
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-errmessage%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         perl(DBI) perl(DBD::mysql)
Recommends:       %{name}-backup%{?_isa} = %{epoch}:%{version}-%{release}
Recommends:       %{name}-gssapi-server%{?_isa} = %{epoch}:%{version}-%{release}
Provides:         server_utils server_utils%{?_isa}
Obsoletes:        server-utils

Requires:         %{_sysconfdir}/my.cnf
Requires:         %{_sysconfdir}/my.cnf.d
Requires:         coreutils, iproute, psmisc
Suggests:         logrotate
Requires:         systemd
Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description      server
MariaDB Server is one of the most popular database servers in the world.


%package          server-galera
Summary:          MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         galera >= 25.3.3
Requires(post):   libselinux-utils
Requires(post):   policycoreutils-python-utils
Requires:         lsof, rsync
Provides:         mariadb-galera-server = %{epoch}:%{version}-%{release}

%description      server-galera
MariaDB Galera Cluster is a synchronous multi-master cluster for MariaDB.


%package          gssapi-server
Summary:          The gssapi authentication plugin
BuildRequires:    krb5-devel
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}

%description      gssapi-server
The gssapi authentication plugin allows the user to authenticate with services.


%package          devel
Summary:          Including header files and library for the developing of mariadb
Requires:         openssl-devel
Requires:         mariadb-connector-c-devel >= 3.0

%description      devel
This contains dynamic libraries and header files for the developing of mariadb.


%package          oqgraph-engine
Summary:          The Open Query GRAPH computation engine
BuildRequires:    boost-devel Judy-devel
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}

%description      oqgraph-engine
The Open Query GRAPH computation engine, or OQGRAPH as the engine itself is called,
allows you to handle hierarchies (tree structures) and complex graphs (nodes having
many connections in several directions).


%package          backup
Summary:          MariaDB physical online backups of InnoDB, Aria and MyISAM tables
BuildRequires:    libarchive-devel
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}

%description      backup
Mariabackup is an open source tool provided by MariaDB for performing physical
online backups of InnoDB, Aria and MyISAM tables. For InnoDB, “hot online” backups
are possible. It was originally forked from Percona XtraBackup 2.3.8. It is available
on Linux and Windows.


%package          cracklib
Summary:          A password validation plugin
BuildRequires:    cracklib-dicts cracklib-devel
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         cracklib-dicts
Provides:         cracklib-password-check cracklib-password-check%{?_isa}
Obsoletes:        cracklib-password-check

%description      cracklib
cracklib_password_check is a password validation plugin. It uses the CrackLib library
to check the strength of new passwords. CrackLib is installed by default in many Linux
distributions, since the system's Pluggable Authentication Module (PAM) authentication
framework is usually configured to check the strength of new passwords with the pam_cracklib
PAM module.


%package          embedded
Summary:          The embedded MariaDB server
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-errmessage%{?_isa} = %{epoch}:%{version}-%{release}

%description      embedded
The embedded MariaDB server, libmysqld has the identical interface as the C client
librarylibmysqclient.

%package          embedded-devel
Summary:          Including header files and library for the developing of embedded MariaDB
Requires:         %{name}-embedded%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         libaio-devel

%description      embedded-devel
This contains dynamic libraries and header files for the developing of embedded MariaDB.


%package          test
Summary:          The test suite of MariaDB
Requires:         %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         perl(Env), perl(Fcntl), perl(Exporter)
Requires:         perl(File::Temp), perl(Data::Dumper), perl(Getopt::Long)
Requires:         perl(IPC::Open3), perl(Socket), perl(Sys::Hostname)
Requires:         perl(Test::More), perl(Time::HiRes)

%description      test
This contains test suitte for the developing of MariaDB.


%prep
%autosetup -n %{name}-%{version} -p1
find . -name "*.jar" -type f -exec rm --verbose -f {} \;

pcre_maj=`grep '^m4_define(pcre_major' pcre/configure.ac | sed -r 's/^m4_define\(pcre_major, \[([0-9]+)\]\)/\1/'`
pcre_min=`grep '^m4_define(pcre_minor' pcre/configure.ac | sed -r 's/^m4_define\(pcre_minor, \[([0-9]+)\]\)/\1/'`

pcre_system_version=`pkgconf %{_libdir}/pkgconfig/libpcre.pc --modversion 2>/dev/null `
if [ "$pcre_system_version" != "$pcre_maj.$pcre_min" ]
then
  echo "\n Warning: Error: Bundled PCRE version is not correct. \n\tSystem version number:$pcre_system_version \n\tUpstream version number: $pcre_maj.$pcre_min\n"
fi


rm -r storage/rocksdb/

rm -r storage/tokudb/mysql-test/tokudb/t/*.py



%build

%if %runtest
    if [ x"$(id -u)" = "x0" ]; then
        echo "mysql can't run test as root"
        exit 1
    fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
CFLAGS="$CFLAGS -fPIC"
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

%cmake . \
         -DBUILD_CONFIG=mysql_release \
         -DFEATURE_SET="community" \
         -DINSTALL_LAYOUT=RPM \
         -DDAEMON_NAME="%{name}" \
         -DDAEMON_NO_PREFIX="%{name}" \
         -DLOG_LOCATION="%{_localstatedir}/log/%{name}/%{name}.log" \
         -DPID_FILE_DIR="%{_rundir}/%{name}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DRPM="openeuler1" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DMYSQL_DATADIR="%{_localstatedir}/lib/mysql" \
         -DMYSQL_UNIX_ADDR="%{_sharedstatedir}/mysql/mysql.sock" \
         -DTMPDIR=%{_tmppath} \
         -DENABLED_LOCAL_INFILE=ON \
         -DENABLE_DTRACE=ON \
         -DSECURITY_HARDENED=ON \
         -DWITH_EMBEDDED_SERVER=ON \
         -DWITH_MARIABACKUP=ON \
         -DWITH_UNIT_TESTS=ON \
         -DCONC_WITH_SSL=NO \
         -DWITH_SSL=system \
         -DWITH_ZLIB=system \
         -DWITH_JEMALLOC=NO \
         -DLZ4_LIBS=%{_libdir}/liblz4.so \
         -DWITH_INNODB_LZ4=ON \
         -DPLUGIN_MROONGA=NO \
         -DPLUGIN_OQGRAPH=DYNAMIC \
         -DPLUGIN_CRACKLIB_PASSWORD_CHECK=DYNAMIC \
         -DPLUGIN_ROCKSDB=NO \
         -DPLUGIN_SPHINX=NO \
         -DPLUGIN_TOKUDB=NO \
         -DPLUGIN_CONNECT=NO \
         -DWITH_CASSANDRA=FALSE \
         -DPLUGIN_AWS_KEY_MANAGEMENT=NO \
         -DCONNECT_WITH_MONGO=OFF \
         -DCONNECT_WITH_JDBC=OFF \
         -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
         -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
         -DINSTALL_DOCDIR="share/doc/%{name}" \
         -DINSTALL_DOCREADMEDIR="share/doc/%{name}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_INFODIR=share/info \
         -DINSTALL_LIBDIR="%{_lib}" \
         -DINSTALL_MANDIR=share/man \
         -DINSTALL_MYSQLSHAREDIR=share/%{name} \
         -DINSTALL_MYSQLTESTDIR=share/mysql-test \
         -DINSTALL_PLUGINDIR="%{_lib}/%{name}/plugin" \
         -DINSTALL_SBINDIR=libexec \
         -DINSTALL_SCRIPTDIR=bin \
         -DINSTALL_SQLBENCHDIR=share \
         -DINSTALL_SUPPORTFILESDIR=share/%{name} \

cmake -L

%make_build VERBOSE=1


%install
%make_install

ln -s mysql_config.1.gz %{buildroot}%{_mandir}/man1/mariadb_config.1.gz

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
mv %{buildroot}/%{_datadir}/pkgconfig/*.pc %{buildroot}/%{_libdir}/pkgconfig

install -p -m 644 Docs/INFO_SRC %{buildroot}%{_libdir}/%{name}/
install -p -m 644 Docs/INFO_BIN %{buildroot}%{_libdir}/%{name}/
rm -r %{buildroot}%{_datadir}/doc/%{name}/MariaDB-server-%{version}/

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
chmod 0750 %{buildroot}%{_localstatedir}/log/%{name}
touch %{buildroot}%{_localstatedir}/log/%{name}

mkdir -p %{buildroot}%{_rundir}/%{name}
install -p -m 0755 -d %{buildroot}%{_localstatedir}/lib/mysql

mv %{buildroot}%{_sysconfdir}/my.cnf.d/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{name}-server.cnf
mv %{buildroot}%{_sysusersdir}/sysusers.conf %{buildroot}%{_sysusersdir}/%{name}.conf

rm %{buildroot}%{_sysconfdir}/init.d/mysql
rm %{buildroot}%{_libexecdir}/rcmysql
rm %{buildroot}%{_tmpfilesdir}/tmpfiles.conf
echo "d %{_rundir}/%{name} 0755 mysql mysql -" >>%{buildroot}%{_tmpfilesdir}/%{name}.conf

mv %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir}
ln -s ../../../../../bin/my_safe_process %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process

rm %{buildroot}%{_bindir}/mysql_embedded
rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_datadir}/%{name}/{magic,binary-configure}

rm %{buildroot}%{_datadir}/%{name}/{mysql.server,mysqld_multi.server}

rm %{buildroot}%{_bindir}/mytop

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mv %{buildroot}%{_datadir}/%{name}/mysql-log-rotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
chmod 644 %{buildroot}%{_sysconfdir}/logrotate.d/%{name}


sed -i -r 's|^wsrep_provider=none|wsrep_provider=%{_libdir}/galera/libgalera_smm.so|' support-files/wsrep.cnf
install -p -m 0644 support-files/wsrep.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/galera.cnf
install -D -p -m 0644 support-files/rpm/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/sysconfig/clustercheck

rm %{buildroot}%{_sysconfdir}/logrotate.d/mysql
rm -r %{buildroot}%{_datadir}/%{name}/policy/apparmor

chmod -x %{buildroot}%{_datadir}/sql-bench/myisam.cnf


rm %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
rm %{buildroot}%{_libdir}/libmariadb.so.*
unlink %{buildroot}%{_libdir}/libmysqlclient.so
unlink %{buildroot}%{_libdir}/libmysqlclient_r.so
unlink %{buildroot}%{_libdir}/libmariadb.so
rm %{buildroot}%{_libdir}/%{name}/plugin/{dialog.so,mysql_clear_password.so,sha256_password.so,auth_gssapi_client.so}

rm %{buildroot}%{_bindir}/{mariadb_config,mysql_config*}
rm %{buildroot}%{_mandir}/man1/mysql_config*.1*
unlink %{buildroot}%{_mandir}/man1/mariadb_config.1*

rm %{buildroot}%{_includedir}/mysql/{mysql_version.h,errmsg.h,ma_list.h,ma_pvio.h,mariadb_com.h,\
mariadb_ctype.h,mariadb_dyncol.h,mariadb_stmt.h,mariadb_version.h,ma_tls.h,mysqld_error.h,mysql.h}
rm -r %{buildroot}%{_includedir}/mysql/{mariadb,mysql}


rm %{buildroot}%{_mandir}/man1/tokuft*
rm -r %{buildroot}%{_datadir}/sql-bench



%check
%if %runtest
export MTR_PARALLEL=1
export MTR_BUILD_THREAD=%{__isa_bits}


(
  set -ex

  cd mysql-test
  perl ./mysql-test-run.pl --parallel=auto --force --retry=1 --ssl \
    --suite-timeout=900 --testcase-timeout=30 \
    --mysqld=--binlog-format=mixed --force-restart \
    --shutdown-timeout=60 --max-test-fail=5 --big-test \
    --skip-test=spider \
    --skip-test-list=unstable-tests

  perl ./mysql-test-run.pl --parallel=auto --force --retry=1 \
    --suite-timeout=60 --testcase-timeout=10 \
    --mysqld=--binlog-format=mixed --force-restart \
    --shutdown-timeout=60 --max-test-fail=0 --big-test \
    --skip-ssl --suite=spider,spider/bg \
)

%endif



%pre server
/usr/sbin/groupadd -g 27 -o -r mysql &> /dev/null || :
/usr/sbin/useradd -M -N -g mysql -o -r -d /var/lib/mysql -s /sbin/nologin \
  -c "MySQL Server" -u 27 mysql &> /dev/null || :


%ldconfig_scriptlets embedded

%post server-galera
semanage port -a -t mysqld_port_t -p tcp 4568 &> /dev/null || :
semanage port -a -t mysqld_port_t -p tcp 4567 &> /dev/null || :
semanage port -a -t mysqld_port_t -p udp 4567 &> /dev/null || :

%post server
%systemd_post %{name}.service

%preun server
%systemd_preun %{name}.service

%postun server-galera
if [ $1 -eq 0 ]; then
    semodule -r %{name}-server-galera 2>/dev/null || :
fi

%postun server
%systemd_postun_with_restart %{name}.service



%files
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%{_bindir}/mysql
%{_bindir}/mysql_find_rows
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump

%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin

%{_bindir}/mysqlimport
%{_bindir}/mysql_plugin

%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/msql2mysql

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_waitpid.1*



%files common
%doc %{_defaultdocdir}/%{name}
%dir %{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/my.cnf
%{_datadir}/%{name}/charsets

%files errmessage
%{_datadir}/%{name}/errmsg-utf8.txt
%{_datadir}/%{name}/*/errmsg.sys


%files server
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/my.cnf.d/%{name}-server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset

%{_bindir}/aria*
%{_bindir}/mariadb-service-convert
%{_bindir}/myisam*
%{_bindir}/my_print_defaults
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysqld_safe
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_setpermission
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqlhotcopy
%{_bindir}/mysql_upgrade
%{_bindir}/mysqld_safe_helper
%{_bindir}/perror
%{_bindir}/innochecksum
%{_bindir}/replace
%{_bindir}/resolve*
%{_bindir}/wsrep_*

%{_libexecdir}/mysqld
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugin
%{_libdir}/%{name}/plugin/*
%{_libdir}/%{name}/INFO_*
%exclude %{_libdir}/%{name}/plugin/ha_oqgraph.so

%{_mandir}/man1/aria*
%{_mandir}/man1/galera*
%{_mandir}/man1/mariadb-service-convert.1*
%{_mandir}/man1/myisam*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqld_safe_helper.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve*
%{_mandir}/man1/wsrep_*.1*
%{_mandir}/man8/mysqld.8*

%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/wsrep.cnf
%{_datadir}/%{name}/wsrep_notify
%dir %{_datadir}/%{name}/policy
%dir %{_datadir}/%{name}/policy/selinux
%{_datadir}/%{name}/policy/selinux/*
%{_datadir}/%{name}/systemd/*.service

%{_unitdir}/%{name}*

%attr(0755,mysql,mysql) %dir %{_rundir}/%{name}
%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysql
%attr(0750,mysql,mysql) %dir %{_localstatedir}/log/%{name}
%attr(0640,mysql,mysql) %config %ghost %verify(not md5 size mtime) %{_localstatedir}/log/%{name}/%{name}.log
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}


%files server-galera
%doc Docs/README-wsrep
%config(noreplace) %{_sysconfdir}/my.cnf.d/galera.cnf
%attr(0640,root,root) %ghost %config(noreplace) %{_sysconfdir}/sysconfig/clustercheck
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%{_datadir}/%{name}/systemd/use_galera_new_cluster.conf

%files gssapi-server
%config(noreplace) %{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%{_libdir}/%{name}/plugin/auth_gssapi.so


%files devel
%{_includedir}/*
%{_datadir}/aclocal/mysql.m4
%{_libdir}/pkgconfig/mariadb.pc


%files oqgraph-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/oqgraph.cnf
%{_libdir}/%{name}/plugin/ha_oqgraph.so


%files backup
%{_bindir}/mariabackup
%{_bindir}/mbstream


%files cracklib
%config(noreplace) %{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%{_libdir}/%{name}/plugin/cracklib_password_check.so


%files embedded
%{_libdir}/libmariadbd.so.*


%files embedded-devel
%{_libdir}/libmysqld.so
%{_libdir}/libmariadbd.so


%files test
%{_bindir}/mysqltest
%{_bindir}/mysql_client_test
%{_bindir}/test-connect-t
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_bindir}/my_safe_process
%{_mandir}/man1/mysql_client_test.1*
%{_mandir}/man1/my_safe_process.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*
%attr(-,mysql,mysql) %{_datadir}/mysql-test


%changelog
* Thu Aug 18 2020 xinghe <xinghe1@huawei.com> - 3:10.3.9-9
- Add release version for update

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

