// NOTE: THE BELOW WORKS

//const accordion = document.getElementsByClassName('container-accord');

//for (i=0; i<accordion.length; i++) {
//  accordion[i].addEventListener('click', function () {
//    this.classList.toggle('active')
//  })
//}


// DATAANNOTATION
const accordionLabels = document.getElementsByClassName('label');

for (let i = 0; i < accordionLabels.length; i++) {
    accordionLabels[i].addEventListener('click', function(e) {
        // Find the parent container-accord element
        const accordionItem = this.parentElement;
        accordionItem.classList.toggle('active');
        
        // Prevent event bubbling to parent elements
        e.stopPropagation();
    });
}

// Prevent form clicks from closing the accordion
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

// Prevent content clicks from toggling the accordion
const contents = document.getElementsByClassName('content');
for (let i = 0; i < contents.length; i++) {
    contents[i].addEventListener('click', function(e) {
        e.stopPropagation();
    });
}