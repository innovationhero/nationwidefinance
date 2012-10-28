var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

nationwide.utils.datatable_factory = function(server_side,aaData,aoColumns,col0) {


	var Abstract_Datatable = {
		"bDestroy"        : true,
		"bJQueryUI"       : true,
		"bPaginate"       : true,
        "bLengthChange"   : false,
        "iDisplayLength"  : 15,
        "bFilter"         : true,
        "bSort"           : true,
        "bInfo"           : true,
        "bAutoWidth"      : false,
        "bProcessing"     : true,
        "bServerSide"     : server_side,
        "sPaginationType" : "full_numbers",
        "aaData"          :  aaData,
        "aoColumns"       : aoColumns,
		fnRowCallback     : function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
			if (typeof(col0) != 'undefined') {
				var id = aData[0];
				var $elm = $("<"+col0['tag']+"/>",
						col0['props']
					);
				$elm.attr('id',id);
				$('td:eq(0)', nRow).html($elm);
			}

		}
		
	};
	return Abstract_Datatable;

}