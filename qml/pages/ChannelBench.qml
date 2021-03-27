import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5
import Sailfish.Pickers 1.0 // File-Loader


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var inputPathPy
    property var outputPathPy

    // variables for UI
    property var itemsPerRow : 5
    property var alphaDetailPicker : 0
    property var redDetailPicker : 0
    property var greenDetailPicker : 0
    property var blueDetailPicker : 0

    // variables for calculation
    property var channelPathAlpha : "original"
    property var channelPathRed : "original"
    property var channelPathGreen : "original"
    property var channelPathBlue : "original"
    property var fileNameAlpha : ""
    property var fileNameRed : ""
    property var fileNameGreen : ""
    property var fileNameBlue : ""
    property var factorA : "gray"
    property var factorR : "gray"
    property var factorG : "gray"
    property var factorB : "gray"
    property var invertA : "keep"
    property var invertR : "keep"
    property var invertG : "keep"
    property var invertB : "keep"

    Component {
       id: alphaPickerPage
       FilePickerPage {
           title: qsTr("Select alpha")
           nameFilters: [ '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff', '*.bmp', '*.gif' ]
           onSelectedContentPropertiesChanged: {
               channelPathAlpha = selectedContentProperties.filePath
               fileNameAlpha = selectedContentProperties.fileName
           }
       }
    }
    Component {
       id: redPickerPage
       FilePickerPage {
           title: qsTr("Select red")
           nameFilters: [ '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff', '*.bmp', '*.gif' ]
           onSelectedContentPropertiesChanged: {
               channelPathRed = selectedContentProperties.filePath
               fileNameRed = selectedContentProperties.fileName
           }
       }
    }
    Component {
       id: greenPickerPage
       FilePickerPage {
           title: qsTr("Select green")
           nameFilters: [ '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff', '*.bmp', '*.gif' ]
           onSelectedContentPropertiesChanged: {
               channelPathGreen = selectedContentProperties.filePath
               fileNameGreen = selectedContentProperties.fileName
           }
       }
    }
    Component {
       id: bluePickerPage
       FilePickerPage {
           title: qsTr("Select blue")
           nameFilters: [ '*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff', '*.bmp', '*.gif' ]
           onSelectedContentPropertiesChanged: {
               channelPathBlue = selectedContentProperties.filePath
               fileNameBlue = selectedContentProperties.fileName
           }
       }
    }


    Python {
        id: py
        Component.onCompleted: {
            //addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?
        }

        // calculate functions in py
        function rechannelMiddleStepFunction() {
            var saturationA = alphaSliderIntensity.value
            var saturationR = redSliderIntensity.value
            var saturationG = greenSliderIntensity.value
            var saturationB = blueSliderIntensity.value

            call("graphx.rechannelMiddleStepFunction", [ channelPathAlpha, channelPathRed, channelPathGreen, channelPathBlue, factorA, factorR, factorG, factorB, saturationA, saturationR, saturationG, saturationB, invertA, invertR, invertG, invertB ])
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
                        text: qsTr("Channel bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: qsTr("replace, invert and saturate") + "\n "
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
                    //enabled: ( idNewBlue.text !== "")
                    visible:  true
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        py.rechannelMiddleStepFunction()
                        pageStack.pop()
                    }
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
                            text: qsTr("keep") + "\n" + qsTr("original")
                        }
                        onClicked: {
                            if (idAlphaPicker.enabled === false) {
                                idAlphaReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idAlphaPicker.enabled = true
                            }
                            else {
                                idAlphaReplaceLabel.text =qsTr("keep") + "\n" + qsTr("original")
                                idAlphaPicker.enabled = false
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
                            text: qsTr("keep") + "\n" + qsTr("original")
                        }
                        onClicked: {
                            if (idRedPicker.enabled === false) {
                                idRedReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idRedPicker.enabled = true
                            }
                            else {
                                idRedReplaceLabel.text =qsTr("keep") + "\n" + qsTr("original")
                                idRedPicker.enabled = false
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
                            text: qsTr("keep") + "\n" + qsTr("original")
                        }
                        onClicked: {
                            if (idGreenPicker.enabled === false) {
                                idGreenReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idGreenPicker.enabled = true
                            }
                            else {
                                idGreenReplaceLabel.text =qsTr("keep") + "\n" + qsTr("original")
                                idGreenPicker.enabled = false
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
                            text: qsTr("keep") + "\n" + qsTr("original")
                        }
                        onClicked: {
                            if (idBluePicker.enabled === false) {
                                idBlueReplaceLabel.text = qsTr("replace") + "\n" + qsTr("with")
                                idBluePicker.enabled = true
                            }
                            else {
                                idBlueReplaceLabel.text =qsTr("keep") + "\n" + qsTr("original")
                                idBluePicker.enabled = false
                            }
                        }
                    }
                }
            }

            Row {
                id: idLoadFileForChannel
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                IconButton {
                    id: idAlphaPicker
                    enabled: false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    onClicked: {
                        pageStack.push(alphaPickerPage)
                    }
                    Label {
                        visible: (idAlphaPicker.enabled) ? true : false
                        width: parent.width
                        height: parent.height
                        color: Theme.highlightColor
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        truncationMode: TruncationMode.Elide
                        text: (fileNameAlpha === "") ? qsTr("load") : fileNameAlpha
                    }
                }
                IconButton {
                    id: idRedPicker
                    enabled: false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    onClicked: {
                        pageStack.push(redPickerPage)
                    }
                    Label {
                        visible: (idRedPicker.enabled) ? true : false
                        width: parent.width
                        height: parent.height
                        color: Theme.highlightColor
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        truncationMode: TruncationMode.Elide
                        text: (fileNameRed === "") ? qsTr("load") : fileNameRed
                    }
                }
                IconButton {
                    id: idGreenPicker
                    enabled: false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    onClicked: {
                        pageStack.push(greenPickerPage)
                    }
                    Label {
                        visible: (idGreenPicker.enabled) ? true : false
                        width: parent.width
                        height: parent.height
                        color: Theme.highlightColor
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        truncationMode: TruncationMode.Elide
                        text: (fileNameGreen === "") ? qsTr("load") : fileNameGreen
                    }
                }
                IconButton {
                    id: idBluePicker
                    enabled: false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    onClicked: {
                        pageStack.push(bluePickerPage)
                    }
                    Label {
                        visible: (idBluePicker.enabled) ? true : false
                        width: parent.width
                        height: parent.height
                        color: Theme.highlightColor
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        truncationMode: TruncationMode.Elide
                        text: (fileNameBlue === "") ? qsTr("load") : fileNameBlue
                    }
                }
            }

            Row {
                id: idDetailChannelPicker
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge

                IconButton {
                    id: idAlphaDetail
                    enabled: (idAlphaPicker.enabled === true && channelPathAlpha !== "original") ? true : false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    Label {
                        id: idAlphaDetailLabel
                        width: parent.width
                        height: parent.height
                        color:  (parent.enabled) ? Theme.highlightColor : "transparent"
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Gray")
                    }
                    onClicked: {
                        alphaDetailPicker = alphaDetailPicker + 1
                        if (alphaDetailPicker === 0) {
                            idAlphaDetailLabel.text = qsTr("Gray")
                            factorA = "gray"
                        }
                        if (alphaDetailPicker === 1) {
                            idAlphaDetailLabel.text = qsTr("Alpha")
                            factorA = "A"
                        }
                        if (alphaDetailPicker === 2) {
                            idAlphaDetailLabel.text = qsTr("Red")
                            factorA = "R"
                        }
                        if (alphaDetailPicker === 3) {
                            idAlphaDetailLabel.text = qsTr("Green")
                            factorA = "G"
                        }
                        if (alphaDetailPicker === 4) {
                            idAlphaDetailLabel.text = qsTr("Blue")
                            factorA = "B"
                            alphaDetailPicker = -1
                        }
                    }
                }
                IconButton {
                    id: idRedDetail
                    enabled: (idRedPicker.enabled === true && channelPathRed !== "original") ? true : false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    Label {
                        id: idRedDetailLabel
                        width: parent.width
                        height: parent.height
                        color:  (parent.enabled) ? Theme.highlightColor : "transparent"
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Gray")
                    }
                    onClicked: {
                        redDetailPicker = redDetailPicker + 1
                        if (redDetailPicker === 0) {
                            idRedDetailLabel.text = qsTr("Gray")
                            factorR = "gray"
                        }
                        if (redDetailPicker === 1) {
                            idRedDetailLabel.text = qsTr("Alpha")
                            factorR = "A"
                        }
                        if (redDetailPicker === 2) {
                            idRedDetailLabel.text = qsTr("Red")
                            factorR = "R"
                        }
                        if (redDetailPicker === 3) {
                            idRedDetailLabel.text = qsTr("Green")
                            factorR = "G"
                        }
                        if (redDetailPicker === 4) {
                            idRedDetailLabel.text = qsTr("Blue")
                            factorR = "B"
                            redDetailPicker = -1
                        }
                    }
                }
                IconButton {
                    id: idGreenDetail
                    enabled: (idGreenPicker.enabled === true && channelPathGreen !== "original") ? true : false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    Label {
                        id: idGreenDetailLabel
                        width: parent.width
                        height: parent.height
                        color:  (parent.enabled) ? Theme.highlightColor : "transparent"
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Gray")
                    }
                    onClicked: {
                        greenDetailPicker = greenDetailPicker + 1
                        if (redDetailPicker === 0) {
                            idGreenDetailLabel.text = qsTr("Gray")
                            factorG = "gray"
                        }
                        if (greenDetailPicker === 1) {
                            idGreenDetailLabel.text = qsTr("Alpha")
                            factorG = "A"
                        }
                        if (greenDetailPicker === 2) {
                            idGreenDetailLabel.text = qsTr("Red")
                            factorG = "R"
                        }
                        if (greenDetailPicker === 3) {
                            idGreenDetailLabel.text = qsTr("Green")
                            factorG = "G"
                        }
                        if (greenDetailPicker === 4) {
                            idGreenDetailLabel.text = qsTr("Blue")
                            factorG = "B"
                            greenDetailPicker = -1
                        }
                    }
                }
                IconButton {
                    id: idBlueDetail
                    enabled: (idBluePicker.enabled === true && channelPathBlue !== "original") ? true : false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    Label {
                        id: idBlueDetailLabel
                        width: parent.width
                        height: parent.height
                        color:  (parent.enabled) ? Theme.highlightColor : "transparent"
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Gray")
                    }
                    onClicked: {
                        blueDetailPicker = blueDetailPicker + 1
                        if (blueDetailPicker === 0) {
                            idBlueDetailLabel.text = qsTr("Gray")
                            factorB = "gray"
                        }
                        if (blueDetailPicker === 1) {
                            idBlueDetailLabel.text = qsTr("Alpha")
                            factorB = "A"
                        }
                        if (blueDetailPicker === 2) {
                            idBlueDetailLabel.text = qsTr("Red")
                            factorB = "R"
                        }
                        if (blueDetailPicker === 3) {
                            idBlueDetailLabel.text = qsTr("Green")
                            factorB = "G"
                        }
                        if (blueDetailPicker === 4) {
                            idBlueDetailLabel.text = qsTr("Blue")
                            factorB = "B"
                            blueDetailPicker = -1
                        }
                    }
                }

                Label {
                    visible: ( idAlphaDetail.enabled || idRedDetail.enabled || idGreenDetail.enabled || idBlueDetail.enabled ) ? true : false
                    width: parent.width / 5
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("use")
                }
            }

            Row {
                id: idInvertChannel
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    IconButton {
                        id: idAlphaInvert
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idAlphaInvertLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("normal")
                        }
                        onClicked: {
                            if (invertA === "keep") {
                                idAlphaInvertLabel.text = qsTr("invert")
                                invertA = "invert"
                            }
                            else {
                                idAlphaInvertLabel.text =qsTr("normal")
                                invertA = "keep"
                            }
                        }
                    }
                    IconButton {
                        id: idRedInvert
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idRedInvertLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("normal")
                        }
                        onClicked: {
                            if (invertR === "keep") {
                                idRedInvertLabel.text = qsTr("invert")
                                invertR = "invert"
                            }
                            else {
                                idRedInvertLabel.text =qsTr("normal")
                                invertR = "keep"
                            }
                        }
                    }
                    IconButton {
                        id: idGreenInvert
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idGreenInvertLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("normal")
                        }
                        onClicked: {
                            if (invertG === "keep") {
                                idGreenInvertLabel.text = qsTr("invert")
                                invertG = "invert"
                            }
                            else {
                                idGreenInvertLabel.text =qsTr("normal")
                                invertG = "keep"
                            }
                        }
                    }
                    IconButton {
                        id: idBlueInvert
                        width: parent.width / 4
                        height: Theme.itemSizeSmall
                        icon.scale: 1
                        Label {
                            id: idBlueInvertLabel
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge
                            font.pixelSize: Theme.fontSizeExtraSmall
                            text: qsTr("normal")
                        }
                        onClicked: {
                            if (invertB === "keep") {
                                idBlueInvertLabel.text = qsTr("invert")
                                invertB = "invert"
                            }
                            else {
                                idBlueInvertLabel.text =qsTr("normal")
                                invertB = "keep"
                            }
                        }
                    }

                }
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

            Row {
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                height: Theme.itemSizeMedium
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    Slider {
                        id: alphaSliderIntensity
                        width: parent.width
                        height: Theme.itemSizeSmall
                        minimumValue: 0
                        maximumValue: 2
                        value: 1
                        stepSize: 0.01
                        leftMargin: Theme.paddingLarge
                        rightMargin: Theme.paddingLarge
                        smooth: true
                        Label {
                            text: qsTr("alpha") + " " + alphaSliderIntensity.value
                            font.pixelSize: Theme.fontSizeExtraSmall
                            anchors {
                                bottom: parent.bottom
                                bottomMargin: -Theme.paddingMedium
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }

            Row {
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                height: Theme.itemSizeMedium
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    Slider {
                        id: redSliderIntensity
                        width: parent.width
                        height: Theme.itemSizeSmall
                        minimumValue: 0
                        maximumValue: 2
                        value: 1
                        stepSize: 0.01
                        leftMargin: Theme.paddingLarge
                        rightMargin: Theme.paddingLarge
                        smooth: true
                        Label {
                            text: qsTr("red") + " " + redSliderIntensity.value
                            font.pixelSize: Theme.fontSizeExtraSmall
                            anchors {
                                bottom: parent.bottom
                                bottomMargin: -Theme.paddingMedium
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }

            Row {
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                height: Theme.itemSizeMedium
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    Slider {
                        id: greenSliderIntensity
                        width: parent.width
                        height: Theme.itemSizeSmall
                        minimumValue: 0
                        maximumValue: 2
                        value: 1
                        stepSize: 0.01
                        leftMargin: Theme.paddingLarge
                        rightMargin: Theme.paddingLarge
                        smooth: true
                        Label {
                            text: qsTr("green") + " " + greenSliderIntensity.value
                            font.pixelSize: Theme.fontSizeExtraSmall
                            anchors {
                                bottom: parent.bottom
                                bottomMargin: -Theme.paddingMedium
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }

            Row {
                x: Theme.paddingLarge
                width: parent.width - Theme.paddingLarge
                height: Theme.itemSizeMedium
                Row {
                    width: parent.width /  itemsPerRow * (itemsPerRow-1)
                    Slider {
                        id: blueSliderIntensity
                        width: parent.width
                        height: Theme.itemSizeSmall
                        minimumValue: 0
                        maximumValue: 2
                        value: 1
                        stepSize: 0.01
                        leftMargin: Theme.paddingLarge
                        rightMargin: Theme.paddingLarge
                        smooth: true
                        Label {
                            text: qsTr("blue") + " " + blueSliderIntensity.value
                            font.pixelSize: Theme.fontSizeExtraSmall
                            anchors {
                                bottom: parent.bottom
                                bottomMargin: -Theme.paddingMedium
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }
                }
            }


        } // end Column
    } // end Silica Flickable

}
