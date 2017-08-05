var likes = document.getElementsByName("like-button");

for (var i=0; i<likes.length; i++)
{
	
	var like = likes[i];
	like.onclick = function(){
		var that = this;
		$.get("likeOrWithdrew?picId=" + this.id, function(data, status){
			//that.innerHTML = data;
			if(data > 0)
				{
					that.innerHTML = "<span class='glyphicon glyphicon-heart' style='color:hotpink' aria-hidden='true'>&nbsp;" + data.toString() + "</span>";
				}
			else
				{
					that.innerHTML = "<span class='glyphicon glyphicon-heart' aria-hidden='true'>&nbsp;" + (-data).toString() + "</span>";
				}

		})
	}
}

var favors = document.getElementsByName("favor-button");

for(var i=0; i<favors.length; i++)
{

	var favor = favors[i];
	favor.onclick = function(){
		var that = this;
		$.get("addFavor?picId=" + this.id, function(data, status){
			//that.innerHTML = data;
			if(data == 1)
				{
					that.innerHTML = "<span class='glyphicon glyphicon-ok' style='color:blue' aria-hidden='true'>&nbsp;favored</span>";
				}
			else
				{
					that.innerHTML = "<span class='glyphicon glyphicon-star' aria-hidden='true'>&nbsp;favor </span>";
				}

		})
	}

}