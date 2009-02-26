Summary:	SUite of Nonlinear and DIfferential/ALgebraic equation Solvers
Name:		sundials
Version:	2.3.0
Release:	0.1
License:	BSD
Group:		Applications/Math
Source0:	https://computation.llnl.gov/casc/sundials/download/code/%{name}-%{version}.tar.gz
# Source0-md5:	c236f2a7e0e6a03b8fab3d189471b933
#Patch0:		%{name}-DESTDIR.patch
URL:		https://computation.llnl.gov/casc/sundials/
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
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

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
# if not running libtool or automake, but config.sub is too old:
#cp -f /usr/share/automake/config.sub .
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
