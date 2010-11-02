%define		plugin		pagequery
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki pagequery plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	20100505
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://github.com/downloads/MrBertie/pagequery/%{plugin}.zip
# Source0-md5:	06f35ccab9739e3a5efa27616fee1723
URL:		http://www.dokuwiki.org/plugin:pagequery
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-pcre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
An all-in-one multipurpose navigation plugin to search for and list
pages; by full-text or page name; neatly grouped results, optionally
in columns, with preview snippet.

%prep
%setup -qc
mv %{plugin}/* .

version=$(awk -F"'" '/date/&&/=>/{print $4}' syntax.php)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm $RPM_BUILD_ROOT%{plugindir}/{readme.txt,changes.txt}

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
%doc changes.txt readme.txt
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/images
