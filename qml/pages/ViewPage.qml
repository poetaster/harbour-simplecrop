import QtQuick 2.6
import Sailfish.Silica 1.0

Page {
    id: imagePage
    property var inputPathPy
    allowedOrientations: Orientation.All

    Component.onCompleted: {
        animateOpacity.start()
    }

    Rectangle {
    //SilicaFlickable {
        id: root
        anchors.fill: parent
        color: "black"  //"transparent" -> for rectangle

        Item {
            id: photoFrame
            width: root.width
            height: root.height
            Image {
                id: image
                anchors.fill: parent
                source: inputPathPy
                fillMode: Image.PreserveAspectFit
                cache: false
            }

            PinchArea {
                anchors.fill: parent
                pinch.target: photoFrame
                pinch.minimumRotation: 0
                pinch.maximumRotation: 0
                pinch.minimumScale: 1
                pinch.maximumScale: 10 //8
                onPinchUpdated: {
                    if(photoFrame.x < dragArea.drag.minimumX)
                        photoFrame.x = dragArea.drag.minimumX
                    else if(photoFrame.x > dragArea.drag.maximumX)
                        photoFrame.x = dragArea.drag.maximumX

                    if(photoFrame.y < dragArea.drag.minimumY)
                        photoFrame.y = dragArea.drag.minimumY
                    else if(photoFrame.y > dragArea.drag.maximumY)
                        photoFrame.y = dragArea.drag.maximumY
                }
                onPinchStarted: {
                    animateOpacity.stop()
                    idZoomLabel.opacity = 1
                }
                onPinchFinished: {
                    animateOpacity.start()
                }

                MouseArea {
                    id: dragArea
                    hoverEnabled: true
                    anchors.fill: parent
                    drag.target: photoFrame
                    //scrollGestureEnabled: false  // 2-finger-flick gesture should pass through to the Flickable
                    drag.minimumX: (root.width - (photoFrame.width * photoFrame.scale))/2
                    drag.maximumX: -(root.width - (photoFrame.width * photoFrame.scale))/2
                    drag.minimumY: (root.height - (photoFrame.height * photoFrame.scale))/2
                    drag.maximumY: -(root.height - (photoFrame.height * photoFrame.scale))/2

                    onDoubleClicked: { //reset size and location of view
                        photoFrame.x = 0
                        photoFrame.y = 0
                        photoFrame.scale = 1
                        animateOpacity.stop()
                        idZoomLabel.opacity = 1
                        animateOpacity.start()
                    }
                    onWheel: {
                        var scaleBefore = photoFrame.scale
                        photoFrame.scale += photoFrame.scale * wheel.angleDelta.y / 120 / 10
                        if(photoFrame.scale < 1)
                            photoFrame.scale = 1
                        else if(photoFrame.scale > 4)
                            photoFrame.scale = 4

                        if(photoFrame.x < drag.minimumX)//dont zoom behind border of image
                            photoFrame.x = drag.minimumX
                        else if(photoFrame.x > drag.maximumX)
                            photoFrame.x = drag.maximumX

                        if(photoFrame.y < drag.minimumY)
                            photoFrame.y = drag.minimumY
                        else if(photoFrame.y > drag.maximumY)
                            photoFrame.y = drag.maximumY
                    }
                }
            }
        }

        Label {
            id: idZoomLabel
            anchors.top: parent.top
            anchors.topMargin: Theme.paddingLarge
            anchors.right: parent.right
            anchors.rightMargin: Theme.paddingLarge
            text: photoFrame.scale.toFixed(1) + "x"
            Rectangle {
                z: -1
                anchors.fill: parent
                anchors.leftMargin: -Theme.paddingMedium
                anchors.rightMargin: -Theme.paddingMedium
                color: Theme.overlayBackgroundColor
                opacity: 0.4
            }
        }

        NumberAnimation {
            id: animateOpacity
            target: idZoomLabel
            properties: "opacity"
            from: 1
            to: 0
            loops: 1 //Animation.Infinite
            duration: 1500
       }

    }
}
