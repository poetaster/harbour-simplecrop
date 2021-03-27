import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5
import Sailfish.Pickers 1.0
import "catmullromcurve.js" as CurveC

Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    // values transmitted from FirstPage.qml
    property var inputPathPy
    property var outputPathPy
    property var tempImageFolderPath
    property var handleWidth
    property var handleHeight
    property var toolsDrawingColorFrame
    property var opacityEdges
    property var opticalDividersWidth

    // variables for UI
    property var itemsPerRow : 5
    property var outputPathHistA : tempImageFolderPath + "histA" + ".tmp" + ".png"
    property var outputPathHistRGB : tempImageFolderPath + "histRGB" + ".tmp" + ".png"
    property var outputPathHistR : tempImageFolderPath + "histR" + ".tmp" + ".png"
    property var outputPathHistG : tempImageFolderPath + "histG" + ".tmp" + ".png"
    property var outputPathHistB : tempImageFolderPath + "histB" + ".tmp" + ".png"
    property var currentColor : "rgb"
    property var amountRegions : 8
    property var currentSliderValue : ""

    // variables for calculation
    property var curveFactors : ""
    property var maxA : "max"
    property var maxR : "max"
    property var maxG : "max"
    property var maxB : "max"
    property var maxRGB : "max"


    Component.onCompleted: {
        // get infos from the original file
        py.createHistogramImageFunction()
    }


    Python {
        id: py
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('../py'));
            importModule('graphx', function () {}); // Which Pythonfile will be used?

            setHandler('histogramsReady', function(max_alpha, max_red, max_green, max_blue, max_rgb) {
                idImageLoadedHistoR.source = ""
                idImageLoadedHistoR.source = outputPathHistRGB
                maxA = max_alpha
                maxR = max_red
                maxG = max_green
                maxB = max_blue
                maxRGB = max_rgb
            })
        }

        function colorcurveMiddleStepFunction() {
            var minValue = (idMinManual.text).toString()
            if (minValue === "") {
                minValue = "0"
            }

            var maxValue = (idMaxManual.text).toString()
            if (maxValue === "") {
                maxValue = "255"
            }
            call("graphx.colorcurveMiddleStepFunction", [ curveFactors, currentColor, minValue, maxValue ])
        }
        function createHistogramImageFunction() {
            call("graphx.createHistogramImageFunction", [ inputPathPy, outputPathPy, outputPathHistA, outputPathHistR, outputPathHistG, outputPathHistB, outputPathHistRGB ])
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
                        text: qsTr("Color bench")
                    }
                    Label {
                        id: idLabelFilePath
                        width: parent.width
                        anchors.right: parent.right
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        truncationMode: TruncationMode.Elide
                        text: qsTr("histogram, adjust curves") + "\n "
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
                        id: labelAlpha
                        width: parent.width / 5
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Alpha")
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentColor = "alpha"
                                labelGraphRight.text = maxA
                                parent.color = Theme.highlightColor
                                labelRGB.color = Theme.primaryColor
                                labelRed.color = Theme.primaryColor
                                labelGreen.color = Theme.primaryColor
                                labelBlue.color = Theme.primaryColor
                                idImageLoadedHistoR.source = ""
                                idImageLoadedHistoR.source = outputPathHistA
                            }
                        }
                    }
                    Label {
                        id: labelRGB
                        width: parent.width / 5
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.horizontalCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        color : Theme.highlightColor
                        text: qsTr("RGB")
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentColor = "rgb"
                                parent.color = Theme.highlightColor
                                labelGraphRight.text = maxRGB
                                labelAlpha.color = Theme.primaryColor
                                labelRed.color = Theme.primaryColor
                                labelGreen.color = Theme.primaryColor
                                labelBlue.color = Theme.primaryColor
                                idImageLoadedHistoR.source = ""
                                idImageLoadedHistoR.source = outputPathHistRGB
                            }
                        }
                    }
                    Label {
                        id: labelRed
                        width: parent.width / 5
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.horizontalCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Red")
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentColor = "red"
                                parent.color = Theme.highlightColor
                                labelGraphRight.text = maxR
                                labelAlpha.color = Theme.primaryColor
                                labelRGB.color = Theme.primaryColor
                                labelGreen.color = Theme.primaryColor
                                labelBlue.color = Theme.primaryColor
                                idImageLoadedHistoR.source = ""
                                idImageLoadedHistoR.source = outputPathHistR
                            }
                        }
                    }
                    Label {
                        id: labelGreen
                        width: parent.width / 5
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.horizontalCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Green")
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentColor = "green"
                                parent.color = Theme.highlightColor
                                labelGraphRight.text = maxG
                                labelAlpha.color = Theme.primaryColor
                                labelRGB.color = Theme.primaryColor
                                labelRed.color = Theme.primaryColor
                                labelBlue.color = Theme.primaryColor
                                idImageLoadedHistoR.source = ""
                                idImageLoadedHistoR.source = outputPathHistG
                            }
                        }
                    }
                    Label {
                        id: labelBlue
                        width: parent.width / 5
                        height: Theme.itemSizeSmall
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.horizontalCenter
                        leftPadding: Theme.paddingLarge
                        font.pixelSize: Theme.fontSizeExtraSmall
                        text: qsTr("Blue")
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentColor = "blue"
                                parent.color = Theme.highlightColor
                                labelGraphRight.text = maxB
                                labelAlpha.color = Theme.primaryColor
                                labelRGB.color = Theme.primaryColor
                                labelRed.color = Theme.primaryColor
                                labelGreen.color = Theme.primaryColor
                                idImageLoadedHistoR.source = ""
                                idImageLoadedHistoR.source = outputPathHistB
                            }
                        }
                    }
                }
                IconButton {
                    id: idApplyButton
                    visible:  true
                    width: parent.width / itemsPerRow
                    height: Theme.itemSizeSmall
                    icon.source: "../symbols/icon-m-apply.svg"
                    icon.width: Theme.iconSizeMedium
                    icon.height: Theme.iconSizeMedium
                    onClicked: {
                        getValues()
                        py.colorcurveMiddleStepFunction()
                        pageStack.pop()
                    }
                }
            }


            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 4
                color: "transparent"
            }


            Image {
                id: idImageLoadedHistoR
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: Theme.paddingLarge * 2
                anchors.rightMargin: Theme.paddingLarge * 2
                height: width
                fillMode: Image.PreserveAspectFit
                source: ""
                cache: false

                Rectangle {
                    id: idBackgroundFillerWhite
                    anchors.fill: parent
                    anchors.topMargin: -3*Theme.paddingLarge
                    anchors.bottomMargin: -3*Theme.paddingLarge
                    anchors.leftMargin: -2*Theme.paddingLarge
                    anchors.rightMargin: -2*Theme.paddingLarge
                    color: Theme.highlightColor
                    opacity: 0.25
                    z: -1
                }
                Label {
                    id: labelGraphLeft
                    anchors.right: idBackgroundFillerWhite.left
                    anchors.rightMargin: -2*Theme.paddingLarge + Theme.paddingSmall
                    anchors.verticalCenter: idBackgroundFillerWhite.top
                    anchors.verticalCenterOffset: Theme.paddingLarge
                    text: "255"
                    font.pixelSize: Theme.fontSizeExtraSmall
                    opacity: 5
                }
                Label {
                    anchors.horizontalCenter: labelGraphLeft.horizontalCenter
                    anchors.verticalCenter: idBackgroundFillerWhite.verticalCenter
                    text: qsTr("output  curve")
                    font.pixelSize: Theme.fontSizeExtraSmall
                    rotation: -90
                }
                Label {
                    id: idMinLabel
                    anchors.right: idBackgroundFillerWhite.left
                    anchors.rightMargin: -2*Theme.paddingLarge + Theme.paddingSmall
                    anchors.bottom: idBackgroundFillerWhite.bottom
                    anchors.bottomMargin: Theme.paddingSmall
                    text: "0"
                    font.pixelSize: Theme.fontSizeExtraSmall
                }
                Label {
                    anchors.horizontalCenter: idBackgroundFillerWhite.horizontalCenter
                    anchors.bottom: idBackgroundFillerWhite.bottom
                    anchors.bottomMargin: Theme.paddingSmall
                    text: qsTr("input  values")
                    font.pixelSize: Theme.fontSizeExtraSmall
                }
                Label {
                    anchors.horizontalCenter: idBackgroundFillerWhite.right
                    anchors.horizontalCenterOffset: -2*Theme.paddingLarge
                    anchors.bottom: idBackgroundFillerWhite.bottom
                    anchors.bottomMargin: Theme.paddingSmall
                    text: "255"
                    font.pixelSize: Theme.fontSizeExtraSmall
                }
                Label {
                    id: labelGraphRight
                    anchors.right: idBackgroundFillerWhite.right
                    anchors.rightMargin: Theme.paddingSmall
                    anchors.verticalCenter: idBackgroundFillerWhite.top
                    anchors.verticalCenterOffset: Theme.paddingLarge
                    text: maxRGB
                    font.pixelSize: Theme.fontSizeExtraSmall
                    opacity: 5
                }
                Label {
                    id: labelGraphLabelRight
                    anchors.horizontalCenter: idBackgroundFillerWhite.right
                    anchors.horizontalCenterOffset: - Theme.paddingLarge
                    anchors.verticalCenter: idBackgroundFillerWhite.verticalCenter
                    text: qsTr("occurances")
                    font.pixelSize: Theme.fontSizeExtraSmall
                    rotation: -90
                }
                Label {
                    id: labelCurrentCurveValue
                    visible:  (mouseHandle1.pressed || mouseHandle2.pressed || mouseHandle3.pressed || mouseHandle4.pressed || mouseHandle5.pressed || mouseHandle6.pressed || mouseHandle7.pressed || mouseHandle8.pressed || mouseHandle9.pressed ) ? true : false
                    anchors.horizontalCenter: idBackgroundFillerWhite.horizontalCenter
                    anchors.verticalCenter: idBackgroundFillerWhite.top
                    anchors.verticalCenterOffset: Theme.paddingLarge
                    text: currentSliderValue
                    font.pixelSize: Theme.fontSizeExtraSmall
                }




                Item {
                    id: idItemPerspectiveHandles
                    anchors.fill: parent

                    Rectangle {
                        id: rectHandle1
                        x: - handleWidth / 2
                        y: idItemPerspectiveHandles.height - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle1
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle1 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle1 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle2
                        x: idItemPerspectiveHandles.width / amountRegions * 1 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-1) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle2
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle2 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle2 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle3
                        x: idItemPerspectiveHandles.width / amountRegions * 2 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-2) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle3
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle3 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle3 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle4
                        x: idItemPerspectiveHandles.width / amountRegions * 3 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-3) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle4
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle4 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle4 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle5
                        x: idItemPerspectiveHandles.width / amountRegions * 4 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-4) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle5
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle5 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle5 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle6
                        x: idItemPerspectiveHandles.width / amountRegions * 5 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-5) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle6
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle6 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle6 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle7
                        x: idItemPerspectiveHandles.width / amountRegions * 6 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-6) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle7
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle7 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle7 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle8
                        x: idItemPerspectiveHandles.width / amountRegions * 7 - handleWidth / 2
                        y: idItemPerspectiveHandles.height / amountRegions * (amountRegions-7) - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle8
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle8 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle8 )
                            }
                        }
                    }
                    Rectangle {
                        id: rectHandle9
                        x: idItemPerspectiveHandles.width - handleWidth / 2
                        y: - handleHeight/2
                        radius: handleWidth
                        width: handleWidth
                        height: handleHeight
                        color: toolsDrawingColorFrame
                        opacity: opacityEdges
                        MouseArea {
                            id: mouseHandle9
                            anchors.fill: parent
                            drag.target: parent
                            drag.axis: Drag.YAxis
                            drag.minimumY: (idItemPerspectiveHandles.y - handleHeight/2)
                            drag.maximumY: (idItemPerspectiveHandles.height - handleHeight/2)
                            onEntered: getCurrentSliderValue( rectHandle9 )
                            onPositionChanged: {
                                colorcurveCanvas.clear_canvas()
                                getCurrentSliderValue( rectHandle9 )
                            }
                        }
                    }

                    // normal distribution
                    Rectangle {
                        opacity: opacityEdges
                        color: "black" // toolsDrawingColorFrame
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: Math.sqrt( ((parent.width) * (parent.width)) + ((parent.height) * (parent.height)) )
                        height: opticalDividersWidth * 2 //ToDo: 1
                        rotation: -Math.atan( (parent.height) / (parent.width) ) * (180 / Math.PI)
                    }

                    // custom distribution
                    Canvas {
                        id: colorcurveCanvas
                        anchors.fill: parent
                        contextType: "2d"
                        function clear_canvas() {
                            var ctx = getContext("2d")
                            ctx.reset()
                            colorcurveCanvas.requestPaint()
                        }
                        Path {
                            id: myPath
                            startX: rectHandle1.x + handleWidth/2
                            startY: rectHandle1.y + handleHeight/2
                            PathCurve { x: rectHandle2.x + handleWidth/2; y: rectHandle2.y + handleHeight/2 }
                            PathCurve { x: rectHandle3.x + handleWidth/2; y: rectHandle3.y + handleHeight/2 }
                            PathCurve { x: rectHandle4.x + handleWidth/2; y: rectHandle4.y + handleHeight/2 }
                            PathCurve { x: rectHandle5.x + handleWidth/2; y: rectHandle5.y + handleHeight/2 }
                            PathCurve { x: rectHandle6.x + handleWidth/2; y: rectHandle6.y + handleHeight/2 }
                            PathCurve { x: rectHandle7.x + handleWidth/2; y: rectHandle7.y + handleHeight/2 }
                            PathCurve { x: rectHandle8.x + handleWidth/2; y: rectHandle8.y + handleHeight/2 }
                            PathCurve { x: rectHandle9.x + handleWidth/2; y: rectHandle9.y + handleHeight/2 }
                        }
                        onPaint: {
                            var ctx = getContext("2d")
                            ctx.strokeStyle = toolsDrawingColorFrame
                            ctx.lineCap = 'round'
                            ctx.lineWidth = Theme.paddingSmall
                            context.path = myPath
                            ctx.stroke()
                        }
                    }
                }
            } // end image


            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 3
                color: "transparent"
            }

            Row {
                //x: Theme.paddingLarge
                width: parent.width //- Theme.paddingLarge

                Label {
                    width: parent.width / 7
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: Theme.paddingLarge * 1.25
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("min")
                }
                TextField {
                    id: idMinManual
                    text: "0"
                    width: parent.width / 7
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingLarge * 0.8
                    horizontalAlignment: Text.AlignLeft //HCenter
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: {
                        idMinManual.focus = false
                    }
                }
                Label {
                    width: parent.width / 7 * 3
                    height: parent.height
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    //text: qsTr("only between")
                }
                TextField {
                    id: idMaxManual
                    text: "255"
                    width: parent.width / 7
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.verticalCenterOffset: Theme.paddingLarge * 0.8
                    horizontalAlignment: Text.AlignRight //HCenter
                    color: Theme.highlightColor
                    inputMethodHints: Qt.ImhDigitsOnly
                    font.pixelSize: Theme.fontSizeExtraSmall
                    validator: IntValidator { bottom: 0; top: 255 }
                    EnterKey.onClicked: {
                        idMaxManual.focus = false
                    }
                }
                Label {
                    width: parent.width / 7
                    height: Theme.itemSizeSmall
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    rightPadding: Theme.paddingLarge * 1.25
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("max")
                }
            }
            Rectangle {
                width: parent.width
                height: Theme.paddingLarge * 1.5
                color: "transparent"
            }


        } // end Column
    } // end Silica Flickable

    function getValues() {
        curveFactors = ""
        var pointsC = [rectHandle1.x + handleWidth/2, rectHandle1.y + handleHeight/2,
                       rectHandle2.x + handleWidth/2, rectHandle2.y + handleHeight/2,
                       rectHandle3.x + handleWidth/2, rectHandle3.y + handleHeight/2,
                       rectHandle4.x + handleWidth/2, rectHandle4.y + handleHeight/2,
                       rectHandle5.x + handleWidth/2, rectHandle5.y + handleHeight/2,
                       rectHandle6.x + handleWidth/2, rectHandle6.y + handleHeight/2,
                       rectHandle7.x + handleWidth/2, rectHandle7.y + handleHeight/2,
                       rectHandle8.x + handleWidth/2, rectHandle8.y + handleHeight/2,
                       rectHandle9.x + handleWidth/2, rectHandle9.y + handleHeight/2
                      ]
        var allPoints = CurveC.getCurvePoints(pointsC, 0.5, 32) // 32_elements in 8_fields = 256_values, plus 0,0 === 257_values!!!
        var helperCounter = 0
        var normalYHere
        var scaleFactor = 256 / colorcurveCanvas.width
        for (var i=0; i<allPoints.length; i++) {
            helperCounter = helperCounter + 1
            if (helperCounter === 1) {
                normalYHere = i/2 // allPoints[i] * scaleFactor // y = x, because y=1x+0
            }
            else if (helperCounter === 2) {
                // Patch: take out middle value, to have only 156 values left, instead of 257
                if (normalYHere !== 128) {
                    // Patch: can not devide first value by zero
                    if (normalYHere !== 0) {
                        var factorIntensity = (( colorcurveCanvas.height-allPoints[i]) * scaleFactor) / normalYHere
                    }
                    else {
                        factorIntensity = (( colorcurveCanvas.height-allPoints[i]) * scaleFactor) / 1
                    }
                    curveFactors = curveFactors + factorIntensity + ";"
                }
                helperCounter = 0
            }
        }
    }

    function getCurrentSliderValue( handleName ) {
        currentSliderValue = Math.round(255 / colorcurveCanvas.height * ( colorcurveCanvas.height - ( handleName.y + handleHeight/2 )))
    }

}
