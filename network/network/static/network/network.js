

document.addEventListener('DOMContentLoaded', function() {

    //var a = document.getElementById('all_posts'); //or grab it by tagname etc
    //a.href = "somelink url"
    // Use buttons to toggle between views
    
    document.querySelector('#following_posts').href = "javascript:load_post_page('following')"
    document.querySelector('#all_posts').href = "javascript:load_post_page('all')"
    //document.querySelector('#new_post').addEventListener('click', () => new_post('request'));
    document.querySelector('#new_post').addEventListener('submit', new_post);
  // in the context of "new_post", javascript eventlistener triggers new_post function when there is a submit click
    if (document.querySelector('#FollowButton') != null) {
      document.querySelector('#FollowButton').addEventListener('click', follow);
    }
  
  //#FollowButton is the id
    var currentLocation = window.location;
    // By default, load the inbox
    if (currentLocation.pathname === '/') {
      load_post_page('all');
    } else {
      user = currentLocation.pathname.split('/')[1]
      load_post_page(user);
    }


  });
  

  function new_post(event) {
    event.preventDefault();

    // compose POST request that contains the post content
    fetch('/posts', {
      method: 'POST',
      body: JSON.stringify({
          content: document.querySelector('#compose-body').value, 
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        if (typeof(result.message) === "string"){
          //load_mailbox('sent');
          alert('new post success');
        } else {
          alert(result.error);
        }
        load_post_page('all');
    }
    );
  }

  // other than user_id, load_post_page needs a page info to load the correct pagination
function load_post_page(user_id, pagenum) {
  if (user_id === 'all') {
    // api stuffs
    load_posts(user_id, pagenum)
    .then(response => {
      // html stuffs
      // set title to All Posts
      // disable profile-view
      document.querySelector('#all-posts-view').innerHTML =compose_post_table(response["posts"])

      let text_areas = document.querySelectorAll('#edit-textarea');
      console.log(text_areas)
      for (i = 0; i < text_areas.length; i ++) {
         text_areas[i].style.display = 'none';
       }
      //document.querySelector('#edit-textarea').style.display = 'none';
      document.querySelector('#paged-view').innerHTML = compose_post_pagination(user_id, response["page_obj"])
      document.querySelector('#title-of-page').innerHTML ="All Posts"

      document.querySelector('#all-posts-view').style.display = 'block';
      if (document.querySelector('#profile-view') != null) {
        document.querySelector('#profile-view').style.display = 'none';
      } 
    }) 

  } else if (user_id === 'following') {
    load_posts(user_id)
    .then(response => {
      // html stuffs
      // set title to Following
      // diable the profile-view
      document.querySelector('#all-posts-view').innerHTML =compose_post_table(response["posts"])
      document.querySelector('#edit-textarea').style.display = 'none';
      document.querySelector('#title-of-page').innerHTML ="Following Posts"

      if (document.querySelector('#profile-view') != null) {
        document.querySelector('#profile-view').style.display = 'none';
      } 


    }) 
  } else {
    load_posts(user_id)
    .then(response => {
      // html stuffs
      // set title to Username
      // enable the profile-view
      document.querySelector('#all-posts-view').innerHTML =compose_post_table(response["posts"])
      document.querySelector('#edit-textarea').style.display = 'none';
      document.querySelector('#title-of-page').innerHTML =`Profile of ${user_id}`
      let edit_buttons = document.querySelectorAll('edit-button');

      // for (i = 0; i < edit_buttons.length; i ++) {
      //   edit_buttons[i].addEventListener('click', edit_post(post_id));
      // }
      


    }) 
  }
}

function edit_post(post_id) {
  console.log("Edit clicked") 
  // edit button:
  //      once clicked:
  //             - hide post content, show the text editting area, hide edit button, show post button, and cancel button
  //             - copy the post content to the text editting area
 //replace the post with innerhtml for textarea
 //select a component in this HTML page to modify using javascript
  
  document.querySelector('#edit-textarea').style.display = 'block';
  console.log(post_id)
  document.querySelector(`#post-content-${post_id}`).style.display = 'none';
}
 
function compose_post_table(posts) {
  body = []

  //for (i = results.posts.length -1;i > -1;  i--){

  a = posts
  // for each post
  // we have a div for each post
  // inside the dive there are components: post content, text editing area, buttons
  // edit button:
  //      once clicked:
  //             - hide post content, show the text editting area, hide edit button, show post button, and cancel button
  //             - copy the post content to the text editting area
  for (let i in a) {
      post_id = a[i].id
      body.push(`
      <div class=mystyle>
      <table class="table table-hover mails">
      <tbody>
      <p>
      ${a[i].id}
      ${a[i].user}
      ${a[i].timestamp}
      <div id="post-content-${post_id}"> ${a[i].content}</div>
      <!--based on the button text, we will toggle between Edit and Save button -->

      <button class="edit-button" onclick="edit_post('${post_id}')">Edit</button>
      <div id="edit-textarea"><textarea class="form-control" id="compose-body" placeholder="Body">${a[i].content}</textarea> </div>
      ${a[i].numlikes}
      </tbody>
      </table>
      </div>
      `
      )
  }

  return  `${body.join('\n')}`
}

async function load_posts(user_id, pagenum) {
  if (pagenum == null) {
    pagenum = 1
  }
  console.log(pagenum)
 if (user_id === 'all') {
    url = `/posts?page=${pagenum}`
  } else if (user_id === 'following') {
    url = `/posts/following`
  } else {
    url = `/users/${user_id}/posts`
  }
  
  response = await fetch(url)
  decoded_response = await response.json()
  return decoded_response
  
}
  // network.js in client
  // templates are in server
  // server renders html and downloads unprocessed javascript to client for realtime processing
  // django python code includes models, views, url in server (django framework is in memory and is the server)

  //client contains javascript and rendered (final) copy of html 

function follow() {
  followed_user = this.value
  
  // make request to server
  fetch(`/follows/${followed_user}`)
  // if request success
  // toggle the follow/unfollow button
  .then (response => response.json())
  .then(result => {
    // Print result
    if (typeof(result.message) === "string"){
      //load_mailbox('sent');
      if (this.innerText === 'Unfollow') {
        this.innerText = 'Follow'
      } else {
        this.innerText = 'Unfollow'
      }
    }
  }
  );
}

function compose_post_pagination(user_id, page_obj) {

    //another javascript function has called the API already
    //and now this javascript function will take in the argument current to form the HTML for pagination page numbers

    //if current between 1 and last page
    //then display first previous, current, next, last

    //input is a string page number
    //inside this javascript
    // if (page_obj.has_previous) {
    //   // load_post_page(user_id, 1);
    //   // load_post_page('all', 1);
    //   //first page href declaration
    //   //<<next last>>
    //   prev = `<a href="javascript:load_post_page('${user_id}', 1)">&laquo; First</a>
    //   <a href="javascript:load_post_page('${user_id}','${page_obj.previous_page_number }')">previous</a><p><p><p><p>`
    // }
    if (page_obj.has_next) {
      // load_post_page(user_id, 1);
      // load_post_page('all', 1);
      //first page href declaration
      //<<next last>>
      prev = `<a href="javascript:load_post_page('${user_id}','${page_obj.num_pages }')">&laquo; First</a>
      <a href="javascript:load_post_page('${user_id}', ${page_obj.next_page_number})">previous</a><p><p><p><p>`
    }
    else {
      prev = ''
    }

    if (page_obj.has_previous) {
      next = `<a href="javascript:load_post_page('${user_id}', ${page_obj.previous_page_number})">next</a>
      <a href="javascript:load_post_page('${user_id}', 1)">last &raquo;</a><p><p><p><p>`  }
    else {
      next = ''
    }
    // if (page_obj.has_next) {
    //   next = `<a href="javascript:load_post_page('${user_id}', ${page_obj.next_page_number})">next</a>
    //   <a href="javascript:load_post_page('${user_id}','${page_obj.num_pages }')">last &raquo;</a><p><p><p><p>`  }
    // else {
    //   next = ''
    // }

    body = `
              <span class="step-links">
                  ${prev}
                  <span class="current">
                      Page ${page_obj.num_pages + 1 - page_obj.number } of ${page_obj.num_pages}<p><p><p><p>.
                  </span>
                  ${next}
              </span>
            `
return body
}