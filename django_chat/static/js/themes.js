$(document).ready(function(){    
    var theme_btn=$('#theme-button')
    if(localStorage.getItem('theme')){
        theme_btn.text(`Theme: ${localStorage.getItem('theme')}`)
        if(localStorage.getItem('theme')=='Dark'){
            $('.navbar').addClass('navbar-dark')
            $('body').addClass('bg-dark text-light')
            $('.chat-section').removeClass('border-dark')
            $('.reverse-other-components').css({
                'background-color':'white',
                'color':'black'
            })
        const boxes = document.querySelectorAll('.other-components');
            for (const box of boxes) {
                box.style.cssText=`
                background-color:black;
                color:white;
                `
              }
        }
        else{
            $('body').removeClass('bg-dark text-light')
            $('.navbar').removeClass('navbar-dark')
            $('.chat-section').addClass('border-dark')
            const boxes = document.querySelectorAll('.other-components');
            $('.reverse-other-components').css({
                'background-color':'black',
                'color':'white'
            })
            for (const box of boxes) {
                box.style.cssText=`
                background-color:white;
                color:black;
                `
              }
        }
    }
    else{
        theme_btn.text('Theme: Light')
    }
    theme_btn.click(function(){
        if(theme_btn.text()=='Theme: Light'){
            localStorage.setItem('theme','Dark')
            theme_btn.text(`Theme: ${localStorage.getItem('theme')}`)
            $('body').addClass('bg-dark text-light')
            $('.navbar').addClass('navbar-dark')
            $('.chat-section').removeClass('border-dark')
            $('.reverse-other-components').css({
                'background-color':'white',
                'color':'black'
            })
            const boxes = document.querySelectorAll('.other-components');
            for (const box of boxes) {
                box.style.cssText=`
                background-color:black;
                color:white;
                `
              }
        }
        else{
            localStorage.setItem('theme','Light')
            $('.navbar').removeClass('navbar-dark')
            $('body').removeClass('bg-dark text-light')
            $('.chat-section').addClass('border-dark')
            theme_btn.text(`Theme: ${localStorage.getItem('theme')}`)
            theme_btn.text(`Theme: ${localStorage.getItem('theme')}`)
            const boxes = document.querySelectorAll('.other-components');
            $('.reverse-other-components').css({
                'background-color':'black',
                'color':'white'
            })
            for (const box of boxes) {
                box.style.cssText=`
                background-color:white;
                color:black;
                `
              }
        }
    })
})