Summary:	Tcl extension to build network management applications using Tcl (and Tk).
Name:		scotty
Version:	2.1.10
Release:	1
Copyright:	Free
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
URL:		http://wwwsnmp.cs.utwente.nl/~schoenw/scotty/
Source:		%{name}-%{version}.tar.gz
Patch:		scotty-DESTDIR.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
You are looking at the source tree of scotty, a Tcl extension to build
network management applications using Tcl (and Tk). The scotty extension
provides new Tcl commands to

	- send and receive ICMP packets
	- query the Domain Name System (DNS)
	- access UDP sockets from Tcl
	- probe and use some selected SUN RPCs
	- retrieve and serve documents via HTTP
	- send and reveice SNMP messages (SNMPv1, SNMPv2USEC, SNMPv2C)
	- write special purpose SNMP agents in Tcl
	- parse and access SNMP MIB definitions
	- schedule jobs that are to be done regularly

and for some OSI-folks there is some optional code to

	- parse and access GDMO MIB definitions
	- invoke CMIP operations based on the osimis/isode toolkit

This distributions also includes the sources for Tkined. Tkined is a
network editor which allows to draw maps showing your network
configuration. The most important feature of Tkined is its programming
interface which allows network management applications to extend the
capabilities of Tkined. Most applications for Tkined are written using
scotty.

%prep
%setup -q
%patch0 -p1

%build
cd unix
%configure
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT

cd unix
make install sinstall DESTDIR=$RPM_BUILD_ROOT

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/scotty
#!/bin/sh
TCLLIBPATH="%{_libdir}/tnm2.1.10 \$TCLLIBPATH"
export TCLLIBPATH
%{_bindir}/scotty%{version}
EOF

ln -s tkined1.4.10 $RPM_BUILD_ROOT%{_bindir}/tkined

strip --strip-unneeded $RPM_BUILD_ROOT%{_bindir}/* || :
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/*.so || :

cd ..

rm -f $RPM_BUILD_ROOT%{_mandir}/mann/http.n

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8,n}/* \
	README TODO license.terms

%post
echo 'foreach f $tnm(mibs) {puts "Parsing $f"; mib load $f}; exit' | %{_bindir}/scotty >/dev/null 2>&1
echo 'cd %{_libdir}/tnm%{version}/library; auto_mkindex . *.tcl; exit' | %{_bindir}/scotty >/dev/null 2>&1
echo 'cd %{_libdir}/tkined1.4.10/apps; auto_mkindex . library.tcl; exit' | %{_bindir}/tclsh >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,TODO,license.terms}.gz
%attr(755,root,root) %{_bindir}/scotty*
%attr(755,root,root) %{_bindir}/tkined*

%attr(4755,root,root) %{_bindir}/ntping
%attr(4755,root,root) %{_bindir}/straps

%attr(-,root,root) %{_libdir}/tkined1.4.10
%attr(-,root,root) %{_libdir}/tnm%{version}

%attr(755,root,root) %{_libdir}/*.so

%{_mandir}/man1/*
%{_mandir}/man8/*
%{_mandir}/mann/*
