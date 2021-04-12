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
    lib/x86_32/PIL/BdfFontFile.py \
    lib/x86_32/PIL/BlpImagePlugin.py \
    lib/x86_32/PIL/BmpImagePlugin.py \
    lib/x86_32/PIL/BufrStubImagePlugin.py \
    lib/x86_32/PIL/ContainerIO.py \
    lib/x86_32/PIL/CurImagePlugin.py \
    lib/x86_32/PIL/DcxImagePlugin.py \
    lib/x86_32/PIL/DdsImagePlugin.py \
    lib/x86_32/PIL/EpsImagePlugin.py \
    lib/x86_32/PIL/ExifTags.py \
    lib/x86_32/PIL/FitsStubImagePlugin.py \
    lib/x86_32/PIL/FliImagePlugin.py \
    lib/x86_32/PIL/FontFile.py \
    lib/x86_32/PIL/FpxImagePlugin.py \
    lib/x86_32/PIL/FtexImagePlugin.py \
    lib/x86_32/PIL/GbrImagePlugin.py \
    lib/x86_32/PIL/GdImageFile.py \
    lib/x86_32/PIL/GifImagePlugin.py \
    lib/x86_32/PIL/GimpGradientFile.py \
    lib/x86_32/PIL/GimpPaletteFile.py \
    lib/x86_32/PIL/GribStubImagePlugin.py \
    lib/x86_32/PIL/Hdf5StubImagePlugin.py \
    lib/x86_32/PIL/IcnsImagePlugin.py \
    lib/x86_32/PIL/IcoImagePlugin.py \
    lib/x86_32/PIL/ImImagePlugin.py \
    lib/x86_32/PIL/Image.py \
    lib/x86_32/PIL/ImageChops.py \
    lib/x86_32/PIL/ImageCms.py \
    lib/x86_32/PIL/ImageColor.py \
    lib/x86_32/PIL/ImageDraw.py \
    lib/x86_32/PIL/ImageDraw2.py \
    lib/x86_32/PIL/ImageEnhance.py \
    lib/x86_32/PIL/ImageFile.py \
    lib/x86_32/PIL/ImageFilter.py \
    lib/x86_32/PIL/ImageFont.py \
    lib/x86_32/PIL/ImageGrab.py \
    lib/x86_32/PIL/ImageMath.py \
    lib/x86_32/PIL/ImageMode.py \
    lib/x86_32/PIL/ImageMorph.py \
    lib/x86_32/PIL/ImageOps.py \
    lib/x86_32/PIL/ImagePalette.py \
    lib/x86_32/PIL/ImagePath.py \
    lib/x86_32/PIL/ImageQt.py \
    lib/x86_32/PIL/ImageSequence.py \
    lib/x86_32/PIL/ImageShow.py \
    lib/x86_32/PIL/ImageStat.py \
    lib/x86_32/PIL/ImageTk.py \
    lib/x86_32/PIL/ImageTransform.py \
    lib/x86_32/PIL/ImageWin.py \
    lib/x86_32/PIL/ImtImagePlugin.py \
    lib/x86_32/PIL/IptcImagePlugin.py \
    lib/x86_32/PIL/Jpeg2KImagePlugin.py \
    lib/x86_32/PIL/JpegImagePlugin.py \
    lib/x86_32/PIL/JpegPresets.py \
    lib/x86_32/PIL/McIdasImagePlugin.py \
    lib/x86_32/PIL/MicImagePlugin.py \
    lib/x86_32/PIL/MpegImagePlugin.py \
    lib/x86_32/PIL/MpoImagePlugin.py \
    lib/x86_32/PIL/MspImagePlugin.py \
    lib/x86_32/PIL/PSDraw.py \
    lib/x86_32/PIL/PaletteFile.py \
    lib/x86_32/PIL/PalmImagePlugin.py \
    lib/x86_32/PIL/PcdImagePlugin.py \
    lib/x86_32/PIL/PcfFontFile.py \
    lib/x86_32/PIL/PcxImagePlugin.py \
    lib/x86_32/PIL/PdfImagePlugin.py \
    lib/x86_32/PIL/PdfParser.py \
    lib/x86_32/PIL/PixarImagePlugin.py \
    lib/x86_32/PIL/PngImagePlugin.py \
    lib/x86_32/PIL/PpmImagePlugin.py \
    lib/x86_32/PIL/PsdImagePlugin.py \
    lib/x86_32/PIL/PyAccess.py \
    lib/x86_32/PIL/SgiImagePlugin.py \
    lib/x86_32/PIL/SpiderImagePlugin.py \
    lib/x86_32/PIL/SunImagePlugin.py \
    lib/x86_32/PIL/TarIO.py \
    lib/x86_32/PIL/TgaImagePlugin.py \
    lib/x86_32/PIL/TiffImagePlugin.py \
    lib/x86_32/PIL/TiffTags.py \
    lib/x86_32/PIL/WalImageFile.py \
    lib/x86_32/PIL/WebPImagePlugin.py \
    lib/x86_32/PIL/WmfImagePlugin.py \
    lib/x86_32/PIL/XVThumbImagePlugin.py \
    lib/x86_32/PIL/XbmImagePlugin.py \
    lib/x86_32/PIL/XpmImagePlugin.py \
    lib/x86_32/PIL/__init__.py \
    lib/x86_32/PIL/__main__.py \
    lib/x86_32/PIL/__pycache__/BdfFontFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/BdfFontFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/BlpImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/BlpImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/BmpImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/BmpImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/BufrStubImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/BufrStubImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ContainerIO.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ContainerIO.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/CurImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/CurImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/DcxImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/DcxImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/DdsImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/DdsImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/EpsImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/EpsImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ExifTags.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ExifTags.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/FitsStubImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/FitsStubImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/FliImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/FliImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/FontFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/FontFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/FpxImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/FpxImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/FtexImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/FtexImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GbrImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GbrImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GdImageFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GdImageFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GifImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GifImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GimpGradientFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GimpGradientFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GimpPaletteFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GimpPaletteFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/GribStubImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/GribStubImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/Hdf5StubImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/Hdf5StubImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/IcnsImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/IcnsImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/IcoImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/IcoImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/Image.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/Image.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageChops.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageChops.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageCms.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageCms.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageColor.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageColor.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageDraw.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageDraw.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageDraw2.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageDraw2.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageEnhance.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageEnhance.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageFilter.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageFilter.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageFont.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageFont.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageGrab.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageGrab.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageMath.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageMath.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageMode.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageMode.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageMorph.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageMorph.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageOps.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageOps.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImagePalette.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImagePalette.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImagePath.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImagePath.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageQt.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageQt.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageSequence.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageSequence.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageShow.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageShow.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageStat.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageStat.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageTk.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageTk.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageTransform.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageTransform.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImageWin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImageWin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/ImtImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/ImtImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/IptcImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/IptcImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/Jpeg2KImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/Jpeg2KImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/JpegImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/JpegImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/JpegPresets.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/JpegPresets.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/McIdasImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/McIdasImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/MicImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/MicImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/MpegImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/MpegImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/MpoImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/MpoImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/MspImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/MspImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PSDraw.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PSDraw.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PaletteFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PaletteFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PalmImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PalmImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PcdImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PcdImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PcfFontFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PcfFontFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PcxImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PcxImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PdfImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PdfImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PdfParser.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PdfParser.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PixarImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PixarImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PngImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PngImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PpmImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PpmImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PsdImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PsdImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/PyAccess.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/PyAccess.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/SgiImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/SgiImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/SpiderImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/SpiderImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/SunImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/SunImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/TarIO.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/TarIO.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/TgaImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/TgaImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/TiffImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/TiffImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/TiffTags.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/TiffTags.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/WalImageFile.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/WalImageFile.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/WebPImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/WebPImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/WmfImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/WmfImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/XVThumbImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/XVThumbImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/XbmImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/XbmImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/XpmImagePlugin.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/XpmImagePlugin.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/__init__.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/__init__.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/__main__.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/__main__.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/_binary.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/_binary.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/_tkinter_finder.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/_tkinter_finder.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/_util.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/_util.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/_version.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/_version.cpython-38.pyc \
    lib/x86_32/PIL/__pycache__/features.cpython-38.opt-1.pyc \
    lib/x86_32/PIL/__pycache__/features.cpython-38.pyc \
    lib/x86_32/PIL/_binary.py \
    lib/x86_32/PIL/_imaging.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/_imagingft.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/_imagingmath.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/_imagingmorph.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/_imagingtk.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/_tkinter_finder.py \
    lib/x86_32/PIL/_util.py \
    lib/x86_32/PIL/_version.py \
    lib/x86_32/PIL/_webp.cpython-38-i386-linux-gnu.so \
    lib/x86_32/PIL/features.py \
    lib/x86_32/Pillow-7.1.2-py3.8.egg-info/PKG-INFO \
    lib/x86_32/Pillow-7.1.2-py3.8.egg-info/SOURCES.txt \
    lib/x86_32/Pillow-7.1.2-py3.8.egg-info/dependency_links.txt \
    lib/x86_32/Pillow-7.1.2-py3.8.egg-info/top_level.txt \
    lib/x86_32/Pillow-7.1.2-py3.8.egg-info/zip-safe \
    qml/cover/CoverPage.qml \
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
    qml/pages/SharePage.qml \
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
RANSLATIONS += translations/harbour-simplecrop-de.ts

HEADERS +=

# include library according to architecture (arm, i486_32bit, arm64)
#pil_static.path = lib/*

#equals(QT_ARCH, arm): {
#  pil_static.path = lib/*
#  message("!!!architecture armv7hl detected!!!");
#}
#equals(QT_ARCH, i386): {
#  pil_static.path = lib/x86_32/*
#  message("!!!architecture x86 / 32bit detected!!!");
#}
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
  python.files = lib/arm/*
  DISTFILES += lib/arm/PIL/* \
  message("!!!architecture armv7hl detected!!!");
}

python.path = "/usr/share/harbour-simplecrop/lib"
INSTALLS += python
