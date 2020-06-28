$(function () {
    csmapi.set_endpoint ('http://demo.iottalk.tw:9999');
    var profile = {
        'dm_name': 'Bulb',
        'idf_list': [],
        'odf_list': [Luminance, Color_O],
    }
    
    var r = 255 ;
    var g = 255;
    var b = 0;
    var lum = 100;
	var firstRun = 1;  // 程式的狀態
	var tout = 0; // time out 時間 -- 過多少 ms 要執行 ccc( ) 變化顏色
	var myLoop;   // 用來記住定時工作的工作代碼 (job ID)
    function draw () {
        var rr = Math.floor((r * lum) / 100);
        var gg = Math.floor((g * lum) / 100);
        var bb = Math.floor((b * lum) / 100);
        $('.bulb-top, .bulb-middle-1, .bulb-middle-2, .bulb-middle-3, .bulb-bottom, .night').css(
            {'background': 'rgb('+ rr +', '+ gg +', '+ bb +')'}
        );
    }

    function Luminance (data) {
        lum = data[0]
        draw();
		if(firstRun==99)if(data[0] < 1) { firstRun=1; clearTimeout(myLoop); }
		if(firstRun==3){ firstRun=99; myLoop=setTimeout(ccc, 3000); } /// 三秒後啟動 ccc( )
		if(firstRun==2)firstRun=3; 
		if(firstRun==1)firstRun=2; 
		// 說明:四列依序..
		// 如果在有變化顏色狀態收到 0 立即取消定時 ccc( ) 工作, 且把 firstRun 設為 1
		// 如果 firstRun 是 3, 把 firstRun 改為 99; 並且 設定過 3 秒後執行 ccc( ) 變化顏色
		// 如果 firstRun 是 2, 把 firstRun 改為 3
		// 如果 firstRun 是 1, 把 firstRun 改為 2
		/// 這種 1 => 2 ==> 3 ==> 99 的做法叫做 finite state machine 有限狀態機
    }
	function ccc( ) {
    r = Math.floor(256 * Math.random( ));
    g = Math.floor(256 * Math.random( ));
    b = Math.floor(256 * Math.random( ));
    if( Math.max(r, g, b) < 102) { r=g=255; b=51;  }
    tout = 150 + 100 * Math.floor( 20* Math.random( ));
    myLoop = setTimeout(ccc, tout);
    draw();
	} 
	// 函數說明:
	// 亂數決定 r, g, b ; 如果 r, g, b 都小於 102 則改為 rgb(255, 255, 51) 黃色
	// 亂數決定 tout, 在 (150, 250, 350, .. 2050) 中挑一個
	// 設定過 tout 微秒(milli second)後執行 ccc( ), 但記住工作代號在 myLoop 這變數
	// 立即 draw( ) 更新燈泡
	// 至於 myLoop 工作代號是要用於接收到 0 時停止 ccc( ) 表示不再變換顏色, 參考(2)
    function Color_O (data) {
        r = data[0];
        g = data[1];
        b = data[2];
        draw();
    }

    function ida_init () {
        $('font')[0].innerText = profile.d_name;
		$('#ggyy')[0].innerText = csmapi.get_endpoint() ;
        draw();
    }

    var ida = {
        'ida_init': ida_init,
    };

    dai(profile, ida);
});
