Name:           farstream
Version:        0.2.7
Release:        1
Summary:        Libraries for video conferencing applications
Group:          System/Libraries
License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/Farstream
Source0:        http://freedesktop.org/software/farstream/releases/farstream/%{name}-%{version}.tar.gz
Source1:        runTest.sh
Source2:        mktests.sh
Patch0:         nemo-tests-install.patch
BuildRequires:  python
BuildRequires:  pkgconfig(nice) >= 0.1.0
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

%description
A collection of GStreamer modules and libraries for video conferencing applications

%package        devel
Summary:        Development files for video conferencing applications
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
A collection of GStreamer modules and libraries for video conferencing applications

%package        tests
Summary:        Tests and tests.xml for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    tests
Testpackage for automated tests with tests and tests.xml

%prep
%setup -q -n %{name}-%{version}/%{name}

# nemo-tests-install.patch
%patch0 -p1

# install the mktests.sh to generate the tests.xml
%__cp $RPM_SOURCE_DIR/mktests.sh tests/
%__chmod 0755 tests/mktests.sh

%build
%autogen --disable-python --disable-static --disable-introspection --disable-gtk-doc

make %{?_smp_mflags}
tests/mktests.sh > tests/tests.xml

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -m 0755 $RPM_SOURCE_DIR/runTest.sh $RPM_BUILD_ROOT/opt/tests/%{name}/bin/runTest.sh
install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/%{name}/tests.xml

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS AUTHORS
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}-0.2
%{_libdir}/%{name}-0.2/*.so
%{_libdir}/gstreamer-1.0/*.so
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/0.2
%dir %{_datadir}/%{name}/0.2/fsrtpconference
%dir %{_datadir}/%{name}/0.2/fsrawconference
%{_datadir}/%{name}/0.2/fsrtpconference/default-codec-preferences
%{_datadir}/%{name}/0.2/fsrtpconference/default-element-properties
%{_datadir}/%{name}/0.2/fsrawconference/default-element-properties

%files devel
%defattr(-,root,root,-)
%{_libdir}/libfarstream-0.2.so
%{_libdir}/pkgconfig/%{name}-0.2.pc
%{_includedir}/%{name}-0.2/%{name}/
%if 0%{?with_docs}
%{_datadir}/gtk-doc/html/%{name}-libs-0.10/
%{_datadir}/gtk-doc/html/%{name}-plugins-0.1/
%endif

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*

