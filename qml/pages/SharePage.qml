import QtQuick 2.6
import Sailfish.Silica 1.0
import Sailfish.TransferEngine 1.0

Page {
    id: page
    allowedOrientations: Orientation.Portrait

    // from FirstPage.qml
    property var shareFilePath
    property var shareFileName

    // UI values
    property var mimeType : "image/*"
    property bool sizeWarning : false

    Component.onCompleted: {
        if (shareFilePath.indexOf(".tmp") === -1) {
            sizeWarning = true
        }
    }

    ShareMethodList {
        id: idShareMethodList
        anchors.fill: parent

        header: SectionHeader {
            id: idSectionHeader
            height: idSectionHeaderColumn.height
            Column {
                id: idSectionHeaderColumn
                width: parent.width / 5 * 4
                height: idLabelProgramName.height + idLabelFileWarning.height
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
                    text: qsTr("Share image")
                }
                Label {
                    id: idLabelFileWarning
                    width: parent.width
                    anchors.right: parent.right
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: Theme.fontSizeTiny
                    color: Theme.highlightColor
                    truncationMode: TruncationMode.Elide
                    text: (sizeWarning === true) ? ( qsTr("sending file to") + "\n") : ( qsTr("You are about to send a large temporary PNG file.") + "\n"
                                                                                    + qsTr("Save as JPG first, if you need smaller filesize.") + "\n"
                                                                                    + "\n" )
                }
            }
        }
        source: shareFilePath
        filter: mimeType

        /*
        content: {
            "name": shareFileName,
            "type": type,
            //"data": shareFilePath,
            //"status": shareFilePath, //e.g. email text
            //"icon": someFileTypeIcon
        }

        ViewPlaceholder {
            enabled: (idShareMethodList.model.count === 0)
            text: qsTr("No sharing plugins installed which can share that image!")
        }
        */
    }
}
