# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = harbour-simplecrop

CONFIG += sailfishapp

SOURCES += src/harbour-simplecrop.cpp \


DISTFILES += qml/harbour-simplecrop.qml \
    lib/arm64/PIL/BdfFontFile.py \
    lib/arm64/PIL/BlpImagePlugin.py \
    lib/arm64/PIL/BmpImagePlugin.py \
    lib/arm64/PIL/BufrStubImagePlugin.py \
    lib/arm64/PIL/ContainerIO.py \
    lib/arm64/PIL/CurImagePlugin.py \
    lib/arm64/PIL/DcxImagePlugin.py \
    lib/arm64/PIL/DdsImagePlugin.py \
    lib/arm64/PIL/EpsImagePlugin.py \
    lib/arm64/PIL/ExifTags.py \
    lib/arm64/PIL/FitsStubImagePlugin.py \
    lib/arm64/PIL/FliImagePlugin.py \
    lib/arm64/PIL/FontFile.py \
    lib/arm64/PIL/FpxImagePlugin.py \
    lib/arm64/PIL/FtexImagePlugin.py \
    lib/arm64/PIL/GbrImagePlugin.py \
    lib/arm64/PIL/GdImageFile.py \
    lib/arm64/PIL/GifImagePlugin.py \
    lib/arm64/PIL/GimpGradientFile.py \
    lib/arm64/PIL/GimpPaletteFile.py \
    lib/arm64/PIL/GribStubImagePlugin.py \
    lib/arm64/PIL/Hdf5StubImagePlugin.py \
    lib/arm64/PIL/IcnsImagePlugin.py \
    lib/arm64/PIL/IcoImagePlugin.py \
    lib/arm64/PIL/ImImagePlugin.py \
    lib/arm64/PIL/Image.py \
    lib/arm64/PIL/ImageChops.py \
    lib/arm64/PIL/ImageCms.py \
    lib/arm64/PIL/ImageColor.py \
    lib/arm64/PIL/ImageDraw.py \
    lib/arm64/PIL/ImageDraw2.py \
    lib/arm64/PIL/ImageEnhance.py \
    lib/arm64/PIL/ImageFile.py \
    lib/arm64/PIL/ImageFilter.py \
    lib/arm64/PIL/ImageFont.py \
    lib/arm64/PIL/ImageGrab.py \
    lib/arm64/PIL/ImageMath.py \
    lib/arm64/PIL/ImageMode.py \
    lib/arm64/PIL/ImageMorph.py \
    lib/arm64/PIL/ImageOps.py \
    lib/arm64/PIL/ImagePalette.py \
    lib/arm64/PIL/ImagePath.py \
    lib/arm64/PIL/ImageQt.py \
    lib/arm64/PIL/ImageSequence.py \
    lib/arm64/PIL/ImageShow.py \
    lib/arm64/PIL/ImageStat.py \
    lib/arm64/PIL/ImageTk.py \
    lib/arm64/PIL/ImageTransform.py \
    lib/arm64/PIL/ImageWin.py \
    lib/arm64/PIL/ImtImagePlugin.py \
    lib/arm64/PIL/IptcImagePlugin.py \
    lib/arm64/PIL/Jpeg2KImagePlugin.py \
    lib/arm64/PIL/JpegImagePlugin.py \
    lib/arm64/PIL/JpegPresets.py \
    lib/arm64/PIL/McIdasImagePlugin.py \
    lib/arm64/PIL/MicImagePlugin.py \
    lib/arm64/PIL/MpegImagePlugin.py \
    lib/arm64/PIL/MpoImagePlugin.py \
    lib/arm64/PIL/MspImagePlugin.py \
    lib/arm64/PIL/PSDraw.py \
    lib/arm64/PIL/PaletteFile.py \
    lib/arm64/PIL/PalmImagePlugin.py \
    lib/arm64/PIL/PcdImagePlugin.py \
    lib/arm64/PIL/PcfFontFile.py \
    lib/arm64/PIL/PcxImagePlugin.py \
    lib/arm64/PIL/PdfImagePlugin.py \
    lib/arm64/PIL/PdfParser.py \
    lib/arm64/PIL/PixarImagePlugin.py \
    lib/arm64/PIL/PngImagePlugin.py \
    lib/arm64/PIL/PpmImagePlugin.py \
    lib/arm64/PIL/PsdImagePlugin.py \
    lib/arm64/PIL/PyAccess.py \
    lib/arm64/PIL/SgiImagePlugin.py \
    lib/arm64/PIL/SpiderImagePlugin.py \
    lib/arm64/PIL/SunImagePlugin.py \
    lib/arm64/PIL/TarIO.py \
    lib/arm64/PIL/TgaImagePlugin.py \
    lib/arm64/PIL/TiffImagePlugin.py \
    lib/arm64/PIL/TiffTags.py \
    lib/arm64/PIL/WalImageFile.py \
    lib/arm64/PIL/WebPImagePlugin.py \
    lib/arm64/PIL/WmfImagePlugin.py \
    lib/arm64/PIL/XVThumbImagePlugin.py \
    lib/arm64/PIL/XbmImagePlugin.py \
    lib/arm64/PIL/XpmImagePlugin.py \
    lib/arm64/PIL/__init__.py \
    lib/arm64/PIL/__main__.py \
    lib/arm64/PIL/_binary.py \
    lib/arm64/PIL/_imaging.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_imagingcms.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_imagingft.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_imagingmath.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_imagingmorph.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_imagingtk.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/_tkinter_finder.py \
    lib/arm64/PIL/_util.py \
    lib/arm64/PIL/_version.py \
    lib/arm64/PIL/_webp.cpython-35m-aarch64-linux-gnu.so \
    lib/arm64/PIL/features.py \
    lib/arm64/Pillow-7.2.0.dist-info/LICENSE \
    lib/arm64/Pillow-7.2.0.dist-info/METADATA \
    lib/arm64/Pillow-7.2.0.dist-info/RECORD \
    lib/arm64/Pillow-7.2.0.dist-info/WHEEL \
    lib/arm64/Pillow-7.2.0.dist-info/top_level.txt \
    lib/arm64/Pillow-7.2.0.dist-info/zip-safe \
    lib/arm64/Pillow.libs/libXau-21870672.so.6.0.0 \
    lib/arm64/Pillow.libs/libfreetype-58427440.so.6.17.2 \
    lib/arm64/Pillow.libs/libjpeg-166ca757.so.9.4.0 \
    lib/arm64/Pillow.libs/liblcms2-d13186b2.so.2.0.10 \
    lib/arm64/Pillow.libs/liblzma-c28580a1.so.5.2.2 \
    lib/arm64/Pillow.libs/libopenjp2-2fc03407.so.2.3.1 \
    lib/arm64/Pillow.libs/libpng16-91e3a340.so.16.37.0 \
    lib/arm64/Pillow.libs/libtiff-4cf5e268.so.5.5.0 \
    lib/arm64/Pillow.libs/libwebp-85499e5a.so.7.1.0 \
    lib/arm64/Pillow.libs/libwebpdemux-d8ede030.so.2.0.6 \
    lib/arm64/Pillow.libs/libwebpmux-113e9fec.so.3.0.5 \
    lib/arm64/Pillow.libs/libxcb-ce05b0d3.so.1.1.0 \
    lib/arm64/Pillow.libs/libz-558a5e64.so.1.2.7 \
    qml/cover/CoverPage.qml \
    qml/pages/AboutPage.qml \
    qml/pages/ChannelBench.qml \
    qml/pages/CollageBench.qml \
    qml/pages/ColorcurveBench.qml \
    qml/pages/EffectsBench.qml \
    qml/pages/FilterBench.qml \
    qml/pages/FirstPage.qml \
    qml/pages/InfoPage.qml \
    qml/pages/MetadataPage.qml \
    qml/pages/NewPage.qml \
    qml/pages/PixelBench.qml \
    qml/pages/RenamePage.qml \
    qml/pages/SavePage.qml \
    qml/pages/ViewPage.qml \
    qml/pages/perspectivetransformhelper.js \
    rpm/harbour-simplecrop.changes.in \
    rpm/harbour-simplecrop.changes.run.in \
    rpm/harbour-simplecrop.spec \
    translations/*.ts \
    harbour-simplecrop.desktop \

SAILFISHAPP_ICONS = 86x86 108x108 128x128 172x172

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

# German translation is enabled as an example. If you aren't
# planning to localize your app, remember to comment out the
# following TRANSLATIONS line. And also do not forget to
# modify the localized app name in the the .desktop file.
TRANSLATIONS += translations/harbour-simplecrop-de.ts

HEADERS +=

# include library according to architecture (arm, i486_32bit, arm64)
#pil_static.path = lib/*

#equals(QT_ARCH, arm64): {
#  pil_static.files = lib/arm64/*
#  message("!!!architecture arm64 detected!!!");
#}
# for instance ffmpeg_static.path = /usr/share/harbour-clipper/lib/ffmpeg
# INSTALLS += pil_static

# include a static library
equals(QT_ARCH, i386): {
  python.files = lib/x86_32/*
  DISTFILES += lib/PIL/x86_32/PIL/* \
  message("!!!architecture x86 / 32bit detected!!!");
}
equals(QT_ARCH, arm): {
  python.files = lib/arm32/*
  DISTFILES += lib/arm32/PIL/* \
  message("!!!architecture armv7hl detected!!!");
}

python.path = "/usr/share/harbour-simplecrop/lib"
INSTALLS += python
