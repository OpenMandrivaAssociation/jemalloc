%define major 2
%define libname %mklibname jemalloc %{major}
%define develname %mklibname -d jemalloc

Summary:	General-purpose scalable concurrent malloc implementation
Name:		jemalloc
Version:	4.4.0
Release:	1
Group:		System/Libraries
License:	BSD
URL:		http://www.canonware.com/jemalloc/
Source0:	https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	xsltproc

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package -n	%{libname}
Summary:	General-purpose scalable concurrent malloc implementation
Group:		System/Libraries

%description -n	%{libname}
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	jemalloc-devel = %{version}-%{release}

%description -n %{develname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%apply_patches

%build
export LC_ALL=C
export CFLAGS="%{optflags} -std=gnu99"
%configure
%make

%check
make check

%install
%makeinstall_std

# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'
mv %{buildroot}%{_bindir}/jemalloc.sh %{buildroot}%{_bindir}/jemalloc

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
