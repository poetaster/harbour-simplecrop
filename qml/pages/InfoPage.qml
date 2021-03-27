import QtQuick 2.6
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.5


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All

    SilicaFlickable {
        id: listView
        anchors.fill: parent
        contentHeight: columnSaveAs.height + idSectionHeader.height  // Tell SilicaFlickable the height of its content.
        VerticalScrollDecorator {}

        SectionHeader {
            id: idSectionHeader
            anchors.top: parent.top
            anchors.topMargin: Theme.paddingMedium
            Row {
                id: idSectionHeaderColumn
                width: parent.width
                spacing: Theme.paddingMedium * 1.3

                Column {
                    width: parent.width - Theme.itemSizeSmall - spacing
                    Label {
                        anchors.right: parent.right
                        font.pixelSize: Theme.fontSizeLarge
                        color: Theme.highlightColor
                        text: qsTr("Imageworks")
                    }
                    Label {
                        anchors.right: parent.right
                        font.pixelSize: Theme.fontSizeTiny
                        color: Theme.highlightColor
                        text: qsTr("Photo editor for SailfishOS") + "\n "
                    }
                }

                Image {
                    width: Theme.itemSizeSmall
                    source: "../cover/imageworks.svg"
                    sourceSize.width: Theme.itemSizeSmall
                    sourceSize.height: Theme.itemSizeSmall
                    fillMode: Image.PreserveAspectFit
                }
            }
        }

        Column {
            id: columnSaveAs
            width: parent.width

            Item {
                width: parent.width
                height: idSectionHeader.height + Theme.paddingLarge * 3
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                text: qsTr("CONTACT") + "\n"
                    + qsTr("Active development of Imageworks has been completed. However, if you would like to send some greetings, report a bug or even sponsor further development, please contact me here:") + " "
                    + qsTr("tobias.planitzer@protonmail.com") + "."
                    + "\n"
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                text: qsTr("INSTALL") + "\n"
                    + qsTr("This app requires SailfishOS 3.3+ and python3-pillow library in version 7+ which is available on Openrepos.net.") + " "
                    + qsTr("Make sure you have only ONE of them installed!")
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                color: Theme.highlightColor
                text: "     Standard: python3-pillow"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        Qt.openUrlExternally("https://openrepos.net/content/birdzhang/python3-pillow")
                    }
                }
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                color: Theme.highlightColor
                text: "     Experimental: python3-pillow-simd"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        Qt.openUrlExternally("https://openrepos.net/content/planetosstore/python3-pillow-simd")
                    }
                }
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                text: "\n"
                      + qsTr("HOW TO") + "\n"
                      + qsTr("1) Download the latest file suitable for your device:") + "\n"
                      + qsTr("     Smartphones usually ...armv7hl.rpm") + "\n"
                      + qsTr("     Tablets possibly ...i486.rpm") + "\n"
                      + qsTr("2) Allow '3rd party software' in Sailfish settings") + "\n"
                      + qsTr("3) Install python3-pillow manually")
                      + "\n"
            }


        } // end Column



    } // end Silica Flickable
}
