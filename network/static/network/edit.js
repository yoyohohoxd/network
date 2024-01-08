document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".posts").forEach(post => {
        post.querySelector('#save').style.display = 'none';
        post.querySelector('#edit-post').style.display = 'none';

        // Add like functionality to all like buttons
        post.querySelector('#like').addEventListener('click', () => {
            like(post);
        })

        // If edit button exists, addEventListener for both Edit and Save button
        const editButton = post.querySelector('#edit');
        if (editButton) {
            post.querySelector('#edit').addEventListener('click', () => {
                edit(post);
            });
            post.querySelector('#save').addEventListener('click', () => {
                save(post);
            })

        }
    });
});

function edit(post) {

    // Display save button and hide edit button
    console.log(post);
    post.querySelector('#save').style.display = 'inline-block';
    post.querySelector('#edit').style.display = 'none';
    const editTextarea = post.querySelector('#edit-post');
    editTextarea.style.display  = 'inline-block';

    document.querySelectorAll('button').disabled = true;
    post.querySelector('#save').disabled = false;

    // Show textarea and populate with text from the old post
    const oldPost = post.querySelector('#post-text');
    oldPost.style.display = 'none';
    const oldText = oldPost.innerHTML;
    editTextarea.value = oldText;
};

function save(post) {
    
    // Get ID from post to fetch operation
    const postID = post.id.slice(5);
    
    // Hide Save and show Edit, hide Textarea and show Paragraph
    post.querySelector('#save').style.display = 'none';
    post.querySelector('#edit').style.display = 'inline-block';
    const editTextarea = post.querySelector('#edit-post');
    editTextarea.style.display = 'none'
    const newPost = post.querySelector('#post-text');
    newPost.style.display = 'block';
    newPost.innerHTML = editTextarea.value;

    document.querySelectorAll('button').disabled = false;


    // Put new text in database
    fetch(`savepost/${postID}/`, {
        method: 'PUT',
        body: JSON.stringify({
            post_text: editTextarea.value
        })
    })
}

function like(post) {
    console.log('Liking');
    // Get ID from post to fetch operation
    const postID = post.id.slice(5);

    likeButton = post.querySelector('#like');

    fetch(`likepost/${postID}/`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        likeButton.innerHTML = data.liked ? 'Unlike' : 'Like';
    });
}