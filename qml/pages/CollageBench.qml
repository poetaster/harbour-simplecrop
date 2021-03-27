import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5
import Sailfish.Pickers 1.0 // File-Loader


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var tempImageFolderPath
    property var inputPathPy
    property var inputImageWidth
    property var outputPathPy
    property var filterSourceFolder
    property var previewImageRatio
    property var handleWidth
    property var toolsDrawingColorFrame
    property var opacityEdges
    property var paintToolColor
    property var symbolSourceFolder
    property var previewBaseImagePath

    // values for UI
    property bool blockApply : false
    property var ratioWidthOriginal2Preview : inputImageWidth / idPreviewImage.width
    property var currentCollageType : "lines"
    property bool warningLargeSize : false
    property var warningInputMaxWidth : 4096

    // values for files
    property var allSelectedPaths : ""
    property var randomAngleList : ""
    property var ratioWanted : ""
    property var selectedFilesCounter : 0

    // autostart functions
    Component.onCompleted: {
        if (inputImageWidth > warningInputMaxWidth) {
            warningLargeSize = true
            inputImageWidth = warningInputMaxWidth
        }
    }

    Component {
        id: multiImagePickerDialog
        MultiImagePickerDialog {
            onAccepted: {
                allSelectedPaths = ""
                randomAngleList = ""
                var urls = []
                var paths = []
                for (var i = 0; i < selectedContent.count; ++i) {
                    var url = selectedContent.get(i).url
                    var path = decodeURIComponent( "/" + (selectedContent.get(i).url).toString().replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") )
                    urls.push(selectedContent.get(i).url)
                    paths.push(decodeURIComponent( "/" + (selectedContent.get(i).url).toString().replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/,"") ))
                }
                allSelectedPaths = paths.join(",")
                selectedFilesCounter = selectedContent.count
                blockApply = true
                py.createImageMosaic("preview")
            }
            onRejected: {
                //allSelectedPaths = ""
                //randomAngleList = ""
                //selectedFilesCounter = 0
            }
        }
    }

    Python {
        id: py
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            // Handlers = Signals to do something in QML whith received Infos from pyotherside
            setHandler('previewImageCreated', function( previewPath, shuffledPaths, randomAngles ) {
                idPreviewImage.source = "" // Patch: make sure not to get old content ever
                idPreviewImage.source = encodeURI( previewPath )
                allSelectedPaths = shuffledPaths.toString()
                randomAngleList = randomAngles.toString()
                blockApply = false
            });
        }



        // Functions affecting preview image
        function createImageMosaic (targetImage) {
            var previewImagePath = tempImageFolderPath + "preview" + "-" + "collage" + ".tmp.png"

            if (idComboBoxBackColor.currentIndex === 0) {
                var targetBackground = "image"
            }
            else if (idComboBoxBackColor.currentIndex === 1) {
                targetBackground = paintToolColor
            }
            else if (idComboBoxBackColor.currentIndex === 2) {
                targetBackground = "#ff000000" //black
            }
            else if (idComboBoxBackColor.currentIndex === 3) {
                targetBackground = "#ffffffff" //white
            }
            else if (idComboBoxBackColor.currentIndex === 4) {
                targetBackground = "#00000000" //transparent
            }

            if (idComboBoxFrameColor.currentIndex === 0) {
                var targetFrameSetup = "none"
            }
            else if (idComboBoxFrameColor.currentIndex === 1) {
                targetFrameSetup = paintToolColor
            }
            else if (idComboBoxFrameColor.currentIndex === 2) {
                targetFrameSetup = "#ff000000"
            }
            else if (idComboBoxFrameColor.currentIndex === 3) {
                targetFrameSetup = "#ffffffff"
            }

            if (idComboBoxAspect.currentIndex === 0) {
                ratioWanted = 3/2
            }
            else if (idComboBoxAspect.currentIndex === 1) {
                ratioWanted = 1
            }
            else if (idComboBoxAspect.currentIndex === 2) {
                ratioWanted = 2/3
            }


            if (targetImage === "preview") {
                var shuffle = "yes"
                var targetWidth = idPreviewImage.width
                var targetBlur = 20 // 1...50
                var targetSpacing = idSliderSpacing.value
                targetFrameSetup = targetFrameSetup + "," + idSliderFrameWidth.value
                if ( currentCollageType === "mosaic") {
                    call("graphx.createCollageMosaic", [ previewImagePath, inputPathPy, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderColumns.value, targetSpacing, targetBlur, targetImage, targetFrameSetup ])
                }
                else if ( currentCollageType === "lines") {
                    call("graphx.createCollageLines", [ previewImagePath, inputPathPy, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderHeight.value, targetSpacing, targetBlur, targetImage, targetFrameSetup ])
                }
                else if ( currentCollageType === "columns") {
                    call("graphx.createCollageColumns", [ previewImagePath, inputPathPy, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderColumns.value, targetSpacing, targetBlur, targetImage, targetFrameSetup ])
                }
                else if ( currentCollageType === "polaroids") {
                    call("graphx.createCollagePolaroids", [ previewImagePath, inputPathPy, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderColumns.value, targetSpacing, targetBlur, targetImage, targetFrameSetup, randomAngleList, ratioWanted ])
                }
                else if ( currentCollageType === "scattered") {
                    call("graphx.createCollageScattered", [ previewImagePath, inputPathPy, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderColumns.value, targetSpacing, targetBlur, targetImage, targetFrameSetup, randomAngleList, ratioWanted ])
                }

            }
            else {
                shuffle = "no"
                targetWidth = inputImageWidth
                targetBlur = Math.round(20 * ratioWidthOriginal2Preview)
                targetSpacing = Math.round(idSliderSpacing.value * ratioWidthOriginal2Preview)
                targetFrameSetup = targetFrameSetup + "," + Math.round(idSliderFrameWidth.value * ratioWidthOriginal2Preview)
                call("graphx.createCollageMiddleStepFunction", [ currentCollageType, targetWidth , allSelectedPaths, shuffle, targetBackground, idSliderColumns.value, targetSpacing, targetBlur, randomAngleList, ratioWanted, targetFrameSetup ])
                pageStack.pop()
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
        contentHeight: columnMoods.height  // Tell SilicaFlickable the height of its content.
        VerticalScrollDecorator {}

        Column {
            id: columnMoods
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
                        text: qsTr("Collage bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: (warningLargeSize === false) ? ( qsTr("combine") + " [" + selectedFilesCounter + "] " + qsTr("images") + "\n" ) : ( qsTr("output limited to ") + warningInputMaxWidth + qsTr("px") + "\n" + qsTr("combine") + " [" + selectedFilesCounter + "] " + qsTr("images") + "\n" )
                    }
                }
            }

            Row {
                width: parent.width

                IconButton {
                    enabled: (blockApply === false)
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "image://theme/icon-m-add?"
                    onClicked: {
                        pageStack.push(multiImagePickerDialog)
                    }
                }

                Item {
                    width: parent.width / 6 * 1.5
                    height: Theme.itemSizeSmall
                }

                IconButton {
                    id: idReshuffleButton
                    enabled: (allSelectedPaths!=="" && blockApply === false)
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "image://theme/icon-m-sync?"
                    icon.scale: 0.85
                    onClicked: {
                        if (allSelectedPaths !== "") {
                            blockApply = true
                            py.createImageMosaic("preview")
                        }
                    }
                    BusyIndicator {
                        id: idNewPreviewButtonRunningIndicator
                        running: (blockApply === true)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }

                Item {
                    width: parent.width / 6 * 1.5
                    height: Theme.itemSizeSmall
                }

                IconButton {
                    enabled: (allSelectedPaths!=="" && blockApply === false)
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        py.createImageMosaic("original")
                    }
                    /*
                    BusyIndicator {
                        id: idNewPreviewButtonRunningIndicator
                        running: (blockApply === true)
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                    */
                }
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

            Image {
                id: idPreviewImage
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: Theme.paddingLarge + Theme.paddingSmall
                anchors.rightMargin: Theme.paddingLarge + Theme.paddingSmall
                fillMode: Image.PreserveAspectFit
                source: ""
                cache: false
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

            ComboBox {
                id: idComboBoxPresets
                enabled: (blockApply === false)
                width: parent.width
                label: qsTr("layout generator:") + " "
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("auto-rows")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("auto-columns")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("mosaic")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("photowall")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("scattered")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onValueChanged: {
                    if (currentIndex === 0) {
                        currentCollageType = "lines"
                    }
                    else if (currentIndex === 1) {
                        currentCollageType = "columns"
                    }
                    else if (currentIndex === 2) {
                        currentCollageType = "mosaic"
                    }
                    else if (currentIndex === 3) {
                        currentCollageType = "polaroids"
                    }
                    else if (currentIndex === 4) {
                        currentCollageType = "scattered"
                    }
                }
            }

            ComboBox {
                id: idComboBoxBackColor
                enabled: (blockApply === false)
                width: parent.width
                label: qsTr("background:") + " "
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("blurry image")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("current color")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("black")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("white")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("transparent")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
            }

            ComboBox {
                id: idComboBoxFrameColor
                enabled: (blockApply === false)
                width: parent.width
                label: qsTr("frames:") + " "
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("none")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("current color")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("black")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("white")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
            }

            ComboBox {
                id: idComboBoxAspect
                visible: (currentCollageType === "polaroids")
                enabled: (blockApply === false)
                width: parent.width
                label: qsTr("ratio:") + " "
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("3 : 2")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("1 : 1")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("2 : 3")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingMedium
                color: "transparent"
            }

            Slider {
                id: idSliderHeight
                visible: (currentCollageType === "lines")
                enabled: (blockApply === false)
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 7
                value: 3
                stepSize: 1
                smooth: true
                Label {
                    text: qsTr("height") + " = 1/" + idSliderHeight.value + " " + qsTr("width")
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            Slider {
                id: idSliderColumns
                visible: (currentCollageType === "mosaic" || currentCollageType === "polaroids" || currentCollageType === "columns" || currentCollageType === "scattered" )
                enabled: (blockApply === false)
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 7
                value: 3
                stepSize: 1
                smooth: true
                Label {
                    text: qsTr("columns") + " " + idSliderColumns.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            Slider {
                id: idSliderSpacing
                enabled: (blockApply === false)
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingSmall
                minimumValue: 0
                maximumValue: 5 * Theme.paddingSmall
                value: Theme.paddingSmall
                stepSize: Theme.paddingSmall / 2
                smooth: true
                Label {
                    text: qsTr("spacing") + " " + idSliderSpacing.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            Slider {
                id: idSliderFrameWidth
                enabled: (blockApply === false)
                visible: (idComboBoxFrameColor.currentIndex !== 0)
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingSmall
                minimumValue: 0
                maximumValue: 5 * Theme.paddingSmall
                value: Theme.paddingSmall
                stepSize: Theme.paddingSmall / 2
                smooth: true
                Label {
                    text: qsTr("frame width") + " " + idSliderFrameWidth.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

        } // end Column
    } // end Silica Flickable

    function dummyFunction () {
        console.log("ToDo")
    }
}
