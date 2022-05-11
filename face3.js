function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function send()
{
    var a=document.getElementById('msg');
    var text=a.value;
    console.log(text);
    if(text=='')
    {
        alert("no message typed!")
        return;
    }
    req= new XMLHttpRequest();
    req.open("POST",'http://127.0.0.1:5000',true);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    var reply=''
    req.onreadystatechange=async function(){
        if(this.readyState==4 && this.status== 200)
        {
            reply=this.responseText;
            console.log(reply);
            var msgbox=document.getElementById('messages');
            msgbox.innerHTML+='<div class="container darker"><img src="humanav.jpg" alt="Avatar" class="right"><p>'+text+'</p><span class="time-left">11:01</span></div>'
            await sleep(100)
            msgbox.innerHTML+='<div class="container"> <img src="botav.jpg" alt="Avatar"><p>'+reply+'</p><span class="time-right">11:00</span></div>'
        }
    }
    var str="msg="+text;
    req.send(str);
    a.value='';
}

window.addEventListener("keyup", function(e) {if (e.keyCode === 13){send();}});