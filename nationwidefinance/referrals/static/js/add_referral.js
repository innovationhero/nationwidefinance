var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

$(function(){
	$("input[name=referrer-email],input[name=referred-email]").on('keyup', function(){
		var self = $(this);
		$(this).autocomplete({
            minLength : 3,
            source : function(request, response) {
                var data = {};
                data['email'] = request.term;
                var result = nationwide.utils.do_ajax('post','/referrals/add_referral_autocomplete/',data,function(data) {response(data)});
            },
            select : function(event, ui) {
            	name = self.attr('name').substring(0,self.attr('name').indexOf('-')+1);
            	$("input[name="+name+"email]").blur();
            	$("input[name="+name+"email]").val(ui.item.email);
            	$("input[name="+name+"first_name]").val(ui.item.first_name);
            	$("input[name="+name+"last_name]").val(ui.item.last_name);
            	$("input[name="+name+"dob]").val(ui.item.dob);
            	return false;

            }
        }).data( "autocomplete" )._renderItem = function( ul, item ) {
            return $( "<li>" ).data( "item.autocomplete", item ).append( "<a>"+item.email+"</a>" ).appendTo( ul );
        };
    });
});