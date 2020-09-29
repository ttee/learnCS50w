document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send_email').addEventListener('click', send_email); //send_email tag is linked to the submit button in inbox.html

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function send_email() {
  // call the emails url so that we can trigger the views.compose 
  fetch('/emails', { //fetch function will send a REQUEST with a body of type string 
    // (email to be sent) to endpoint /emails
    method: 'POST',
    body: JSON.stringify({
        recipients: '1@1.com',
        subject: 'Meeting time',
        body: 'How about we meet tomorrow at 3pm?'
    })
  })
  .then(response => response.json()) //response of type byte string from python view is converted to a some kind of dictionary object in javascript using the json method

  // response byte string from python view --- using json method ----> response object in javascript

  .then(result => {
      // Print result
      console.log(result);
      alert(result);
  });
  // Show sent-box view and display a message that email has been sent
  load_mailbox('sent')
}


