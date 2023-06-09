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


// function follow(userId) {
//   const followCount = document.querySelector('#profile-number-followers');
//   const followButton = document.querySelector('#follow-btn');

//   fetch(`/user/follow/${userId}`, { method: "POST" })
//     .then((res) => res.json())
//     .then((data) => {
//       followCount.innerHTML = data.followers;
//       if (data.followed) {
//         followButton.textContent = "Unfollow";
//         followButton.classList.remove("follow-btn");
//         followButton.classList.add("unfollow-btn");
//       } else {
//         followButton.textContent = "Follow";
//         followButton.classList.remove("unfollow-btn");
//         followButton.classList.add("follow-btn");
//       }
//     })
//     .catch((e) => alert("Could not follow user. Are you logged in?"));
// }

function follow(userId) {
  const followCount = document.querySelector('#profile-number-followers');
  const followButton = document.querySelector('#follow-btn');

  fetch(`/user/follow/${userId}`, { method: "POST" })
    .then((res) => {
      console.log(res); 
      if (res.ok) {
        return res.json();
      } else {
        throw new Error("Not logged in");
      }
    })
    .then((data) => {
      followCount.innerHTML = data.followers;
      if (data.followed) {
        followButton.textContent = "Unfollow";
        followButton.classList.remove("follow-btn");
        followButton.classList.add("unfollow-btn");
      } else {
        followButton.textContent = "Follow";
        followButton.classList.remove("unfollow-btn");
        followButton.classList.add("follow-btn");
      }
    })
    .catch((error) => {
      alert("Could not follow user. " + error.message);
    });
}


