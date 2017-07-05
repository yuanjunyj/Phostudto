var likes = document.getElementsByName('like');

for (var i=0; i<likes.length; i++)
{
	
	var like = likes[i];
	like.onclick = function(){
		var that = this;
		$.get("likeOrWithdrew?picId=" + this.id, function(data){
			//that.innerHTML = data;
			if(data == 0)
			{
				that.innerHTML = (parseInt(that.innerHTML) - 1).toString()
			}
			else
			{
				that.innerHTML = (parseInt(that.innerHTML) + 1).toString()
			}

		})
	}
}