document.addEventListener('DOMContentLoaded', function() {
    const resultSections = document.querySelectorAll('.result-section p');

    function typeText(element, text, speed) {
        let index = 0;

        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, speed);
            }
        }

        type();
    }

    resultSections.forEach(section => {
        const text = section.textContent;
        section.textContent = ''; // Clear the original text
        typeText(section, text, 50); // Adjust the speed as needed
    });
});
