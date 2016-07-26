%{?scl:%scl_package nodejs-%{npm_name}}
%{!?scl:%global pkg_name %{name}}

%{?nodejs_find_provides_and_requires}
%global npm_name nodemon

# Disable until dependencies are met
%global enable_tests 0

Summary:       Simple monitor script for use during development of a node.js app
Name:          %{?scl_prefix}nodejs-%{npm_name}
Version:       1.8.1
Release:       5%{?dist}
License:       MIT
URL:           https://github.com/remy/nodemon
Source0:       http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: nodejs010-runtime
ExclusiveArch: %{nodejs_arches} noarch
BuildArch:     noarch
Provides:      %{?scl_prefix}nodejs-%{npm_name} = %{version}

%if 0%{?enable_tests}
BuildRequires:  %{?scl_prefix}npm(mocha)
BuildRequires:  %{?scl_prefix}npm(coveralls)
%endif

%description
Simple monitor script for use during development of a node.js app.

For use during development of a node.js based application.

nodemon will watch the files in the directory in which nodemon 
was started, and if any files change, nodemon will automatically 
restart your node application.

nodemon does not require any changes to your code or method of 
development. nodemon simply wraps your node application and keeps 
an eye on any files that have changed. Remember that nodemon is a 
replacement wrapper for node, think of it as replacing the word "node" 
on the command line when you run your script.

%prep
%setup -q -n package

%nodejs_fixdep update-notifier '>=0.5.0'

%build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr doc  bin lib package.json web %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/nodemon.js %{buildroot}%{_bindir}/nodemon


%nodejs_symlink_deps

%if 0%{?enable_tests}

%check
%nodejs_symlink_deps --check
npm run lint && npm run spec
%endif

%files
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md doc faq.md README.md
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/nodemon

%changelog
* Wed Jan 06 2016 Tomas Hrcka <thrcka@redhat.com> - 1.8.1-5
- Enable scl macros

* Thu Dec 17 2015 Troy Dawson <tdawson@redhat.com> - 1.8.1-2
- Fix dependencies

* Wed Dec 16 2015 Troy Dawson <tdawson@redhat.com> - 1.8.1-1
- Initial package
