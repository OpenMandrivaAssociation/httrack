%define name httrack
%define version 3.40.3
%define ftp_version 3.40-2
%define release %mkrel 1

%define major 1
%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

%define summary A free (libre/open source) and easy-to-use offline browser utility

Summary:	%summary
Name:		%name
Version: 	%version
Release:	%release
Group: 		Networking/WWW
License: 	GPL
Source: 	%{name}-%{ftp_version}.tar.bz2
URL: 		http://www.httrack.com
BuildRequires: perl, zlib-devel

%description
HTTrack is a free (open source) and easy-to-use offline browser utility.
Download a World Wide Web site from the Internet to a local directory.
Builds recursively all directories.
Getting HTML, images, and other files from the server.
HTTrack arranges the original site's relative link-structure.
Simply open a page of the "mirrored" website in your browser.
You can browse the site from link to link, as if you were viewing it online. 
It can update an existing mirrored site, and resume interrupted downloads.
It is fully configurable, and has an integrated help system.

%package -n %libname
Summary:     %summary
Group: 		System/Libraries
Provides:       libhttrack=%version-%release

%description -n %libname
libraries needed for httrack

%package -n %libnamedev 
Summary:	Headers and static libraries for httrack
Group:		Development/C++
Requires:	libhttrack=%version-%release
Provides:       libhttrack-devel
#Requires: 	libhttrack1 = %version

%description -n %libnamedev
libraries headers for needed building using httrack

%prep
%__rm -rf $RPM_BUILD_ROOT

%setup -q -n %name-%version

%build

%configure2_5x

%install
%makeinstall_std
 
%__mkdir_p $RPM_BUILD_ROOT/etc

%__cat  >$RPM_BUILD_ROOT/etc/httrack.conf <<"EOF"
# HTTrack Website Copier Settings
# See httrack --help for more information

# Examples: (to uncomment)

# set proxy proxy.myisp.com:8080
# retries=2
# set max-size 10000000
# set max-time 36000
# set user-agent Mouzilla/17.0 (compatible; HTTrack; I)
#
# There are MUCH more options.. try 'httrack --quiet --help | more'

# Deny and allow for links
# this will be used by default for all mirrors
allow *.gif
allow *.png
deny ad.doubleclick.net/*

# Path and other options
# '~' in the *begining* means 'home dir'
# '#' at the *end* means "projectname" (that is, the first URL given)
# Example: '~/websites/#' will create /home/smith/websites/www.foo.com
# folder when launching 'httrack www.foo.com'
set path ~/websites/#
EOF
 
%__chmod 644 $RPM_BUILD_ROOT/etc/httrack.conf

ln -sf %_docdir/%name/html  $RPM_BUILD_ROOT/%_datadir/%name/html 

%clean
%__rm -rf $RPM_BUILD_ROOT
 
%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_docdir}/httrack/
%_bindir/htsserver
%_bindir/httrack
%_bindir/webhttrack
%_bindir/proxytrack
%config (noreplace) /etc/httrack.conf
%{_mandir}/man1/htsserver.*
%{_mandir}/man1/httrack.*
%{_mandir}/man1/webhttrack.*
%{_mandir}/man1/proxytrack.*
%_datadir/applications/WebHTTrack-Websites.desktop
%_datadir/applications/WebHTTrack.desktop
%_datadir/pixmaps/httrack.xpm
%dir %_datadir/%name
%_datadir/%name/*.def
%_datadir/%name/html
%_datadir/%name/icons/webhttrack.xpm
%_datadir/%name/lang
%_datadir/%name/templates
%_datadir/%name/lang.indexes
%defattr(644,root,root,755)
%doc httrack-doc.html templates COPYING INSTALL README *.txt

%files -n %libname
%defattr(-, root, root)
%{_libdir}/lib%name.so.1
%{_libdir}/lib%name.so.1.0.40
%{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/*.so

%files -n %libnamedev
%defattr(-,root,root)  
%{_libdir}/lib%name.so
%{_libdir}/lib%name.a
%{_libdir}/lib%name.la
%{_libdir}/%{name}/*.a
%{_libdir}/%{name}/*.la
%_includedir/%name
%_datadir/%name/libtest


