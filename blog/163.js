// ==UserScript==
// @name           blog1by1
// @namespace      http://hankjin.vicp.net/script/blog/163
// @include        http://hankjin.blog.163.com/*
// ==/UserScript==

window.logPage = function () {
    var nextLink;
    nextLink = document.evaluate("//a[@class='m2a']", document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
    var req = new XMLHttpRequest();
    var blogurl = "http://hankjin.vicp.net/util/163.php?id=hankjin&url=" + window.location.href;
    GM_log(blogurl);
    req.open("GET", blogurl, true);
    req.addEventListener("load", function (e) {
        if (0 == nextLink.snapshotLength) {
            alert("Over");
        }
        else {
            nextLink.snapshotItem(0).click();
        }
    }, false)
    req.send();
}
window.onload = function () {
    alert("hi");
    setTimeout("logPage()", 5000); //¸ô֮ºóÐӦ¸þÍܽâÕ¸öâ
}
