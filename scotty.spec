%define	snap		00-02-21
%define	snapdate	20000221
%define	tkined_version	1.5.0
Summary:	Tcl extension to build network management applications using Tcl (and Tk)
Summary(pl):	Rozszerzenie Tcl do budowania aplikacji zarz±dzaj±cych sieci±
Name:		scotty
Version:	3.0.0
Release:	0.%{snapdate}.1
License:	Free
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
URL:		http://wwwsnmp.cs.utwente.nl/~schoenw/scotty/
Source0:	%{name}-%{snap}.tar.gz
#Source0:	ftp://ftp.ibr.cs.tu-bs.de/pub/local/tkined/%{name}-%{version}.tar.gz
Patch0:		%{name}-configure.patch
Patch1:		%{name}-install.patch
BuildRequires:	tcl-devel >= 8.2
BuildRequires:	tk-devel >= 8.2
BuildRequires:	libsmi-devel >= 0.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scotty is a Tcl extension to build network management applications
using Tcl (and Tk). The scotty extension provides new Tcl commands to

	- send and receive ICMP packets
	- query the Domain Name System (DNS)
	- access UDP sockets from Tcl
	- probe and use some selected SUN RPCs
	- retrieve and serve documents via HTTP
	- send and reveice SNMP messages (SNMPv1, SNMPv2C, SNMPv3)
	- write special purpose SNMP agents in Tcl
	- parse and access SNMP MIB definitions
	- schedule jobs that are to be done regularly
	- realize event driven programming on network maps

This scotty distributions also includes the sources for Tkined. Tkined
is a network editor which allows to draw maps showing your network
configuration. The most important feature of Tkined is its programming
interface which allows network management applications to extend the
capabilities of Tkined. Most applications for Tkined are written using
the Tnm Tcl extension.

%description -l pl
Scotty jest rozszerzeniem Tcl do budowania aplikacji do zarz±dzania
sieci± przy u¿yciu Tcl (i Tk). Scotty udostêpnia nowe polecenia Tcl
do:
	- wysy³ania i odbierania pakietów ICMP\
	- odpytywania DNS
	- dostêpu do gniazdek UDP
	- testowania i u¿ywania niektórych Sun RPC
	- ¶ci±gania i serwowania dokumentów po HTTP
	- wysy³ania i odbierania komunikatów SNMP (v1, v2C, v3)
	- pisania agentów SNMP
	- parsowania i dostêpu do definicji SNMP MIB
	- kolejkowania zadañ do regularnego wykonywania
	- realizacji programowania sterowanego zdarzeniami na mapach
	  sieciowych

Ta dystrybucja Scotty zawiera tak¿e ¼ród³a Tkined. Jest to sieciowy
edytor pozwalaj±cy rysowaæ mapy obrazuj±ce konfiguracjê sieci.
Najwa¿niejsz± cech± Tkined jest programistyczny interfejs pozwalaj±cy
aplikacjom zarz±dzaj±cym sieci± rozszerzaæ jego mo¿liwo¶ci. Wiêkszo¶æ
aplikacji dla Tkined jest pisana przy u¿yciu rozszerzenia Tnm dla Tcl.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1
%patch1 -p1

%build
cd unix
autoconf
%configure
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C unix \
	install sinstall \
	DESTDIR=$RPM_BUILD_ROOT

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/scotty
#!/bin/sh
TCLLIBPATH="%{_libdir}/tnm%{version} \$TCLLIBPATH"
export TCLLIBPATH
%{_bindir}/scotty%{version}
EOF

ln -sf tkined%{tkined_version} $RPM_BUILD_ROOT%{_bindir}/tkined

perl -pi -e "s|$RPM_BUILD_ROOT||g" \
	$RPM_BUILD_ROOT%{_libdir}/{tkined%{tkined_version},tnm%{version}}/pkgIndex.tcl

rm -f $RPM_BUILD_ROOT%{_mandir}/mann/http.n

gzip -9nf README license.terms

%clean
rm -rf $RPM_BUILD_ROOT

%post
cd %{_libdir}/tkined%{tkined_version}/apps
echo auto_mkindex . library.tcl | %{_bindir}/tclsh

%preun
rm -f %{_libdir}/tkined%{tkined_version}/apps/tclIndex

%files
%defattr(644,root,root,755)
%doc {README,license.terms}.gz
%attr(755,root,root) %{_bindir}/scotty*
%attr(755,root,root) %{_bindir}/tkined*

%attr(4755,root,root) %{_bindir}/nmicmpd
%attr(4755,root,root) %{_bindir}/nmtrapd

%attr(-,root,root) %{_libdir}/tkined%{tkined_version}
%attr(-,root,root) %{_libdir}/tnm%{version}

%attr(755,root,root) %{_libdir}/*.so

%{_mandir}/man1/*
%{_mandir}/man8/*
%{_mandir}/mann/*
