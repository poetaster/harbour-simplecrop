import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var tempImageFolderPath
    property var myColors
    property var maxScalePixels
    property int copyPasteImageWidth
    property int copyPasteImageHeight

    // variables for saving
    property var fileName : "empty.tmp.png"
    property var newImageSizeX
    property var newImageSizeY
    property var paintToolColor : "white"

    // other variables
    property var oldTextfieldWidth
    property var oldTextfieldHeight

    Component.onCompleted: {
        newImageSizeY = (page.width).toString()
        newImageSizeX = (page.height).toString()
    }


    Python {
        id: py
        Component.onCompleted: {
            //addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            setHandler('fileIsSaved', function() {
                idNewImageButtonRunningIndicator.running = false
                idNewImageButton.enabled = true
                pageStack.pop()
            });

        }

        // file operations
        function createNewImageFunction() {
            var savePath = tempImageFolderPath + fileName
            call("graphx.createNewFunction", [ savePath, idNewImageWidth.text.toString(), idNewImageHeight.text.toString(), paintToolColor ])
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
                title: qsTr("Create Image")
            }


            Row {
                width: parent.width
                Row {
                    width: parent.width / 6 * 5
                    height: Theme.itemSizeSmall
                    TextField {
                        id: idNewImageWidth
                        width: parent.width / 5*1.5
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.verticalCenterOffset: Theme.paddingLarge
                        text: newImageSizeX
                        label: qsTr("width")
                        color: Theme.highlightColor
                        inputMethodHints: Qt.ImhDigitsOnly
                        font.pixelSize: Theme.fontSizeExtraSmall
                        validator: IntValidator { bottom: 1; top: maxScalePixels }
                        EnterKey.onClicked: idNewImageWidth.focus = false
                    }
                    IconButton {
                        id: idPaintOrientationPicker
                        width: parent.width/5*0.5
                        height: Theme.itemSizeSmall
                        icon.source: "image://theme/icon-m-transfer?" //icon-s-retweet?"
                        icon.scale: 0.75 //1.32
                        icon.color: Theme.secondaryHighlightColor
                        icon.rotation: 90
                        onClicked: {
                            var oldWidth = idNewImageWidth.text
                            var oldHeight = idNewImageHeight.text
                            idNewImageWidth.text = oldHeight
                            idNewImageHeight.text = oldWidth
                        }
                    }
                    TextField {
                        id: idNewImageHeight
                        width: parent.width / 5*1.5
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.verticalCenterOffset: Theme.paddingLarge
                        text: newImageSizeY
                        label: qsTr("height")
                        horizontalAlignment: Text.AlignRight
                        color: Theme.highlightColor
                        inputMethodHints: Qt.ImhDigitsOnly
                        font.pixelSize: Theme.fontSizeExtraSmall
                        validator: IntValidator { bottom: 1; top: maxScalePixels }
                        EnterKey.onClicked: idNewImageHeight.focus = false
                    }
                    IconButton {
                        id: idPaintColorPicker
                        width: parent.width/5*1.5
                        height: Theme.itemSizeSmall
                        icon.source: "image://theme/icon-s-group-chat?"
                        icon.color: paintToolColor
                        icon.scale: 2//1.32
                        onClicked: {
                            var page = pageStack.push("Sailfish.Silica.ColorPickerPage", { "colors" : myColors})
                            page.colorClicked.connect(function(color) {
                                paintToolColor = color.toString()
                                pageStack.pop()
                            })
                        }
                        Label {
                            horizontalAlignment: Text.AlignHCenter
                            text: qsTr("color")
                            color: Theme.secondaryHighlightColor
                            font.pixelSize: Theme.fontSizeSmall
                            anchors {
                                top: parent.bottom
                                topMargin: -Theme.paddingMedium * 1.05
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }

                IconButton {
                    id: idNewImageButton
                    visible: ( idNewImageWidth.text.length > 0 && idNewImageHeight.text.length > 0 ) ? true : false
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        idNewImageButtonRunningIndicator.running = true
                        idNewImageButton.enabled = false
                        py.createNewImageFunction()
                    }
                    BusyIndicator {
                        id: idNewImageButtonRunningIndicator
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }

            } // end row save filename


            Item {
                width: page.width
                height: 2* Theme.paddingLarge
            }

            SectionHeader {
                text: qsTr("Presets")
            }

            Grid {
                x: Theme.paddingSmall
                width: parent.width - 2* Theme.paddingSmall
                rowSpacing: Theme.itemSizeExtraSmall * 0.8
                columns: 5

                IconButton {
                    id: idApplyCopyPasteImageSizeButton
                    enabled: ( copyPasteImageWidth !== 0 ) ? true : false
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = copyPasteImageWidth
                        idNewImageHeight.text = copyPasteImageHeight
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("from") + "\n" + qsTr("clipboard")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyScreenResolutionButton
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = page.width
                        idNewImageHeight.text = page.height
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("screen") + "\n" + qsTr("resolution")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyA4dpi72Button
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 595
                        idNewImageHeight.text = 842
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("DIN A4") + "\n" + qsTr("72 dpi")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyA4dpi150Button
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 1240
                        idNewImageHeight.text = 1754
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("DIN A4") + "\n" + qsTr("150 dpi")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyA4dpi300Button
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 2480
                        idNewImageHeight.text = 3508
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("DIN A4") + "\n" + qsTr("300 dpi")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApply1024Button
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 1024
                        idNewImageHeight.text = 768
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("XGA")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyWXGAButton
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 1366
                        idNewImageHeight.text = 768
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("WXGA")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyWXGAplusButton
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 1440
                        idNewImageHeight.text = 900
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("WXGA+")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApplyFullHDButton
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 1920
                        idNewImageHeight.text = 1080
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("Full HD")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                IconButton {
                    id: idApply4kButton
                    height: Theme.itemSizeMedium
                    icon.source: "../symbols/icon-m-resize.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    icon.color: Theme.secondaryHighlightColor
                    width: parent.width / 5
                    onClicked: {
                        oldTextfieldWidth = idNewImageWidth.text
                        oldTextfieldHeight = idNewImageHeight.text
                        idNewImageWidth.text = 4096
                        idNewImageHeight.text = 2160
                    }

                    Label {
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("4k")
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color: Theme.secondaryHighlightColor
                        anchors {
                            top: parent.bottom
                            topMargin: -Theme.paddingSmall
                            horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

            }

        } // end Column
    } // end Silica Flickable
}
