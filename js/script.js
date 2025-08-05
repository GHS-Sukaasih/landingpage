
        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });

        // Add scroll animation to elements
        const scrollElements = document.querySelectorAll('.scroll-fade');

        const elementInView = (el, dividend = 1) => {
            const elementTop = el.getBoundingClientRect().top;
            return (
                elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
            );
        };

        const displayScrollElement = (element) => {
            element.classList.add('visible');
        };

        const handleScrollAnimation = () => {
            scrollElements.forEach((el) => {
                if (elementInView(el, 1.25)) {
                    displayScrollElement(el);
                }
            });
        };

        window.addEventListener('scroll', () => {
            handleScrollAnimation();
        });

        // Copy bank account number to clipboard
        const copyBtn = document.querySelector('.copy-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                const accountNumber = '0275802987';
                navigator.clipboard.writeText(accountNumber).then(() => {
                    alert('Nomor rekening berhasil disalin!');
                }).catch(err => {
                    console.error('Gagal menyalin: ', err);
                });
            });
        }

        // Gallery Slideshow
        document.addEventListener('DOMContentLoaded', () => {
            const slides = document.querySelectorAll('.gallery-slide');
            const prevBtn = document.querySelector('.gallery-prev');
            const nextBtn = document.querySelector('.gallery-next');
            let currentSlide = 0;

            function showSlide(n) {
                if (slides.length === 0) return;
                slides.forEach(slide => slide.classList.remove('active'));
                slides[n].classList.add('active');
            }

            function nextSlide() {
                if (slides.length === 0) return;
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }

            function prevSlide() {
                if (slides.length === 0) return;
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                showSlide(currentSlide);
            }

            if(slides.length > 0) {
                showSlide(currentSlide);
                prevBtn.addEventListener('click', prevSlide);
                nextBtn.addEventListener('click', nextSlide);

                // Optional: Auto-play, uncomment the line below
                // setInterval(nextSlide, 5000); 
            }
        });
