function buildMenu()
{
	menu = document.getElementById("menutree").value;

	document.write('<label type="button" data-toggle="collapse" data-target="#0">');
	document.write('root');
	document.write('</label>');

	build(menu, 0, 1);
}

function build(str, nodes, depth)
{
	if (str == "")
		return;

	if (str[0] == '(' && str[str.length - 1] == ')')
		str = str.substring(1, str.length - 1);
	console.log(str);

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
			for (var j=0; j < 4 * depth; ++j)
				document.write("&nbsp;");
			document.write(tmp + '<br/>');
		}
		else
		{
			document.write('<label type="button" data-toggle="collapse" data-target="#' + nodes + '">');
			for (var j=0; j < 4 * depth; ++j)
				document.write("&nbsp;");
			document.write(tmp.substring(0, pos));
			document.write('</label><br/>');
			tmp = tmp.substring(pos, len);
	  		build(tmp, nodes, depth + 1);
		}
		
	}

	document.write('</div>')
}