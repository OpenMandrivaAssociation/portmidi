# Java interface is discontinued since 2021
%bcond_with	java

%define		major	2
%define		veryoldlibname %mklibname %{name} 0
%define		oldlibname %mklibname %{name} 2
%define		libname	%mklibname %{name}
%define		jlibname	%mklibname pmjni
%define		develname	%mklibname -d %{name}

Summary:	Real-time MIDI input/output, audio I/O library
Name:		portmidi
Version:	2.0.8
Release:	1
Epoch:	1
License:	GPLv2+
Group:		Sound
Url:		https://github.com/PortMidi/portmidi
Source0:	https://github.com/PortMidi/portmidi/archive/refs/tags/%{name}-%{version}.tar.gz
Patch0:	portmidi-2.0.8-fix-version-in-CMakeList-file.patch
BuildRequires:	cmake >= 3.21
BuildRequires:	jdk-current
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	pkgconfig(alsa)

%description
PortMidi -- real-time MIDI input/output. This package provides test
applications that utilize the portmidi library; among them:
 * portmidi-latency;
 * portmidi-midithread;
 * portmidi-midithru;
 * portmidi-mm;
 * portmidi-sysex;
 * portmidi-testio;
 * portmidi-virttest.

%files
%license license.txt
%doc CHANGELOG.txt
%{_bindir}/%{name}-fast
%{_bindir}/%{name}-fastrcv
%{_bindir}/%{name}-latency
%{_bindir}/%{name}-midiclock
%{_bindir}/%{name}-midithread
%{_bindir}/%{name}-midithru
%{_bindir}/%{name}-mm
%{_bindir}/%{name}-multivirtual
%{_bindir}/%{name}-recvvirtual
%{_bindir}/%{name}-sendvirtual
%{_bindir}/%{name}-sysex
%{_bindir}/%{name}-testio
%{_bindir}/%{name}-virttest
	
#-----------------------------------------------------------------------------
 
%package -n	%{libname}
Summary:		Real-time MIDI input/output, audio I/O library
Group:		System/Libraries
Conflicts:	%{_lib}portmidi-devel < %{EVRD}
%rename %{oldlibname}
#Obsoletes: %%{veryoldlibname}
%if %{without java}
%rename %{jlibname}
%endif

%description -n	%{libname}
PortMidi -- real-time MIDI input/output. This package provides the shared
library.

%files -n %{libname}
%doc CHANGELOG.txt README.md license.txt portmusic_logo.png pm_linux/README_LINUX.txt
%{_libdir}/libportmidi.so.%{major}*

#-----------------------------------------------------------------------------

%package -n	%{develname}
Summary:	Development files for PortMidi
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:		%{name}-devel < %{EVRD}

%description -n	%{develname}
PortMidi -- real-time MIDI input/output. This package provides the development
libraries and headers for %{name}.

%files -n %{develname}
%doc CHANGELOG.txt license.txt
%doc build/docs/*
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/PortMidi/*.cmake

#-----------------------------------------------------------------------------

%if %{with java}
%package -n	%{jlibname}
Summary:	Java interface to the PortMidi library
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n	%{jlibname}
Java interface to PortMidi -- real-time MIDI input/output.

%files -n %{jlibname}
%{_libdir}/libpmjni.so*
%endif

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

# Fix permissons issues:
find -name "*.c" -o -name "*.h" -exec chmod -x {} \;
chmod -x pm_linux/README_LINUX.txt


%build
%if %{with java}
. /etc/profile.d/90java.sh
%endif

%cmake	-DCMAKE_CACHEFILE_DIR=`pwd`	\
%if %{with java}
	-DBUILD_JAVA_NATIVE_INTERFACE="ON" \
%else
	-DBUILD_JAVA_NATIVE_INTERFACE="OFF" \
%endif
	-DBUILD_PORTMIDI_TESTS="ON" \
	-DBUILD_DOC="ON" \
	-G Ninja

%ninja_build


%install
%ninja_install -C build

install -d %{buildroot}%{_bindir}
pushd build/pm_test
	install -m0755 fast %{buildroot}%{_bindir}/%{name}-fast
	install -m0755 fastrcv %{buildroot}%{_bindir}/%{name}-fastrcv
	install -m0755 latency %{buildroot}%{_bindir}/%{name}-latency
	install -m0755 midiclock %{buildroot}%{_bindir}/%{name}-midiclock
	install -m0755 midithread %{buildroot}%{_bindir}/%{name}-midithread
	install -m0755 midithru %{buildroot}%{_bindir}/%{name}-midithru
	install -m0755 mm %{buildroot}%{_bindir}/%{name}-mm
	install -m0755 multivirtual %{buildroot}%{_bindir}/%{name}-multivirtual
	install -m0755 recvvirtual %{buildroot}%{_bindir}/%{name}-recvvirtual
	install -m0755 sendvirtual %{buildroot}%{_bindir}/%{name}-sendvirtual
	install -m0755 sysex %{buildroot}%{_bindir}/%{name}-sysex
	install -m0755 testio %{buildroot}%{_bindir}/%{name}-testio
	install -m0755 virttest %{buildroot}%{_bindir}/%{name}-virttest
popd
