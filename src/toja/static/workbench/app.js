(function(t){function e(e){for(var n,o,r=e[0],c=e[1],d=e[2],l=0,h=[];l<r.length;l++)o=r[l],Object.prototype.hasOwnProperty.call(s,o)&&s[o]&&h.push(s[o][0]),s[o]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(t[n]=c[n]);u&&u(e);while(h.length)h.shift()();return i.push.apply(i,d||[]),a()}function a(){for(var t,e=0;e<i.length;e++){for(var a=i[e],n=!0,r=1;r<a.length;r++){var c=a[r];0!==s[c]&&(n=!1)}n&&(i.splice(e--,1),t=o(o.s=a[0]))}return t}var n={},s={app:0},i=[];function o(e){if(n[e])return n[e].exports;var a=n[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=t,o.c=n,o.d=function(t,e,a){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},o.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(o.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)o.d(a,n,function(e){return t[e]}.bind(null,n));return a},o.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="/";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],c=r.push.bind(r);r.push=e,r=r.slice();for(var d=0;d<r.length;d++)e(r[d]);var u=c;i.push([1,"chunk-vendors"]),a()})({0:function(t,e){},1:function(t,e,a){t.exports=a("cd49")},2:function(t,e){},cd49:function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var n=a("2b0e"),s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"workbench",attrs:{id:"app"}},[a("joke-selector"),a("joke-list"),a("joke-transcriber")],1)},i=[],o=a("d4ec"),r=a("bee2"),c=a("99de"),d=a("7e84"),u=a("262e"),l=a("9ab4"),h=a("60a3"),f=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeMove},on:{click:function(e){return t.setMode("move")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M13,6V11H18V7.75L22.25,12L18,16.25V13H13V18H16.25L12,22.25L7.75,18H11V13H6V16.25L1.75,12L6,7.75V11H11V6H7.75L12,1.75L16.25,6H13Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeAdd},on:{click:function(e){return t.setMode("add")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeEdit},on:{click:function(e){return t.setMode("edit")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}})])])]),a("li",{attrs:{role:"separator"}}),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomInitial}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M9.5,13.09L10.91,14.5L6.41,19H10V21H3V14H5V17.59L9.5,13.09M10.91,9.5L9.5,10.91L5,6.41V10H3V3H10V5H6.41L10.91,9.5M14.5,13.09L19,17.59V14H21V21H14V19H17.59L13.09,14.5L14.5,13.09M13.09,9.5L17.59,5H14V3H21V10H19V6.41L14.5,10.91L13.09,9.5Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomIn}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M15.5,14L20.5,19L19,20.5L14,15.5V14.71L13.73,14.43C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.43,13.73L14.71,14H15.5M9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14M12,10H10V12H9V10H7V9H9V7H10V9H12V10Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomOut}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M15.5,14H14.71L14.43,13.73C15.41,12.59 16,11.11 16,9.5A6.5,6.5 0 0,0 9.5,3A6.5,6.5 0 0,0 3,9.5A6.5,6.5 0 0,0 9.5,16C11.11,16 12.59,15.41 13.73,14.43L14,14.71V15.5L19,20.5L20.5,19L15.5,14M9.5,14C7,14 5,12 5,9.5C5,7 7,5 9.5,5C12,5 14,7 14,9.5C14,12 12,14 9.5,14M7,9H12V10H7V9Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotEdit,disabled:t.nothingSelected},on:{click:t.saveChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotEdit,disabled:t.nothingSelected},on:{click:t.discardChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z"}})])])])])]),a("div",{staticStyle:{overflow:"hidden"},attrs:{id:t.guid}},[a("canvas")])])},m=[],v=(a("4160"),a("159b"),a("803b")),b=function(t){function e(){var t;return Object(o["a"])(this,e),t=Object(c["a"])(this,Object(d["a"])(e).apply(this,arguments)),t.guid="joke-selector-canvas",t.viewer=null,t.canvas=null,t.viewerWidth=0,t.viewerHeight=0,t.zoom=1,t.imgBounds={x:0,y:0,width:0,height:0},t.dragging=!1,t.img=null,t.mode="move",t.newRect=null,t.jokes=[],t.selected=null,t}return Object(u["a"])(e,t),Object(r["a"])(e,[{key:"mounted",value:function(){var t=this;this.$data.viewer=document.querySelector("#"+this.$data.guid),this.$data.viewer&&(this.$data.canvas=new v["fabric"].Canvas(this.$data.viewer.querySelector("canvas")),this.$data.canvas.set({selection:!1,uniScaleTransform:!0}),this.$data.canvas.on("mouse:down",(function(e){t.mouseDown(e.e)})),this.$data.canvas.on("mouse:move",(function(e){t.mouseMove(e.e)})),this.$data.canvas.on("mouse:up",(function(e){t.mouseUp(e.e)})),this.$data.canvas.on("mouse:dblclick",(function(){t.zoomIn()})),this.$data.canvas.on("mouse:wheel",(function(e){t.mouseScroll(e.e)})),this.$data.canvas.on("selection:created",(function(e){t.objectSelected()})),this.$data.canvas.on("selection:cleared",(function(e){t.objectDeselected()})),window.addEventListener("resize",this.resize),this.resize())}},{key:"beforeDestroy",value:function(){window.removeEventListener("resize",this.resize)}},{key:"resize",value:function(){if(this.$data.viewerWidth=this.$data.viewer.clientWidth,this.$data.viewerHeight=this.$data.viewer.clientHeight,this.$data.canvas.setWidth(this.$data.viewerWidth),this.$data.canvas.setHeight(this.$data.viewerHeight),this.$data.img){this.$data.zoom=this.$data.viewerHeight/this.$data.imgBounds.height,this.$data.maxZoom=this.$data.zoom;var t=this.$data.canvas.viewportTransform;t[5]=0,this.$data.canvas.setViewportTransform(t),this.update()}}},{key:"setMode",value:function(t){"edit"===this.$data.mode&&(this.$data.jokes.forEach((function(t){t.set({selectable:!1})})),this.$data.canvas.discardActiveObject().renderAll(),this.$data.canvas.hoverCursor="pointer"),this.$data.mode=t,"move"===t?this.$data.canvas.hoverCursor="move":"add"===t?this.$data.canvas.hoverCursor="crosshair":"edit"===t&&(this.$data.canvas.hoverCursor="pointer",this.$data.jokes.forEach((function(t){t.set({selectable:!0})})),this.$data.canvas.renderAll())}},{key:"zoomInitial",value:function(){this.$data.zoom=this.$data.maxZoom;var t=this.$data.canvas.viewportTransform;t[5]=0,this.$data.canvas.setViewportTransform(t),this.update()}},{key:"zoomIn",value:function(){this.$data.zoom=Math.min(this.$data.zoom+(1-this.$data.maxZoom)/5,1),this.update()}},{key:"zoomOut",value:function(){this.$data.zoom=Math.max(this.$data.zoom-(1-this.$data.maxZoom)/5,this.$data.maxZoom),this.update()}},{key:"mouseDown",value:function(t){this.$data.dragging=!0,this.$data.startMouseX=t.offsetX,this.$data.startMouseY=t.offsetY,"add"===this.$data.mode&&(this.$data.newRect=new v["fabric"].Rect({left:(t.offsetX-this.$data.canvas.viewportTransform[4])/this.$data.zoom,top:(t.offsetY-this.$data.canvas.viewportTransform[5])/this.$data.zoom,width:0,height:0,fill:"transparent",stroke:"#00aa00",hasRotatingPoint:!1,hasBorders:!1,hasCorners:!1}),this.$data.canvas.add(this.$data.newRect))}},{key:"mouseMove",value:function(t){if(this.$data.dragging)if("move"===this.$data.mode){var e=this.$data.canvas.viewportTransform;e[4]=e[4]+(t.offsetX-this.$data.startMouseX),e[5]=e[5]+(t.offsetY-this.$data.startMouseY),this.$data.canvas.setViewportTransform(e),this.$data.startMouseX=t.offsetX,this.$data.startMouseY=t.offsetY}else"add"===this.$data.mode&&(this.$data.newRect.set({width:(t.offsetX-this.$data.startMouseX)/this.$data.zoom,height:(t.offsetY-this.$data.startMouseY)/this.$data.zoom}),this.$data.canvas.renderAll())}},{key:"mouseUp",value:function(t){this.$data.dragging=!1,"add"===this.$data.mode&&(this.$store.dispatch("addJoke",this.$data.newRect.getBoundingRect(!0,!0)),this.$data.canvas.remove(this.$data.newRect),this.$data.newRect=null,this.setMode("edit"))}},{key:"mouseScroll",value:function(t){var e=this.$data.canvas.viewportTransform;e[4]=e[4]+10*t.deltaX,e[5]=e[5]+10*t.deltaY,this.$data.canvas.setViewportTransform(e)}},{key:"objectSelected",value:function(){this.$data.selected=this.$data.canvas.getActiveObject()}},{key:"objectDeselected",value:function(){this.$data.selected.set({left:this.$data.selected.sourceData.attributes.bbox.left,top:this.$data.selected.sourceData.attributes.bbox.top,width:this.$data.selected.sourceData.attributes.bbox.width,height:this.$data.selected.sourceData.attributes.bbox.height}),this.$data.selected=null,this.$data.canvas.renderAll()}},{key:"discardChanges",value:function(){this.$data.canvas.discardActiveObject().renderAll()}},{key:"saveChanges",value:function(){this.nothingSelected||(this.$store.dispatch("updateJoke",{jid:this.$data.selected.sourceData.id,attrs:{bbox:this.$data.selected.getBoundingRect(!0,!0)}}),this.$data.canvas.discardActiveObject().renderAll())}},{key:"watchJokesList",value:function(t,e){var a=this;if(this.$data.jokes.forEach((function(t){a.$data.canvas.remove(t)})),t){var n=[];t.forEach((function(t){var e=new v["fabric"].Rect({left:t.attributes.bbox.left,top:t.attributes.bbox.top,width:t.attributes.bbox.width,height:t.attributes.bbox.height,fill:"transparent",stroke:"#00aa00",hasRotatingPoint:!1,hasBorders:!1,transparentCorners:!1,selectable:"edit"===a.$data.mode,cornerColor:"#000000",sourceData:t});n.push(e),a.$data.canvas.add(e)})),this.$data.jokes=n}}},{key:"watchSourceUrl",value:function(t,e){var a=this;""!==t&&v["fabric"].Image.fromURL(t,(function(t){a.$data.img=t,a.$data.canvas.add(t),t.set({selectable:!1}),a.$data.canvas.sendToBack(t),a.$data.imgBounds=a.$data.img.getBoundingRect(),a.$data.zoom=a.$data.viewerHeight/a.$data.imgBounds.height,a.$data.maxZoom=a.$data.zoom,a.update()}))}},{key:"update",value:function(){this.$data.canvas.setZoom(this.$data.zoom)}},{key:"modeMove",get:function(){return"move"===this.$data.mode?"true":"false"}},{key:"modeNotMove",get:function(){return"move"!==this.$data.mode?"true":"false"}},{key:"modeAdd",get:function(){return"add"===this.$data.mode?"true":"false"}},{key:"modeEdit",get:function(){return"edit"===this.$data.mode?"true":"false"}},{key:"modeNotEdit",get:function(){return"edit"!==this.$data.mode?"true":"false"}},{key:"nothingSelected",get:function(){return null!==this.$data.selected?null:"disabled"}}]),e}(h["b"]);Object(l["a"])([Object(h["c"])("$store.state.jokes")],b.prototype,"watchJokesList",null),Object(l["a"])([Object(h["c"])("$store.state.source.attributes.raw")],b.prototype,"watchSourceUrl",null),b=Object(l["a"])([h["a"]],b);var p=b,g=p,k=a("2877"),$=Object(k["a"])(g,f,m,!1,null,null,null),y=$.exports,j=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"joke-list"},[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"move",role:"menuitem",disabled:t.nothingSelected},on:{click:function(e){return t.deleteSelected()}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"}})])])])])]),a("div",[t.jokes.length>0?a("ul",t._l(t.jokes,(function(e){return a("li",[e===t.selectedJoke?a("a",{staticClass:"selected",on:{click:function(a){return t.select(e)}}},[a("img",{attrs:{src:e.attributes.raw}})]):a("a",{on:{click:function(a){return t.select(e)}}},[a("img",{attrs:{src:e.attributes.raw}})])])})),0):a("p",[t._v("Draw joke outlines on the left-hand side to extract jokes.")])])])},w=[],O=function(t){function e(){return Object(o["a"])(this,e),Object(c["a"])(this,Object(d["a"])(e).apply(this,arguments))}return Object(u["a"])(e,t),Object(r["a"])(e,[{key:"select",value:function(t){this.$store.commit("selectJoke",t)}},{key:"deleteSelected",value:function(){this.$store.dispatch("deleteJoke",this.$store.state.selected)}},{key:"jokes",get:function(){return this.$store.state.jokes}},{key:"selectedJoke",get:function(){return this.$store.state.selected}},{key:"nothingSelected",get:function(){return null===this.$store.state.selected?"disabled":null}}]),e}(h["b"]);O=Object(l["a"])([h["a"]],O);var L=O,V=L,H=Object(k["a"])(V,j,w,!1,null,null,null),M=H.exports,C=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"joke-transcriber"},[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"confirm",role:"menuitem"},on:{click:t.saveChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"cancel",role:"menuitem"},on:{click:t.discardChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z"}})])])]),a("li",{attrs:{role:"separator"}}),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-checked":"transcribe"===t.mode?"true":"false"},on:{click:function(e){return t.setMode("transcribe")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M8,12H16V14H8V12M10,20H6V4H13V9H18V12.1L20,10.1V8L14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H10V20M8,18H12.1L13,17.1V16H8V18M20.2,13C20.3,13 20.5,13.1 20.6,13.2L21.9,14.5C22.1,14.7 22.1,15.1 21.9,15.3L20.9,16.3L18.8,14.2L19.8,13.2C19.9,13.1 20,13 20.2,13M20.2,16.9L14.1,23H12V20.9L18.1,14.8L20.2,16.9Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-checked":"attributes"===t.mode?"true":"false"},on:{click:function(e){return t.setMode("attributes")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M21.7,13.35L20.7,14.35L18.65,12.3L19.65,11.3C19.86,11.08 20.21,11.08 20.42,11.3L21.7,12.58C21.92,12.79 21.92,13.14 21.7,13.35M12,18.94L18.07,12.88L20.12,14.93L14.06,21H12V18.94M4,2H18A2,2 0 0,1 20,4V8.17L16.17,12H12V16.17L10.17,18H4A2,2 0 0,1 2,16V4A2,2 0 0,1 4,2M4,6V10H10V6H4M12,6V10H18V6H12M4,12V16H10V12H4Z"}})])])])]),"transcribe"===t.mode?a("editor-menu-bar",{attrs:{editor:t.editor},scopedSlots:t._u([{key:"default",fn:function(e){var n=e.commands,s=e.isActive;return[a("ul",{staticClass:"menu",staticStyle:{"flex-wrap":"wrap"},attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-checked":s.annotation()?"true":"false"},on:{click:n.annotation}},[t._v("Annotation")])])])]}}],null,!1,2445674567)}):t._e()],1),"transcribe"===t.mode?a("div",[a("editor-content",{attrs:{editor:t.editor}}),a("editor-menu-bar",{attrs:{editor:t.editor},scopedSlots:t._u([{key:"default",fn:function(e){e.commands;var n=e.isActive;return[n.annotation()?a("div",[a("label",[t._v("Annotation Type "),a("select",{on:{change:function(e){return t.setAnnotationAttributeValue("category",e.target.value)}}},[a("option",{attrs:{value:""}},[t._v("--- Please Select ---")]),t._l(t.annotations,(function(e){return[e.separate?a("option",{staticStyle:{"font-size":"1pt","background-color":"#000000"},attrs:{disabled:"disabled"}}):t._e(),a("option",{domProps:{value:e.name,selected:t.hasAnnotationAttributeValue("category",e.name)?"selected":null,innerHTML:t._s(e.label)}})]}))],2)]),t._l(t.annotations,(function(e){return[t._l(e.attrs,(function(n){return t.hasAnnotationAttributeValue("category",e.name)?[a("label",[t._v(t._s(n.label)+" "),"select"===n.type?a("select",{on:{change:function(e){return t.setAnnotationAttributeValue("settings",{name:n.name,value:e.target.value})}}},t._l(n.values,(function(e){return a("option",{domProps:{value:e[0],selected:t.getAnnotationAttributeValue("settings")[n.name]===e[0]?"selected":null,innerHTML:t._s(e[1])}})})),0):t._e()])]:t._e()}))]}))],2):t._e()]}}],null,!1,3116511434)})],1):"attributes"===t.mode?a("div",t._l(t.metadata,(function(e){return a("div",{staticClass:"margin-bottom"},[a("h2",{staticClass:"font-size-default"},[t._v(t._s(e.label))]),"multichoice"===e.type?a("div",t._l(e.values,(function(n){return a("label",[a("input",{attrs:{type:"checkbox"},domProps:{value:n[0],checked:t.hasAttributeValue(e.name,n[0],!0)?"checked":null},on:{change:function(a){a.target.checked?t.addAttributeValue(e.name,n.name):t.removeAttributeValue(e.name,n.name)}}}),t._v(" "),a("span",{domProps:{innerHTML:t._s(n[1])}})])})),0):"select"===e.type?a("select",{on:{change:function(a){return t.setAttributeValue(e.name,a.target.value)}}},t._l(e.values,(function(n){return a("option",{domProps:{value:n[0],selected:t.hasAttributeValue(e.name,n[0])?"selected":null,innerHTML:t._s(n[1])}})})),0):t._e()])})),0):t._e(),t.noTranscription?a("div",{staticClass:"overlay"},[a("p",[t._v("Please select a joke from the list to transcribe and annotate it.")])]):t._e()])},A=[],x=(a("a4d3"),a("e01a"),a("d28b"),a("4de4"),a("c975"),a("a434"),a("b0c0"),a("e439"),a("dbb4"),a("b64b"),a("d3b7"),a("3ca3"),a("ddb0"),a("ade3")),_=a("cd42"),S=a("a9de"),T=function(t){function e(){return Object(o["a"])(this,e),Object(c["a"])(this,Object(d["a"])(e).apply(this,arguments))}return Object(u["a"])(e,t),Object(r["a"])(e,[{key:"commands",value:function(t){var e=t.type;return function(){return Object(S["c"])(e)}}},{key:"name",get:function(){return"annotation"}},{key:"schema",get:function(){return{attrs:{category:{default:""},settings:{default:{}}},parseDOM:[{tag:"span.mark-annotation"}],toDOM:function(){return["span",{class:"mark-annotation"},0]}}}}]),e}(_["d"]),P=a("4979"),z=a.n(P);function J(t,e){var a=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),a.push.apply(a,n)}return a}function B(t){for(var e=1;e<arguments.length;e++){var a=null!=arguments[e]?arguments[e]:{};e%2?J(Object(a),!0).forEach((function(e){Object(x["a"])(t,e,a[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(a)):J(Object(a)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(a,e))}))}return t}var R=function(t){function e(){var t;return Object(o["a"])(this,e),t=Object(c["a"])(this,Object(d["a"])(e).apply(this,arguments)),t.mode="transcribe",t.editor=null,t.attributes={},t}return Object(u["a"])(e,t),Object(r["a"])(e,[{key:"mounted",value:function(){this.editor=new _["a"]({extensions:[new T]})}},{key:"beforeDestroy",value:function(){this.editor&&this.editor.destroy()}},{key:"saveChanges",value:function(){this.attributes=B({},this.attributes,{},{text:this.editor.getJSON()}),this.$store.dispatch("updateTranscription",this.attributes)}},{key:"discardChanges",value:function(){this.editor.setContent(this.$store.state.transcription.attributes.text)}},{key:"setMode",value:function(t){this.mode=t}},{key:"addAttributeValue",value:function(t,e){var a=this.$store.state.transcription.attributes[t];a||(a=[]),a.indexOf(e)<0&&a.push(e),this.attributes=B({},this.attributes,{},Object(x["a"])({},t,a))}},{key:"removeAttributeValue",value:function(t,e){var a=this.$store.state.transcription.attributes[t];a?(a.indexOf(e)>=0&&a.splice(a.indexOf(e),1),this.attributes=B({},this.attributes,{},Object(x["a"])({},t,a))):this.attributes=B({},this.attributes,{},Object(x["a"])({},t,[]))}},{key:"setAttributeValue",value:function(t,e){this.attributes=B({},this.attributes,{},Object(x["a"])({},t,e))}},{key:"watchSelectedJoke",value:function(t,e){this.$store.dispatch("loadTranscription")}},{key:"watchTranscription",value:function(t){t?(this.editor.setContent(t.attributes.text),this.attributes=z()(t.attributes)):(this.editor.setContent(""),this.attributes={})}},{key:"getAnnotationAttributeValue",value:function(t){var e=!0,a=!1,n=void 0;try{for(var s,i=this.selectedNodes[Symbol.iterator]();!(e=(s=i.next()).done);e=!0){var o=s.value;if(o.marks){var r=!0,c=!1,d=void 0;try{for(var u,l=o.marks[Symbol.iterator]();!(r=(u=l.next()).done);r=!0){var h=u.value;if("annotation"===h.type.name)return h.attrs[t]}}catch(f){c=!0,d=f}finally{try{r||null==l.return||l.return()}finally{if(c)throw d}}}}}catch(f){a=!0,n=f}finally{try{e||null==i.return||i.return()}finally{if(a)throw n}}return""}},{key:"hasAnnotationAttributeValue",value:function(t,e){return this.getAnnotationAttributeValue(t)===e}},{key:"setAnnotationAttributeValue",value:function(t,e){if(e){var a=this.editor.state.selection,n=a.from,s=a.to,i={};this.editor.state.doc.nodesBetween(n,s,(function(t){t.marks&&t.marks.forEach((function(t){"annotation"===t.type.name&&(i=B({},i,{},t.attrs))}))})),"settings"===t?(i.settings||(i.settings={}),i.settings[e.name]=e.value):"category"===t&&(i[t]=e),Object(S["d"])(this.editor.schema.marks.annotation,i)(this.editor.state,this.editor.dispatchTransaction.bind(this.editor))}else Object(S["a"])(this.editor.schema.marks.annotation)(this.editor.state,this.editor.dispatchTransaction.bind(this.editor))}},{key:"hasAttributeValue",value:function(t,e,a){var n=this.$store.state.transcription.attributes[t];return a?!!n&&n.indexOf(e)>=0:n===e}},{key:"annotations",get:function(){return this.$store.state.annotations}},{key:"metadata",get:function(){return this.$store.state.metadata}},{key:"noTranscription",get:function(){return null===this.$store.state.transcription}},{key:"selectedNodes",get:function(){if(this.editor){var t=this.editor.state.selection,e=t.from,a=t.to,n=[];return this.editor.state.doc.nodesBetween(e,a,(function(t){n.push(t)})),n}return[]}}]),e}(h["b"]);Object(l["a"])([Object(h["c"])("$store.state.selected")],R.prototype,"watchSelectedJoke",null),Object(l["a"])([Object(h["c"])("$store.state.transcription")],R.prototype,"watchTranscription",null),R=Object(l["a"])([Object(h["a"])({components:{EditorContent:_["b"],EditorMenuBar:_["c"]}})],R);var E=R,D=E,Z=Object(k["a"])(D,C,A,!1,null,null,null),I=Z.exports,U=function(t){function e(){return Object(o["a"])(this,e),Object(c["a"])(this,Object(d["a"])(e).apply(this,arguments))}return Object(u["a"])(e,t),Object(r["a"])(e,[{key:"mounted",value:function(){this.$store.dispatch("loadSource"),this.$store.dispatch("loadJokes")}}]),e}(h["b"]);U=Object(l["a"])([Object(h["a"])({components:{JokeSelector:y,JokeList:M,JokeTranscriber:I}})],U);var N=U,X=N,Y=Object(k["a"])(X,s,i,!1,null,null,null),W=Y.exports,q=(a("fb6a"),a("bc3a")),F=a.n(q),G=a("2f62");function K(t,e){var a=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),a.push.apply(a,n)}return a}function Q(t){for(var e=1;e<arguments.length;e++){var a=null!=arguments[e]?arguments[e]:{};e%2?K(Object(a),!0).forEach((function(e){Object(x["a"])(t,e,a[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(a)):K(Object(a)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(a,e))}))}return t}function tt(t){return{baseURL:t.baseURL,sourceId:t.sourceId,userId:t.userId,annotations:t.annotations,metadata:t.metadata,source:{},jokes:[],selected:null,transcription:null}}function et(t){return new G["a"].Store({state:tt(t),mutations:{updateSource:function(t,e){t.source=e},updateJokesList:function(t,e){t.jokes=e},selectJoke:function(t,e){t.selected===e||null===e?(t.selected=null,t.transcription=null):t.selected=e},setTranscription:function(t,e){t.transcription=e}},actions:{loadSource:function(t){F.a.get(t.state.baseURL+"/sources/"+t.state.sourceId).then((function(e){t.commit("updateSource",e.data.data),t.dispatch("loadJokes")}))},loadJokes:function(t){F.a.get(t.state.baseURL+"/jokes",{params:{"filter[owner_id]":t.state.userId,"filter[parent_id]":t.state.sourceId}}).then((function(e){t.commit("updateJokesList",e.data.data)}))},loadTranscription:function(t){if(t.state.selected){var e=t.state.selected.id;F.a.get(t.state.baseURL+"/transcriptions",{params:{"filter[owner_id]":t.state.userId,"filter[source_id]":e}}).then((function(a){0===a.data.data.length?F.a.get(t.state.baseURL+"/transcriptions",{params:{"filter[source_id]":e,"filter[status]":"ocr"}}).then((function(a){0===a.data.data.length?t.commit("setTranscription",{type:"transcriptions",attributes:{source_id:e,text:"",status:"new"}}):t.commit("setTranscription",{type:"transcriptions",attributes:{source_id:e,text:a.data.data[0].attributes.text,status:"new"}})})):t.commit("setTranscription",a.data.data[0])}))}},addJoke:function(t,e){F.a.post(t.state.baseURL+"/jokes",{data:{type:"jokes",attributes:{parent_id:t.state.sourceId,bbox:e}}}).then((function(e){var a=t.state.jokes.slice();a.push(e.data.data),t.commit("updateJokesList",a)}))},updateJoke:function(t,e){var a=e.jid,n=e.attrs;t.state.jokes.forEach((function(e){e.id===a&&(e=Q({},e),e.attributes=Q({},e.attributes,{},n),F.a.put(t.state.baseURL+"/jokes/"+e.id,{data:e}).then((function(e){var n=[];t.state.jokes.forEach((function(t){t.id===a?n.push(e.data.data):n.push(t)})),t.commit("updateJokesList",n)})))}))},deleteJoke:function(t,e){F.a.delete(t.state.baseURL+"/jokes/"+e.id).then((function(e){t.commit("selectJoke",null),t.dispatch("loadJokes")}))},updateTranscription:function(t,e){var a=Q({},t.state.transcription);a.attributes=Q({},a.attributes,{},e),a.id?F.a.patch(t.state.baseURL+"/transcriptions/"+a.id,{data:a}).then((function(e){t.commit("setTranscription",e.data.data)})):F.a.post(t.state.baseURL+"/transcriptions",{data:a}).then((function(e){t.commit("setTranscription",e.data.data)}))}}})}n["a"].use(G["a"]),n["a"].config.productionTip=!1;var at=document.getElementById("config"),nt={baseURL:"",sourceId:null,userId:null,annotations:[],metadata:[]};at&&(nt=JSON.parse(at.innerHTML));var st=et(nt);new n["a"]({store:st,render:function(t){return t(W)}}).$mount("#app")}});
//# sourceMappingURL=app.js.map