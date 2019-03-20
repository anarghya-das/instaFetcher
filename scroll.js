function fun() {
	divs = document.getElementsByClassName('Nnq7C weEfm');
	var i = 0;
	while (i != divs.length) {
		i = divs.length;
		divs[divs.length - 1].scrollIntoView();
		divs = document.getElementsByClassName('Nnq7C weEfm');
		setTimeout(fun, 1000);
	}
}

fun();
