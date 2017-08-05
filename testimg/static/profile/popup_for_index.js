var imgs = document.getElementsByClassName('content-img');
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("origin");
var span = document.getElementsByClassName("close")[0];
//var captionText = document.getElementById("caption");
var present_showing_img = -1;

for (var i=0; i<imgs.length; i++)
{
	var img = imgs[i];
	img.onclick = function(){
		modal.style.display = "block";
		modalImg.src = this.src;
	//	captionText.innerHTML = this.alt;
		for(var j=0; j<imgs.length; j++)
		{
			if(this.src == imgs[j].src)
				present_showing_img = j;
		}
	}
}

span.onclick = function() { 
	modal.style.display = "none";
}

var previous_picture = document.getElementById("previous-picture");
var next_picture = document.getElementById("next-picture");
previous_picture.onclick = function(){
	if(present_showing_img == 0)
		return;
	present_showing_img -= 1;

	//transfer to new picture
	
	modalImg.src = imgs[present_showing_img].src;
	//captionText.innerHTML = imgs[present_showing_img].alt;
}
next_picture.onclick = function(){
	if(present_showing_img == imgs.length - 1)
		return;
	present_showing_img += 1;
	modalImg.src = imgs[present_showing_img].src;
	//captionText.innerHTML = imgs[present_showing_img].alt;
}

