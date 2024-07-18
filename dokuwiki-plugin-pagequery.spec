%define		plugin		pagequery
%define		php_min_version 5.3.0
Summary:	DokuWiki plugin to search for and list pages, sorted by name, date, creator, etc
Name:		dokuwiki-plugin-%{plugin}
Version:	20180122
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/MrBertie/pagequery/tarball/master/%{plugin}-%{version}.tgz
# Source0-md5:	77fc93596880c4b2046e187bc8898536
URL:		http://www.dokuwiki.org/plugin:pagequery
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20091225
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_prefix}/lib/rpm/dokuwiki-find-lang.sh %{buildroot}

%description
An all-in-one multipurpose navigation plugin to search for and list
pages; by full-text or page name; neatly grouped results, optionally
in columns, with preview snippet.

%prep
%setup -qc
mv *-%{plugin}-*/* .
%undos *.txt

# using date from latest commit
#version=$(awk '/^date/{print $2}' plugin.info.txt)
#if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
#	: %%{version} mismatch
#	exit 1
#fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm $RPM_BUILD_ROOT%{plugindir}/readme.md

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc readme.md
%dir %{plugindir}
%{plugindir}/*.txt
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/images
%{plugindir}/inc
%{plugindir}/res
