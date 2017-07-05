var imgs = document.getElementsByName('myImgs');
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("origin");
var pic = document.getElementById("new");
var captionText = document.getElementById("caption");
var span = document.getElementsByClassName("close")[0];
var save_new = document.getElementById("save_new");

var labels_text = document.getElementsByName("labels_text");
var labels_button = document.getElementsByName("labels_button");

var new_str = new Array();
var is_saved = new Array();
var mode_select;

for (var i=0; i<imgs.length; i++)
{
	var img = imgs[i];
	img.onclick = function(){
		modal.style.display = "block";
		modalImg.src = this.src;
		captionText.innerHTML = this.alt;
		save_new.style.display = "none";
		for (var j=0; j<5; ++j)
		{
			is_saved[j] = false;
			new_str[j] = "";
		}
		$.get("getPicLabels?&path=" + captionText.innerHTML, function(data)
		{
			labels = data.split(",");
			for(i = 0; i < labels.length; i++)
			{
				if(labels[i] != '')
					labels_text[i].value = labels[i];
				//console.log(labels[i]);
			}
		})
	}
}

//choose-label buttons
for(var i=0; i<labels_button.length; i++)
{
	var button = labels_button[i];
	button.onclick = function(){
		var flag = 0;
		for(var j=0; j<3; j++)
		{
			if(labels_text[j].value == this.innerHTML)
			{
				flag = 1;
				break;
			}
		}
		if(flag == 0)
		{
			for(var j=0; j<3; j++)
			{
				if(!labels_text[j].value)
				{
					labels_text[j].value = this.innerHTML
					break;
				}
			}
		}
	}
}

//save-labels button
var save_labels_button = document.getElementById("save_labels");
save_labels_button.onclick = function(){
	var inputStr = "chooseLabels?label0=" + labels_text[0].value +
				   "&label1=" + labels_text[1].value+
				   "&label2=" + labels_text[2].value+
				   "&path=" + captionText.innerHTML;
	console.log(inputStr);
	$.get(inputStr, function(data){
		alert("save labels successfully!")	
	})
}

span.onclick = function() { 
	modal.style.display = "none";
	pic.src = "";
	pic.style.display = "none";
	
	save_new.style.display = "none";
	for (var j=0; j<5; ++j)
	{
		if (!is_saved[j])
		{
			$.get("deleteTempImg?path=" + new_str[j], function(data,status){})
		}
	}
	location.reload();
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

var zoom = document.getElementById("zoom");
zoom.onclick = function() {
	if (new_str[3] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=zoom", function(data,status){
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

var rotate = document.getElementById("rotate");
rotate.onclick = function() {
	if (new_str[4] == '')
	{
		$.get("imageProcess?path=" + captionText.innerHTML + "&mode=rotate", function(data,status){
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