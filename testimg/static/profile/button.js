var filter = document.getElementById('Filter');
var filterbtns = document.getElementsByName('filters_button');
var choo = document.getElementById('Choose');
var del = document.getElementById("delete");
var selall = document.getElementById('selectAll');
var checkboxes = document.getElementsByName('deleteList')
var filterStatus = false;
var checkboxStatus = false;

for (var i=0; i<checkboxes.length; i++)
	{
		var checkbox = checkboxes[i];
		checkbox.style.position = "relative";
		checkbox.style.left = "0px";
		checkbox.style.top = "0px";
	}

choo.onclick = function() {
	if (!checkboxStatus)
	{
		this.style.color = 'white';
		this.style.background = '#D8BFD8'; //Thistle
		for (var i=0; i<checkboxes.length; i++)
		{
			checkboxes[i].style.display = 'block';
			checkboxes[i].checked = false;
		}
		checkboxStatus = true;
		del.style.display = 'block';
		selall.style.display = 'block';
	}
	else
	{
		this.style.color = 'black';
		this.style.background = 'white';
		for (var i=0; i<checkboxes.length; i++)
		{
			checkboxes[i].style.display = 'none';
		}
		checkboxStatus = false;
		del.style.display = 'none';
		selall.style.display = 'none';
	}
}

selall.onclick = function() {
	var sum = checkboxes.length;
	for (var i=0; i<checkboxes.length; i++)
	{
		var checkbox = checkboxes[i];
		if (checkbox.checked)
			sum--;
		else
			checkbox.checked = true;
	}
	if (!sum)
	{
		for (var i=0; i<checkboxes.length; i++)
		{
			var checkbox = checkboxes[i];
			checkbox.checked = false;
		}
	}
}

var imgboxes = document.getElementsByClassName('col-md-4 box')
var labelboxes = document.getElementsByClassName('labels-in-caption');

Filter.onclick = function() {
	if (filterStatus)
	{
		for (var i=0; i<filterbtns.length; i++)
		{
			filterbtns[i].style.display = 'none';
		}
		filterStatus = false;
		for (var j=0; j<labelboxes.length; j++)
			{
				imgboxes[j].style.opacity = '1.0';
			}
	}
	else
	{
		for (var i=0; i<filterbtns.length; i++)
		{
			filterbtns[i].style.display = 'block';
			filterbtns[i].style.background = '#7FFFD4'; //Aquamarine
			filterbtns[i].style.color = 'white';
			for (var j=0; j<labelboxes.length; j++)
			{
				var lbls = labelboxes[j].getElementsByTagName("span");
				if (!lbls.length)
					imgboxes[j].style.opacity = '0.5';
			}
		}
		filterStatus = true;
	}
}

for (var i=0; i<filterbtns.length; i++)
{
	var filterbtn = filterbtns[i];
	filterbtn.onclick = function(){
		var that = this;
		if (this.style.color == 'white')
		{
			that.style.background = 'white';
			that.style.color = 'black';
			for (var j=0; j<labelboxes.length; j++)
			{
				var lbls = labelboxes[j].getElementsByTagName("span");
				for(var k=0; k<lbls.length; k++)
				{
					if (lbls[k].innerHTML == this.innerHTML)
						{
							imgboxes[j].style.opacity = '0.5';
							break;
						}
				}
			}
		}
		else
		{
			that.style.background = '#7FFFD4'; //Aquamarine
			that.style.color = 'white';
			for (var j=0; j<labelboxes.length; j++)
			{
				var lbls = labelboxes[j].getElementsByTagName("span");
				for(var k=0; k<lbls.length; k++)
				{
					if (lbls[k].innerHTML == this.innerHTML)
						{
							imgboxes[j].style.opacity = '1.0';
							break;
						}
				}
			}
		}

	}
}
