%define		major	2
%define		veryoldlibname %mklibname %{name} 0
%define		oldlibname %mklibname %{name} 2
%define		libname	%mklibname %{name}
%define		jlibname	%mklibname pmjni
%define		develname	%mklibname -d %{name}

Summary:	Real-time MIDI input/output, audio I/O library
Name:		portmidi
Version:	2.0.4
Release:	2
License:	GPLv2+
Group:		Sound
Url:		https://github.com/PortMidi/portmidi
Source0:	https://github.com/PortMidi/portmidi/archive/refs/tags/%{name}-%{version}.tar.gz
#Patch0:	portmidi-2.0.3-disable-missing-test-program.patch
BuildRequires:	cmake >= 3.21
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	pkgconfig(alsa)
BuildRequires:	jdk-current

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
%doc CHANGELOG.txt license.txt
%{_bindir}/portmidi-fast
%{_bindir}/portmidi-fastrcv
%{_bindir}/portmidi-latency
%{_bindir}/portmidi-midiclock
%{_bindir}/portmidi-midithread
%{_bindir}/portmidi-midithru
%{_bindir}/portmidi-mm
%{_bindir}/portmidi-multivirtual
%{_bindir}/portmidi-recvvirtual
%{_bindir}/portmidi-sendvirtual
%{_bindir}/portmidi-sysex
%{_bindir}/portmidi-testio
%{_bindir}/portmidi-virttest
	
#-----------------------------------------------------------------------------
 
%package -n	%{libname}
Summary:		Real-time MIDI input/output, audio I/O library
Group:		System/Libraries
Conflicts:	%{_lib}portmidi-devel < %{EVRD}
%rename %{oldlibname}
Obsoletes: %{veryoldlibname}

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
Obsoletes:	%{name}-devel < %{EVRD}

%description -n	%{develname}
PortMidi -- real-time MIDI input/output. This package provides the development
libraries and headers for portmidi.

%files -n %{develname}
%doc CHANGELOG.txt license.txt
%doc github-portmidi-portmidi_docs/docs/*
%{_includedir}/*.h
%{_libdir}/libportmidi.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/PortMidi/*.cmake

#-----------------------------------------------------------------------------
 
%package -n	%{jlibname}
Summary:	Java interface to the PortMidi library
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n	%{jlibname}
Java interface to PortMidi -- real-time MIDI input/output.

%files -n %{jlibname}
%{_libdir}/libpmjni.so*

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

# Fix permissons issues:
find -name "*.c" -o -name "*.h" -exec chmod -x {} \;
chmod -x pm_linux/README_LINUX.txt

# Fix libdir in pkgconfig file template
sed -i 's|${prefix}\/lib|${prefixr}\/%{_lib}|g' packaging/%{name}.pc.in


%build
. /etc/profile.d/90java.sh

%cmake	-DCMAKE_CACHEFILE_DIR=`pwd`	\
	-DBUILD_JAVA_NATIVE_INTERFACE="ON" \
	-DBUILD_PORTMIDI_TESTS="ON" \
	-G Ninja

%ninja_build

# Make devel docs
doxygen ../Doxyfile


%install
%ninja_install -C build

install -d %{buildroot}%{_bindir}
pushd build/pm_test
	install -m0755 fast %{buildroot}%{_bindir}/portmidi-fast
	install -m0755 fastrcv %{buildroot}%{_bindir}/portmidi-fastrcv
	install -m0755 latency %{buildroot}%{_bindir}/portmidi-latency
	install -m0755 midiclock %{buildroot}%{_bindir}/portmidi-midiclock
	install -m0755 midithread %{buildroot}%{_bindir}/portmidi-midithread
	install -m0755 midithru %{buildroot}%{_bindir}/portmidi-midithru
	install -m0755 mm %{buildroot}%{_bindir}/portmidi-mm
	install -m0755 multivirtual %{buildroot}%{_bindir}/portmidi-multivirtual
	install -m0755 recvvirtual %{buildroot}%{_bindir}/portmidi-recvvirtual
	install -m0755 sendvirtual %{buildroot}%{_bindir}/portmidi-sendvirtual
	install -m0755 sysex %{buildroot}%{_bindir}/portmidi-sysex
	install -m0755 testio %{buildroot}%{_bindir}/portmidi-testio
	install -m0755 virttest %{buildroot}%{_bindir}/portmidi-virttest
popd
