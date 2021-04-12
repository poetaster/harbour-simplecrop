import QtQuick 2.0
import Sailfish.Silica 1.0

Page {
    objectName: "AboutPage"

    allowedOrientations: Orientation.All

    Column {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: Theme.paddingMedium
        anchors.rightMargin: Theme.paddingMedium

        PageHeader {
            title: qsTr("About Imageworks")
        }

        Item {
            width: 1
            height: 3 * Theme.paddingLarge
        }

        Image {
            width: parent.width / 5
            height: width
            anchors.horizontalCenter: parent.horizontalCenter
            source: "../cover/imageworks.svg"
            smooth: true
            asynchronous: true
        }

        Item {
            width: 1
            height: Theme.paddingLarge
        }

        Label {
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: Theme.fontSizeMedium
            color: Theme.primaryColor
            text: qsTr("An Image Editor")
        }

        Item {
            width: 1
            height: Theme.paddingLarge
        }

        Label {
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: Theme.fontSizeExtraSmall
            color: Theme.secondaryColor
            text: qsTr("Copyright © 2020 Tobias Planitzer") + "\n "
                  + qsTr(" © 2021 Mark Washeim")
        }

        Item {
            width: 1
            height: 2 * Theme.paddingLarge
        }

        Label {
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: Theme.fontSizeSmall
            color: Theme.secondaryColor
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
            text: qsTr("Tidings is open source software licensed under the terms of ")
                  + qsTr("the GNU General Public License.")
        }

        /*Item {
            width: 1
            height: 2 * Theme.paddingLarge
        }

        Button {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("View license")
            onClicked: {
                pageStack.push(Qt.resolvedUrl("LicensePage.qml"));
            }
        }*/

    }

    Label {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: Theme.paddingSmall
        color: Theme.secondaryColor
        font.pixelSize: Theme.fontSizeTiny
        text: "https://github.com/poetaster/harbour-simplecrop"
    }

}
