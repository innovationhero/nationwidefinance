var nationwide = nationwide || {};
nationwide.utils = nationwide.utils || {};

nationwide.utils.modal_factory = function ($html,title, $buttons, width, height) {
    return $('<div></div>').appendTo('body')
                    .html($html)
                    .dialog({
                        modal    : true, 
                        title: title, 
                        zIndex: 10000, 
                        autoOpen: true,
                        width    : 'auto', 
                        resizable: false,
                        buttons  : $buttons,
                        width    : width,
                        height   : height   
                    });    
}