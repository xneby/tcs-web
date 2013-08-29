function ready(){
	$('.comment_link').click(
		function() {
			$(this).parents('.comment_box').children('.comments').slideToggle();
			var url = $(this).attr('data-bucket');
			$.ajax({
				type: "GET",
				url: url,
			});
			return false;
		}		
	);
	if($('.comments').length == 1){
		$('.comments').children('.comment_link').click();
	}
	$('.voting .badge').dblclick(function(){
		$(this).parents('form').submit();
	});
}

$(document).ready(ready);
