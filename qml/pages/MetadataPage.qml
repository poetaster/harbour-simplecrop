import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var origImageFileName
    property var origImageFolderPath
    property var inputPathPy

    // meta variables
    property var estimatedFileSize
    property var origImageFileNameArray
    property var fileName
    property var fileType
    property var imgDataFormat
    property var imgDataMode
    property var imgDataPalette
    property var imgDateWidth
    property var imgDataHeight
    property var imgDataExifFull
    property var metaPath


    // autostart functions
    Component.onCompleted: {
        // get infos from the original file
        py.getImageSizeFunction()
        py.getImageMetaDataFunction()
    }


    Python {
        id: py
        Component.onCompleted: {
            //addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            // Handlers = Signals to do something in QML whith received Infos from pyotherside.send
            setHandler('metaDataReceived', function( imgFormat, imgMode, imgPalette, imgWidth, imgHeight, imgExifFull ) {
                imgDataFormat = imgFormat
                imgDataMode = imgMode
                imgDataPalette = imgPalette
                imgDateWidth = imgWidth
                imgDataHeight = imgHeight

                if (imgExifFull === "This file contains no EXIF tags.") {
                    imgDataExifFull = qsTr("File contains no EXIF tags.")
                }
                else if (imgExifFull === "Filetype does not support EXIF tags.") {
                    imgDataExifFull = qsTr("Filetype does not support EXIF tags.")
                }
                else {imgDataExifFull = imgExifFull}
            });
            setHandler('estimatedFileSize', function(estimatedSize) {
                estimatedFileSize = Math.round ( (parseInt(estimatedSize)/1000) * 100) / 100
            });

        }

        // meta data operations
        function getImageSizeFunction() {
            metaPath = origImageFolderPath + origImageFileName
            call("graphx.getImageSizeFunction", [ metaPath ])
        }
        function getImageMetaDataFunction() {
            metaPath = origImageFolderPath + origImageFileName
            inputPathPy = "/" + inputPathPy.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"")
            call("graphx.getImageMetaDataFunction", [ metaPath ])
        }

        onError: {
            // when an exception is raised, this error handler will be called
            //console.log('python error: ' + traceback);
        }
        onReceived: {
            // asychronous messages from Python arrive here; done there via pyotherside.send()
            //console.log('got message from python: ' + data);
        }
    } // end Python


    SilicaFlickable {
        id: listView
        anchors.fill: parent
        contentHeight: columnSaveAs.height  // Tell SilicaFlickable the height of its content.
        VerticalScrollDecorator {}

        Column {
            id: columnSaveAs
            width: parent.width

            PageHeader {
                title: qsTr("Metadata")
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2*Theme.paddingLarge
                font.pixelSize: Theme.fontSizeExtraSmall
                wrapMode: Text.Wrap
                text:   qsTr("File") + ": " + origImageFileName + "\n"
                      + qsTr("Path") + ": " + origImageFolderPath + "\n"
                      + qsTr("Size") + ": " + estimatedFileSize + " kb" + "\n"
                      + qsTr("Width") + ": " + imgDateWidth + " px" + "\n"
                      + qsTr("Height") + ": " + imgDataHeight + " px" + "\n"
                      + qsTr("Format") + ": " + imgDataFormat + "\n"
                      + qsTr("Mode") + ": " + imgDataMode + "\n"
                      + qsTr("Palette") + ": " + imgDataPalette + "\n"
            }

            SectionHeader {
                text: "EXIF tags"
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                text: imgDataExifFull + "\n" + "\n"
            }

        } // end Column
    } // end Silica Flickable
}
