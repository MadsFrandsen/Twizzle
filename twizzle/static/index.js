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


function follow(userId) {
  const followCount = document.getElementById(`profile-label-followers`);
  const followButton = document.getElementById(`follow-btn`);

  fetch(`/user/follow/${userId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      followCount.innerHTML = data['followers'];
      if (data["followed"]) {
        followButton.className = "follow-btn";
      } else {
        followButton.className = "unfollow-btn";
      }
    })
    .catch((e) => alert("Could not follow user. Are you logged in?"));
}

