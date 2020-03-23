$(function(){
    $("#searchform").submit(function(event){
        event.preventDefault();
        alert("You searched for: " + $(event.target).find("input").val() + "\nThis feature is not yet implemented.");

    })

    let user_token = localStorage.getItem("token");

    if (user_token != null){
        let firstname = localStorage.getItem("firstname");
        let lastname = localStorage.getItem("lastname");

        $("#login_button").text(`${firstname} ${lastname}`);
        $("#login_button").attr("href", "account");
    }
})