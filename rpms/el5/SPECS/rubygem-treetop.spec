%global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname treetop
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:        A Ruby-based text parsing and interpretation DSL
Name:           rubygem-%{gemname}
Version:        1.4.10
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://treetop.rubyforge.org/
Source0:        http://rubygems.org/downloads/%{gemname}-%{version}.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ruby(abi) = 1.8
Requires:       rubygems
Requires:       rubygem(polyglot)
BuildRequires:  rubygems
# The Following are required for testing
#BuildRequires:  rubygem(rake)
#BuildRequires:  rubygem(rspec)
#BuildRequires:  rubygem(ruby-debug)
BuildArch:      noarch
Provides:       rubygem(%{gemname}) = %{version}

%description
Treetop is a language for describing languages. It helps you analyze syntax.


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            -V \
            --force --rdoc %{SOURCE0}

pushd ./%{gemdir}

%build


%install
mkdir -p $RPM_BUILD_ROOT%{gemdir}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT%{gemdir}/bin/* $RPM_BUILD_ROOT/%{_bindir}
rmdir $RPM_BUILD_ROOT%{gemdir}/bin
find $RPM_BUILD_ROOT%{geminstdir}/bin -type f |xargs chmod a+x
find $RPM_BUILD_ROOT%{gemdir} -name '*.rb' |xargs chmod a-x

# Remove zero-length documentation files
find $RPM_BUILD_ROOT%{gemdir}/doc/%{gemname}-%{version} -empty -delete


%clean
rm -rf $RPM_BUILD_ROOT

# Uncomment as soon as we have rubygem-rr in fedora
#%check
#pushd %{buildroot}%{geminstdir}
#rake spec

%files
%defattr(-,root,root,-)
%{_bindir}/tt
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%{geminstdir}/Rakefile
%doc %{geminstdir}/doc
%doc %{geminstdir}/examples
%doc %{geminstdir}/README.md
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/spec
%doc %{geminstdir}/%{gemname}.gemspec
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Sun Jan 08 2012 <stahnma@fedoraproject.org> - 1.4.10-1
- Rebuilt and fix bz#716045

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Mohammed Morsi <mmorsi@redhat.com> - 1.4.9-1
- Updated to latest upstream release

* Fri Jul 31 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.3.0-1
- Update to new upstream version
- Mark more documentation files as such

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.2.5-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.2.5-2
- Fix up documentation list
- Use geminstdir macro where appropriate
- Do not move examples around
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.2.5-1
- Package generated by gem2rpm
- Move examples into documentation
- Remove empty files
- Fix file permissions
- Fix up License
