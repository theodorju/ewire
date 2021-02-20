// Get the scroll class anchor elements
const scrollElems = document.querySelectorAll('.js-scroll-trigger');

// Add event listeners to those elements
for(let i = 0; i < scrollElems.length; i++){
    const elem = scrollElems[i];
    
    elem.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Get the element id
    const scrollElemId = e.target.href.split('#')[1];

    // Find that node from the document
    const scrollEndElem = document.getElementById(scrollElemId);

    // Animate to that node 
    const anim = requestAnimationFrame((timestamp) => {
        const stamp = timestamp || new Date().getTime();
        const duration = 1000;
        const start = stamp;

        const startScrollOffset = window.pageYOffset;
        const scrollEndElemTop = scrollEndElem.getBoundingClientRect().top;

        scrollToElem(start, stamp, duration, scrollEndElemTop, startScrollOffset);
        })
    })
}

// Add event listeners for smooth scrolling to top when clicking on the logo
const logo = document.querySelectorAll(".top-scroll-trigger");

for(let i = 0; i < logo.length; i++){

    const elem = logo[i];

    elem.addEventListener('click', function(e) {
        e.preventDefault();

        const scrollEndElem = document.getElementById("top");

        // Animate to top 
        const anim = requestAnimationFrame((timestamp) => {
            const stamp = timestamp || new Date().getTime();
            const duration = 1000;
            const start = stamp;

            const startScrollOffset = window.pageYOffset;
            const scrollEndElemTop = scrollEndElem.getBoundingClientRect().top;

            scrollToElem(start, stamp, duration, scrollEndElemTop, startScrollOffset);
            })
    })
}


const easeInCubic = function (t) { return t*t*t }
 
const scrollToElem = (startTime, currentTime, duration, scrollEndElemTop, startScrollOffset) => {
   const runtime = currentTime - startTime;
   let progress = runtime / duration;
   
   progress = Math.min(progress, 1);
   
   const ease = easeInCubic(progress);
   
   window.scroll(0, startScrollOffset + (scrollEndElemTop * ease));
if(runtime < duration){
     requestAnimationFrame((timestamp) => {
       const currentTime = timestamp || new Date().getTime();
       scrollToElem(startTime, currentTime, duration, scrollEndElemTop, startScrollOffset);
     })
   }
 }