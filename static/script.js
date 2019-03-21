function fetch() {
	var add = document.getElementById('url_input').value;
	var o = {
		link: add
	};
	var js = JSON.stringify(o);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {
			createDiv(this.response);
		}
	};
	xhttp.open('POST', '/fetch');
	xhttp.setRequestHeader('Content-Type', 'application/json');
	xhttp.send(js);
}

function createDiv(value) {
	var div = document.createElement('a');
	div.style.width = '100px';
	div.style.height = '100px';
	div.href = value;
	div.download = 'picture';
	div.innerHTML = 'get it';
	div.style.background = 'red';

	document.getElementsByClassName('main')[0].appendChild(div);
}
