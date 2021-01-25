
$(document).ready(function(){

  let w=0;

  function handleResize(){
    let w1=$(window).width();
    if(w>=1000 && w1<1000){
      $(".scroll > div").offset({top:$(".scroll").offset().top});
      $(".scroll > div > div").css("opacity",1);
    }
    if(w<1000 && w1>=1000) handleScroll(0);
    if(w>=1000 && w1<1000) handleScroll();
    w=w1;
  }

  /* Scrolling stuff */
  function handleScroll(delta){
    if((delta==undefined && w>=1000) || (delta!=undefined && w<1000)) return;
    let rect=$(".scroll").get(0).getBoundingClientRect();
    if(delta!=undefined){
      let inner=$(".scroll > div").get(0).getBoundingClientRect();
      let {left,top}=$(".scroll > div").offset();
      let orig_top=top;
      top+=delta;
      if(top>rect.y) top=rect.y;
      let last_top=$(".scroll > div > div").last().offset().top-orig_top;
      if(top+last_top<rect.top) top=rect.top-last_top;
      $(".scroll > div").offset({top,left});
    }
    let above=true;
    let possible=true;
    $(".scroll > div > div").each(function(){
      let {top}=$(this).offset();
      let delta=top-rect.y;
      let opacity=0.1;
      if(possible && delta>=0 && above){
        opacity=1;
        possible=false;
        let thumb=$(this).attr("thumbnail");
        if(thumb.length) $(".preview").attr("src",thumb);
        else $(".preview").attr("src","res/where/white.png");
      }
      $(this).css("opacity",opacity);
      above=(delta<0);
    });
  }

  // Set up event handlers
  $(window).resize(() => handleResize());
  document.addEventListener("wheel",function(evt){
    handleScroll(-12*evt.deltaY);
  });
  $(".scroll").get(0).addEventListener("scroll",function(evt){
    handleScroll();
  });
  handleResize();
  if(w>=1000) handleScroll(0);
  else handleScroll();

  // Search bar stuff
  $(".search-label").click(function(){
    $(".search-label").remove();
    $(".main-page .header").append($("<input class=\"search-label\" type=\"text\" placeholder=\"Search\"/>")
      .on("input",function(e){
        let query=e.target.value;
        $(".scroll > div > div").each(function(){
          let q=$(this).attr("query");
          let show=(query.length==0 || q.indexOf(query)>=0);
          if(show) $(this).show();
          else $(this).hide();
        });
        handleScroll();
      })
    );
  });

});
