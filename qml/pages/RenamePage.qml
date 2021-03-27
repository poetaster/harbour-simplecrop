import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var origImageFileName
    property var origImageFolderPath
    property var tempImageFolderPath
    property var origImageFilePath
    property var imageWidthSave
    property var imageHeightSave
    property var inputPathPy

    // variables for saving
    property var oldFileType
    property var oldFileName
    property var origImageFileNameArray
    property var savePath
    property var estimatedFileSize



    // autostart functions
    Component.onCompleted: {
        // get infos from the original file
        origImageFileNameArray = origImageFileName.split(".")
        oldFileName = (origImageFileNameArray.slice(0, origImageFileNameArray.length-1)).join(".")
        oldFileType = origImageFileNameArray[origImageFileNameArray.length - 1]
        idComboBoxFileExtension.currentIndex = 0
        py.getImageSizeFunction()
    }



    Python {
        id: py
        Component.onCompleted: {
            //addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            // Handlers = Signals to do something in QML whith received Infos from pyotherside.send
            setHandler('tempFilesDeleted', function(i) {
                //console.log("temp files deleted: " + i)
            });
            setHandler('estimatedFileSize', function(estimatedSize) {
                estimatedFileSize = Math.round ( (parseInt(estimatedSize)/1000) * 100) / 100
            });

        }

        // file operations
        function getImageSizeFunction() {
            inputPathPy = decodeURIComponent( "/" + inputPathPy.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") )
            call("graphx.getImageSizeFunction", [ inputPathPy ])
        }

        function renameOriginalFunction() {
            if (origImageFileName !== undefined) {
                inputPathPy = origImageFilePath
                var renamedImageFilePath = origImageFolderPath + idFilenameNew.text + "." + oldFileType
                call("graphx.renameOriginalFunction", [ inputPathPy, renamedImageFilePath ])
            }
            else {
                console.log("image not loaded")
            }
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
            width: page.width

            PageHeader {
                title: qsTr("Rename as")
            }

            Row {
                width: parent.width
                TextField {
                    id: idFilenameNew
                    width: parent.width / 6 * 3.75
                    anchors.top: parent.top
                    anchors.topMargin: Theme.paddingMedium
                    y: Theme.paddingSmall
                    inputMethodHints: Qt.ImhNoPredictiveText
                    text: (origImageFileName !== undefined) ? oldFileName : "none"
                    EnterKey.onClicked: idFilenameNew.focus = false
                    //validator: RegExpValidator { regExp: /[a-zA-Z0-9äöüÄÖÜ_=().!?#%+-]*$/ }
                    validator: RegExpValidator { regExp: /^[^<>'\"/;*:`#?]*$/ } // negative list
                }
                ComboBox {
                    id: idComboBoxFileExtension
                    width: parent.width / 6 * 1.25
                    menu: ContextMenu {
                        MenuItem {
                            text: (origImageFileName !== undefined) ? ("." + oldFileType) : "???"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                IconButton {
                    visible: (idFilenameNew.text.length > 0) ? true : false
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        py.renameOriginalFunction()
                        pageStack.pop()
                    }
                }
            } // end row save filename

            Label {
                leftPadding: Theme.paddingLarge
                font.pixelSize: Theme.fontSizeSmall
                text: qsTr("Path") + ": " + origImageFolderPath + "\n"
                        + qsTr("Width") + ": " + imageWidthSave + "\n"
                        + qsTr("Height") + ": " + imageHeightSave + "\n"
                        + qsTr("Size") + ": " + estimatedFileSize + " kb"
                color: Theme.highlightColor
            }


        } // end Column


    } // end Silica Flickable
}
