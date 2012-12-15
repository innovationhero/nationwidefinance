var nationwide = nationwide || {};

nationwide.utils = nationwide.utils || {};

$(function(){
	$("#org_lookup").on('click', function(){
		nationwide.utils.do_ajax('post', '/referrals/search_organization/', {'business_name' : ''}, function(data){
			
			$("#modal").html(data);
			$("#modal").dialog({
				width : 1200,
    			height : 350,
        		autoOpen: true,
        		title: 'Login',
        		resizable : false,
        		modal : true,
        		scrollbars : true
			});
		},
		function(data){

		},
		"html");
		
	});
});