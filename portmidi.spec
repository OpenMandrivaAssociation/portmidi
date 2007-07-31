%define version 20070107

%define	major 0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	PortMidi -- real-time MIDI input/output, audio I/O library
Name:		portmidi
Version:	%{version}
Release:	%mkrel 1
License:	GPL
Group:		System/Libraries
URL:		http://www-2.cs.cmu.edu/~music/portmusic/
Source0:	http://www.cs.cmu.edu/~music/portmusic/portmidi/portmidi17Jan07.zip
Patch0:		portmidi-shared.diff
BuildRequires:	libalsa-devel >= 0.9
BuildRequires:	dos2unix
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
Summary:	PortMidi -- real-time MIDI input/output, audio I/O library
Group:		System/Libraries

%description -n	%{libname}
PortMidi -- real-time MIDI input/output.

This package provides the shared libraries for portmidi and porttime.

%package -n	%{develname}
Summary:	Development files for PortMidi
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
PortMidi -- real-time MIDI input/output.

This package provides the development libraries and headers for portmidi and
porttime.

%prep

%setup -q -n %{name}

# strip away annoying ^M
find -type f | xargs dos2unix -U

%patch0 -p0

cp pm_linux/Makefile .

# fix attribs
chmod 644 CHANGELOG.txt README.txt license.txt portmusic_logo.png pm_cl/* pm_linux/README_LINUX.txt

%build

%make CFLAGS="%{optflags} -fPIC" PMFLAGS="-DNEWBUFFER"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}

install -m0755 pm_test/latency %{buildroot}%{_bindir}/portmidi-latency
install -m0755 pm_test/midithread %{buildroot}%{_bindir}/portmidi-midithread
install -m0755 pm_test/midithru %{buildroot}%{_bindir}/portmidi-midithru
install -m0755 pm_test/sysex %{buildroot}%{_bindir}/portmidi-sysex
install -m0755 pm_test/test %{buildroot}%{_bindir}/portmidi-test

install -m0755 pm_linux/libportmidi.so.0.17 %{buildroot}%{_libdir}/
ln -snf libportmidi.so.0.17 %{buildroot}%{_libdir}/libportmidi.so.0
ln -snf libportmidi.so.0.17 %{buildroot}%{_libdir}/libportmidi.so

install -m0755 porttime/libporttime.so.0.17 %{buildroot}%{_libdir}/
ln -snf libporttime.so.0.17 %{buildroot}%{_libdir}/libporttime.so.0
ln -snf libporttime.so.0.17 %{buildroot}%{_libdir}/libporttime.so

install -m0644 pm_common/%{name}.h %{buildroot}%{_includedir}/
install -m0644 porttime/porttime.h %{buildroot}%{_includedir}/

install -m0644 pm_linux/libportmidi.a %{buildroot}%{_libdir}
install -m0644 porttime/libporttime.a %{buildroot}%{_libdir}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

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
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
