Name:       harbour-simplecrop

# >> macros
%define __provides_exclude_from ^%{_datadir}/%{name}/lib/.*\\.so\\>
%define __requires_exclude_from ^%{_datadir}/%{name}/lib/.*\\.so\\>
# << macros

Summary:    Imageworks image editor
Version:    1.2.1
Release:    1
Group:      Qt/Qt
License:    GPLv3
URL:        https://github.com/poetaster/harbour-simplecrop
Source0:    %{name}-%{version}.tar.bz2
Requires:   sailfishsilica-qt5 >= 0.10.9
Requires:   pyotherside-qml-plugin-python3-qt5
#Requires:   python%{python3_version}(pillow) >= 8

#Requires:   python3-imaging
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  desktop-file-utils

%description
Image editing application for Sailfish OS.


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%qmake5 

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake5_install

# usefull for different post installs
%ifarch armv7hl
%endif
%ifarch aarch64
%endif

# usefull for post install jolla/chum
#%vendor chum

# >> install post
%ifnarch aarch64
install -D -t %{buildroot}/%{_datadir}/%{name}/lib/ \
    %{_libdir}/libjpeg.so.62 \
    %{_libdir}/libopenjp2.so.7 \
    %{_libdir}/libtiff.so.5 \
    %{_libdir}/libfreetype.so.6 \
    %{_libdir}/libwebpdemux.so.2 \
    %{_libdir}/libwebpmux.so.3 \
    %{_libdir}/libwebp.so.7
%endif
# << install post

# strip executable bit from all libraries
#chmod -x %{buildroot}%{_datadir}/%{name}/lib/*.so*

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%{_bindir}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%attr(644,root,root) %{_datadir}/%{name}/qml/py/graphx.py
# >> files
# << files
