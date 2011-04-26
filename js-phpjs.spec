Summary:	Use PHP functions in JavaScript
Name:		js-phpjs
# there seems not to be any unified version
Version:	0.1
Release:	1
License:	GPL, MIT
Group:		Applications/WWW
Source0:	https://github.com/kvz/phpjs/tarball/master#/%{name}.tgz
# Source0-md5:	1a6fa88ed91ba6ee1f36d5729f6b8470
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://www.phpjs.org/
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		phpjs
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
php.js is an open source project that brings high-level PHP functions
to low-level JavaScript platforms such as webbrowsers, AIR, V8 and
rhino.

If you want to perform high-level operations on these platforms, you
probably need to write JS that combines it's lower-level functions and
build it up until you have something useful like: md5(), strip_tags(),
strtotime(), number_format(), wordwrap().

%prep
%setup -qc
mv kvz-phpjs-*/* .

%build
install -d build

# compress .js
for js in $(find functions -name '*.js'); do
	o=build/$js
	d=${o%/*}
	install -d $d
	yuicompressor --charset UTF-8 $js -o $o
	js -C -f $o
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a build/functions/* $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
