document.addEventListener('DOMContentLoaded', function() {

    // Select button to like
    const buttonsLike = document.querySelectorAll("#like");

    buttonsLike.forEach((button) => button.addEventListener('click', () => like()));

});

function like() {
    alert('Like');
};