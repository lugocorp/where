
$(document).ready(function(){

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
    let inner=$(".scroll > div").get(0).getBoundingClientRect();
    let rect=$(".scroll").get(0).getBoundingClientRect();
    let {left,top}=$(".scroll > div").offset();
    top+=delta;
    if(top>rect.y) top=rect.y;
    if(top+inner.height<rect.bottom) top=rect.bottom-inner.height;
    //let last=$(".scroll > div > div").children().last().offset();
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
      }
      $(this).css("opacity",opacity);
      above=(delta<0);
    });
  }
  document.addEventListener("wheel",function(evt){
    handleScroll(-12*evt.deltaY);
  });
  handleScroll(0);

});
