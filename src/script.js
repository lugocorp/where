
$(document).ready(function(){

  let w=0;

  function handleResize(){
    let w1=$(window).width();
    if(w>=1000 && w1<1000){
      $(".scroll > div").offset({top:$(".scroll").offset().top});
      $(".scroll > div > div").css("opacity",1);
    }
    if(w<1000 && w1>=1000) handleScroll(0);
    w=w1;
  }

  /* Scrolling stuff */
  /*function automateScroll(){
    let component=null;
    let dist=1000000;
    let {top}=$(".scroll").offset();
    $(".scroll > div > div").each(function(){
      let d=Math.abs(top-$(this).offset().top);
      if(d<dist){
        component=this;
        dist=d;
      }
    });
    let delta=dist<10?dist:10;
    if($(component).offset().top>top) delta*=-1;
    handleScroll(delta);
    setTimeout(automateScroll,100);
  }*/
  function handleScroll(delta){
    if(w<1000) return;
    let inner=$(".scroll > div").get(0).getBoundingClientRect();
    let rect=$(".scroll").get(0).getBoundingClientRect();
    let {left,top}=$(".scroll > div").offset();
    let orig_top=top;
    top+=delta;
    if(top>rect.y) top=rect.y;
    let last_top=$(".scroll > div > div").last().offset().top-orig_top;
    if(top+last_top<rect.top) top=rect.top-last_top;
    $(".scroll > div").offset({top,left});
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
  
  $(window).resize(() => handleResize());
  document.addEventListener("wheel",function(evt){
    handleScroll(-12*evt.deltaY);
  });
  handleScroll(0);
  handleResize();

});
