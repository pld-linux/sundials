# TODO: MPI support
#
# Conditional build:
%bcond_without	openmp	# OpenMP support

Summary:	SUite of Nonlinear and DIfferential/ALgebraic equation Solvers
Summary(pl.UTF-8):	Zbiór procedur do rozwiązywania równań nieliniowych i różniczkowych/algebraicznych
Name:		sundials
Version:	2.6.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://computing.llnl.gov/sites/default/files/inline-files/%{name}-%{version}.tar.gz
# Source0-md5:	3deeb0ede9f514184c6bd83ecab77d95
Patch0:		%{name}-cmake.patch
URL:		https://computing.llnl.gov/projects/sundials
BuildRequires:	cmake >= 2.8.1
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers) consists of the following solvers:

ARKODE: solves ordinary differential equation (ODE) systems based on
Runge-Kutta methods.

CVODE: solves initial value problems for ordinary differential
equation (ODE) systems.

CVODES:	solves ODE systems and includes sensitivity analysis
capabilities (forward and adjoint).

IDA: solves initial value problems for differential-algebraic equation
(DAE) systems.

IDAS: solves differential-algebraic equation (DAE) systems with
sensitivity analysis.

KINSOL: solves nonlinear algebraic systems.

%description -l pl.UTF-8
SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers) to zbiór procedur do rozwiązywania równań nieliniowych i
różniczkowych/algebraicznych, składający się z czterech części:

ARKODE - rozwiązuje układy równań różniczkowych zwyczajnych (ODE) przy
użyciu metod Rungego-Kutty.

CVODE - rozwiązuje problemy wartości początkowej dla układów
równań różniczkowych zwyczajnych (ODE)

CVODES - rozwiązuje układy równań różniczkowych zwyczajnych; zawiera
funkcjonalność analizy wrażliwości (prostej i sprzężonej).

IDA - rozwiązuje problemy wartości początkowej dla układów równań
różniczkowo-algebraicznych (DAE).

IDAS - rozwiązuje układy równań różniczkowo-algebraicznych z analizą
wrażliwości.

KINSOL - rozwiązuje układy nieliniowych równań algebraicznych.

%package devel
Summary:	SUNDIALS development files
Summary(pl.UTF-8):	Pliki programistyczne SUNDIALS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and development files needed to
develop applications with SUNDIALS.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i programistyczne potrzebne do
tworzenia aplikacji z użyciem SUNDIALS.

%package static
Summary:	SUNDIALS static libraries
Summary(pl.UTF-8):	Biblioteki statyczne SUNDIALS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains SUNDIALS static libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki SUNDIALS.

%package apidocs
Summary:	API documentation for SUNDIALS libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek SUNDIALS
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SUNDIALS libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek SUNDIALS.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DEXAMPLES_INSTALL_PATH=%{_examplesdir}/%{name}-%{version} \
	-DFCMIX_ENABLE=ON \
	-DKLU_ENABLE=ON \
	-DLAPACK_ENABLE=ON \
	%{?with_openmp:-DOPENMP_ENABLE=ON} \
	-DPTHREAD_ENABLE=ON

# SUPERLUMT_ENABLE?

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libsundials_arkode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_arkode.so.1
%attr(755,root,root) %{_libdir}/libsundials_cvode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_cvode.so.1
%attr(755,root,root) %{_libdir}/libsundials_cvodes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_cvodes.so.2
%attr(755,root,root) %{_libdir}/libsundials_ida.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_ida.so.2
%attr(755,root,root) %{_libdir}/libsundials_idas.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_idas.so.0
%attr(755,root,root) %{_libdir}/libsundials_kinsol.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_kinsol.so.1
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_nvecopenmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecopenmp.so.0
%endif
%attr(755,root,root) %{_libdir}/libsundials_nvecpthreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecpthreads.so.0
%attr(755,root,root) %{_libdir}/libsundials_nvecserial.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecserial.so.0
# Fortran - shared
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecopenmp.so.0
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecpthreads.so.0
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecserial.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsundials_arkode.so
%attr(755,root,root) %{_libdir}/libsundials_cvode.so
%attr(755,root,root) %{_libdir}/libsundials_cvodes.so
%attr(755,root,root) %{_libdir}/libsundials_ida.so
%attr(755,root,root) %{_libdir}/libsundials_idas.so
%attr(755,root,root) %{_libdir}/libsundials_kinsol.so
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_nvecopenmp.so
%endif
%attr(755,root,root) %{_libdir}/libsundials_nvecpthreads.so
%attr(755,root,root) %{_libdir}/libsundials_nvecserial.so
# Fortran - shared
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp.so
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads.so
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial.so
# Fortran - static only
%{_libdir}/libsundials_farkode.a
%{_libdir}/libsundials_fcvode.a
%{_libdir}/libsundials_fida.a
%{_libdir}/libsundials_fkinsol.a
%{_libdir}/libsundials_fnvecserial.a
%{_includedir}/arkode
%{_includedir}/cvode
%{_includedir}/cvodes
%{_includedir}/ida
%{_includedir}/idas
%{_includedir}/kinsol
%{_includedir}/nvector
%{_includedir}/sundials
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libsundials_arkode.a
%{_libdir}/libsundials_cvode.a
%{_libdir}/libsundials_cvodes.a
%{_libdir}/libsundials_ida.a
%{_libdir}/libsundials_idas.a
%{_libdir}/libsundials_kinsol.a
%if %{with openmp}
%{_libdir}/libsundials_nvecopenmp.a
%endif
%{_libdir}/libsundials_nvecpthreads.a
%{_libdir}/libsundials_nvecserial.a
# Fortran
%if %{with openmp}
%{_libdir}/libsundials_fnvecopenmp.a
%endif
%{_libdir}/libsundials_fnvecpthreads.a
%{_libdir}/libsundials_fnvecserial.a

%files apidocs
%defattr(644,root,root,755)
%doc doc/*/*.pdf
