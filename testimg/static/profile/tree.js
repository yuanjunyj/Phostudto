function buildMenu()
{
	menu = document.getElementById("menutree").value;
	document.write('<style type="text/css">label.jmp:active, label.jmp:hover {color: #F08080; cursor:pointer}</style>');
	document.write('&nbsp;&nbsp;&nbsp;<label type="button" data-toggle="collapse" data-target="#0">'
		+ '<span name="sparrows" class="glyphicon glyphicon-folder-close" style="cursor:pointer;"></span>'
		+ '</label><label class="jmp" value=" ">&nbsp;&nbsp;root&nbsp;&nbsp;</label>');

	build(menu, 1, "");
}

nodes = 0;

function build(str, depth, dir)
{
	if (str == "")
		return;

	if (str[0] == '(' && str[str.length - 1] == ')')
		str = str.substring(1, str.length - 1);
	
	var children = new Array();
	var k = 0, st = 0, match = 0;
	while (k < str.length)
	{
		if (str[k] == '(')
			match++;
		else if (str[k] == ')')
			match--;
		else if (str[k] == ',')
		{
			if (match == 0)
			{
				children[children.length] = str.substring(st, k);
				st = k + 1;
				k++;
			}
		}
		k++;
	}
	children[children.length] = str.substring(st, k);

	document.write('<div id="' + nodes + '" class="collapse">');

	for (var i = 0; i <children.length; i++)
	{
		nodes++;
		var tmp = children[i];
		var len = tmp.length;
		var pos = tmp.indexOf('(');

		if (pos == -1)
		{
			console.log(depth);
			for (var j = 0; j < depth; j++){
				document.write('&nbsp;&nbsp;&nbsp;&nbsp;');
			}
			document.write('&nbsp;&nbsp;&nbsp;');
			document.write('<span class="glyphicon glyphicon-unchecked"></span>');
			document.write('<label class="jmp" value="' + dir + tmp + '/">'+ "&nbsp;&nbsp;" + tmp + "&nbsp;&nbsp;");
			document.write('</label><br/>');
		}
		else
		{
			console.log(depth);
			for (var j = 0; j < depth; j++){
				document.write('&nbsp;&nbsp;&nbsp;&nbsp;');
			}
			document.write('&nbsp;&nbsp;&nbsp;');
			document.write('<label type="button" data-toggle="collapse" data-target="#' + nodes + '">');
			document.write('<span name="sparrows" class="glyphicon glyphicon-folder-close"></span></label>');
			document.write('<label class="jmp" value="' + dir + tmp.substring(0, pos) + '/">');
			document.write("&nbsp;&nbsp;" + tmp.substring(0, pos) + "&nbsp;&nbsp;");
			document.write('</label><br/>');
			build(tmp.substring(pos, len), depth + 1, dir + tmp.substring(0, pos) + '/');
		}
		
	}

	document.write('</div>')
}

function binding()
{
	jmps = document.getElementsByClassName("jmp");
	for (var i=0; i<jmps.length; i++)
	{
		var jmp = jmps[i];
		jmp.onclick = function() {
			window.location.href = "enterdir?path=" + this.getAttribute("value");
		}
		jmp.hover = function() {
			console.log('111');
			this.style.color = 'white';
		}
	}
	var arrs = document.getElementsByName("sparrows");
	for (var i=0; i<arrs.length; i++)
	{
		arr = arrs[i];
			arr.onclick = function() {
				if (this.getAttribute("class") == "glyphicon glyphicon-folder-close")
					this.setAttribute("class", "glyphicon glyphicon-folder-open"); 
				else
					this.setAttribute("class", "glyphicon glyphicon-folder-close"); 
			}
	}
}
