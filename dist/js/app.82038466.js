(function(e){function t(t){for(var o,s,u=t[0],l=t[1],i=t[2],d=0,p=[];d<u.length;d++)s=u[d],Object.prototype.hasOwnProperty.call(a,s)&&a[s]&&p.push(a[s][0]),a[s]=0;for(o in l)Object.prototype.hasOwnProperty.call(l,o)&&(e[o]=l[o]);c&&c(t);while(p.length)p.shift()();return r.push.apply(r,i||[]),n()}function n(){for(var e,t=0;t<r.length;t++){for(var n=r[t],o=!0,u=1;u<n.length;u++){var l=n[u];0!==a[l]&&(o=!1)}o&&(r.splice(t--,1),e=s(s.s=n[0]))}return e}var o={},a={app:0},r=[];function s(t){if(o[t])return o[t].exports;var n=o[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=o,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)s.d(n,o,function(t){return e[t]}.bind(null,o));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="";var u=window["webpackJsonp"]=window["webpackJsonp"]||[],l=u.push.bind(u);u.push=t,u=u.slice();for(var i=0;i<u.length;i++)t(u[i]);var c=l;r.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"56d7":function(e,t,n){"use strict";n.r(t);n("d81d"),n("4fad"),n("d3b7"),n("96cf");var o=n("1da1"),a=n("3835"),r=n("53ca"),s=(n("e260"),n("e6cf"),n("cca6"),n("a79d"),n("a026")),u=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[e.isleaf?n("div",{staticClass:"leaf"},[e._v(" "+e._s(e.label)+" "),e.nodes.writable?n("div",[n("button",{on:{click:e.get}},[e._v("GET")])]):n("div",["boolean"==e.nodes.type?n("input",{directives:[{name:"model",rawName:"v-model",value:e.outval,expression:"outval"}],attrs:{type:"checkbox"},domProps:{checked:Array.isArray(e.outval)?e._i(e.outval,null)>-1:e.outval},on:{change:function(t){var n=e.outval,o=t.target,a=!!o.checked;if(Array.isArray(n)){var r=null,s=e._i(n,r);o.checked?s<0&&(e.outval=n.concat([r])):s>-1&&(e.outval=n.slice(0,s).concat(n.slice(s+1)))}else e.outval=a}}}):e._e(),"integer"==e.nodes.type?n("input",{directives:[{name:"model",rawName:"v-model.lazy",value:e.outval,expression:"outval",modifiers:{lazy:!0}}],attrs:{type:"number"},domProps:{value:e.outval},on:{change:function(t){e.outval=t.target.value}}}):e._e(),"string"==e.nodes.type?n("input",{directives:[{name:"model",rawName:"v-model.lazy",value:e.outval,expression:"outval",modifiers:{lazy:!0}}],attrs:{type:"Text"},domProps:{value:e.outval},on:{change:function(t){e.outval=t.target.value}}}):e._e()]),n("div",{staticClass:"disp"},[e._v(e._s(e.value))])]):n("div",{staticClass:"node"},[n("div",[e._v(e._s(e.label))]),e._l(e.nodes,(function(e){return n("node",{key:e.id,attrs:{nodes:e.nodes,label:e.label}})}))],2)])},l=[],i={props:["label","nodes"],data:function(){return{outval:null}},name:"node",computed:{isleaf:function(){return!!this.nodes&&this.nodes.type},value:function(e,t){return!!this.nodes&&(t==this.nodes.value?this.nodes.value:t)}},created:function(){var e=this;this.nodes&&this.nodes.type&&(console.log(this.nodes.path+" created"),this.$connect("ws://localhost:11111"+this.nodes.path),console.log(this.nodes.path+" connected"),this.$options.sockets.onmessage=function(t){var n=t.data,o=JSON.parse(n);o.path==e.nodes.path&&e.update(o.value)},console.log(this.nodes.path+" done"))},methods:{update:function(e){this.nodes.value=e},get:function(){var e=this;fetch(this.nodes.path).then((function(e){return e.json()})).then((function(t){e.nodes.readable||(e.nodes.value=t.data)}))}},watch:{outval:function(){var e=Object(o["a"])(regeneratorRuntime.mark((function e(t,n){var o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:n!=t&&(o="string"!=typeof this.outval?this.outval:JSON.parse(this.outval),fetch(this.path,{headers:{"Content-Type":"application/json; charset=utf-8"},method:"PATCH",body:JSON.stringify({op:"replace",path:this.nodes.path,value:o})}).then((function(e){return console.log(e)})));case 1:case"end":return e.stop()}}),e,this)})));function t(t,n){return e.apply(this,arguments)}return t}()},destroyed:function(){this.$disconnect()}},c=i,d=(n("d7b7"),n("2877")),p=Object(d["a"])(c,u,l,!1,null,"51b6ebe0",null),v=p.exports,f=n("b408"),h=n.n(f);function b(e,t,n){var o=new Object;return o.path=n+"/"+e,o.label=e,o.nodes=y(t,o.path),o}function y(e,t){if("object"===Object(r["a"])(e)&&null!==e){var n=[];if("number"==typeof e.$count){var o=e.$count;delete e.$count;for(var s=0;s<o;s++)n.push(b(String(s),e,t));return n}if(e.$type){console.log("type");var u=new Object;return u.label="",u.path=t,u.value="unknown",u.type=e.$type,u.readable=!e.r,u.writable=!e.w,u}for(var l=0,i=Object.entries(e);l<i.length;l++){var c=Object(a["a"])(i[l],2),d=c[0],p=c[1];"$count"!=d&&n.push(b(d,p,t))}return n}}s["a"].config.productionTip=!1,s["a"].use(h.a,"ws://localhost:11111/",{connectManually:!0}),fetch("/schema").then(function(){var e=Object(o["a"])(regeneratorRuntime.mark((function e(t){var n,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,t.json();case 2:n=e.sent,console.log(n),o=new Object,o.label=n.controller,o.nodes=y(n,""),new s["a"]({el:"#app",data:{tree:o},components:{Node:v}});case 8:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}())},"5df6":function(e,t,n){},d7b7:function(e,t,n){"use strict";var o=n("5df6"),a=n.n(o);a.a}});
//# sourceMappingURL=app.82038466.js.map