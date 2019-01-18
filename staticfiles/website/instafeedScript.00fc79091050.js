        //instafeed
        var feed = new Instafeed({
            get: 'user',
            limit:4,
            userId: '2111940828',
            clientId: 'b52122e520644fc1ba87a691de15936d',
            accessToken:'2111940828.1677ed0.1a691d0ab4d448528e6580ba97fae5ea',
            resolution:'standard_resolution',
            template:'<div id="instaBlock">'+'<img src="{{image}}" width="240"/>'+'<p>"{{caption}}"</p><p id="instaLink"><a href="{{link}}" target="_blank"><span>View on instagram</span></a></p></div>'
        });
        feed.run();