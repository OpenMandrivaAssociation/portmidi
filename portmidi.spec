%define	major 0
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Real-time MIDI input/output, audio I/O library
Name:		portmidi
Epoch:		1
Version:	217
Release:	3
License:	GPL
Group:		System/Libraries
URL:		http://portmedia.sourceforge.net
Source0:	http://downloads.sourceforge.net/portmedia/%{name}-src-%{version}.zip
Patch0:		portmidi-217-cmake-libdir-java-opts.patch
BuildRequires:	pkgconfig(alsa)
BuildRequires:	cmake

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
%makeinstall_std -C build

install -d %{buildroot}%{_bindir}
pushd build/release
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
%{_libdir}/*.so

%files -n %{develname}
%{_includedir}/*

%changelog
* Wed Mar 16 2011 Funda Wang <fwang@mandriva.org> 1:217-1mdv2011.0
+ Revision: 645495
- bump epoch
- new version 217
- add gentoo propsed patch to conditonal build java binding
- fix linkage

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 20070107-3mdv2009.0
+ Revision: 242328
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Jul 31 2007 Oden Eriksson <oeriksson@mandriva.com> 20070107-1mdv2008.0
+ Revision: 57170
- Import portmidi



* Tue Jul 31 2007 Oden Eriksson <oeriksson@mandriva.com> 20070107-1mdv2008.0
- initial Mandriva package
