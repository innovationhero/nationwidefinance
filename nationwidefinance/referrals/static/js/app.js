var nationwide = nationwide || {};

nationwide.utils = {};

nationwide.helpers = {};

/**
	Utility function to perform all Ajax GET and POST calls
*/
nationwide.utils.do_ajax = function (type, url, data, success, error, dataType) {
	if (typeof(dataType) == 'undefined') {
		var dataType = 'json';
	}
    return $.ajax({
            url: url,
	        type: type,
	        data: data,
	        dataType: dataType,
	        headers: {
	               "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
	        },
	        success: success,
	        error: error
	    });
}

nationwide.utils.update = function(obj1, obj2) {
	$.each(obj2, function(key,value){
		if (type(obj1[key]) == 'undefined') {
			obj1[key] = value;
		} else {
			obj1[key] = obj2[key];
		}
	});
}

nationwide.utils.show_hide = function() {
	var show = arguments[0];
	var $elm = arguments[1];
	
	if (show) {
		$elm.show();
	} else{
		$elm.hide();
	}

}

nationwide.utils.select_processor = function() {
	var args = arguments;
	var $select = args[0];
	var conditions = args[1];
	var result_function = args[2];
	//var result_args = arguments.slice(1,args.lenght);

	for (key in conditions) {
		if ($select.val() == key) {
			result_args = conditions[key];
			for (i =0; i < result_args.length; i++) {
				result_function.apply(this||window,result_args[i]);
			}
			break;
		}
	}
}


/**
	Helper method for All Aajax failures
*/
nationwide.helpers.error = function() {
	alert('error');
};
