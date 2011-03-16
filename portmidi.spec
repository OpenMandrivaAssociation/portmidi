%define	major 0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Real-time MIDI input/output, audio I/O library
Name:		portmidi
Epoch:		1
Version:	217
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://portmedia.sourceforge.net
Source0:	http://downloads.sourceforge.net/portmedia/%{name}-src-%{version}.zip
Patch0:		portmidi-217-cmake-libdir-java-opts.patch
BuildRequires:	libalsa-devel
BuildRequires:	cmake
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Conflicts:	%{_lib}portmidi-devel < %{epoch}:%{version}

%description -n	%{libname}
PortMidi -- real-time MIDI input/output.

This package provides the shared libraries for portmidi and porttime.

%package -n	%{develname}
Summary:	Development files for PortMidi
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-devel < %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}

%description -n	%{develname}
PortMidi -- real-time MIDI input/output.

This package provides the development libraries and headers for portmidi and
porttime.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .java

%build
%define Werror_cflags %nil
%cmake -DPORTMIDI_ENABLE_JAVA=OFF -DCMAKE_CACHEFILE_DIR=`pwd`
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

install -d %{buildroot}%{_bindir}
pushd build/release
install -m0755 latency %{buildroot}%{_bindir}/portmidi-latency
install -m0755 midithread %{buildroot}%{_bindir}/portmidi-midithread
install -m0755 midithru %{buildroot}%{_bindir}/portmidi-midithru
install -m0755 sysex %{buildroot}%{_bindir}/portmidi-sysex
install -m0755 test %{buildroot}%{_bindir}/portmidi-test
popd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/portmidi-latency
%{_bindir}/portmidi-midithread
%{_bindir}/portmidi-midithru
%{_bindir}/portmidi-sysex
%{_bindir}/portmidi-test

%files -n %{libname}
%defattr(-,root,root)
%doc CHANGELOG.txt README.txt license.txt portmusic_logo.png pm_cl/* pm_linux/README_LINUX.txt
%{_libdir}/*.so

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
