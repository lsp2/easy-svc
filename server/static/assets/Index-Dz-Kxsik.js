import{u as e}from"./user-CnHw-90H.js";import{d as t,k as a,c as n,a as s,B as l,C as o,O as r,o as u,R as i,P as d,p,b as c,_ as m}from"./index-B9ZAPPyA.js";import"./requst-SMwGbunC.js";const g=e=>/^[a-zA-Z0-9]{2,12}$/.test(e),w=e=>/^[a-zA-Z0-9]{6,18}$/.test(e),v=e=>(p("data-v-04b3b474"),e=e(),c(),e),b={class:"container"},f={class:"content"},I={key:0,action:"#",class:"row"},y=[v((()=>s("h3",{class:"mb-3"},"登录",-1))),v((()=>s("input",{class:"input-text mb-1",type:"text",placeholder:"账号",id:"login-uId"},null,-1))),v((()=>s("input",{class:"input-text mb-1",type:"password",placeholder:"密码",id:"login-pw"},null,-1)))],x={key:1,action:"#",id:"reister",class:"row"},h=[v((()=>s("h3",{class:"mb-3"},"注册",-1))),v((()=>s("input",{class:"input-text mb-1",type:"text",placeholder:"设置账号（2-12位字母或数字的组合）",id:"reg-uId"},null,-1))),v((()=>s("input",{class:"input-text mb-1",type:"password",placeholder:"设置密码（6-18位字母或数字的组合）",id:"reg-pw"},null,-1))),v((()=>s("input",{class:"input-text mb-1",type:"password",placeholder:"确认密码",id:"reg-pw2"},null,-1)))],_=m(t({__name:"Index",setup(t){const p=e(),c=a(!0),m=()=>{if(!c.value)return void _(!0);const e=document.getElementById("login-uId").value,t=document.getElementById("login-pw").value;e?t?g(e)?w(t)?p.login({userId:e,password:t}):d.warning("密码格式不对"):d.warning("账号格式不对"):d.warning("未输入密码"):d.warning("未输入账号")},v=()=>{if(c.value)return void _(!1);const e=document.getElementById("reg-uId").value,t=document.getElementById("reg-pw").value,a=document.getElementById("reg-pw2").value;e?t?a?g(e)?w(t)?t===a?p.register({userId:e,password:t}):d.warning("两次密码不一致"):d.warning("密码格式不对"):d.warning("账号格式不对"):d.warning("未确认密码"):d.warning("未输入密码"):d.warning("未输入账号")},_=e=>{c.value=e};return(e,t)=>{const a=r("a-col"),d=r("a-row");return u(),n("div",b,[s("div",f,[c.value?(u(),n("form",I,y)):(u(),n("form",x,h)),l(d,{class:"row mt-1"},{default:o((()=>[l(a,{span:11,offset:0},{default:o((()=>[s("button",{class:i(["btn normal long",c.value?"hollow":"normal"]),onClick:v},"注册",2)])),_:1}),l(a,{span:11,offset:2},{default:o((()=>[s("button",{class:i(["btn normal long",c.value?"normal":"hollow"]),onClick:m},"登录",2)])),_:1})])),_:1})])])}}}),[["__scopeId","data-v-04b3b474"]]);export{_ as default};
