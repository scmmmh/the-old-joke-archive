(function(t){function e(e){for(var s,n,r=e[0],c=e[1],d=e[2],l=0,h=[];l<r.length;l++)n=r[l],i[n]&&h.push(i[n][0]),i[n]=0;for(s in c)Object.prototype.hasOwnProperty.call(c,s)&&(t[s]=c[s]);u&&u(e);while(h.length)h.shift()();return o.push.apply(o,d||[]),a()}function a(){for(var t,e=0;e<o.length;e++){for(var a=o[e],s=!0,r=1;r<a.length;r++){var c=a[r];0!==i[c]&&(s=!1)}s&&(o.splice(e--,1),t=n(n.s=a[0]))}return t}var s={},i={app:0},o=[];function n(e){if(s[e])return s[e].exports;var a=s[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,n),a.l=!0,a.exports}n.m=t,n.c=s,n.d=function(t,e,a){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},n.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(n.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var s in t)n.d(a,s,function(e){return t[e]}.bind(null,s));return a},n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],c=r.push.bind(r);r.push=e,r=r.slice();for(var d=0;d<r.length;d++)e(r[d]);var u=c;o.push([1,"chunk-vendors"]),a()})({0:function(t,e){},1:function(t,e,a){t.exports=a("cd49")},2:function(t,e){},cd49:function(t,e,a){"use strict";a.r(e);a("cadf"),a("551c"),a("f751"),a("097d");var s=a("2b0e"),i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"workbench",attrs:{id:"app"}},[a("router-view")],1)},o=[],n=a("2877"),r={},c=Object(n["a"])(r,i,o,!1,null,null,null),d=c.exports,u=a("8c4f"),l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("joke-selector"),a("joke-list"),a("joke-transcriber")],1)},h=[],f=a("d225"),v=a("308d"),m=a("6bb5"),p=a("4e2b"),b=a("9ab4"),$=a("60a3"),g=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeMove},on:{click:function(e){return t.setMode("move")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M13,6V11H18V7.75L22.25,12L18,16.25V13H13V18H16.25L12,22.25L7.75,18H11V13H6V16.25L1.75,12L6,7.75V11H11V6H7.75L12,1.75L16.25,6H13Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeAdd},on:{click:function(e){return t.setMode("add")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-current":t.modeEdit},on:{click:function(e){return t.setMode("edit")}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}})])])]),a("li",{attrs:{role:"separator"}}),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomInitial}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M9.5,13.09L10.91,14.5L6.41,19H10V21H3V14H5V17.59L9.5,13.09M10.91,9.5L9.5,10.91L5,6.41V10H3V3H10V5H6.41L10.91,9.5M14.5,13.09L19,17.59V14H21V21H14V19H17.59L13.09,14.5L14.5,13.09M13.09,9.5L17.59,5H14V3H21V10H19V6.41L14.5,10.91L13.09,9.5Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomIn}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M15.5,14L20.5,19L19,20.5L14,15.5V14.71L13.73,14.43C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.43,13.73L14.71,14H15.5M9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14M12,10H10V12H9V10H7V9H9V7H10V9H12V10Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotMove},on:{click:t.zoomOut}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M15.5,14H14.71L14.43,13.73C15.41,12.59 16,11.11 16,9.5A6.5,6.5 0 0,0 9.5,3A6.5,6.5 0 0,0 3,9.5A6.5,6.5 0 0,0 9.5,16C11.11,16 12.59,15.41 13.73,14.43L14,14.71V15.5L19,20.5L20.5,19L15.5,14M9.5,14C7,14 5,12 5,9.5C5,7 7,5 9.5,5C12,5 14,7 14,9.5C14,12 12,14 9.5,14M7,9H12V10H7V9Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotEdit,disabled:t.nothingSelected},on:{click:t.saveChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem","aria-hidden":t.modeNotEdit,disabled:t.nothingSelected},on:{click:t.discardChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z"}})])])])])]),a("div",{staticStyle:{overflow:"hidden"},attrs:{id:t.guid}},[a("canvas")])])},k=[],w=(a("ac6a"),a("b0b4")),j=a("803b"),y=function(t){function e(){var t;return Object(f["a"])(this,e),t=Object(v["a"])(this,Object(m["a"])(e).apply(this,arguments)),t.guid="joke-selector-canvas",t.viewer=null,t.canvas=null,t.viewerWidth=0,t.viewerHeight=0,t.zoom=1,t.imgBounds={x:0,y:0,width:0,height:0},t.dragging=!1,t.img=null,t.mode="move",t.newRect=null,t.jokes=[],t.selected=null,t}return Object(p["a"])(e,t),Object(w["a"])(e,[{key:"mounted",value:function(){var t=this;this.$data.viewer=document.querySelector("#"+this.$data.guid),this.$data.viewer&&(this.$data.canvas=new j["fabric"].Canvas(this.$data.viewer.querySelector("canvas")),this.$data.canvas.set({selection:!1,uniScaleTransform:!0}),this.$data.canvas.on("mouse:down",function(e){t.mouseDown(e.e)}),this.$data.canvas.on("mouse:move",function(e){t.mouseMove(e.e)}),this.$data.canvas.on("mouse:up",function(e){t.mouseUp(e.e)}),this.$data.canvas.on("mouse:dblclick",function(){t.zoomIn()}),this.$data.canvas.on("mouse:wheel",function(e){t.mouseScroll(e.e)}),this.$data.canvas.on("selection:created",function(e){t.objectSelected()}),this.$data.canvas.on("selection:cleared",function(e){t.objectDeselected()}),window.addEventListener("resize",this.resize),this.resize())}},{key:"beforeDestroy",value:function(){window.removeEventListener("resize",this.resize)}},{key:"resize",value:function(){if(this.$data.viewerWidth=this.$data.viewer.clientWidth,this.$data.viewerHeight=this.$data.viewer.clientHeight,this.$data.canvas.setWidth(this.$data.viewerWidth),this.$data.canvas.setHeight(this.$data.viewerHeight),this.$data.img){this.$data.zoom=this.$data.viewerHeight/this.$data.imgBounds.height,this.$data.maxZoom=this.$data.zoom;var t=this.$data.canvas.viewportTransform;t[5]=0,this.$data.canvas.setViewportTransform(t),this.update()}}},{key:"setMode",value:function(t){"edit"===this.$data.mode&&(this.$data.jokes.forEach(function(t){t.set({selectable:!1})}),this.$data.canvas.discardActiveObject().renderAll(),this.$data.canvas.hoverCursor="pointer"),this.$data.mode=t,"move"===t?this.$data.canvas.hoverCursor="move":"add"===t?this.$data.canvas.hoverCursor="crosshair":"edit"===t&&(this.$data.canvas.hoverCursor="pointer",this.$data.jokes.forEach(function(t){t.set({selectable:!0})}),this.$data.canvas.renderAll())}},{key:"zoomInitial",value:function(){this.$data.zoom=this.$data.maxZoom;var t=this.$data.canvas.viewportTransform;t[5]=0,this.$data.canvas.setViewportTransform(t),this.update()}},{key:"zoomIn",value:function(){this.$data.zoom=Math.min(this.$data.zoom+(1-this.$data.maxZoom)/5,1),this.update()}},{key:"zoomOut",value:function(){this.$data.zoom=Math.max(this.$data.zoom-(1-this.$data.maxZoom)/5,this.$data.maxZoom),this.update()}},{key:"mouseDown",value:function(t){this.$data.dragging=!0,this.$data.startMouseX=t.offsetX,this.$data.startMouseY=t.offsetY,"add"===this.$data.mode&&(this.$data.newRect=new j["fabric"].Rect({left:t.offsetX-this.$data.canvas.viewportTransform[4],top:t.offsetY/this.$data.zoom-this.$data.canvas.viewportTransform[5],width:0,height:10,fill:"transparent",stroke:"#00aa00",hasRotatingPoint:!1,hasBorders:!1,hasCorners:!1}),this.$data.canvas.add(this.$data.newRect))}},{key:"mouseMove",value:function(t){if(this.$data.dragging)if("move"===this.$data.mode){var e=this.$data.canvas.viewportTransform;e[4]=e[4]+(t.offsetX-this.$data.startMouseX),e[5]=e[5]+(t.offsetY-this.$data.startMouseY),this.$data.canvas.setViewportTransform(e),this.$data.startMouseX=t.offsetX,this.$data.startMouseY=t.offsetY}else"add"===this.$data.mode&&(this.$data.newRect.set({width:(t.offsetX-this.$data.startMouseX)/this.$data.zoom-this.$data.canvas.viewportTransform[4],height:(t.offsetY-this.$data.startMouseY)/this.$data.zoom-this.$data.canvas.viewportTransform[5]}),this.$data.canvas.renderAll())}},{key:"mouseUp",value:function(t){if(this.$data.dragging=!1,"add"===this.$data.mode){this.$data.canvas.remove(this.$data.newRect);var e=this.$data.newRect.getBoundingRect(!0,!0);e.left=e.left-this.$data.canvas.viewportTransform[4],e.top=e.top-this.$data.canvas.viewportTransform[5],this.$store.dispatch("addJoke",e),this.$data.newRect=null,this.setMode("edit")}}},{key:"mouseScroll",value:function(t){var e=this.$data.canvas.viewportTransform;e[4]=e[4]+10*t.deltaX,e[5]=e[5]+10*t.deltaY,this.$data.canvas.setViewportTransform(e)}},{key:"objectSelected",value:function(){this.$data.selected=this.$data.canvas.getActiveObject()}},{key:"objectDeselected",value:function(){this.$data.selected.set({left:this.$data.selected.sourceData.attributes.bbox.left,top:this.$data.selected.sourceData.attributes.bbox.top,width:this.$data.selected.sourceData.attributes.bbox.width,height:this.$data.selected.sourceData.attributes.bbox.height}),this.$data.selected=null,this.$data.canvas.renderAll()}},{key:"discardChanges",value:function(){this.$data.canvas.discardActiveObject().renderAll()}},{key:"saveChanges",value:function(){this.nothingSelected||(this.$store.dispatch("updateJoke",{jid:this.$data.selected.sourceData.id,attrs:{bbox:this.$data.selected.getBoundingRect(!0,!0)}}),this.$data.canvas.discardActiveObject().renderAll())}},{key:"watchJokesList",value:function(t,e){var a=this;if(this.$data.jokes.forEach(function(t){a.$data.canvas.remove(t)}),t){var s=[];t.forEach(function(t){var e=new j["fabric"].Rect({left:t.attributes.bbox.left,top:t.attributes.bbox.top,width:t.attributes.bbox.width,height:t.attributes.bbox.height,fill:"transparent",stroke:"#00aa00",hasRotatingPoint:!1,hasBorders:!1,transparentCorners:!1,selectable:"edit"===a.$data.mode,cornerColor:"#000000",sourceData:t});s.push(e),a.$data.canvas.add(e)}),this.$data.jokes=s}}},{key:"watchSourceUrl",value:function(t,e){var a=this;""!==t&&j["fabric"].Image.fromURL(t,function(t){a.$data.img=t,a.$data.canvas.add(t),t.set({selectable:!1}),a.$data.canvas.sendToBack(t),a.$data.imgBounds=a.$data.img.getBoundingRect(),a.$data.zoom=a.$data.viewerHeight/a.$data.imgBounds.height,a.$data.maxZoom=a.$data.zoom,a.update()})}},{key:"update",value:function(){this.$data.canvas.setZoom(this.$data.zoom)}},{key:"modeMove",get:function(){return"move"===this.$data.mode?"true":"false"}},{key:"modeNotMove",get:function(){return"move"!==this.$data.mode?"true":"false"}},{key:"modeAdd",get:function(){return"add"===this.$data.mode?"true":"false"}},{key:"modeEdit",get:function(){return"edit"===this.$data.mode?"true":"false"}},{key:"modeNotEdit",get:function(){return"edit"!==this.$data.mode?"true":"false"}},{key:"nothingSelected",get:function(){return null!==this.$data.selected?null:"disabled"}}]),e}($["b"]);b["a"]([Object($["c"])("$store.state.jokes")],y.prototype,"watchJokesList",null),b["a"]([Object($["c"])("$store.state.source.attributes.raw")],y.prototype,"watchSourceUrl",null),y=b["a"]([$["a"]],y);var L=y,O=L,C=Object(n["a"])(O,g,k,!1,null,null,null),H=C.exports,M=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"joke-list"},[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"move",role:"menuitem",disabled:t.nothingSelected},on:{click:function(e){return t.deleteSelected()}}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"}})])])])])]),a("div",[t.jokes.length>0?a("ul",t._l(t.jokes,function(e){return a("li",[e===t.selectedJoke?a("a",{staticClass:"selected",on:{click:function(a){return t.select(e)}}},[a("img",{attrs:{src:e.attributes.raw}})]):a("a",{on:{click:function(a){return t.select(e)}}},[a("img",{attrs:{src:e.attributes.raw}})])])}),0):a("p",[t._v("Draw joke outlines on the left-hand side to extract jokes.")])])])},x=[],V=function(t){function e(){return Object(f["a"])(this,e),Object(v["a"])(this,Object(m["a"])(e).apply(this,arguments))}return Object(p["a"])(e,t),Object(w["a"])(e,[{key:"select",value:function(t){this.$store.commit("selectJoke",t)}},{key:"deleteSelected",value:function(){this.$store.dispatch("deleteJoke",this.$store.state.selected)}},{key:"jokes",get:function(){return this.$store.state.jokes}},{key:"selectedJoke",get:function(){return this.$store.state.selected}},{key:"nothingSelected",get:function(){return null===this.$store.state.selected?"disabled":null}}]),e}($["b"]);V=b["a"]([$["a"]],V);var _=V,T=_,S=Object(n["a"])(T,M,x,!1,null,null,null),A=S.exports,J=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"joke-transcriber"},[a("nav",[a("ul",{staticClass:"menu",attrs:{role:"menu"}},[a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"confirm",role:"menuitem"},on:{click:t.saveChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}})])])]),a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{"data-action":"cancel",role:"menuitem"},on:{click:t.discardChanges}},[a("svg",{staticClass:"icon mdi",attrs:{viewBox:"0 0 24 24"}},[a("path",{attrs:{d:"M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12C4,13.85 4.63,15.55 5.68,16.91L16.91,5.68C15.55,4.63 13.85,4 12,4M12,20A8,8 0 0,0 20,12C20,10.15 19.37,8.45 18.32,7.09L7.09,18.32C8.45,19.37 10.15,20 12,20Z"}})])])]),a("li",{attrs:{role:"separator"}}),t._m(0)])]),a("editor-content",{attrs:{editor:t.editor}}),a("div",[t._v("Attributes")]),t.noTranscription?a("div",{staticClass:"overlay"},[a("p",[t._v("Please select a joke from the list to transcribe and annotate it.")])]):t._e()],1)},z=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("li",{attrs:{role:"presentation"}},[a("a",{attrs:{role:"menuitem"}},[t._v("Title")])])}],R=a("cd42"),E=function(t){function e(){var t;return Object(f["a"])(this,e),t=Object(v["a"])(this,Object(m["a"])(e).apply(this,arguments)),t.editor=new R["a"]({content:"<p></p>"}),t}return Object(p["a"])(e,t),Object(w["a"])(e,[{key:"beforeDestroy",value:function(){this.$data.editor.destroy()}},{key:"saveChanges",value:function(){this.$store.dispatch("updateTranscription",{text:this.$data.editor.getJSON()})}},{key:"discardChanges",value:function(){this.$data.editor.setContent(this.$store.state.transcription.attributes.text)}},{key:"watchSelectedJoke",value:function(t,e){this.$store.dispatch("loadTranscription")}},{key:"watchTranscription",value:function(t,e){t?this.$data.editor.setContent(t.attributes.text):this.$data.editor.setContent("")}},{key:"noTranscription",get:function(){return null===this.$store.state.transcription}}]),e}($["b"]);b["a"]([Object($["c"])("$store.state.selected")],E.prototype,"watchSelectedJoke",null),b["a"]([Object($["c"])("$store.state.transcription")],E.prototype,"watchTranscription",null),E=b["a"]([Object($["a"])({components:{EditorContent:R["b"]}})],E);var B=E,I=B,Z=Object(n["a"])(I,J,z,!1,null,null,null),D=Z.exports,P=function(t){function e(){return Object(f["a"])(this,e),Object(v["a"])(this,Object(m["a"])(e).apply(this,arguments))}return Object(p["a"])(e,t),e}($["b"]);P=b["a"]([Object($["a"])({components:{JokeSelector:H,JokeList:A,JokeTranscriber:D},mounted:function(){this.$store.dispatch("loadSource"),this.$store.dispatch("loadJokes")}})],P);var U=P,X=U,Y=Object(n["a"])(X,l,h,!1,null,null,null),N=Y.exports,W=function(){var t=this,e=t.$createElement;t._self._c;return t._m(0)},q=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"about"},[a("h1",[t._v("This is an about page")])])}],F={},G=Object(n["a"])(F,W,q,!1,null,null,null),K=G.exports;s["a"].use(u["a"]);var Q=new u["a"]({routes:[{path:"/",name:"workbench",component:N},{path:"/about",name:"about",component:K}]}),tt=(a("8e6e"),a("456d"),a("bd86")),et=a("bc3a"),at=a.n(et),st=a("2f62");function it(t,e){var a=Object.keys(t);return Object.getOwnPropertySymbols&&a.push.apply(a,Object.getOwnPropertySymbols(t)),e&&(a=a.filter(function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable})),a}function ot(t){for(var e=1;e<arguments.length;e++){var a=null!=arguments[e]?arguments[e]:{};e%2?it(a,!0).forEach(function(e){Object(tt["a"])(t,e,a[e])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(a)):it(a).forEach(function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(a,e))})}return t}function nt(t){return{baseURL:t.baseURL,sourceId:t.sourceId,userId:t.userId,source:{},jokes:[],selected:null,transcription:null}}function rt(t){return new st["a"].Store({state:nt(t),mutations:{updateSource:function(t,e){t.source=e},updateJokesList:function(t,e){t.jokes=e},selectJoke:function(t,e){t.selected===e?(t.selected=null,t.transcription=null):t.selected=e},setTranscription:function(t,e){t.transcription=e}},actions:{loadSource:function(t){at.a.get(t.state.baseURL+"/sources/"+t.state.sourceId).then(function(e){t.commit("updateSource",e.data.data),t.dispatch("loadJokes")})},loadJokes:function(t){at.a.get(t.state.baseURL+"/jokes",{params:{"filter[owner_id]":t.state.userId,"filter[parent_id]":t.state.sourceId}}).then(function(e){t.commit("updateJokesList",e.data.data)})},loadTranscription:function(t){if(t.state.selected){var e=t.state.selected.id;at.a.get(t.state.baseURL+"/transcriptions",{params:{"filter[owner_id]":t.state.userId,"filter[source_id]":e}}).then(function(a){0===a.data.data.length?at.a.get(t.state.baseURL+"/transcriptions",{params:{"filter[source_id]":e,"filter[status]":"ocr"}}).then(function(a){0===a.data.data.length?t.commit("setTranscription",{type:"transcriptions",attributes:{source_id:e,text:"",status:"new"}}):t.commit("setTranscription",{type:"transcriptions",attributes:{source_id:e,text:a.data.data[0].attributes.text,status:"new"}})}):t.commit("setTranscription",a.data.data[0])})}},addJoke:function(t,e){at.a.post(t.state.baseURL+"/jokes",{data:{type:"jokes",attributes:{parent_id:t.state.sourceId,bbox:e}}}).then(function(e){var a=t.state.jokes.slice();a.push(e.data.data),t.commit("updateJokesList",a)})},updateJoke:function(t,e){var a=e.jid,s=e.attrs;t.state.jokes.forEach(function(e){e.id===a&&(e=ot({},e),e.attributes=ot({},e.attributes,{},s),at.a.put(t.state.baseURL+"/jokes/"+e.id,{data:e}).then(function(e){var s=[];t.state.jokes.forEach(function(t){t.id===a?s.push(e.data.data):s.push(t)}),t.commit("updateJokesList",s)}))})},deleteJoke:function(t,e){at.a.delete(t.state.baseURL+"/jokes/"+e.id).then(function(e){t.dispatch("loadJokes")})},updateTranscription:function(t,e){var a=ot({},t.state.transcription);a.attributes=ot({},a.attributes,{},e),a.id?at.a.patch(t.state.baseURL+"/transcriptions/"+a.id,{data:a}).then(function(e){t.commit("setTranscription",e.data.data)}):at.a.post(t.state.baseURL+"/transcriptions",{data:a}).then(function(e){t.commit("setTranscription",e.data.data)})}}})}s["a"].use(st["a"]),s["a"].config.productionTip=!1;var ct=document.getElementById("config"),dt={baseURL:"",sourceId:null,userId:null};ct&&(dt=JSON.parse(ct.innerHTML));var ut=rt(dt);new s["a"]({router:Q,store:ut,render:function(t){return t(d)}}).$mount("#app")}});
//# sourceMappingURL=app.js.map