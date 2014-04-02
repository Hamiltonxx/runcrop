$(function(){

    $(".showpassword").each(function(index,input) {
        var $input = $(input);
        $("<p class='opt'/>").append(
            $("<input type='checkbox' class='showpasswordcheckbox' id='showPassword' />").click(function() {
                var change = $(this).is(":checked") ? "text" : "password";
                var rep = $("<input placeholder='Password' type='" + change + "' />")
                    .attr("id", $input.attr("id"))
                    .attr("name", $input.attr("name"))
                    .attr('class', $input.attr('class'))
                    .val($input.val())
                    .insertBefore($input);
                $input.remove();
                $input = rep;
             })
        ).append($("<label for='showPassword'/>").text("Show password")).insertAfter($input.parent());
    });

    $('#showPassword').click(function(){
		if($("#showPassword").is(":checked")) {
			$('.icon-lock').addClass('icon-unlock');
			$('.icon-unlock').removeClass('icon-lock');    
		} else {
			$('.icon-unlock').addClass('icon-lock');
			$('.icon-lock').removeClass('icon-unlock');
		}
    });

   
    $('.log-twitter').click(function(){
        $(this).parent().parent().hide();
    });

    $('.loginsubmit').click(function(){
    	var username = $('.username').val();
    	var password = $('.password').val();
    	$.ajax({
    		url:'/api/user',
    		type:'GET',
    		dataType:'json',
    		contentType:'application/json',
    		success:function(data){
    			var users = data.objects;
    			console.log(data.objects);
    			for(var i=0;i<users.length;i++){
    				if(username==users[i].username && password==users[i].password){
    					sessionStorage.setItem('userid',users[i].id);
    					sessionStorage.setItem('username',username);
    					console.log("welcome back "+username+" userid: "+sessionStorage.getItem("userid"));
    					$('.form-2').hide();
    					$('.logininfo').html('<a href="#" class="loginuser cssbutton blue">'+username+'</a> <button href="#" class="signoutbutton cssbutton blue" onclick="logAnonymous()">Log Out</button>');
    					break;
    				}else{
    					alert("username or password wrong.");
    				}
    			}

    		}
    	});
    });
/*    $('.signoutbutton').click(function(){
    	alert('...');
    	sessionStorage.clear();
    	$('.logininfo').html('<a href="#" class="loginuser cssbutton blue">Anonymous</a> <a href="#" class="signinbutton cssbutton blue">Sign In</a>');
    });
  */  
});

$(function(){
	if(sessionStorage.getItem('username')){
    	$('.logininfo').html('<a href="#" class="loginuser cssbutton blue">'+sessionStorage.getItem("username")+'</a> <a href="#" class="signoutbutton cssbutton blue" onclick="logAnonymous()">Log Out</a>');
    	
    }
});

function logAnonymous(){
	sessionStorage.clear();
    $('.logininfo').html('<a href="#" class="loginuser cssbutton blue">Register</a> <button href="#" class="signinbutton cssbutton blue" onclick="showForm2()">Sign In</button>');
}
function logUser(){
	if(sessionStorage.getItem('username')){
    	$('.logininfo').html('<a href="#" class="loginuser cssbutton blue">'+sessionStorage.getItem("username")+'</a> <a href="#" class="signoutbutton cssbutton blue">Log Out</a>');
    }
}

function showForm2(){
	$('.form-2').show();
}
function hideForm2(){
	$('.form-2').hide();
}