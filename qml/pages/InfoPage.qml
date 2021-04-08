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
                    + qsTr("Active development of Imageworks takes place at https://github.com/poetaster/harbour-simplecrop:") + " "
                    + qsTr("Imageworks was developed by tobias.planitzer@protonmail.com and is maintained by blueprint@poetaster.de") + "."
                    + "\n"
            }

            Label {
                x: Theme.paddingLarge
                width: parent.width - 2 * Theme.paddingLarge
                wrapMode: Text.Wrap
                font.pixelSize: Theme.fontSizeExtraSmall
                text: qsTr("INSTALL") + "\n"
                    + qsTr("This app requires SailfishOS 3.3+.")

            }


        } // end Column



    } // end Silica Flickable
}
