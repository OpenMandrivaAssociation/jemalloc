%define major 2
%define libname %mklibname jemalloc %{major}
%define develname %mklibname -d jemalloc
# (tpg) https://github.com/jemalloc/jemalloc/issues/1057
%define _disable_lto 1

# (tpg) optimize it a bit
%global optflags %optflags -O3

Summary:	General-purpose scalable concurrent malloc implementation
Name:		jemalloc
Version:	5.2.1
Release:	1
Group:		System/Libraries
License:	BSD
URL:		http://www.canonware.com/jemalloc/
Source0:	https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	xsltproc
Requires:	%{libname} = %{EVRD}

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package -n %{libname}
Summary:	General-purpose scalable concurrent malloc implementation
Group:		System/Libraries

%description -n %{libname}
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

If you want to use jemalloc as default malloc(3) implementation on your
system follow below:

1. create /etc/ld.so.preload
2. add to that file %{_libdir}/libjemalloc.so.%{major}

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	jemalloc-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
export LC_ALL=C
%configure
%make_build

%check
make check

%install
%make_install

# Install this with doc macro instead
rm -rf %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'
mv %{buildroot}%{_bindir}/jemalloc.sh %{buildroot}%{_bindir}/jemalloc

# (tpg) fix it
# BUILDSTDERR: error: Invalid version (double separator '-'): 5.0.1-0-g896ed3a8b3f41998d4fb4d625d30ac63ef2d51fb: pkgconfig(jemalloc) = 5.0.1-0-g896ed3a8b3f41998d4fb4d625d30ac63ef2d51fb
sed -i -e "s/^Version:.*/Version: %{version}/g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%files
%{_bindir}/jemalloc
%{_bindir}/jeprof
%{_mandir}/man3/jemalloc.3*

%files -n %{libname}
%{_libdir}/libjemalloc.so.%{major}*

%files -n %{develname}
%doc COPYING README VERSION
%doc doc/jemalloc.html
%{_bindir}/jemalloc-config
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_libdir}/pkgconfig/%{name}.pc
