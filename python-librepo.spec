#
# Conditional build:
%bcond_without	apidocs	# Sphinx documentation

Summary:	Python 2 binding for librepo library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki librepo
Name:		python-librepo
# keep 1.12.x here for python2 support
Version:	1.12.1
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/librepo/releases
Source0:	https://github.com/rpm-software-management/librepo/archive/%{version}/librepo-%{version}.tar.gz
# Source0-md5:	52521f10eb5aa0cabcf65cae540039c5
Patch0:		sphinx_executable.patch
URL:		http://rpm-software-management.github.io/librepo/
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.8.5
BuildRequires:	curl-devel >= 7.52
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	python-devel >= 1:2.5
%{?with_apidocs:BuildRequires:	sphinx-pdg-2}
BuildRequires:	tar >= 1:1.22
BuildRequires:	zchunk-devel >= 0.9.11
BuildRequires:	xz
Requires:	curl-libs >= 7.52
Requires:	librepo >= %{version}
Requires:	zchunk-libs >= 0.9.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 2 binding for librepo library.

%description -l pl.UTF-8
Wiązanie Pythona 2 do biblioteki librepo.

%package apidocs
Summary:	API documentation for Python librepo binding
Summary(pl.UTF-8):	Dokumentacja API do wiązań Pythona do librepo
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python librepo binding.

%description apidocs -l pl.UTF-8
Dokumentacja API do wiązań Pythona do librepo.

%prep
%setup -q -n librepo-%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DENABLE_TESTS=OFF \
	-DPYTHON_DESIRED=2 \
	-DPYTHON_INSTALL_DIR="%{py_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-2

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

# package just the python binding (relying on system librepo.so.0)
%{__rm} -r $RPM_BUILD_ROOT{%{_includedir},%{_pkgconfigdir}}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librepo.so*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py_sitedir}/librepo
%attr(755,root,root) %{py_sitedir}/librepo/_librepomodule.so
%{py_sitedir}/librepo/__init__.py[co]

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/python/{_static,*.html,*.js}
%endif
