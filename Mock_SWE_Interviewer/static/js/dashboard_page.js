document.addEventListener('DOMContentLoaded', function() {
	const dashboard = document.getElementById('home_button');
	const start = document.getElementById('start_button');
	const preference = document.getElementById('preference_container');

	start.addEventListener('click', function(){
		start.classList.add('slide');
		preference.classList.add('slide');

	})

	dashboard.classList.add('highlight');

});