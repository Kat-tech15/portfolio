document.getElementById('DocumentLoaded', function(){
    document.getElementById('click', function(e){
        if (e.target.classList.contains('notification')){
            e.target.style.display = 'none';
        }
    });

    const contactForm = document.getElementById('contact-form');
    if (contactForm){
        contactForm.addEventListener('submit', function(e){

            setTimeout(()=>{
                if (document.querySelector('.notification.success')) {
                    this.requestFullscreen();
                }
            },100);
        });
    };
});