
        function displayCity(province) {
        console.log(province);
        $('input[name="province"]').val(province);
        $.ajax({
            url: '/static/json/location.json',
            type:'GET',
            dataType:'json',
            success: function (data) {
                console.log(data);
                var str = '';
                var cityList=[];
                for(var i=0;i<data.length;i++){
                    console.log(data[i]);
                    if(data[i]['name']==province){
                        cityList=data[i]['cityList'];
                        console.log(data[i]['cityList']);
                        break;
                    }
                }
                for(var i=0;i<cityList.length;i++){
                    var cityName=cityList[i]['name'];
                    str+='<li class="uk-parent"> <a href="#" uk-icon="chevron-down" onclick="displayArea('
                        +"'"+province+"','"+cityName+"'"+')"><span>'
                        +cityName
                        +'</span></a><ul id="arealist-'+cityName+'" class="cl-area"></ul></li>';
                }
                document.getElementById('list-'+province).innerHTML=str;
            }
        });
        return false;
    };
    function displayArea(province,city) {
        console.log(province);
        console.log(city);
        $('input[name="currentProvince"]').val(city);
        $('input[name="city"]').val(city);
        $.ajax({
            url: '/static/json/location.json',
            type:'GET',
            dataType:'json',
            success: function (data) {
                console.log(data);
                str='';
                cityList=[];
                areaList=[];
                for(var i=0;i<data.length;i++){
                    if(data[i]['name']==province){
                        cityList=data[i]['cityList'];
                        break;
                    }
                }
                for(var i=0;i<cityList.length;i++){
                    if(cityList[i]['name']==city){
                        areaList=cityList[i]['areaList'];
                        break;
                    }
                }
                console.log(areaList);
                for(var i=0;i<areaList.length;i++){
                    str+='<li><form method="get" action="/search-by-area">'
                         +'<input type="text" style="display: none" name="area-field" value="'
                         +areaList[i]['name']+'">'
                         +'<input class="uk-button uk-button-text" type="submit" value="'
                        +areaList[i]['name']+'">'
                         +'</form>'
                         +'</li>';
                }
                document.getElementById('arealist-'+city).innerHTML=str;
            }
        });
        return false;
    }
