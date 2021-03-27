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
    property var outputPathPy
    property var filterSourceFolder
    property var previewImageRatio
    property var handleWidth
    property var toolsDrawingColorFrame
    property var opacityEdges
    property var previewBaseImagePath

    // values for preview image
    property var previewBaseImageWidth : idPreviewImage.width
    property var currentEffectName : "original"
    property var tintColor

    // variables for UI
    property var cubeFilePath : ""
    property var cubeFileName : ""
    property var cubeImagePath : ""
    property var cubeImageName : ""
    property var lut3dType
    property bool blockerApply : (idComboBoxMoods.currentIndex === 0 && idComboBoxPresets.currentIndex === 0) || ( idComboBoxMoods.currentIndex === 1 && cubeFileName === "")

    // autostart functions
    Component.onCompleted: {
        py.createPreviewBaseImage()
    }

    Component {
       id: lutCubeFilePickerPage
       FilePickerPage {
           title: qsTr("Select LUT (*.cube, *.png)")
           nameFilters: [ '*.cube', '*.png' ]
           onSelectedContentPropertiesChanged: {
               cubeFilePath = selectedContentProperties.filePath
               cubeFileName = selectedContentProperties.fileName
               var cubeFileNameArray = cubeFileName.split(".")
               var oldFileName = (cubeFileNameArray.slice(0, cubeFileNameArray.length-1)).join(".")
               var oldFileType = cubeFileNameArray[cubeFileNameArray.length - 1]
               if ( oldFileType === "cube" || oldFileType === "CUBE" ) {
                   lut3dType = "cubeFile"
               }
               else {
                   lut3dType = "imageFile"
               }
               py.apply3dLUTcubeFileFromPy(cubeFilePath, lut3dType)
           }
       }
    }


    Python {
        id: py
        Component.onCompleted: {
            // addImportPath(Qt.resolvedUrl('../lib'));
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            // Handlers = Signals to do something in QML whith received Infos from pyotherside
            setHandler('previewImageCreated', function( previewPath ) {
                idPreviewImage.source = "" // Patch: make sure not to get old content ever
                idPreviewImage.source = encodeURI( previewPath )
                idOriginalOverlayImage.source = previewBaseImagePath
                idNewPreviewButtonRunningIndicator.running = false
                idPreviewImage.visible = true
            });
        }


        // Functions affecting original image
        function filtersEffectsMiddleStepFunction() {
            var coalValue = "none"
            var blurValue = "none"
            var centerFocusValue = "none"
            var miniatureBlurValue = "none"
            var miniatureColorValue = "none"
            var addFrameValue = "none"
            var brushSize = "none"
            var quantizeColors = "none"
            var targetColor2Alpha = "none"
            var alphaTolerance = "none"
            var opacityValue ="none"
            var colorExtractARGB = "none"
            var channelExtractARGB = "none"
            var unsharpRadiusMask = "none"
            var unsharpPercentMask = "none"
            var unsharpThresholdMask = "none"
            var brightspotSize = "none"
            call("graphx.filtersEffectsMiddleStepFunction", [ currentEffectName, coalValue, blurValue, centerFocusValue, miniatureBlurValue, miniatureColorValue, addFrameValue, brushSize, quantizeColors, targetColor2Alpha, alphaTolerance, opacityValue, colorExtractARGB, channelExtractARGB, unsharpRadiusMask, unsharpPercentMask, unsharpThresholdMask, brightspotSize ])
            pageStack.pop()
        }
        function apply3dLUTcubeMiddleStepFunction() {
            call("graphx.apply3dLUTcubeMiddleStepFunction", [ cubeFilePath, lut3dType ])
            pageStack.pop()
        }


        // Functions affecting preview image
        function createPreviewBaseImage () {
            idNewPreviewButtonRunningIndicator.running = true
            call("graphx.createPreviewBaseImage", [ inputPathPy, previewBaseImagePath, previewBaseImageWidth ])
        }

        function apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType ) {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + "lut3d" + ".tmp.png"
            call("graphx.apply3dLUTcubeFile", [ targetImage, previewBaseImagePath, cubeFilePath, lut3dType, previewImageEffectPath ])
        }

        function gothamFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var sharpenValue = 1.3
            call("graphx.gothamFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, sharpenValue ])
        }
        function cremaFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var colorFactor = 0.8
            var contrastFactor = 0.9
            call("graphx.cremaFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, colorFactor, contrastFactor ])
        }
        function junoFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var brightnessValue = 1.15
            var saturationValue = 1.7
            call("graphx.junoFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, brightnessValue, saturationValue ])
        }
        function kelvinFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.kelvinFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function xproiiFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.xproiiFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function amaroFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.amaroFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function mayfairFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.mayfairFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function nineteen77FilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.nineteen77FilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function lofiFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.lofiFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function hudsonFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.hudsonFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function redtealFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var colorFactor = 1.35
            call("graphx.redtealFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, colorFactor ])
        }
        function nashvilleFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.nashvilleFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function hefeFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.hefeFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function sierraFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.sierraFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function clarendonFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.sierraFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function tintWithColorFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var factorBrightnessTint = 1.2
            call("graphx.tintWithColorFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, tintColor, factorBrightnessTint ])
        }
        function sepiaFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.sepiaFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
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
                        text: qsTr("Filter bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: "apply color filters" + "\n"
                    }
                }
            }

            Row {
                width: parent.width
                Rectangle {
                    width: Theme.paddingMedium
                    height: 1
                    color: "transparent"
                }
                ComboBox {
                    id: idComboBoxMoods
                    width: parent.width / 6 * 5 - Theme.paddingMedium
                    menu: ContextMenu {
                        MenuItem {
                            text: qsTr("use preset")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("use 3D-LUT file (cube, hald-png)")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                    }
                    onCurrentIndexChanged: {
                        idPreviewImage.source = ""
                        idPreviewImage.source = previewBaseImagePath
                        if (currentIndex === 0) {
                            idComboBoxPresets.currentIndex = 0
                        }
                        if (currentIndex === 1) {
                            cubeFilePath = ""
                            cubeFileName = ""
                            cubeImagePath = ""
                            cubeImageName = ""
                        }

                    }
                }
                IconButton {
                    visible: true
                    enabled: blockerApply !== true
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        if (idComboBoxMoods.currentIndex === 0) {
                            py.filtersEffectsMiddleStepFunction()
                        }
                        if (idComboBoxMoods.currentIndex === 1) {
                            py.apply3dLUTcubeMiddleStepFunction()
                        }
                    }
                    BusyIndicator {
                        id: idNewPreviewButtonRunningIndicator
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
                    }
                }
            }

            ComboBox {
                id: idComboBoxPresets
                visible: idComboBoxMoods.currentIndex === 0
                x: Theme.paddingMedium
                width: parent.width - 2 * Theme.paddingMedium
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("original")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("warmer")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("colder")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("sepia")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("gotham")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("crema")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("juno")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("kelvin")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("xpro-ii")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("amaro")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("mayfair")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("nineteen77")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("lofi")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hudson")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("redteal")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("nashville")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hefe")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("sierra")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("clarendon")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("reyes")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("lark")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }

                    MenuItem {
                        text: qsTr("spring")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("summer")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("fall")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("winter")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("backlight")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("goldvibrant")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("polaroid")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("fadeprint")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("bleakfuture")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("desaturated")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("monotint")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("fujigray")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }



                    MenuItem {
                        text: qsTr("moon")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("moonlight")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("gingham")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("tensiongreen")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("anime")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("tealmagentagold")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("juno2")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hudson2")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("darkblue")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("howlite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }


                    MenuItem {
                        text: qsTr("cinevibrant")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("sweetgelatto")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("newspaper")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("analog oldstyle")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hilutite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hackmanite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("herderite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("heulandite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("hiddenite")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("bleach")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("dropblues")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("latesunset")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onCurrentIndexChanged: {
                    previewImageEffectPicker()
                }
            }

            Row {
                visible: idComboBoxMoods.currentIndex === 1
                x: Theme.paddingMedium
                width: parent.width - 2 * Theme.paddingMedium
                Row {
                    width: parent.width
                    Label {
                        width: parent.width / 6
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        //font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("file:")
                    }
                    IconButton {
                        id: idFilePicker
                        enabled: true
                        width: parent.width / 6 * 5
                        height: Theme.itemSizeSmall
                        onClicked: {
                            pageStack.push(lutCubeFilePickerPage)
                        }
                        Label {
                            visible: (idFilePicker.enabled) ? true : false
                            width: parent.width
                            height: parent.height
                            color: Theme.highlightColor
                            verticalAlignment: Text.AlignVCenter
                            leftPadding: Theme.paddingLarge * 1.5
                            rightPadding: Theme.paddingLarge * 1.5
                            //font.pixelSize: Theme.fontSizeExtraSmall
                            truncationMode: TruncationMode.Elide
                            text: (cubeFileName === "") ? qsTr("load") : cubeFileName
                        }
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

            Image {
                id: idPreviewImage
                visible: false
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                anchors.rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                fillMode: Image.PreserveAspectFit
                source: ""
                cache: false

                Item {
                    id: idOriginalImageArea
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    width: parent.width / 2
                    clip: true
                    Image {
                        id: idOriginalOverlayImage
                        source: ""
                        cache: false
                    }
                }

                Item {
                    id: idHandlesPreviewOriginal
                    anchors.fill: parent
                    Rectangle {
                        id: rectDrag1
                        x: parent.width/2 - handleWidth/2
                        y: parent.height/2 - handleWidth/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleWidth
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: dragArea1
                            preventStealing: true
                            anchors.centerIn: parent
                            width: parent.width * 3
                            height: parent.height * 3
                            drag.target: parent
                            drag.axis: Drag.XAxis
                            drag.minimumX: 0 - handleWidth/2
                            drag.maximumX: idHandlesPreviewOriginal.width - handleWidth/2
                            onPositionChanged: {
                                idOriginalImageArea.width = (rectDrag1.x + handleWidth/2)
                            }
                        }
                        Rectangle {
                            id: idVerticalLine
                            //opacity: opacityEdges
                            color: toolsDrawingColorFrame
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                            width: 5
                            height: idPreviewImage.height + 1
                        }
                    }
                }


            }



        } // end Column
    } // end Silica Flickable

    function previewImageEffectPicker () {
        idNewPreviewButtonRunningIndicator.running = true
        if (idComboBoxPresets.currentIndex === 0) {
            currentEffectName = "original"
            idPreviewImage.source = ""
            idPreviewImage.source = previewBaseImagePath
            idNewPreviewButtonRunningIndicator.running = false
        }
        else if (idComboBoxPresets.currentIndex === 1) {
            currentEffectName = "warmer"
            tintColor = "warmer"
            py.tintWithColorFunction()
        }
        else if (idComboBoxPresets.currentIndex === 2) {
            currentEffectName = "colder"
            tintColor = "colder"
            py.tintWithColorFunction()
        }
        else if (idComboBoxPresets.currentIndex === 3) {
            currentEffectName = "sepia"
            py.sepiaFunction()
        }
        else if (idComboBoxPresets.currentIndex === 4) {
            currentEffectName = "gotham"
            py.gothamFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 5) {
            currentEffectName = "crema"
            py.cremaFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 6) {
            currentEffectName = "juno"
            py.junoFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 7) {
            currentEffectName = "kelvin"
            py.kelvinFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 8) {
            currentEffectName = "xpro-ii"
            py.xproiiFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 9) {
            currentEffectName = "amaro"
            py.amaroFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 10) {
            currentEffectName = "mayfair"
            py.mayfairFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 11) {
            currentEffectName = "nineteen77"
            py.nineteen77FilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 12) {
            currentEffectName = "lofi"
            py.lofiFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 13) {
            currentEffectName = "hudson"
            py.hudsonFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 14) {
            currentEffectName = "redteal"
            py.redtealFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 15) {
            currentEffectName = "nashville"
            py.nashvilleFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 16) {
            currentEffectName = "hefe"
            py.hefeFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 17) {
            currentEffectName = "sierra"
            py.sierraFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 18) {
            currentEffectName = "clarendon"
            var cubeFilePath = "/" + filterSourceFolder + "Clarendon.png"
            var lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 19) {
            currentEffectName = "reyes"
            cubeFilePath = "/" + filterSourceFolder + "Reyes.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 20) {
            currentEffectName = "lark"
            cubeFilePath = "/" + filterSourceFolder + "Lark.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }

        else if (idComboBoxPresets.currentIndex === 21) {
            currentEffectName = "spring"
            cubeFilePath = "/" + filterSourceFolder + "spring.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 22) {
            currentEffectName = "summer"
            cubeFilePath = "/" + filterSourceFolder + "summer.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 23) {
            currentEffectName = "fall"
            cubeFilePath = "/" + filterSourceFolder + "fall.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 24) {
            currentEffectName = "winter"
            cubeFilePath = "/" + filterSourceFolder + "winter.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 25) {
            currentEffectName = "backlight"
            cubeFilePath = "/" + filterSourceFolder + "backlight.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 26) {
            currentEffectName = "goldvibrant"
            cubeFilePath = "/" + filterSourceFolder + "goldvibrant.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 27) {
            currentEffectName = "polaroid"
            cubeFilePath = "/" + filterSourceFolder + "polaroid.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 28) {
            currentEffectName = "fadeprint"
            cubeFilePath = "/" + filterSourceFolder + "fadeprint.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 29) {
            currentEffectName = "bleakfuture"
            cubeFilePath = "/" + filterSourceFolder + "bleakfuture.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 30) {
            currentEffectName = "desaturated"
            cubeFilePath = "/" + filterSourceFolder + "desaturated.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 31) {
            currentEffectName = "monotint"
            cubeFilePath = "/" + filterSourceFolder + "monotint.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 32) {
            currentEffectName = "fujigray"
            cubeFilePath = "/" + filterSourceFolder + "fujigray.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }

        else if (idComboBoxPresets.currentIndex === 33) {
            currentEffectName = "moon"
            cubeFilePath = "/" + filterSourceFolder + "Moon.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 34) {
            currentEffectName = "moonlight"
            cubeFilePath = "/" + filterSourceFolder + "moonlight.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 35) {
            currentEffectName = "gingham"
            cubeFilePath = "/" + filterSourceFolder + "Gingham.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 36) {
            currentEffectName = "tensiongreen"
            cubeFilePath = "/" + filterSourceFolder + "tensiongreen.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 37) {
            currentEffectName = "anime"
            cubeFilePath = "/" + filterSourceFolder + "anime.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 38) {
            currentEffectName = "tealmagentagold"
            cubeFilePath = "/" + filterSourceFolder + "tealmagentagold.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 39) {
            currentEffectName = "juno2"
            cubeFilePath = "/" + filterSourceFolder + "Juno2.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 40) {
            currentEffectName = "hudson2"
            cubeFilePath = "/" + filterSourceFolder + "Hudson2.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 41) {
            currentEffectName = "darkblue"
            cubeFilePath = "/" + filterSourceFolder + "darkblue.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 42) {
            currentEffectName = "howlite"
            cubeFilePath = "/" + filterSourceFolder + "howlite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }

        else if (idComboBoxPresets.currentIndex === 43) {
            currentEffectName = "cinevibrant"
            cubeFilePath = "/" + filterSourceFolder + "cinevibrant.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 44) {
            currentEffectName = "sweetGelatto"
            cubeFilePath = "/" + filterSourceFolder + "sweetGelatto.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 45) {
            currentEffectName = "newspaper"
            cubeFilePath = "/" + filterSourceFolder + "newspaper.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 46) {
            currentEffectName = "analogOldstyle"
            cubeFilePath = "/" + filterSourceFolder + "analogOldstyle.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 47) {
            currentEffectName = "hilutite"
            cubeFilePath = "/" + filterSourceFolder + "hilutite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 48) {
            currentEffectName = "hackmanite"
            cubeFilePath = "/" + filterSourceFolder + "hackmanite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 49) {
            currentEffectName = "herderite"
            cubeFilePath = "/" + filterSourceFolder + "herderite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 50) {
            currentEffectName = "heulandite"
            cubeFilePath = "/" + filterSourceFolder + "heulandite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 51) {
            currentEffectName = "hiddenite"
            cubeFilePath = "/" + filterSourceFolder + "hiddenite.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 52) {
            currentEffectName = "bleach"
            cubeFilePath = "/" + filterSourceFolder + "bleach.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 53) {
            currentEffectName = "dropblues"
            cubeFilePath = "/" + filterSourceFolder + "dropblues.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }
        else if (idComboBoxPresets.currentIndex === 54) {
            currentEffectName = "latesunset"
            cubeFilePath = "/" + filterSourceFolder + "latesunset.png"
            lut3dType = "imageFile"
            py.apply3dLUTcubeFileFromPy( cubeFilePath, lut3dType )
        }

    }
}
