const loginAncor = document.querySelector("#loginAncor");
const registerAncor = document.querySelector("#registerAncor");

    
    // Forms submit the data automatically, prevent this default action;
    document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
        e.preventDefault();
    });
    });

    
    // Switch pages when clicking the ancor ( login to register and vice versa); 
    
    registerAncor.addEventListener("click", function(){
        event.preventDefault()
        loginContainer.classList.remove("show");
        registerContainer.classList.add("show");
    });

    loginAncor.addEventListener("click", function(){
        event.preventDefault()
        registerContainer.classList.remove("show");
        loginContainer.classList.add("show");
    });





