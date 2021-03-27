import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var homeDirectory
    property var origImageFileName
    property var origImageFolderPath
    property var tempImageFolderPath
    property var imageWidthSave
    property var imageHeightSave
    property var inputPathPy

    // variables for saving
    property var oldFileType
    property var oldFileName
    property var origImageFileNameArray
    property var savePath
    property var estimatedFileSize
    property var pageNumberMultiPDF : 0
    property var multiPdfPageNamesList : ""
    property bool validatorNameOverwrite : false

    // variables for warning overwrite
    property var estimatedFolder


    // autostart functions
    Component.onCompleted: {
        // get infos from the original file
        origImageFileNameArray = origImageFileName.split(".")
        oldFileName = (origImageFileNameArray.slice(0, origImageFileNameArray.length-1)).join(".")
        oldFileType = origImageFileNameArray[origImageFileNameArray.length - 1]
        if (oldFileType.indexOf('jpg') !== -1 || oldFileType.indexOf('jpeg') !== -1) {
            idComboBoxFileExtension.currentIndex = 0
        }
        else if (oldFileType.indexOf('png') !== -1) {
            idComboBoxFileExtension.currentIndex = 1
        }
        else if (oldFileType.indexOf('gif') !== -1) {
            idComboBoxFileExtension.currentIndex = 2
        }
        else if (oldFileType.indexOf('bmp') !== -1) {
            idComboBoxFileExtension.currentIndex = 3
        }
        else {
            // suggested file format if none of the above
            idComboBoxFileExtension.currentIndex = 0
        }
        py.getImageSizeFunction()
        py.getMultiPdfPagesFunction()
        //console.log(origImageFolderPath)
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
            setHandler('fileIsSaved', function() {
                idSaveButtonRunningIndicator.running = false
                idSaveButtonRunningIndicatorMultiPDF.running = false
                idSaveButton.enabled = true
                idSaveButtonMultiPDF.enabled = (pageNumberMultiPDF > 0) ? true : false
                idClearMultiPDFListButton.enabled = (pageNumberMultiPDF > 0) ? true : false
                pageStack.pop()
            });
            setHandler('fileMultiPagePdfIsAdded', function() {
                idSaveButtonRunningIndicator.running = false
                idSaveButton.enabled = true
                idSaveButtonMultiPDF.enabled = (pageNumberMultiPDF > 0) ? true : false
                idClearMultiPDFListButton.enabled = (pageNumberMultiPDF > 0) ? true : false
            });
            setHandler('getPagesMultiPDF', function(pagesCounter, pagesNamesList) {
                pageNumberMultiPDF = parseInt(pagesCounter)
                multiPdfPageNamesList = pagesNamesList
                idSaveButtonMultiPDF.enabled = (pageNumberMultiPDF > 0) ? true : false
                idClearMultiPDFListButton.enabled = (pageNumberMultiPDF > 0) ? true : false
            });
            setHandler('tempMultiPDFfilesDeleted', function( ) {
                idClearMultiPDFButtonRunningIndicator.running = false
            });
            setHandler('debugPythonLogs', function(i) {
                console.log(i)
            });




        }

        // file operations
        function saveFunction() {
            var folderSavePath
            if (idComboBoxTargetFolder.currentIndex === 0) {
                if (idComboBoxFileExtension.currentIndex === 5 || idComboBoxFileExtension.currentIndex === 4) {
                    folderSavePath = homeDirectory + "/Documents/"
                }
                else {
                    folderSavePath = origImageFolderPath
                }
            }
            else if (idComboBoxTargetFolder.currentIndex === 1) {
                folderSavePath = homeDirectory + "/Pictures" + "/Imageworks/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 2) {
                folderSavePath = homeDirectory + "/Pictures/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 3) {
                folderSavePath = homeDirectory + "/Downloads/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 4) {
                folderSavePath = homeDirectory + "/"
            }
            savePath = folderSavePath + idFilenameNew.text.toString() + idComboBoxFileExtension.value.toString()
            inputPathPy = ( "/" + inputPathPy.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") )
            var fileTargetType = idComboBoxFileExtension.value.toString()
            var pdfResolution = 300 //96
            call("graphx.saveNowFunction", [ inputPathPy, savePath, tempImageFolderPath, pdfResolution, fileTargetType ])
        }
        function getImageSizeFunction() {
            inputPathPy = decodeURIComponent( "/" + inputPathPy.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") )
            call("graphx.getImageSizeFunction", [ inputPathPy ])
        }



        function gatherMultiPagePdfFunction() {
            pageNumberMultiPDF = pageNumberMultiPDF + 1
            multiPdfPageNamesList = multiPdfPageNamesList + pageNumberMultiPDF + "-" + idFilenameNew.text.toString() + "\n"
            inputPathPy = ( inputPathPy.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") )
            call("graphx.gatherMultiPagePdfFunction", [ inputPathPy, pageNumberMultiPDF, multiPdfPageNamesList ])
        }
        function getMultiPdfPagesFunction() {
            call("graphx.getMultiPdfPagesFunction", [])
        }
        function deleteTempMultiPagePDF() {
            call("graphx.deleteTempMultiPagePDF", [ tempImageFolderPath ])
        }        
        function createMultiPagePDFFunction() {
            var folderSavePath
            if (idComboBoxTargetFolder.currentIndex === 0) {
                if (idComboBoxFileExtension.currentIndex === 5 || idComboBoxFileExtension.currentIndex === 4) {
                    folderSavePath = homeDirectory + "/Documents/"
                }
                else {
                    folderSavePath = origImageFolderPath
                }
            }
            else if (idComboBoxTargetFolder.currentIndex === 1) {
                folderSavePath = homeDirectory + "/Pictures" + "/Imageworks/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 2) {
                folderSavePath = homeDirectory + "/Pictures/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 3) {
                folderSavePath = homeDirectory + "/Downloads/"
            }
            else if (idComboBoxTargetFolder.currentIndex === 4) {
                folderSavePath = homeDirectory + "/"
            }
            savePath = folderSavePath + idFilenameMultiPDF.text.toString() + ".pdf"
            call("graphx.createMultiPagePDFFunction", [ savePath, tempImageFolderPath ])
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
        contentHeight: columnSaveAs.height  // Tell SilicaFlickable the height of its content
        VerticalScrollDecorator {}


        Column {
            id: columnSaveAs
            width: page.width

            PageHeader {
                title:  qsTr("Save as")
            }

            Row {
                width: parent.width
                TextField {
                    id: idFilenameNew
                    label: (validatorNameOverwrite === true) ? qsTr("overwrite...") : ""
                    enabled: (idComboBoxFileExtension.currentIndex !== 5)
                    width: parent.width / 6 * 3.75
                    anchors.top: parent.top
                    anchors.topMargin: Theme.paddingMedium
                    y: Theme.paddingSmall
                    inputMethodHints: Qt.ImhNoPredictiveText
                    text: oldFileName + "_edit"
                    EnterKey.onClicked: idFilenameNew.focus = false
                    // validator: RegExpValidator { regExp: /[a-zA-Z0-9äöüÄÖÜ_=()\/.!?#%+-]*$/ } // positive list
                    validator: RegExpValidator { regExp: /^[^<>'\"/;*:`#?]*$/ } // negative list

                    onTextChanged: {
                        checkOverwriting()
                    }
                }
                ComboBox {
                    id: idComboBoxFileExtension
                    width: parent.width / 6 * 1.25
                    menu: ContextMenu {
                        MenuItem {
                            text: ".jpg"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ".png"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ".gif"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ".bmp"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ".pdf"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "PDF+"
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                IconButton {
                    id: idSaveButton
                    visible: (idFilenameNew.text.length > 0) ? true : false
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    //icon.source: ( idComboBoxFileExtension.currentIndex != 5 ) ? "image://theme/icon-m-acknowledge?" : "image://theme/icon-m-add?"
                    icon.source: ( idComboBoxFileExtension.currentIndex != 5 ) ? "../symbols/icon-m-apply.svg" : "image://theme/icon-m-add?"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        idSaveButtonRunningIndicator.running = true
                        idSaveButton.enabled = false
                        idSaveButtonMultiPDF.enabled = false
                        idClearMultiPDFListButton.enabled = false
                        if (idComboBoxFileExtension.currentIndex != 5) {
                            py.saveFunction()
                        }
                        // if creating a multi-page PDF
                        else {
                            py.gatherMultiPagePdfFunction()
                        }
                    }
                    BusyIndicator {
                        id: idSaveButtonRunningIndicator
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }
            } // end row save filename

            Row {
                visible: (idComboBoxFileExtension.currentIndex === 5)
                width: parent.width
                TextField {
                    id: idFilenameMultiPDF
                    enabled: ( pageNumberMultiPDF > 0) ? true : false
                    width: parent.width / 6 * 3.75
                    anchors.top: parent.top
                    anchors.topMargin: Theme.paddingMedium
                    y: Theme.paddingSmall
                    inputMethodHints: Qt.ImhNoPredictiveText
                    text: "multipage"
                    EnterKey.onClicked: idFilenameNew.focus = false
                    validator: RegExpValidator { regExp: /[a-zA-Z0-9äöüÄÖÜ_=()\/.!?#+-]*$/ }
                }
                ComboBox {
                    enabled: false //( pageNumberMultiPDF > 0) ? true : false
                    id: idComboBoxFileExtensionMultiPDF
                    width: parent.width / 6 * 1.25
                    menu: ContextMenu {
                        MenuItem {
                            text: qsTr(".pdf")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                IconButton {
                    id: idSaveButtonMultiPDF
                    enabled: pageNumberMultiPDF > 0
                    visible: (idFilenameNew.text.length > 0) ? true : false
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        idSaveButtonRunningIndicatorMultiPDF.running = true
                        idSaveButton.enabled = false
                        idSaveButtonMultiPDF.enabled = false
                        py.createMultiPagePDFFunction()
                    }
                    BusyIndicator {
                        id: idSaveButtonRunningIndicatorMultiPDF
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }
            } // end row save filename

            ComboBox {
                id: idComboBoxTargetFolder
                width: parent.width
                menu: ContextMenu {
                    id: idCropShape
                    MenuItem {
                        text: (idComboBoxFileExtension.currentIndex === 5 || idComboBoxFileExtension.currentIndex === 4) ? qsTr("Documents") :  qsTr("Original Folder")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: "Pictures/Imageworks"
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: "Pictures"
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: "Downloads"
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: "/home"
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onCurrentItemChanged: {
                    checkOverwriting()
                }
            }
            SectionHeader {
                visible: (idComboBoxFileExtension.currentIndex === 5)
                text: "\n" + qsTr("Pages Contained")
            }
            Grid {
                visible: (idComboBoxFileExtension.currentIndex === 5)
                width: parent.width
                columns: 2
                Label {
                    id: idLabelMultiPagesListPDF
                    visible: (idComboBoxFileExtension.currentIndex === 5)
                    topPadding: Theme.iconSizeExtraSmall
                    leftPadding: Theme.paddingLarge
                    width: parent.width/6 * 5
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: multiPdfPageNamesList
                }
                IconButton {
                    id: idClearMultiPDFListButton
                    visible: pageNumberMultiPDF > 0
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "image://theme/icon-m-clear?"
                    onClicked: {
                        idClearMultiPDFButtonRunningIndicator.running = true
                        py.deleteTempMultiPagePDF()
                    }
                    BusyIndicator {
                        id: idClearMultiPDFButtonRunningIndicator
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }
            } // end row add multipage PDF
            Rectangle {
                visible: (idComboBoxFileExtension.currentIndex === 5)
                // spacer item
                width: parent.width
                height: Theme.iconSizeExtraSmall
                color: "transparent"
            }

            Label {
                x: Theme.paddingLarge * 1.2
                visible: (idComboBoxFileExtension.currentIndex !== 5) ? true : false
                width: parent.width - 2*Theme.paddingLarge
                font.pixelSize: Theme.fontSizeExtraSmall
                text: qsTr("Original Folder") + ": " + origImageFolderPath + "\n"
                        + qsTr("Width") + ": " + imageWidthSave + "\n"
                        + qsTr("Height") + ": " + imageHeightSave + "\n"
                        + qsTr("Size") + ": " + estimatedFileSize + " kb"
            }
            Label {
                id: idWarningTransparencySupport
                visible: (idComboBoxFileExtension.currentIndex === 1 || idComboBoxFileExtension.currentIndex === 5) ? false : true
                topPadding: Theme.iconSizeExtraSmall
                leftPadding: Theme.paddingLarge * 1.2
                width: parent.width - 2*Theme.paddingLarge
                font.pixelSize: Theme.fontSizeExtraSmall
                text: qsTr("Filetype does not support transparency.")
            }

        } // end Column

    } // end Silica Flickable


    function checkOverwriting() {
        if (idComboBoxTargetFolder.currentIndex === 0) {
            if (idComboBoxFileExtension.currentIndex === 5 || idComboBoxFileExtension.currentIndex === 4) {
                estimatedFolder = homeDirectory + "/Documents/"
            }
            else {
                estimatedFolder = origImageFolderPath
            }
        }
        else if (idComboBoxTargetFolder.currentIndex === 1) {
            estimatedFolder = homeDirectory + "/Pictures" + "/Imageworks/"
        }
        else if (idComboBoxTargetFolder.currentIndex === 2) {
            estimatedFolder = homeDirectory + "/Pictures/"
        }
        else if (idComboBoxTargetFolder.currentIndex === 3) {
            estimatedFolder = homeDirectory + "/Downloads/"
        }
        else if (idComboBoxTargetFolder.currentIndex === 4) {
            estimatedFolder = homeDirectory + "/"
        }

        if ( (estimatedFolder === origImageFolderPath ) && (oldFileName === idFilenameNew.text) && (("."+oldFileType) === (idComboBoxFileExtension.value.toString())) ) {
            validatorNameOverwrite = true
        }
        else {
            validatorNameOverwrite = false
        }
    }
}
