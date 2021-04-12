import QtQuick 2.6
import Sailfish.Silica 1.0


Page {
    id: page
    allowedOrientations: Orientation.Portrait //All
    PageHeader {
        title: qsTr("About Imageworks")
    }
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
                Image {
                    width: Theme.itemSizeSmall
                    source: "../cover/imageworks.svg"
                    sourceSize.width: Theme.itemSizeSmall
                    sourceSize.height: Theme.itemSizeSmall
                    fillMode: Image.PreserveAspectFit
                }
                Item {
                    width: parent.width
                    height: idSectionHeader.height + Theme.paddingLarge * 3
                }
                Label {
                    width: parent.width
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: Theme.fontSizeExtraSmall
                    color: Theme.secondaryColor
                    text: qsTr("Copyright © 2020 Tobias Planitzer")
                          + qsTr(" © 2021 Mark Washeim")
                }
                Item {
                    width: parent.width
                    height: idSectionHeader.height + Theme.paddingLarge * 3
                }
                Label {
                    x: Theme.paddingLarge
                    width: parent.width - 2 * Theme.paddingLarge
                    wrapMode: Text.Wrap
                    font.pixelSize: Theme.fontSizeExtraSmall
                    text: qsTr("Feedback: https://github.com/poetaster/harbour-simplecrop:")
                }

                }
            }
        }




    } // end Silica Flickable
}
