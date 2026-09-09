document.addEventListener("DOMContentLoaded",function(){
  const header=document.querySelector(".main-header");
  const toggle=document.querySelector(".mobile-toggle");
  const desktopNav=document.querySelector(".main-nav");

  if(header && toggle && desktopNav){
    let mobileNav=document.querySelector(".mobile-nav");

    if(!mobileNav){
      mobileNav=document.createElement("nav");
      mobileNav.className="mobile-nav";
      mobileNav.setAttribute("aria-label","Mobile navigation");
      mobileNav.hidden=true;

      desktopNav.querySelectorAll("a").forEach(function(link){
        mobileNav.appendChild(link.cloneNode(true));
      });

      header.appendChild(mobileNav);
    }

    toggle.addEventListener("click",function(){
      const open=toggle.getAttribute("aria-expanded")==="true";
      toggle.setAttribute("aria-expanded",String(!open));
      mobileNav.hidden=open;
    });

    mobileNav.addEventListener("click",function(e){
      if(e.target.closest("a")){
        mobileNav.hidden=true;
        toggle.setAttribute("aria-expanded","false");
      }
    });

    window.addEventListener("resize",function(){
      if(window.innerWidth>980){
        mobileNav.hidden=true;
        toggle.setAttribute("aria-expanded","false");
      }
    });
  }

  document.querySelectorAll(".faq-item button").forEach(function(btn){
    btn.addEventListener("click",function(){
      const item=btn.closest(".faq-item");
      if(!item)return;
      const open=item.classList.toggle("open");
      btn.setAttribute("aria-expanded",String(open));
    });
  });

  document.querySelectorAll('button').forEach(function(btn){
    if(btn.textContent.trim().toLowerCase().includes("back to top")){
      btn.addEventListener("click",function(){
        window.scrollTo({top:0,behavior:"smooth"});
      });
    }
  });
});
