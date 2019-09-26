$(document).ready(function(){
    var current = window.location.href;
    $('.nav-item').each(function(){
        $(this).removeClass('active');
        if(this.href==current){
            $(this).addClass('active');
        }
    });

});
       
    


function clickbtn(img_name){
    var img_obj = document.getElementsByClassName(img_name)

    var ID = img_obj[0].value;
    var road = img_obj[1].value;
    var time = img_obj[2].value;
    var name = img_obj[3].value;
    var path = img_obj[4].value;
    var btn = document.getElementById(img_name)

    if(!btn.classList.contains("disabled")){
        d ={"ID":ID,"road":road,"time":time,"name":name,"path":path}
        $.ajax({
            type:"POST",
            url: "/index",
            contentType:"application/json",
            data:JSON.stringify(d),
            success: function(response) {
                console.log(name+" has been sent")
            },
            error: function(xhr) {
                //Do Something to handle error
                console.log("error");
            }
            }
        );
    }
    
    btn.classList.remove("btn-primary");
    btn.className += " btn-secondary disabled";
}
