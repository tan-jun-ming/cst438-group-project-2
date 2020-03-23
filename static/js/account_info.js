$(function(){
    $("#logout").click(function(event){
        localStorage.clear();
        window.location = "/";
        
    })
    let user_token = localStorage.getItem("token");

    if (user_token != null){
        window.location = "/";
    } else {
        let firstname = localStorage.getItem("firstname");
        let lastname = localStorage.getItem("lastname");
        let username = localStorage.getItem("username");
    
        $("#name").text(`${firstname} ${lastname}`);
        $("#username").text(username);
    }
	

})