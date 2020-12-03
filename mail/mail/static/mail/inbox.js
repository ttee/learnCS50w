document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);


  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (!email.hasOwnProperty('sender')) {
    document.querySelector('#compose-recipients').value = "";
    document.querySelector('#compose-subject').value = "";
    document.querySelector('#compose-body').value = "";
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    if (email.subject.startsWith('Re:')) {
      document.querySelector('#compose-subject').value = `${email.subject}`;
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:`;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  // Show the mailbox name
  // document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
  
      // ... do something else with emails ...
      body = []
      for (i = 0; i < emails.length; i++){
        if (emails[i].read){
          body.push(`
          <tr class="active">
          <td class="mail-select">
              <label class="cr-styled">
                  <input type="checkbox"><i class="fa"></i>
              </label>
          </td>
          <td class="mail-rateing">
              <i class="fa fa-star"></i>
          </td>
          <td>
              ${emails[i].sender}
          </td>
          <td>
            <a href="javascript:load_email(${emails[i].id})"><i class="fa fa-circle text-purple m-r-15">${emails[i].subject}</i></a>
          </td>
          <td>
              <i class="fa fa-paperclip"></i>
          </td>
          <td class="text-right">
              ${emails[i].timestamp}
          </td>
          </tr>
          `
          )
        } else {
          
          body.push(
          `
          <tr>
          <td class="mail-select">
              <label class="cr-styled">
                  <input type="checkbox"><i class="fa"></i>
              </label>
          </td>
          <td class="mail-rateing">
              <i class="fa fa-star"></i>
          </td>
          <td>
              ${emails[i].sender}
          </td>
          <td>
              <a href="javascript:load_email(${emails[i].id})"><i class="fa fa-circle text-info m-r-15">${emails[i].subject}</i></a>
          </td>
          <td>
              <i class="fa fa-paperclip"></i>
          </td>
          <td class="text-right">
              ${emails[i].timestamp}
          </td>
          </tr>
          `
          )
        }

      }
      document.querySelector('#emails-view').innerHTML = `
      <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
      <table class="table table-hover mails">
      <tbody>
        ${body.join('\n')}
      </tbody>
      </table>
        `;

  });

}

function send_email(event) {
  event.preventDefault();
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject:  document.querySelector('#compose-subject').value,
        body:  document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if (typeof(result.message) === "string"){
        load_mailbox('sent');
      } else {
        alert(result.error);
      }
  });
}

function archive_email(emailID) {
  fetch(`/emails/${emailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(() =>  load_mailbox('inbox'));
}

function unarchive_email(emailID) {
  fetch(`/emails/${emailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(() =>  load_mailbox('inbox'));
}

function load_email(emailID) {

  // Show compose view and hide other views
  document.querySelector('#single-email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  //put request to server to update status of email as read
  fetch(`/emails/${emailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // Make some requests to server API
  fetch(`/emails/${emailID}`)
  .then(response => response.json())
  .then(email => {
    // ... do something else with email ...
    // compose the inner HTML from the response
    if (email.archived){
      document.querySelector('#single-email-view').innerHTML = `
      <td>
      <tr><h5><b>From :</b>${email.sender}<h5></tr>
      <tr><h5><b>To :</b>${email.recipients}<h5></tr>
      <tr><h5><b>Subject :</b>${email.subject}<h5></tr>
      <tr><h5><b>Timestamp :</b>${email.timestamp}<h5></tr>
      </td>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <button class="btn btn-sm btn-outline-primary" id="unarchive">UnArchive</button>
          <br>${email.body}<br>
  
      `;
      document.querySelector('#reply').addEventListener('click', () => compose_email(email));
      document.querySelector('#unarchive').addEventListener('click', () => unarchive_email(emailID));
    } else {
      document.querySelector('#single-email-view').innerHTML = `
      <td>
      <tr><h5><b>From :</b>${email.sender}<h5></tr>
      <tr><h5><b>To :</b>${email.recipients}<h5></tr>
      <tr><h5><b>Subject :</b>${email.subject}<h5></tr>
      <tr><h5><b>Timestamp :</b>${email.timestamp}<h5></tr>
      </td>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
          <br>${email.body}<br>

      `;
      document.querySelector('#reply').addEventListener('click', () => compose_email(email));
      document.querySelector('#archive').addEventListener('click', () => archive_email(emailID));
    }
  });
}
 