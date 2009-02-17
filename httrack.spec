%define ftp_version 3.43-2

%define major 2
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d

Name:		httrack
Version: 	3.43.2
Release:	%mkrel 1
Summary:	A free (libre/open source) and easy-to-use offline browser utility
Group: 		Networking/WWW
License: 	GPLv2+
Source: 	%{name}-%{ftp_version}.tar.gz
Patch0:		httrack-3.42-generic-macros.patch
Patch1:		httrack-3.42-libhtsjava.patch
Patch2:		httrack-3.42-utf-8.patch
Patch3:		%{name}-%{version}-openssl.patch
Patch5:		%{name}-3.43.2-string-format.patch
URL: 		http://www.httrack.com
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires: 	perl, zlib-devel
BuildRequires:	dos2unix
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	chrpath
Requires:       openssl

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
Summary:     	%summary
Group: 		System/Libraries
Provides:       libhttrack=%{version}-%{release}

%description -n %libname
libraries needed for httrack

%package -n %libnamedev
Summary:	Headers and static libraries for httrack
Group:		Development/C++
Requires:	libhttrack=%{version}-%{release}
Provides:       libhttrack-devel
Conflicts:	%mklibname -d httrack 1
Obsoletes:	%mklibname -d httrack 1
#Requires: 	libhttrack1 = %version

%description -n %libnamedev
libraries headers for needed building using httrack

%prep
rm -rf %{buildroot}
%setup -q -n %{name}-%{version}
#%patch0 -p1 -b .generic-macros
#%patch1 -p1 -b .libhtsjava
%patch2 -p1 -b .utf8
%patch3 -p1 -b .openssl
%patch5 -p1 -b .strfmt

# Suppress rpmlint error.
dos2unix ./AUTHORS
dos2unix ./README
dos2unix ./greetings.txt
dos2unix ./history.txt
dos2unix ./html/step3.html
dos2unix ./%{name}-doc.html
dos2unix ./libtest/*.c
dos2unix ./libtest/example.h
dos2unix ./libtest/readme.txt
dos2unix ./license.txt
dos2unix ./templates/*.html


iconv --from-code ISO8859-1 --to-code UTF-8 ./greetings.txt \
  --output greetings.utf-8 && mv greetings.utf-8 ./greetings.txt
iconv --from-code ISO8859-1 --to-code UTF-8 ./history.txt \
  --output history.utf-8 && mv history.utf-8 ./history.txt
iconv --from-code ISO8859-1 --to-code UTF-8 ./html/contact.html \
  --output contact.utf-8 && mv contact.utf-8 ./html/contact.html

%build
%configure2_5x --disable-static

%install
%makeinstall_std
find %{buildroot} -type f -name "*.la" -delete

mkdir -p %{buildroot}/etc

cat > %{buildroot}/etc/httrack.conf <<"EOF"
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

chmod 644 %{buildroot}/etc/httrack.conf

# Move libtest and templates from /usr/share/httrack to RPM_BUILD_DIR.
# To be later listed against %doc.
rm -rf ./libtest ./templates
mv %{buildroot}%{_datadir}/%{name}/libtest .
mv %{buildroot}%{_datadir}/%{name}/templates .

# We need to have a copy of html in /usr/share/httrack.
# The other is to be listed against %doc.
rm -rf ./html
cp -pr %{buildroot}%{_datadir}/%{name}/html .

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}%{_datadir}/%{name}/icons/webhttrack.xpm %buildroot%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{buildroot}%{_datadir}/%{name}/icons/webhttrack.xpm %buildroot%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}%{_datadir}/%{name}/icons/webhttrack.xpm %buildroot%{_iconsdir}/hicolor/16x16/apps/%{name}.png

rm -rf %{buildroot}%{_datadir}/%{name}/icons

# This just opens a web browser on ~/websites, which is empty by
# default, so this is a bit useless
rm -f %{buildroot}%{_datadir}/applications/WebHTTrack-Websites.desktop

desktop-file-install --vendor ""  \
	--remove-key Encoding \
	--remove-category="Application" \
	--remove-key Terminal \
	--remove-key MultipleArgs \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# fix icon and shorten name
sed -i	-e 's!^Icon=.*$!Icon=httrack!' \
	-e 's!WebHTTrack Website Copier!HTTrack Website Copier!' \
	%{buildroot}%{_datadir}/applications/*

# Remove rpaths.
chrpath --delete %{buildroot}%{_bindir}/htsserver
chrpath --delete %{buildroot}%{_bindir}/%{name}
chrpath --delete %{buildroot}%{_libdir}/libhtsjava.so.*


%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc httrack-doc.html templates AUTHORS README license.txt history.txt greetings.txt
%{_bindir}/htsserver
%{_bindir}/httrack
%{_bindir}/webhttrack
%{_bindir}/proxytrack
%config (noreplace) /etc/httrack.conf
%{_mandir}/man1/htsserver.*
%{_mandir}/man1/httrack.*
%{_mandir}/man1/webhttrack.*
%{_mandir}/man1/proxytrack.*
%{_datadir}/applications/WebHTTrack.desktop
%{_datadir}/pixmaps/httrack.xpm
%dir %{_datadir}/%name
%{_datadir}/%name/*.def
%{_datadir}/%name/html
%{_datadir}/%name/lang
%{_datadir}/%name/lang.indexes
%{_iconsdir}/hicolor/*/apps/*
%defattr(644,root,root,755)

%files -n %libname
%defattr(-, root, root)
%{_libdir}/lib%name.so.%{major}
%{_libdir}/lib%name.so.2.0.43
%{_libdir}/libhtsjava.so.%{major}
%{_libdir}/libhtsjava.so.2.0.43
%{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/*.so

%files -n %libnamedev
%defattr(-,root,root)
%{_libdir}/lib%name.so
%{_libdir}/libhtsjava.so
%{_includedir}/%name


