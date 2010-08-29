// No copyright is asserted on this file.

function xhrDfnShow(node, panel, panelDiv) {
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
  var loading = document.createElement("i");
  loading.textContent = "loading";
  panelDiv.appendChild(loading);
  request.onreadystatechange = function () {
    var networkStatus = document.createElement("span");
    panelDiv.appendChild(networkStatus);
    var dots = "..";
    for (var i = 0; i < parseInt(request.readyState); i++) {
      dots += ".";
    }
    while (networkStatus.firstChild) networkStatus.removeChild(networkStatus.firstChild);
    networkStatus.textContent = dots;
    if (request.readyState == 4) {
      panelDiv.innerHTML = request.responseText;
      var pfc = panelDiv.firstChild;
      while (pfc && pfc.nodeType != pfc.ELEMENT_NODE) {
        pfc = pfc.nextSibling;
      }
      if (pfc.className == "has-norefs") {
        var pps = panelDiv.previousSibling;
        while (pps && pps.nodeType != pps.ELEMENT_NODE) {
          pps = pps.previousSibling;
        }
        panel.removeChild(pps);
        panelDiv.innerHTML = "<p class='norefs'>No references in this document.</p>";
        return;
      }
      var pfg = pfc.firstChild;
      while (pfg && pfg.nodeType != pfg.ELEMENT_NODE) {
        pfg = pfg.nextSibling;
      }
      if (pfg.className == "dfn-excerpt") {
        pfc.removeChild(pfg);
      }
    }
  };
  try {
    request.open('GET', 'index-of-terms/'+node.id+'.html', true);
    request.send(null);
  } catch (e) {
    console.log(e);
    return -1;
  }
}
var dfnPanel;
document.addEventListener('click', dfnShow, false);
document.addEventListener("keyup", function(e) {
  if(!e) e=window.event;
  var key = e.keyCode ? e.keyCode : e.which;
  if ( key == 27 && dfnPanel) {
    dfnPanel.parentNode.removeChild(dfnPanel);
    dfnPanel = null;
  }
}, true);
function dfnShow(event) {
  if (dfnPanel) {
    dfnPanel.parentNode.removeChild(dfnPanel);
    dfnPanel = null;
  }
  var dfnClicked = false
  var node = event.target;
  if (node.tagName == "DFN") {
    dfnClicked = true;
  }
  while (node && node.parentNode && (node.nodeType != event.target.ELEMENT_NODE || node.tagName == "A" || !node.hasAttribute("id"))) {
    if (node.parentNode.nodeType == node.parentNode.ELEMENT_NODE && node.parentNode.tagName == "DFN") {
      dfnClicked = true;
    }
    node = node.parentNode;
  }
  var panel = document.createElement('div');
  panel.className = 'dfnPanel';
  if (node && dfnClicked) {
    var permalinkP = document.createElement('p');
    var permalinkA = document.createElement('a');
    permalinkA.href = '#' + node.id;
    permalinkA.textContent = '#' + node.id;
    permalinkP.appendChild(permalinkA);
    panel.appendChild(permalinkP);
    var introP = document.createElement('p');
    panel.appendChild(introP);
    panelDiv = document.createElement('div');
    if (node.id) {
      introP.textContent = "Referenced in:";
      if (document.documentElement.className.indexOf("split") != -1) {
        xhrDfnShow(node, panel, panelDiv);
      } else {
        var targetNode = document.getElementById(node.id+"_index");
        if (targetNode) {
          panelDiv.innerHTML = targetNode.innerHTML;
          panelDiv.removeChild(panelDiv.firstChild);
          if (targetNode.className == "has-norefs") {
            panel.removeChild(introP);
            panelDiv.innerHTML = "<p class='norefs'>No references in this document.</p>";
          }
        } else {
          console.log(node);
          return -1;
        }
      }
      panel.appendChild(panelDiv);
    } else {
      console.log(node);
      return -1;
    }
    node.appendChild(panel);
    dfnPanel = panel;
  } else {
    // Do nothing: The user just clicked at some place in the page
    // that's not special.
  }
}
