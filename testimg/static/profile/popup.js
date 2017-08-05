var imgs = document.getElementsByClassName('content-img');
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("origin");
var pic = document.getElementById("new");
var captionText = document.getElementById("caption");
var span = document.getElementsByClassName("close")[0];
var save_new = document.getElementById("save_new");

var labels_button = document.getElementsByName("labels_button");
var label_is_choosed = new Array();

var new_str = new Array();
var is_saved = new Array();
var mode_select;
var present_showing_img = -1;



for (var i=0; i<imgs.length; i++)
{
	var img = imgs[i];
	img.onclick = function(){
		modal.style.display = "block";
		modalImg.src = this.src;
		captionText.innerHTML = this.alt;
		save_new.style.display = "none";
		for (var j=0; j<8; ++j)
		{
			is_saved[j] = false;
			new_str[j] = "";
		}
		$.get("getPicLabels?&path=" + captionText.innerHTML, function(data)
		{
			labels = data.split(",");
			for (var j=0; j<labels_button.length; j++)
			{
				if(labels.indexOf(labels_button[j].innerHTML) >= 0)
				{
					label_is_choosed[j] = true;
					labels_button[j].setAttribute("class", "btn btn-primary");
				}
				else
				{
					label_is_choosed[j] = false;		
					labels_button[j].setAttribute("class", "btn btn-default");
				}
			}
		})
		for(var j=0; j<imgs.length; j++)
		{
			if(this.src == imgs[j].src)
				present_showing_img = j;
		}
		
	}
}

//choose-label buttons
for(var i=0; i<labels_button.length; i++)
{
	var button = labels_button[i];
	button.onclick = function(){
		var j = 0;
		for(j = 0; j<labels_button.length; j++)
			if(this == labels_button[j])
				break;
		console.log(j);
		if(label_is_choosed[j] == true)
		{
			label_is_choosed[j] = false;
			labels_button[j].setAttribute("class", "btn btn-default");
			var inputStr = "chooseLabels?label=" + this.innerHTML + "&path=" + captionText.innerHTML;
			$.get(inputStr, function(data){})
			console.log(inputStr);
		}
		else
		{
			var has_choosen_num = 0;
			for(var k=0; k<labels_button.length; k++)
			{
				if(label_is_choosed[k] == true)
					has_choosen_num ++;
			}
			if(has_choosen_num < 3)
			{
				label_is_choosed[j] = true;
				labels_button[j].setAttribute("class", "btn btn-primary");
				var inputStr = "chooseLabels?label=" + this.innerHTML + "&path=" + captionText.innerHTML;
				$.get(inputStr, function(data){})
				console.log(inputStr);
			}
			else
			{
				alert("3 labels for a photo at most")
			}
		}
		//console.log('111');
		
	}
}



span.onclick = function() { 
	modal.style.display = "none";
	pic.src = "";
	pic.style.display = "none";
	save_new.style.display = "none";
	for (var j=0; j<8; ++j)
	{
		if (!is_saved[j])
		{
			$.get("deleteTempImg?path=" + new_str[j], function(data,status){});
		}
	}
	location.reload();
}

var previous_picture = document.getElementById("previous-picture");
var next_picture = document.getElementById("next-picture");
previous_picture.onclick = function(){
	if(present_showing_img == 0)
		return;
	present_showing_img -= 1;
	//delete tempimg
	for (var j=0; j<8; ++j)
	{
		if (!is_saved[j])
		{
			$.get("deleteTempImg?path=" + new_str[j], function(data,status){});
			is_saved[j] = 0;
		}
	}

	//delete processed picture
	mode_select = -1;
	for(var j=0; j<8; j++)
	{
		new_str[j] = "";
	}

	//transfer to new picture
	
	modalImg.src = imgs[present_showing_img].src;
	captionText.innerHTML = imgs[present_showing_img].alt;
	save_new.style.display = "none";
	pic.style.display = "none";
	for (var j=0; j<8; ++j)
	{
		is_saved[j] = false;
		new_str[j] = "";
	}
	$.get("getPicLabels?&path=" + captionText.innerHTML, function(data)
	{
		labels = data.split(",");
			for (var j=0; j<labels_button.length; j++)
			{
				if(labels.indexOf(labels_button[j].innerHTML) >= 0)
				{
					label_is_choosed[j] = true;
					labels_button[j].setAttribute("class", "btn btn-primary");
				}
				else
				{
					label_is_choosed[j] = false;		
					labels_button[j].setAttribute("class", "btn btn-default");
				}
			}
	})
}
next_picture.onclick = function(){
	if(present_showing_img == imgs.length - 1)
		return;
	present_showing_img += 1;
	console.log(present_showing_img);
	for (var j=0; j<8; ++j)
	{
		if (!is_saved[j])
		{
			$.get("deleteTempImg?path=" + new_str[j], function(data,status){});
			is_saved[j] = 0;
		}
	}
//delete processed picture
	mode_select = -1;
	for(var j=0; j<8; j++)
	{
		new_str[j] = "";
	}
	//transfer to new picture
	modalImg.src = imgs[present_showing_img].src;
	captionText.innerHTML = imgs[present_showing_img].alt;
	save_new.style.display = "none";
	pic.style.display = "none";
	for (var j=0; j<8; ++j)
	{
		is_saved[j] = false;
		new_str[j] = "";
	}
	$.get("getPicLabels?&path=" + captionText.innerHTML, function(data)
	{
		labels = data.split(",");
			for (var j=0; j<labels_button.length; j++)
			{
				if(labels.indexOf(labels_button[j].innerHTML) >= 0)
				{
					label_is_choosed[j] = true;
					labels_button[j].setAttribute("class", "btn btn-primary");
				}
				else
				{
					label_is_choosed[j] = false;		
					labels_button[j].setAttribute("class", "btn btn-default");
				}
			}
	})
}


var gray = document.getElementById("gray");
gray.onclick = function() {
	if (new_str[0] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=gray", function(data,status){
			pic.src = new_str[0] = data;
		})
	}
	else
	{
		pic.src = new_str[0];
	}
	mode_select = 0;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var binary = document.getElementById("binary");
binary.onclick = function() {
	if (new_str[1] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=binary", function(data,status){
			pic.src = new_str[1] = data;
		})
	}
	else
	{
		pic.src = new_str[1];
	}
	pic.src = new_str[1];
	mode_select = 1;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var gaussian = document.getElementById("gaussian");
gaussian.onclick = function() {
	if (new_str[2] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=gaussian", function(data,status){
			pic.src = new_str[2] = data;
		})
	}
	else
	{
		pic.src = new_str[2];
	}
	pic.src = new_str[2];
	mode_select = 2;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var shrink = document.getElementById("shrink");
shrink.onclick = function() {
	if (new_str[3] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=shrink", function(data,status){
			pic.src = new_str[3] = data;
		})
	}
	else
	{
		pic.src = new_str[3];
	}
	pic.src = new_str[3];
	mode_select = 3;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var enlarge = document.getElementById("enlarge");
enlarge.onclick = function() {
	if (new_str[4] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=enlarge", function(data,status){
			pic.src = new_str[4] = data;
		})
	}
	else
	{
		pic.src = new_str[4];
	}
	pic.src = new_str[4];
	mode_select = 4;
	pic.style.display = "block";
	save_new.style.display = "block";
}


var rotate90 = document.getElementById("rotate90");
rotate90.onclick = function() {
	if (new_str[5] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=rotate90", function(data,status){
			pic.src = new_str[5] = data;
		})
	}
	else
	{
		pic.src = new_str[5];
	}
	pic.src = new_str[5];
	mode_select = 5;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var rotate180 = document.getElementById("rotate180");
rotate180.onclick = function() {
	if (new_str[6] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=rotate180", function(data,status){
			pic.src = new_str[6] = data;
		})
	}
	else
	{
		pic.src = new_str[6];
	}
	pic.src = new_str[6];
	mode_select = 6;
	pic.style.display = "block";
	save_new.style.display = "block";
}

var rotate270 = document.getElementById("rotate270");
rotate270.onclick = function() {
	if (new_str[7] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=rotate270", function(data,status){
			pic.src = new_str[7] = data;
		})
	}
	else
	{
		pic.src = new_str[7];
	}
	pic.src = new_str[7];
	mode_select = 7;
	pic.style.display = "block";
	save_new.style.display = "block";
}

save_new.onclick = function() {
	if (is_saved[mode_select])
	{
		alert("New Photo is already saved to your album!");
	}
	else
	{
		is_saved[mode_select] = true;
		$.get("saveNewPhoto?path=" + new_str[mode_select], function(data,status){
			alert(data);
		})
	}
}