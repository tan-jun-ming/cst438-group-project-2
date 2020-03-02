$(function(){
    $("#searchform").submit(function(event){
        event.preventDefault();
        alert("You searched for: " + $(event.target).find("input").val());

    })
})