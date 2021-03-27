import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var inputPathPy
    property var outputPathPy
    property var oldA_tmp
    property var oldR_tmp
    property var oldG_tmp
    property var oldB_tmp

    // variables for UI
    property var itemsPerRow : 5

    // variables for calculation
    property var oldA
    property var oldR
    property var oldG
    property var oldB
    property var tolA
    property var tolR
    property var tolG
    property var tolB
    property var newA
    property var newR
    property var newG
    property var newB
    property var compareA
    property var compareR
    property var compareG
    property var compareB
    property var changeA
    property var changeR
    property var changeG
    property var changeB
    property var modePixeldraw


    Python {
        id: py
        Component.onCompleted: {
            //addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?
        }

        // calculate functions in py
        function repixelMiddleStepFunction() {
            collectValues()
            call("graphx.repixelMiddleStepFunction", [ oldA, oldR, oldG, oldB, newA, newR, newG, newB, compareA, compareR, compareG, compareB, tolA, tolR, tolG, tolB, changeA, changeR, changeG, changeB, modePixeldraw ])
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
            width: page.width //- 2* Theme.paddingLarge

            SectionHeader {
                id: idSectionHeader
                height: idSectionHeaderColumn.height
                Column {
                    id: idSectionHeaderColumn
                    width: parent.width / 5 * 4
                    height: idLabelProgramName.height + idLabelFilePath.height
                    anchors.top: parent.top
                    anchors.topMargin: Theme.paddingMedium
                    anchors.right: parent.right
                    Label {
                        id: idLabelProgramName
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeLarge
                        color: Theme.highlightColor
                        text: qsTr("Pixel bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: qsTr("find and replace") + "\n "
                    }
                }
            }


            Row {
                id: idRecolorizeInfoRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    Label {
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Alpha")
                    }
                    Label {
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Red")
                    }
                    Label {
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Green")
                    }
                    Label {
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Blue")
                    }
                }


                IconButton {
                    id: idApplyButton
                    enabled: ( idOldAlpha.text !== "" && idOldRed.text !== "" && idOldGreen.text !== "" && idOldBlue.text !== "" && idOldAlphaTolerance.text !== "" && idOldRedTolerance.text !== "" && idOldGreenTolerance.text !== "" &&idOldBlueTolerance.text  !== "" && idNewAlpha.text  !== "" && idNewRed.text !== "" && idNewGreen.text !== "" && idNewBlue.text !== "")
                    visible:  true
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        py.repixelMiddleStepFunction()
                        pageStack.pop()
                    }
                }
            }

            Row {
                id: idComparatorRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                ComboBox {
                    id: idComboBoxAlpha
                    width: parent.width / itemsPerRow
                    menu: ContextMenu {
                        MenuItem {
                            text: "="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }                        
                        MenuItem {
                            text: "!="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "<="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ">="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                ComboBox {
                    id: idComboBoxRed
                    width: parent.width / itemsPerRow
                    menu: ContextMenu {
                        MenuItem {
                            text: "="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "!="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "<="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ">="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                ComboBox {
                    id: idComboBoxGreen
                    width: parent.width / itemsPerRow
                    menu: ContextMenu {
                        MenuItem {
                            text: "="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "!="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "<="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ">="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
                ComboBox {
                    id: idComboBoxBlue
                    width: parent.width / itemsPerRow
                    menu: ContextMenu {
                        MenuItem {
                            text: "="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "!="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: "<="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: ">="
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                }
            }

            Row {
                id: idOldValuesRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                TextField {
                    id: idOldAlpha
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: oldA_tmp
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldAlpha.focus = false
                }
                TextField {
                    id: idOldRed
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: oldR_tmp
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldRed.focus = false
                }
                TextField {
                    id: idOldGreen
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: oldG_tmp
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldGreen.focus = false
                }
                TextField {
                    id: idOldBlue
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: oldB_tmp
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldBlue.focus = false
                }
                Label {
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("old")
                }
            }

            Row {
                id: idOldValuesTolerance
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                TextField {
                    id: idOldAlphaTolerance
                    width: parent.width / itemsPerRow
                    enabled: (idComboBoxAlpha.currentIndex === 0 || idComboBoxAlpha.currentIndex === 1) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    font.strikeout : (idComboBoxAlpha.currentIndex === 0 || idComboBoxAlpha.currentIndex === 1) ? false : true
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldAlphaTolerance.focus = false
                }
                TextField {
                    id: idOldRedTolerance
                    width: parent.width / itemsPerRow
                    enabled: (idComboBoxRed.currentIndex === 0 || idComboBoxRed.currentIndex === 1) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    font.strikeout : (idComboBoxRed.currentIndex === 0 || idComboBoxRed.currentIndex === 1) ? false : true
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldRedTolerance.focus = false
                }
                TextField {
                    id: idOldGreenTolerance
                    width: parent.width / itemsPerRow
                    enabled: (idComboBoxGreen.currentIndex === 0 || idComboBoxGreen.currentIndex === 1) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    font.strikeout : (idComboBoxGreen.currentIndex === 0 || idComboBoxGreen.currentIndex === 1) ? false : true
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldGreenTolerance.focus = false
                }
                TextField {
                    id: idOldBlueTolerance
                    width: parent.width / itemsPerRow
                    enabled: (idComboBoxBlue.currentIndex === 0 || idComboBoxBlue.currentIndex === 1) ? true : false
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    font.strikeout : (idComboBoxBlue.currentIndex === 0 || idComboBoxBlue.currentIndex === 1) ? false : true
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: idOldBlueTolerance.focus = false
                }
                Label {
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    enabled: (idComboBoxAlpha.currentIndex === 0 || idComboBoxRed.currentIndex === 0 || idComboBoxGreen.currentIndex === 0 || idComboBoxBlue.currentIndex === 0 || idComboBoxAlpha.currentIndex === 1 || idComboBoxRed.currentIndex === 1 || idComboBoxGreen.currentIndex === 1 || idComboBoxBlue.currentIndex === 1) ? true : false
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("+/-")
                }
            }

            Row {
                id: idReplaceOrKeepRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)

                    IconButton {
                        id: idAlphaReplace
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idAlphaReplaceLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("replace") + "\n" + qsTr("with")
                        }
                        onClicked: {
                            if (idNewAlpha.enabled === true) {
                                idAlphaReplaceLabel.text = qsTr("keep")+ "\n" + qsTr("values")
                                idNewAlpha.font.strikeout = true
                                idNewAlpha.enabled = false
                            }
                            else {
                                idAlphaReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idNewAlpha.font.strikeout = false
                                idNewAlpha.enabled = true
                            }
                        }
                    }
                    IconButton {
                        id: idRedReplace
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idRedReplaceLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("replace") + "\n" + qsTr("with")
                        }
                        onClicked: {
                            if (idNewRed.enabled === true) {
                                idRedReplaceLabel.text =  qsTr("keep")+ "\n" + qsTr("values")
                                idNewRed.font.strikeout = true
                                idNewRed.enabled = false
                            }
                            else {
                                idRedReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idNewRed.font.strikeout = false
                                idNewRed.enabled = true
                            }
                        }
                    }
                    IconButton {
                        id: idGreenReplace
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idGreenReplaceLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("replace") + "\n" + qsTr("with")
                        }
                        onClicked: {
                            if (idNewGreen.enabled === true) {
                                idGreenReplaceLabel.text =  qsTr("keep")+ "\n" + qsTr("values")
                                idNewGreen.font.strikeout = true
                                idNewGreen.enabled = false
                            }
                            else {
                                idGreenReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idNewGreen.font.strikeout = false
                                idNewGreen.enabled = true
                            }
                        }
                    }
                    IconButton {
                        id: idBlueReplace
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idBlueReplaceLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("replace") + "\n" + qsTr("with")
                        }
                        onClicked: {
                            if (idNewBlue.enabled === true) {
                                idBlueReplaceLabel.text = qsTr("keep")+ "\n" + qsTr("values")
                                idNewBlue.font.strikeout = true
                                idNewBlue.enabled = false
                            }
                            else {
                                idBlueReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idNewBlue.font.strikeout = false
                                idNewBlue.enabled = true
                            }
                        }
                    }
                }
            }

            Row {
                id: idNewValuesRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                TextField {
                    id: idNewAlpha
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: {
                        idNewAlpha.focus = false
                    }
                }
                TextField {
                    id: idNewRed
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked:  {
                        idNewRed.focus = false
                    }
                }
                TextField {
                    id: idNewGreen
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked:  {
                        idNewGreen.focus = false
                    }
                }
                TextField {
                    id: idNewBlue
                    width: parent.width / itemsPerRow
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingMedium * 1.4
                    text: "0"
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked:  {
                        idNewBlue.focus = false
                    }
                }
                Label {
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("new")
                }
            }

            Row {
                id: idOtherOptionsRow
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                Label {
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: Theme.paddingLarge
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("Results")
                }
                IconButton {
                    id: idInvertResults
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    icon.scale: 1
                    Label {
                        id: idInvertResultsLabel
                        enabled: true
                        width: parent.width
                        height: parent.height
                        color: Theme.highlightColor
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("normal")
                    }
                    onClicked: {
                        if (idInvertResultsLabel.enabled === true) {
                            idInvertResultsLabel.text = qsTr("invert")
                            idInvertResultsLabel.enabled = false
                        }
                        else {
                            idInvertResultsLabel.text = qsTr("normal")
                            idInvertResultsLabel.enabled = true
                        }
                    }
                }
            }

        } // end Column
    } // end Silica Flickable

    function collectValues() {
        oldA = idOldAlpha.text
        oldR = idOldRed.text
        oldG = idOldGreen.text
        oldB = idOldBlue.text

        tolA = idOldAlphaTolerance.text
        tolR = idOldRedTolerance.text
        tolG = idOldGreenTolerance.text
        tolB = idOldBlueTolerance.text

        newA = idNewAlpha.text
        newR = idNewRed.text
        newG = idNewGreen.text
        newB = idNewBlue.text

        if (idNewAlpha.enabled === true) { changeA = "true" }
        else {changeA = "false"}
        if (idNewRed.enabled === true) { changeR = "true" }
        else {changeR = "false"}
        if (idNewGreen.enabled === true) { changeG = "true" }
        else {changeG = "false"}
        if (idNewBlue.enabled === true) { changeB = "true" }
        else {changeB = "false"}

        if (idComboBoxAlpha.currentIndex === 0)
            compareA = "="
        if (idComboBoxAlpha.currentIndex === 1)
            compareA = "!="
        if (idComboBoxAlpha.currentIndex === 2)
            compareA = "<="
        if (idComboBoxAlpha.currentIndex === 3)
            compareA = ">="

        if (idComboBoxRed.currentIndex === 0)
            compareR = "="
        if (idComboBoxRed.currentIndex === 1)
            compareR = "!="
        if (idComboBoxRed.currentIndex === 2)
            compareR = "<="
        if (idComboBoxRed.currentIndex === 3)
            compareR = ">="

        if (idComboBoxGreen.currentIndex === 0)
            compareG = "="
        if (idComboBoxGreen.currentIndex === 1)
            compareG = "!="
        if (idComboBoxGreen.currentIndex === 2)
            compareG = "<="
        if (idComboBoxGreen.currentIndex === 3)
            compareG = ">="

        if (idComboBoxBlue.currentIndex === 0)
            compareB = "="
        if (idComboBoxBlue.currentIndex === 1)
            compareB = "!="
        if (idComboBoxBlue.currentIndex === 2)
            compareB = "<="
        if (idComboBoxBlue.currentIndex === 3)
            compareB = ">="

        if (idInvertResultsLabel.enabled === true) {
            modePixeldraw = "normal"
        }
        else {
            modePixeldraw = "invert"
        }


    }
}
