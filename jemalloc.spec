%define major 1
%define libname %mklibname jemalloc %{major}
%define develname %mklibname -d jemalloc

Summary:	General-purpose scalable concurrent malloc implementation
Name:		jemalloc
Version:	3.6.0
Release:	7
Group:		System/Libraries
License:	BSD
URL:		http://www.canonware.com/jemalloc/
Source0:	http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
# Remove pprof, as it already exists in google-perftools
Patch0:		jemalloc-3.5.0-no_pprof.patch
# ARMv5tel has no atomic operations
Patch1:		jemalloc-armv5-force-atomic.patch
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
%configure2_5x
%make

%check
make check

%install
%makeinstall_std

# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

%files -n %{libname}
%doc COPYING README VERSION
%doc doc/jemalloc.html
%{_libdir}/libjemalloc.so.%{major}*
%{_bindir}/jemalloc.sh

%files -n %{develname}
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*
