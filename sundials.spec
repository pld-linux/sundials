Summary:	SUite of Nonlinear and DIfferential/ALgebraic equation Solvers
Name:		sundials
Version:	2.3.0
Release:	1
License:	BSD
Group:		Applications/Math
Source0:	https://computation.llnl.gov/casc/sundials/download/code/%{name}-%{version}.tar.gz
# Source0-md5:	c236f2a7e0e6a03b8fab3d189471b933
Patch0:		%{name}-DESTDIR.patch
URL:		https://computation.llnl.gov/casc/sundials/
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SUNDIALS (SUite of Nonlinear and DIfferential/ALgebraic equation Solvers)
consists of the following four solvers:

CVODE 	solves initial value problems for ordinary differential
	equation (ODE) systems.
CVODES 	solves ODE systems and includes sensitivity analysis
	capabilities (forward and adjoint).
IDA 	solves initial value problems for differential-algebraic
	equation (DAE) systems.
KINSOL 	solves nonlinear algebraic systems.

%prep
%setup -q
%patch0 -p1

%build
rm -f libtool ltmain.sh
cp -f /usr/share/libtool/config/ltmain.sh config
%{__aclocal}
%{__autoconf}
%configure \
	F77="gfortran" \
	--enable-shared \
	--disable-mpi \
	--enable-examples

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	EXS_INSTDIR=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sundials-config
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %ghost %{_libdir}/lib*.so.0
%attr(755,root,root) %ghost %{_libdir}/lib*.so.1
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_includedir}/*
%{_examplesdir}/%{name}-%{version}
