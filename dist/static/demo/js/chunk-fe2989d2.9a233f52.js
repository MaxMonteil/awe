(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-fe2989d2"],{"1f97":function(t,a,e){"use strict";var n=e("c141"),r=e.n(n);r.a},c141:function(t,a,e){},f3fc:function(t,a,e){"use strict";e.r(a);var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{attrs:{id:"visualizer"}},[e("h1",{staticClass:"title"},[t._v("AWE Visualizer")]),e("form",{attrs:{id:"url-form"},on:{submit:function(t){t.preventDefault()}}},[e("input",{directives:[{name:"model",rawName:"v-model",value:t.targetUrl,expression:"targetUrl"}],attrs:{type:"url",name:"url",id:"target-url-input",placeholder:"Paste URL here"},domProps:{value:t.targetUrl},on:{input:function(a){a.target.composing||(t.targetUrl=a.target.value)}}}),e("div",{staticClass:"form-buttons"},[e("button",{staticClass:"vis-button crawlButton",on:{click:t.crawlURL}},[t._v("Crawl Site")]),e("button",{staticClass:"vis-button analyzeButton",on:{click:t.analyzeURL}},[t._v("Analyze Site")])])])])},r=[],l=e("bc3a"),o=e.n(l),c={name:"home",data:function(){return{targetUrl:"",result:""}},methods:{crawlURL:function(){var t=this;if(console.log("crawl"),""!==this.targetUrl){var a="http://localhost:5000/api/crawl";o.a.get("".concat(a,"?url=").concat(this.targetUrl)).then(function(a){t.result=a.data}).catch(function(t){console.log(t)})}},analyzeURL:function(){var t=this;if(console.log("analyze"),""!==this.targetUrl){var a="http://localhost:5000/api/analyze";o.a.get("".concat(a,"?url=").concat(this.targetUrl)).then(function(a){t.result=a.data}).catch(function(t){console.log(t)})}}}},i=c,s=(e("1f97"),e("2877")),u=Object(s["a"])(i,n,r,!1,null,"79ec0cae",null);a["default"]=u.exports}}]);
//# sourceMappingURL=chunk-fe2989d2.9a233f52.js.map