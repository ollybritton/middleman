/*

This script has been inserted into this page by the Middleman application.

*/

window.onload = function () {
    var anchors = document.getElementsByTagName("a");

    for (var i = 0; i < anchors.length; i++) {
        anchors[i].href = "localhost:8000/url/" + anchors[i].href;
    }
};