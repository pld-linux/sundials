# TODO:
# CUDA + RAJA (on bconds)
# MPI support
# MAGMA support
# ONEMKL support
# SUPERLUDIST support
# HYPRE (BR: hypre-devel)
# OPENMP_DEVICE
# PETSC (BR: petsc-devel)
# SUPERLUMT http://crd-legacy.lbl.gov/~xiaoye/SuperLU/#superlu_mt
# TRILINOS support
# XBRAID support
#
# Conditional build:
%bcond_without	openmp	# OpenMP support

Summary:	SUite of Nonlinear and DIfferential/ALgebraic equation Solvers
Summary(pl.UTF-8):	Zbiór procedur do rozwiązywania równań nieliniowych i różniczkowych/algebraicznych
Name:		sundials
Version:	5.8.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://computing.llnl.gov/projects/sundials/sundials-software
Source0:	https://github.com/LLNL/sundials/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a087032a72127c12e162bfe4405b03cd
Patch0:		%{name}-fortran.patch
Patch1:		%{name}-link.patch
URL:		https://computing.llnl.gov/projects/sundials
BuildRequires:	SuiteSparse-KLU-devel
BuildRequires:	cmake >= 3.12
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
%patch1 -p1

# duplicate of cvodes/ckpng.pdf
%{__rm} doc/idas/ckpnt.pdf

%build
install -d build
cd build
%cmake .. \
	-DBUILD_FORTRAN_MODULE_INTERFACE=ON \
	-DBUILD_FORTRAN77_INTERFACE=ON \
	-DENABLE_KLU=ON \
	-DENABLE_LAPACK=ON \
	%{?with_openmp:-DENABLE_OPENMP=ON -DOpenMP_gcc_s_LIBRARY=/%{_lib}/libgcc_s.so} \
	-DENABLE_PTHREAD=ON \
	-DEXAMPLES_INSTALL_PATH=%{_examplesdir}/%{name}-%{version} \
	-DFortran_INSTALL_MODDIR=%{_includedir}/sundials_fortran \
	-DKLU_INCLUDE_DIR=%{_includedir}/suitesparse \
	-DKLU_LIBRARY_DIR=%{_libdir}

%{__make} -j1

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
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libsundials_arkode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_arkode.so.4
%attr(755,root,root) %{_libdir}/libsundials_cvode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_cvode.so.5
%attr(755,root,root) %{_libdir}/libsundials_cvodes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_cvodes.so.5
%attr(755,root,root) %{_libdir}/libsundials_generic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_generic.so.5
%attr(755,root,root) %{_libdir}/libsundials_ida.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_ida.so.5
%attr(755,root,root) %{_libdir}/libsundials_idas.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_idas.so.4
%attr(755,root,root) %{_libdir}/libsundials_kinsol.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_kinsol.so.5
%attr(755,root,root) %{_libdir}/libsundials_nvecmanyvector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecmanyvector.so.5
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_nvecopenmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecopenmp.so.5
%endif
%attr(755,root,root) %{_libdir}/libsundials_nvecpthreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecpthreads.so.5
%attr(755,root,root) %{_libdir}/libsundials_nvecserial.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_nvecserial.so.5
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolband.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsoldense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsoldense.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolklu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolklu.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsollapackband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsollapackband.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsollapackdense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsollapackdense.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolpcg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolpcg.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspbcgs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolspbcgs.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspfgmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolspfgmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspgmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolspgmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolsptfqmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunlinsolsptfqmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunmatrixband.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixdense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunmatrixdense.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixsparse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunmatrixsparse.so.3
%attr(755,root,root) %{_libdir}/libsundials_sunnonlinsolfixedpoint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunnonlinsolfixedpoint.so.2
%attr(755,root,root) %{_libdir}/libsundials_sunnonlinsolnewton.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_sunnonlinsolnewton.so.2

# Fortran 77 - shared
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecopenmp.so.5
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecpthreads.so.5
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecserial.so.5
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolband.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsoldense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsoldense.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolklu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolklu.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsollapackband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsollapackband.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsollapackdense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsollapackdense.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolpcg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolpcg.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspbcgs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspbcgs.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspfgmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspfgmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspgmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspgmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolsptfqmr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolsptfqmr.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixband.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixdense.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixdense.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixsparse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixsparse.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolfixedpoint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunnonlinsolfixedpoint.so.2
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolnewton.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunnonlinsolnewton.so.2

# Fortran 90/2003
%attr(755,root,root) %{_libdir}/libsundials_farkode_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_farkode_mod.so.4
%attr(755,root,root) %{_libdir}/libsundials_fcvode_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fcvode_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fcvodes_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fcvodes_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fida_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fida_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fidas_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fidas_mod.so.4
%attr(755,root,root) %{_libdir}/libsundials_fkinsol_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fkinsol_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fnvecmanyvector_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecmanyvector_mod.so.5
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecopenmp_mod.so.5
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecpthreads_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fnvecserial_mod.so.5
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolband_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolband_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsoldense_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsoldense_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolklu_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolklu_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolpcg_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolpcg_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspbcgs_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspbcgs_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspfgmr_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspfgmr_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspgmr_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolspgmr_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolsptfqmr_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunlinsolsptfqmr_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixband_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixband_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixdense_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixdense_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixsparse_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunmatrixsparse_mod.so.3
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolfixedpoint_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunnonlinsolfixedpoint_mod.so.2
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolnewton_mod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsundials_fsunnonlinsolnewton_mod.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsundials_arkode.so
%attr(755,root,root) %{_libdir}/libsundials_cvode.so
%attr(755,root,root) %{_libdir}/libsundials_cvodes.so
%attr(755,root,root) %{_libdir}/libsundials_ida.so
%attr(755,root,root) %{_libdir}/libsundials_idas.so
%attr(755,root,root) %{_libdir}/libsundials_generic.so
%attr(755,root,root) %{_libdir}/libsundials_kinsol.so
%attr(755,root,root) %{_libdir}/libsundials_nvecmanyvector.so
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_nvecopenmp.so
%endif
%attr(755,root,root) %{_libdir}/libsundials_nvecpthreads.so
%attr(755,root,root) %{_libdir}/libsundials_nvecserial.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolband.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsoldense.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolklu.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsollapackband.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsollapackdense.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolpcg.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspbcgs.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspfgmr.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolspgmr.so
%attr(755,root,root) %{_libdir}/libsundials_sunlinsolsptfqmr.so
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixband.so
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixdense.so
%attr(755,root,root) %{_libdir}/libsundials_sunmatrixsparse.so
%attr(755,root,root) %{_libdir}/libsundials_sunnonlinsolfixedpoint.so
%attr(755,root,root) %{_libdir}/libsundials_sunnonlinsolnewton.so
%{_includedir}/arkode
%{_includedir}/cvode
%{_includedir}/cvodes
%{_includedir}/ida
%{_includedir}/idas
%{_includedir}/kinsol
%{_includedir}/nvector
%{_includedir}/sundials
%{_includedir}/sunlinsol
%{_includedir}/sunmatrix
%{_includedir}/sunnonlinsol
%{_libdir}/cmake/sundials
%{_examplesdir}/%{name}-%{version}

# Fortran 77 - shared
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp.so
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads.so
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolband.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsoldense.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolklu.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsollapackband.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsollapackdense.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolpcg.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspbcgs.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspfgmr.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspgmr.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolsptfqmr.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixband.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixdense.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixsparse.so
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolfixedpoint.so
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolnewton.so
# Fortran 77 - static only
%{_libdir}/libsundials_farkode.a
%{_libdir}/libsundials_fcvode.a
%{_libdir}/libsundials_fida.a
%{_libdir}/libsundials_fkinsol.a
%{_libdir}/libsundials_fnvecserial.a

# Fortran 90/2003
%attr(755,root,root) %{_libdir}/libsundials_farkode_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fcvode_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fcvodes_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fida_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fidas_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fkinsol_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fnvecmanyvector_mod.so
%if %{with openmp}
%attr(755,root,root) %{_libdir}/libsundials_fnvecopenmp_mod.so
%endif
%attr(755,root,root) %{_libdir}/libsundials_fnvecpthreads_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fnvecserial_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolband_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsoldense_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolklu_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolpcg_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspbcgs_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspfgmr_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolspgmr_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunlinsolsptfqmr_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixband_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixdense_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunmatrixsparse_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolfixedpoint_mod.so
%attr(755,root,root) %{_libdir}/libsundials_fsunnonlinsolnewton_mod.so
%{_includedir}/sundials_fortran

%files static
%defattr(644,root,root,755)
%{_libdir}/libsundials_arkode.a
%{_libdir}/libsundials_cvode.a
%{_libdir}/libsundials_cvodes.a
%{_libdir}/libsundials_generic.a
%{_libdir}/libsundials_ida.a
%{_libdir}/libsundials_idas.a
%{_libdir}/libsundials_kinsol.a
%{_libdir}/libsundials_nvecmanyvector.a
%if %{with openmp}
%{_libdir}/libsundials_nvecopenmp.a
%endif
%{_libdir}/libsundials_nvecpthreads.a
%{_libdir}/libsundials_nvecserial.a
%{_libdir}/libsundials_sunlinsolband.a
%{_libdir}/libsundials_sunlinsoldense.a
%{_libdir}/libsundials_sunlinsolklu.a
%{_libdir}/libsundials_sunlinsollapackband.a
%{_libdir}/libsundials_sunlinsollapackdense.a
%{_libdir}/libsundials_sunlinsolpcg.a
%{_libdir}/libsundials_sunlinsolspbcgs.a
%{_libdir}/libsundials_sunlinsolspfgmr.a
%{_libdir}/libsundials_sunlinsolspgmr.a
%{_libdir}/libsundials_sunlinsolsptfqmr.a
%{_libdir}/libsundials_sunmatrixband.a
%{_libdir}/libsundials_sunmatrixdense.a
%{_libdir}/libsundials_sunmatrixsparse.a
%{_libdir}/libsundials_sunnonlinsolfixedpoint.a
%{_libdir}/libsundials_sunnonlinsolnewton.a

# Fortran 77
%if %{with openmp}
%{_libdir}/libsundials_fnvecopenmp.a
%endif
%{_libdir}/libsundials_fnvecpthreads.a
%{_libdir}/libsundials_fnvecserial.a
%{_libdir}/libsundials_fsunlinsolband.a
%{_libdir}/libsundials_fsunlinsoldense.a
%{_libdir}/libsundials_fsunlinsolklu.a
%{_libdir}/libsundials_fsunlinsollapackband.a
%{_libdir}/libsundials_fsunlinsollapackdense.a
%{_libdir}/libsundials_fsunlinsolpcg.a
%{_libdir}/libsundials_fsunlinsolspbcgs.a
%{_libdir}/libsundials_fsunlinsolspfgmr.a
%{_libdir}/libsundials_fsunlinsolspgmr.a
%{_libdir}/libsundials_fsunlinsolsptfqmr.a
%{_libdir}/libsundials_fsunmatrixband.a
%{_libdir}/libsundials_fsunmatrixdense.a
%{_libdir}/libsundials_fsunmatrixsparse.a
%{_libdir}/libsundials_fsunnonlinsolfixedpoint.a
%{_libdir}/libsundials_fsunnonlinsolnewton.a

# Fortran 90/2003
%{_libdir}/libsundials_farkode_mod.a
%{_libdir}/libsundials_fcvode_mod.a
%{_libdir}/libsundials_fcvodes_mod.a
%{_libdir}/libsundials_fida_mod.a
%{_libdir}/libsundials_fidas_mod.a
%{_libdir}/libsundials_fkinsol_mod.a
%{_libdir}/libsundials_fnvecmanyvector_mod.a
%if %{with openmp}
%{_libdir}/libsundials_fnvecopenmp_mod.a
%endif
%{_libdir}/libsundials_fnvecpthreads_mod.a
%{_libdir}/libsundials_fnvecserial_mod.a
%{_libdir}/libsundials_fsunlinsolband_mod.a
%{_libdir}/libsundials_fsunlinsoldense_mod.a
%{_libdir}/libsundials_fsunlinsolklu_mod.a
%{_libdir}/libsundials_fsunlinsolpcg_mod.a
%{_libdir}/libsundials_fsunlinsolspbcgs_mod.a
%{_libdir}/libsundials_fsunlinsolspfgmr_mod.a
%{_libdir}/libsundials_fsunlinsolspgmr_mod.a
%{_libdir}/libsundials_fsunlinsolsptfqmr_mod.a
%{_libdir}/libsundials_fsunmatrixband_mod.a
%{_libdir}/libsundials_fsunmatrixdense_mod.a
%{_libdir}/libsundials_fsunmatrixsparse_mod.a
%{_libdir}/libsundials_fsunnonlinsolfixedpoint_mod.a
%{_libdir}/libsundials_fsunnonlinsolnewton_mod.a

%files apidocs
%defattr(644,root,root,755)
%doc doc/*/*.pdf
