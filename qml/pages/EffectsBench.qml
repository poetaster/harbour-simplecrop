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

    // values for preview image
    property var previewBaseImageWidth : idPreviewImage.width
    property var currentEffectName : "original"
    property var spotType

    // variables for UI
    property var cubeFilePath : ""
    property var cubeFileName : ""
    property bool blockerApply : false // (idComboBoxMoods.currentIndex === 0 && idComboBoxPresets.currentIndex === 0) || ( idComboBoxMoods.currentIndex === 1 && cubeFileName === "")
    property var ratioWidthOriginal2Base


    // autostart functions
    Component.onCompleted: {
        py.createPreviewBaseImage()
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
                blockerApply = false
                idPreviewImage.visible = true
                ratioWidthOriginal2Base = inputImageWidth / previewBaseImageWidth
            });
        }


        // Functions affecting original image
        function filtersEffectsMiddleStepFunction() {
            var coalValue = idFxSliderCoalBlur.value
            var blurValue = idFxSliderBlur.value
            var centerFocusValue = idFxSliderCentralFocus.value
            var miniatureBlurValue = idFxSliderMiniatureBlur.value
            var miniatureColorValue = idFxSliderMiniatureColor.value
            var addFrameValue = idFxSliderAddFrame.value
            var brushSize = idFxSliderDrawing.value
            var quantizeColors = idFxSliderQuantize.value

            if (idComboBoxAlphaColor.currentIndex === 0) {
                var targetColor2Alpha = "white"
            }
            else {
                targetColor2Alpha = "black"
            }
            var alphaTolerance = idFxSliderAlphaTolerance.value

            var opacityValue = idFxSliderOpacity.value
            if (idComboBoxColorExtract.currentIndex === 0) {
                var colorExtractARGB = "R"
            }
            else if (idComboBoxColorExtract.currentIndex === 1) {
                colorExtractARGB = "G"
            }
            else {
                colorExtractARGB = "G"
            }

            if (idComboBoxChannelExtract.currentIndex === 0) {
                var channelExtractARGB = "R"
            }
            else if (idComboBoxChannelExtract.currentIndex === 1) {
                channelExtractARGB = "G"
            }
            else if (idComboBoxChannelExtract.currentIndex === 2) {
                channelExtractARGB = "B"
            }
            else {
                channelExtractARGB = "A"
            }
            var unsharpRadiusMask = idFxUnsharpRadiusMask.value
            var unsharpPercentMask = idFxUnsharpPercentMask.value
            var unsharpThresholdMask = idFxUnsharpThresholdMask.value
            var brightspotSize = idFxSliderBrightspotSize.value
            call("graphx.filtersEffectsMiddleStepFunction", [ currentEffectName, coalValue, blurValue, centerFocusValue, miniatureBlurValue, miniatureColorValue, addFrameValue, brushSize, quantizeColors, targetColor2Alpha, alphaTolerance, opacityValue, colorExtractARGB, channelExtractARGB, unsharpRadiusMask, unsharpPercentMask, unsharpThresholdMask, brightspotSize ])
            pageStack.pop()
        }


        // Functions affecting preview image
        function createPreviewBaseImage () {
            idNewPreviewButtonRunningIndicator.running = true
            blockerApply = true
            call("graphx.createPreviewBaseImage", [ inputPathPy, previewBaseImagePath, previewBaseImageWidth ])
        }


        function autocontrastFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.autocontrastFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function stretchContrastFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.stretchContrastFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function blackWhiteFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.blackWhiteFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function coalFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var blurRadius = Math.round( idFxSliderCoalBlur.value / ratioWidthOriginal2Base)
            call("graphx.coalFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, blurRadius ])
        }
        function grayscaleFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.grayscaleFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function invertFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.invertFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function equalizeFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.equalizeFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function solarizeFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.solarizeFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function modedrawingFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var brushSize = Math.round( idFxSliderDrawing.value / ratioWidthOriginal2Base)
            call("graphx.modedrawingFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, brushSize ])
        }
        function posterizeFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.posterizeFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function blurFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var blurFactor =  Math.round( idFxSliderBlur.value / ratioWidthOriginal2Base)
            call("graphx.blurFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, blurFactor ])
        }
        function smoothSurfaceFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var smoothingStrength = "strong"
            call("graphx.smoothSurfaceFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, smoothingStrength ])
        }
        function centerFocusFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var alphaMaskPath = "/" + symbolSourceFolder + "alphaMaskCircleSmall.png"
            var radiusEdgeBlur = Math.round( idFxSliderCentralFocus.value / ratioWidthOriginal2Base) // 6 // 4
            var enhanceColorFaktor = 1
            var enhanceContrastFaktor = 1
            var addExtraBlurAroundPath = "none"
            call("graphx.miniatureFocusFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, alphaMaskPath, radiusEdgeBlur, enhanceColorFaktor, enhanceContrastFaktor, addExtraBlurAroundPath ])
        }
        function miniatureFocusFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var alphaMaskPath = "/" + symbolSourceFolder + "alphaMaskStandard.png"
            var radiusEdgeBlur = Math.round( idFxSliderMiniatureBlur.value / ratioWidthOriginal2Base) // 5 // 4
            var enhanceColorFaktor = Math.round( idFxSliderMiniatureColor.value ) // 1.75 // 1.9
            var enhanceContrastFaktor = 1.3 // 1.4
            var addExtraBlurAroundPath = "/" + symbolSourceFolder + "alphaMaskCircleSmall.png"
            call("graphx.miniatureFocusFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, alphaMaskPath, radiusEdgeBlur, enhanceColorFaktor, enhanceContrastFaktor, addExtraBlurAroundPath ])
        }
        function edgeenhanceFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.edgeenhanceFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function unsharpmaskFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var radiusMask = idFxUnsharpRadiusMask.value // 3 //2
            var percentMask = idFxUnsharpPercentMask.value // 150 //150
            var thresholdMask = idFxUnsharpThresholdMask.value // 4 //3
            call("graphx.unsharpmaskFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, radiusMask, percentMask, thresholdMask ])
        }
        function findedgesFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var fileTargetType = inputPathPy.slice(inputPathPy.length - 4)
            call("graphx.findedgesFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, fileTargetType ])
        }
        function contourFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.contourFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }
        function embossFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.embossFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath ])
        }



        function addFrameFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var addFrameValue = Math.round( idFxSliderAddFrame.value / ratioWidthOriginal2Base)
            call("graphx.addFrameFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, addFrameValue, paintToolColor ])
        }
        function tintWithColorFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var factorBrightnessTint = 1.2
            call("graphx.tintWithColorFunction", [ targetImage, inputPathPy, outputPathPy, paintToolColor, factorBrightnessTint ])
        }
        function quantizeFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var colorsAmount = idFxSliderQuantize.value
            call("graphx.quantizeFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, colorsAmount ])
        }
        function colorToAlphaFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var targetColorTolerance = idFxSliderAlphaTolerance.value //"30"
            if (idComboBoxAlphaColor.currentIndex === 0) {
                var targetColor2Alpha = "white"
            }
            else {
                targetColor2Alpha = "black"
            }
            call("graphx.colorToAlphaFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, targetColor2Alpha, targetColorTolerance ])
        }
        function addAlphaFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            var percentAlpha = idFxSliderOpacity.value
            call("graphx.addAlphaFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, percentAlpha ])
        }
        function extractColorFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            if (idComboBoxColorExtract.currentIndex === 0) {
                var colorExtractARGB = "R"
            }
            else if (idComboBoxColorExtract.currentIndex === 1) {
                colorExtractARGB = "G"
            }
            else {
                colorExtractARGB = "B"
            }
            call("graphx.extractColorFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, colorExtractARGB ])
        }
        function extractChannelFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            if (idComboBoxChannelExtract.currentIndex === 0) {
                var channelExtractARGB = "R"
            }
            else if (idComboBoxChannelExtract.currentIndex === 1) {
                channelExtractARGB = "G"
            }
            else if (idComboBoxChannelExtract.currentIndex === 2) {
                channelExtractARGB = "B"
            }
            else {
                channelExtractARGB = "A"
            }
            call("graphx.extractChannelFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, channelExtractARGB ])
        }
        function brightspotFilterFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            if (currentEffectName === "fxMinFilter") {
                var spotType = "min"
            }
            else if (currentEffectName === "fxMaxFilter") {
                spotType = "max"
            }
            else if (currentEffectName === "fxMedFilter") {
                spotType = "med"
            }
            var brightspotSize = Math.round( idFxSliderBrightspotSize.value / ratioWidthOriginal2Base)
            // check that it stays an odd number, even numbers do not work in PILLOW
            if (brightspotSize % 2 === 0 ) {
                brightspotSize = brightspotSize + 1
            }
            call("graphx.brightspotFilterFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, spotType, brightspotSize ])
        }
        function fishEyeFunction() {
            var targetImage = "preview"
            var previewImageEffectPath = tempImageFolderPath + "preview" + "-" + currentEffectName + ".tmp.png"
            call("graphx.fishEyeFunction", [ targetImage, previewBaseImagePath, previewImageEffectPath, paintToolColor ])
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
                        text: qsTr("Effects bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: "apply effects" + "\n"
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
                    id: idComboBoxPresets
                    x: Theme.paddingMedium
                    width: parent.width / 6 * 5 - Theme.paddingMedium
                    //width: parent.width - 2 * Theme.paddingMedium
                    menu: ContextMenu {
                        MenuItem {
                            text: qsTr("original")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("auto contrast")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("stretch contrast")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("dithering")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("coal drawing")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("grayscale")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("invert colors")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("equalize colors")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("solarize")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("brush art")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("posterize")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("blur image")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("smooth surface")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("central focus")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("miniature world")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("enhance edges")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("digital unsharp masking")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("find edges")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("find contour")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("emboss")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("add current colored frame")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("tint with current color")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("reduce colors")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("change opacity")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("create alpha from")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("extract color")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("extract channel")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }

                        MenuItem {
                            text: qsTr("minFilter (bright spots darker)")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("maxFilter (dark spots brighter)")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("mediumFilter")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }
                        MenuItem {
                            text: qsTr("fishEye")
                            font.pixelSize: Theme.fontSizeExtraSmall
                        }

                    }
                    onCurrentIndexChanged: {
                        blockerApply = true
                        previewImageEffectPicker()
                    }
                }

                IconButton {
                    visible: true
                    enabled: ( blockerApply !== true && idComboBoxPresets.currentIndex !== 0 )
                    width: parent.width / 6
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        py.filtersEffectsMiddleStepFunction()
                    }
                    BusyIndicator {
                        id: idNewPreviewButtonRunningIndicator
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        size: BusyIndicatorSize.Medium
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

            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }

            Slider {
                id: idFxSliderCoalBlur
                visible: idComboBoxPresets.currentIndex === 4
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 100
                value: 20
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("coal") + " " + idFxSliderCoalBlur.value //"blur"
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderDrawing
                visible: idComboBoxPresets.currentIndex === 9
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 50
                value: 9
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("brush size") + " " + idFxSliderDrawing.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderBlur
                visible: idComboBoxPresets.currentIndex === 11
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 50
                value: 5
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("blur") + " " + idFxSliderBlur.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderCentralFocus
                visible: idComboBoxPresets.currentIndex === 13
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 20
                value: 6
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("blur") + " " + idFxSliderCentralFocus.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderMiniatureBlur
                visible: idComboBoxPresets.currentIndex === 14
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 20
                value: 5
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("blur") + " " + idFxSliderMiniatureBlur.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderMiniatureColor
                visible: idComboBoxPresets.currentIndex === 14
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 0
                maximumValue: 2
                value: 1.75
                stepSize: 0.02
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("color") + " " + idFxSliderMiniatureColor.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderAddFrame
                visible: idComboBoxPresets.currentIndex === 20
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 100
                value: 10
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("frame") + " " + idFxSliderAddFrame.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderQuantize
                visible: idComboBoxPresets.currentIndex === 22
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 2
                maximumValue: 256
                value: 256
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("amount colors") + " " + idFxSliderQuantize.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderOpacity
                visible: idComboBoxPresets.currentIndex === 23
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 0
                maximumValue: 100
                value: 100
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("opacity") + " " + idFxSliderOpacity.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            ComboBox {
                id: idComboBoxAlphaColor
                visible: idComboBoxPresets.currentIndex === 24
                x: Theme.paddingMedium
                width: parent.width - Theme.paddingMedium
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("white")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("black")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onCurrentIndexChanged: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
            }
            Slider {
                id: idFxSliderAlphaTolerance
                visible: idComboBoxPresets.currentIndex === 24
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 0
                maximumValue: 256
                value: 30
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("tolerance") + " " + idFxSliderAlphaTolerance.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            ComboBox {
                id: idComboBoxColorExtract
                visible: idComboBoxPresets.currentIndex === 25
                x: Theme.paddingMedium
                width: parent.width - Theme.paddingMedium
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("red")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("green")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("blue")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onCurrentIndexChanged: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
            }
            ComboBox {
                id: idComboBoxChannelExtract
                visible: idComboBoxPresets.currentIndex === 26
                x: Theme.paddingMedium
                width: parent.width - Theme.paddingMedium
                menu: ContextMenu {
                    MenuItem {
                        text: qsTr("red")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("green")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("blue")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                    MenuItem {
                        text: qsTr("alpha")
                        font.pixelSize: Theme.fontSizeExtraSmall
                    }
                }
                onCurrentIndexChanged: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
            }
            Slider {
                id: idFxUnsharpRadiusMask
                visible: idComboBoxPresets.currentIndex === 16
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 0.5
                maximumValue: 5
                value: 3
                stepSize: 0.5
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("radius") + " " + idFxUnsharpRadiusMask.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxUnsharpPercentMask
                visible: idComboBoxPresets.currentIndex === 16
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 5
                maximumValue: 250
                value: 150
                stepSize: 5
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("percent") + " " + idFxUnsharpPercentMask.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxUnsharpThresholdMask
                visible: idComboBoxPresets.currentIndex === 16
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 1
                maximumValue: 10
                value: 3
                stepSize: 1
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("threshold") + " " + idFxUnsharpThresholdMask.value
                    font.pixelSize: Theme.fontSizeExtraSmall
                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -Theme.paddingSmall
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
            Slider {
                id: idFxSliderBrightspotSize
                visible: (idComboBoxPresets.currentIndex === 27 || idComboBoxPresets.currentIndex === 28 || idComboBoxPresets.currentIndex === 29) ? true : false
                enabled: blockerApply === false
                width: parent.width
                height: Theme.itemSizeSmall * 1.1
                leftMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                rightMargin: Theme.paddingLarge + Theme.paddingMedium + Theme.paddingSmall
                minimumValue: 3
                maximumValue: 15
                value: 3
                stepSize: 2
                smooth: true
                onReleased: {
                    blockerApply = true
                    previewImageEffectPicker()
                }
                Label {
                    text: qsTr("size") + " " + idFxSliderBrightspotSize.value
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

    function previewImageEffectPicker () {
        idNewPreviewButtonRunningIndicator.running = true
        if (idComboBoxPresets.currentIndex === 0) {
            currentEffectName = "original"
            idPreviewImage.source = ""
            idPreviewImage.source = previewBaseImagePath
            idNewPreviewButtonRunningIndicator.running = false
        }
        else if (idComboBoxPresets.currentIndex === 1) {
            currentEffectName = "fxAutoContrast"
            py.autocontrastFunction()
        }
        else if (idComboBoxPresets.currentIndex === 2) {
            currentEffectName = "fxStretchContrast"
            py.stretchContrastFunction()
        }
        else if (idComboBoxPresets.currentIndex === 3) {
            currentEffectName = "fxDither"
            py.blackWhiteFunction()
        }
        else if (idComboBoxPresets.currentIndex === 4) {
            currentEffectName = "fxCoal"
            py.coalFilterFunction()
        }        
        else if (idComboBoxPresets.currentIndex === 5) {
            currentEffectName = "fxGray"
            py.grayscaleFunction()
        }
        else if (idComboBoxPresets.currentIndex === 6) {
            currentEffectName = "fxInvert"
            py.invertFunction()
        }
        else if (idComboBoxPresets.currentIndex === 7) {
            currentEffectName = "fxEqualize"
            py.equalizeFunction()
        }
        else if (idComboBoxPresets.currentIndex === 8) {
            currentEffectName = "fxSolarize"
            py.solarizeFunction()
        }
        else if (idComboBoxPresets.currentIndex === 9) {
            currentEffectName = "fxDrawing"
            py.modedrawingFunction()
        }
        else if (idComboBoxPresets.currentIndex === 10) {
            currentEffectName = "fxPosterize"
            py.posterizeFunction()
        }
        else if (idComboBoxPresets.currentIndex === 11) {
            currentEffectName = "fxBlur"
            py.blurFunction()
        }
        else if (idComboBoxPresets.currentIndex === 12) {
            currentEffectName = "fxSmoothSurface"
            py.smoothSurfaceFunction()
        }
        else if (idComboBoxPresets.currentIndex === 13) {
            currentEffectName = "fxCentralFocus"
            py.centerFocusFunction()
        }
        else if (idComboBoxPresets.currentIndex === 14) {
            currentEffectName = "fxMiniature"
            py.miniatureFocusFunction()
        }
        else if (idComboBoxPresets.currentIndex === 15) {
            currentEffectName = "fxEnhanceEdges"
            py.edgeenhanceFunction()
        }
        else if (idComboBoxPresets.currentIndex === 16) {
            currentEffectName = "fxUnsharpMask"
            py.unsharpmaskFunction()
        }
        else if (idComboBoxPresets.currentIndex === 17) {
            currentEffectName = "fxFindEdges"
            py.findedgesFunction()
        }
        else if (idComboBoxPresets.currentIndex === 18) {
            currentEffectName = "fxFindContour"
            py.contourFunction()
        }
        else if (idComboBoxPresets.currentIndex === 19) {
            currentEffectName = "fxEmboss"
            py.embossFunction()
        }
        else if (idComboBoxPresets.currentIndex === 20) {
            currentEffectName = "fxAddFrame"
            py.addFrameFunction()
        }
        else if (idComboBoxPresets.currentIndex === 21) {
            currentEffectName = "fxTintColor"
            py.tintWithColorFunction()
        }
        else if (idComboBoxPresets.currentIndex === 22) {
            currentEffectName = "fxReduceColors"
            py.quantizeFunction()
        }
        else if (idComboBoxPresets.currentIndex === 23) {
            currentEffectName = "fxOpacity"
            py.addAlphaFunction()
        }
        else if (idComboBoxPresets.currentIndex === 24) {
            currentEffectName = "fxAlphaFrom"
            py.colorToAlphaFunction()
        }
        else if (idComboBoxPresets.currentIndex === 25) {
            currentEffectName = "fxExtractColor"
            py.extractColorFunction()
        }
        else if (idComboBoxPresets.currentIndex === 26) {
            currentEffectName = "fxGetChannel"
            py.extractChannelFunction()
        }

        else if (idComboBoxPresets.currentIndex === 27) {
            currentEffectName = "fxMinFilter"
            py.brightspotFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 28) {
            currentEffectName = "fxMaxFilter"
            py.brightspotFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 29) {
            currentEffectName = "fxMedFilter"
            py.brightspotFilterFunction()
        }
        else if (idComboBoxPresets.currentIndex === 30) {
            currentEffectName = "fxFishEye"
            py.fishEyeFunction()
        }

    }
}
