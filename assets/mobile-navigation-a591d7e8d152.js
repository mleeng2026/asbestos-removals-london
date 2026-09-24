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

// Keep the enquiry fields in one column and collect the requested timescale.
document.addEventListener("DOMContentLoaded",function(){
  const style=document.createElement("style");
  style.textContent=".quote-form .quote-row{grid-template-columns:minmax(0,1fr)}";
  document.head.appendChild(style);
  document.querySelectorAll("form.quote-form").forEach(function(form){
    if(form.querySelector('[name="when_needed"]'))return;
    const location=form.querySelector('[name="location"]');
    if(!location)return;
    const label=document.createElement("label");
    label.textContent="When do you need it done?";
    const input=document.createElement("input");
    input.type="text";
    input.name="when_needed";
    input.placeholder="e.g. ASAP or a preferred date";
    label.appendChild(input);
    location.closest("label").after(label);
  });
});
