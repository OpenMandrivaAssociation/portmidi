%define	major 0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Real-time MIDI input/output, audio I/O library
Name:		portmidi
Version:	234
Release:	3
License:	GPL
Group:		System/Libraries
URL:		https://portmedia.sourceforge.net
Source0:	https://nav.dl.sourceforge.net/project/portmedia/portmedia-code-r%{version}.zip
Patch0:		portmidi-217-cmake-libdir-java-opts.patch
Patch1:		portmidi-fix-soname-and-cflags.patch
BuildRequires:	pkgconfig(alsa)
BuildRequires:	cmake
BuildRequires:	ninja

%description
PortMidi -- real-time MIDI input/output.

This package provides test applications that utilizes the shared portmidi and
porttime libraries.


 * %{_bindir}/portmidi-latency
 * %{_bindir}/portmidi-midithread
 * %{_bindir}/portmidi-midithru
 * %{_bindir}/portmidi-sysex
 * %{_bindir}/portmidi-test

%package -n	%{libname}
Summary:	Real-time MIDI input/output, audio I/O library
Group:		System/Libraries
Conflicts:	%{_lib}portmidi-devel < %{version}

%description -n	%{libname}
PortMidi -- real-time MIDI input/output.

This package provides the shared libraries for portmidi and porttime.

%package -n	%{develname}
Summary:	Development files for PortMidi
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
PortMidi -- real-time MIDI input/output.

This package provides the development libraries and headers for portmidi and
porttime.

%prep
%autosetup -p1 -n portmedia-code-r%{version}/portmidi/trunk

%build
%cmake -DPORTMIDI_ENABLE_JAVA=OFF -DCMAKE_CACHEFILE_DIR=`pwd`
%make_build

%install
%make_install -C build

install -d %{buildroot}%{_bindir}
pushd build/RelWithDebInfo
install -m0755 latency %{buildroot}%{_bindir}/portmidi-latency
install -m0755 midithread %{buildroot}%{_bindir}/portmidi-midithread
install -m0755 midithru %{buildroot}%{_bindir}/portmidi-midithru
install -m0755 sysex %{buildroot}%{_bindir}/portmidi-sysex
install -m0755 test %{buildroot}%{_bindir}/portmidi-test
popd

%files
%{_bindir}/portmidi-latency
%{_bindir}/portmidi-midithread
%{_bindir}/portmidi-midithru
%{_bindir}/portmidi-sysex
%{_bindir}/portmidi-test

%files -n %{libname}
%doc CHANGELOG.txt README.txt license.txt portmusic_logo.png pm_cl/* pm_linux/README_LINUX.txt
%{_libdir}/*.so.*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
