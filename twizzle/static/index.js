function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/post/like/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"]) {
          likeButton.className = "fa fa-thumbs-up";
        } else {
          likeButton.className = "fa fa-thumbs-o-up";
        }
      })
      .catch((e) => alert("Could not like post. Are you logged in?"));
}
  