// http://jsbin.com/IBIDalEn/2/edit?html,css,js,output
$.fn.stars = function() {
    return this.each(function(i,e){$(e).html($('<span/>').width($(e).text()*16));});
};
$('.stars').stars();

// https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
function topFunction() {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
