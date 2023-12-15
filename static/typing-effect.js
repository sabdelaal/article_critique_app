document.addEventListener('DOMContentLoaded', function() {
    // Function to simulate typing effect
    function typeText(element, text) {
        let index = 0;
        const interval = 50; // Adjust the typing speed by changing this value

        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, interval);
            }
        }

        type();
    }

    // Get result elements
    const researchQuestionDescription = document.querySelector('.result-section h2:first-of-type + p');
    const methodologyDescription = document.querySelector('.result-section h2:nth-of-type(2) + p');
    const researchFindings = document.querySelector('.result-section h2:nth-of-type(3) + p');

    // Type the result text
    typeText(researchQuestionDescription, "{{ critique_result['Research Question Description'] }}");
    typeText(methodologyDescription, "{{ critique_result['Methodology Description'] }}");
    typeText(researchFindings, "{{ critique_result['Research Findings'] }}");
});
