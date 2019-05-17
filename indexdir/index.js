
        
        // document.addEventListener('DOMContentLoaded', function()
        // {
        //  let stars = document.querySelectorAll('.star');
        //  stars.forEach(function(star){
        //      star.addEventListener('click',setRating);
        //  });
            
        //  let rating = parseInt(document.querySelector('.stars').getAttribute('data-rating'));
        //  let target = stars[rating - 1];
        //  target.dispatchEvent(new MouseEvent('click'));  
        // });
        
        
        
        
        function setRating(ev){
            let span = ev.currentTarget;
            let stars = document.querySelectorAll('.star');
            let match = false;
            let num = 0;
            stars.forEach(function(star, index)
            {
                if(match){
                    star.classList.remove('rated');
                }else{
                    star.classList.add('rated');
                }
                
                if(star === span){
                    match = true;
                    num = index + 1;
                }
                
                let starValue = parseInt(star.getAttribute('data-val'));
            });
            
            document.querySelector('.stars').setAttribute('data-rating',num);
        }


var obj = (function(){
    return {
        init:function(){
            obj.getData();
        },
        getData:function(){
            var term = $("#searchId").val();
            var _URL = "http://127.0.0.1:5000/api/search?term=" + term;
            console.log(_URL);
            $.ajax({
                url: "http://127.0.0.1:5000/api/search?term=" + term,
                dataType: 'jsonp',

                success: function(data) {
                    console.log(data);
                    var arr = data;
                    var str = [];
                    var i = 0;
                    for(var i = 0;i<arr.length;i++){
                        var html = "<div class='list-item'>";
                        html +="<p><strong>Number</strong> : " + arr[i].Number +"</p>";
                        console.log(arr[i].Number)
                        html +="<p><strong>Name_of_Covered_Entity</strong> : " + arr[i].Name_of_Covered_Entity;
                        html += "<span class = 'stars' data-rating = '0'>";
                        html += "<span class = 'star'>&nbsp;</span>";
                        html += "<span class = 'star'>&nbsp;</span>";
                        html += "<span class = 'star'>&nbsp;</span>";
                        html += "<span class = 'star'>&nbsp;</span>";
                        html += "<span class = 'star'>&nbsp;</span>";
                        html += "</span></p>";
                        html +="<p>Summary : " + arr[i].Summary+ "</p>";
                        html +="</div>";
                        str[i] = html;
                    }
                    $("#list-container").html(str.join());

                    let stars = document.querySelectorAll('.star');
                    stars.forEach(function(star){
                        star.addEventListener('click',setRating);
                    });
                    
                    let rating = parseInt(document.querySelector('.stars').getAttribute('data-rating'));
                    let target = stars[rating - 1];
                    target.dispatchEvent(new MouseEvent('click'));  
                }
            });
        },
        searchData:function(val,data){
            var _dummy = [];
            _dummy = data;
            var result = _dummy.filter(element => {
                return element["Summary"].toString().toLowerCase().includes(val);
            });
            return result;
        }
    }
})();





