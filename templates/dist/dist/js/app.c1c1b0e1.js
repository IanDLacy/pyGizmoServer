(function(e){function t(t){for(var r,l,u=t[0],i=t[1],c=t[2],d=0,f=[];d<u.length;d++)l=u[d],Object.prototype.hasOwnProperty.call(a,l)&&a[l]&&f.push(a[l][0]),a[l]=0;for(r in i)Object.prototype.hasOwnProperty.call(i,r)&&(e[r]=i[r]);s&&s(t);while(f.length)f.shift()();return o.push.apply(o,c||[]),n()}function n(){for(var e,t=0;t<o.length;t++){for(var n=o[t],r=!0,u=1;u<n.length;u++){var i=n[u];0!==a[i]&&(r=!1)}r&&(o.splice(t--,1),e=l(l.s=n[0]))}return e}var r={},a={app:0},o=[];function l(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,l),n.l=!0,n.exports}l.m=e,l.c=r,l.d=function(e,t,n){l.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},l.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.t=function(e,t){if(1&t&&(e=l(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(l.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)l.d(n,r,function(t){return e[t]}.bind(null,r));return n},l.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return l.d(t,"a",t),t},l.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},l.p="/static/dist/";var u=window["webpackJsonp"]=window["webpackJsonp"]||[],i=u.push.bind(u);u.push=t,u=u.slice();for(var c=0;c<u.length;c++)t(u[c]);var s=i;o.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"0f3a":function(e,t,n){"use strict";var r=n("471d"),a=n.n(r);a.a},"471d":function(e,t,n){},"56d7":function(e,t,n){"use strict";n.r(t);n("d81d"),n("4fad");var r=n("3835"),a=n("53ca"),o=(n("e260"),n("e6cf"),n("cca6"),n("a79d"),n("a026")),l=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[e.isleaf?n("div",{staticClass:"leaf"},[e._v(" "+e._s(e.label)+": "+e._s(e.value)+" ")]):n("div",{staticClass:"node"},[n("div",[e._v(e._s(e.label))]),e._l(e.nodes,(function(e){return n("node",{key:e.id,attrs:{nodes:e.nodes,label:e.label}})}))],2)])},u=[],i={props:["label","nodes"],name:"node",computed:{isleaf:function(){return!!this.nodes&&this.nodes.type},value:function(){return!!this.nodes&&this.nodes.value}}},c=i,s=(n("0f3a"),n("2877")),d=Object(s["a"])(c,l,u,!1,null,"e243bdca",null),f=d.exports;o["a"].config.productionTip=!1;var p={relayController:{relays:[{enabled:!0},{enabled:!1}]},pwmController:{pwmMonitorUpdateRate:100,bankA:{frequency:1e3},bankB:{frequency:1234},pwms:[{enabled:!1,dutyCycle:50},{enabled:!1,dutyCycle:50}]}};function b(e,t,n){var r=new Object;return r.path=n+"/"+e,r.label=e,r.nodes=v(t,r.path),r}function v(e,t){if("object"===Object(a["a"])(e)&&null!==e){for(var n=[],o=0,l=Object.entries(e);o<l.length;o++){var u=Object(r["a"])(l[o],2),i=u[0],c=u[1];n.push(b(i,c,t))}return n}if(Array.isArray(e))return e.map((function(e,n){return b(String(n),e,t)}));var s=new Object;return s.label="",s.path=t,s.value=e,s.type=String(Object(a["a"])(e)),s}var y=new Object;y.label=p.controller,y.nodes=v(p,""),new o["a"]({el:"#app",data:{tree:y},components:{Node:f}})}});
//# sourceMappingURL=app.c1c1b0e1.js.map