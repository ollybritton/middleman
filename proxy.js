/*

This script has been inserted into this page by the Middleman application.

*/

let url_elements = {
    "a": ["href"],
    "applet": ["codebase"],
    "area": ["href"],
    "base": ["href"],
    "blockquote": ["cite"],
    "body": ["background"],
    "del": ["cite"],
    "form": ["action"],
    "frame": ["longdesc", "src"],
    "head": ["profile"],
    "iframe": ["longdesc", "src"],
    "img": ["longdesc", "src", "usemap"],
    "input": ["src", "usemap"],
    "ins": ["cite"],
    "link": ["href"],
    "object": ["classid", "codebase", "data", "usemap"],
    "q": ["cite"],
    "script": ["src"]
}

window.onload = function () {
    // var anchors = document.getElementsByTagName("a");

    // for (var i = 0; i < anchors.length; i++) {
    //     anchors[i].href = "localhost:8000/url/" + anchors[i].href;
    // }

    for(let element of url_elements.keys()) {
        let document_elements = document.getElementsByTagName(element)

        for (let document_element of document_elements) {
            for (let attribute of url_elements[element]) {
                document_element[attribute] = "localhost:8000/url/" + document_element[attribute]
            }
        }
    }
};