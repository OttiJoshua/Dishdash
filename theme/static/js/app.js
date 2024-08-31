const indexSwiper = new Swiper('.index-swiper', {
      effect: "coverflow",
      grabCursor: true,
      initialSlide: 2,
      loop: true,
      centeredSlides: true,
      speed: 600,
      slidesPerView: 4,
      spaceBetween: 20,
      coverflowEffect: {
        rotate: 8,
        stretch: 70,
        depth: 350,
        modifier: 1,
        slideShadows: true,
      },
      on: {
        click(event) {
          indexSwiper.slideTo(this.clickedIndex);
        },
      },
      on: {
        init: function () {
          this.slides.forEach(slide => {
            slide.classList.remove('shrink-0');
          });
        },
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
          spaceBetween: 10,
        },
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
        },
        1024: {
          slidesPerView: 4,
          spaceBetween: 20,
        },
      },
    });
    var swiper = new Swiper(".foodSwiper", {
      loop: true,
      grabCursor: true,
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
     
    });
  
    const nextButton = document.querySelector('.swiper-button-next');
    const prevButton = document.querySelector('.swiper-button-prev');

    if (nextButton && prevButton) {
      nextButton.style.color = 'orange';
      prevButton.style.color = 'orange';

      nextButton.style.transition = 'transform 0.3s ease-in-out';
      prevButton.style.transition = 'transform 0.3s ease-in-out';

      nextButton.addEventListener('mouseover', () => {
        nextButton.style.transform = 'scale(1.2)';
      });
      nextButton.addEventListener('mouseout', () => {
        nextButton.style.transform = 'scale(1)';
      });

      prevButton.addEventListener('mouseover', () => {
        prevButton.style.transform = 'scale(1.2)';
      });
      prevButton.addEventListener('mouseout', () => {
        prevButton.style.transform = 'scale(1)';
      });
    }

    const paginationBullets = document.querySelectorAll('.swiper-pagination-bullet');

    paginationBullets.forEach(bullet => {
      bullet.style.backgroundColor = 'gray';
      bullet.style.width = '8px';
      bullet.style.height = '8px';
      bullet.style.borderRadius = '50%';
    });

    swiper.on('slideChange', function () {
      paginationBullets.forEach(bullet => {
        bullet.style.backgroundColor = 'gray';
        bullet.style.width = '8px';
      });
      
      const activeBullet = document.querySelector('.swiper-pagination-bullet-active');
      if (activeBullet) {
        activeBullet.style.backgroundColor = 'orange';
        activeBullet.style.width = '16px';
      }
    });



    function updateNavigationButtonsVisibility() {
      const prevButton = document.querySelector('.swiper-button-prev');
      const nextButton = document.querySelector('.swiper-button-next');
      const windowWidth = window.innerWidth;

      if (prevButton && nextButton) {
        if (windowWidth < 968) {
          prevButton.style.display = 'none';
          nextButton.style.display = 'none';
        } else {
          prevButton.style.display = 'block';
          nextButton.style.display = 'block';
        }
      }
    }

    document.addEventListener('DOMContentLoaded', function () {
      const tabs = document.querySelectorAll('.tab-link');
      const contents = document.querySelectorAll('.tab-content');
  
      tabs.forEach(tab => {
          tab.addEventListener('click', function (e) {
              e.preventDefault();
  
              // Remove 'active' class from all tabs and hide all content
              tabs.forEach(t => t.classList.remove('bg-orange-500', 'text-white'));
              contents.forEach(content => content.classList.add('hidden'));
  
              // Add 'active' class to clicked tab and show the corresponding content
              tab.classList.add('bg-orange-500', 'text-white');
              document.getElementById(tab.dataset.target).classList.remove('hidden');
          });
      });
  
      // Show the first tab by default
      tabs[0].click();
  });



  document.getElementById("heartIcon").addEventListener("click", function() {
    this.classList.toggle("text-orange-600");
  });
  



// Cart Counter
const decreaseBtn = document.getElementById('decrease');
const increaseBtn = document.getElementById('increase');
const counter = document.getElementById('counter');

let count = 1;

decreaseBtn.addEventListener('click', () => {
  if (count > 1) {
    count--;
    counter.textContent = count;
  }
});

increaseBtn.addEventListener('click', () => {
  count++;
  counter.textContent = count;
});



    window.onload = updateNavigationButtonsVisibility;
    window.addEventListener('resize', updateNavigationButtonsVisibility);