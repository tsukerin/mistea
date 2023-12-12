document.addEventListener("DOMContentLoaded", function() {
  const editSubButton = document.getElementById("editSubButton");
  
  const editPopup = document.getElementById("editPopup");
  const overlay = document.getElementById("overlay");
  const closePopup = document.getElementById("closePopup");

  editSubButton.addEventListener("click", function() {
    editPopup.style.display = "block";
    overlay.style.display = "block";
  });

  closePopup.addEventListener("click", function() {
    editPopup.style.display = "none";
    overlay.style.display = "none";
  });
});
document.getElementById("saveChangesBtn").addEventListener("click", function() {
  saveChanges();
});
 

function closeEditPopup() {
  document.getElementById("editPopup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}


function saveChanges() {
  closeEditPopup();
}
  const unsubscribeButton = document.getElementById("unsubscribeButton");
  const unsubscribePopup = document.getElementById("unsubscribePopup");
  const closeUnsubscribePopup = document.getElementById("closeUnsubscribePopup");
  const confirmUnsubscribeBtn = document.getElementById("confirmUnsubscribeBtn");
  const cancelUnsubscribeBtn = document.getElementById("cancelUnsubscribeBtn");


  unsubscribeButton.addEventListener("click", function() {
    unsubscribePopup.style.display = "block";
    overlay.style.display = "block";
  });


  closeUnsubscribePopup.addEventListener("click", function() {
    unsubscribePopup.style.display = "none";
    overlay.style.display = "none";
  });


  cancelUnsubscribeBtn.addEventListener("click", function() {
    unsubscribePopup.style.display = "none";
    overlay.style.display = "none";
  });


  confirmUnsubscribeBtn.addEventListener("click", function() {
    unsubscribePopup.style.display = "none";
    overlay.style.display = "none";
  });

// scripts.js

// DOM elements
document.addEventListener("DOMContentLoaded", function() {
  const deleteButton = document.getElementById("deleteButton");
  const deletePopup = document.getElementById("deletePopup");
  const closeDeletePopup = document.getElementById("closeDeletePopup");
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");

  deleteButton.addEventListener("click", function() {
      deletePopup.style.display = "block";
      overlay.style.display = "block";
  });

  closeDeletePopup.addEventListener("click", function() {
      deletePopup.style.display = "none";
      overlay.style.display = "none";
  });

  cancelDeleteBtn.addEventListener("click", function() {
      deletePopup.style.display = "none";
      overlay.style.display = "none";
  });

  confirmDeleteBtn.addEventListener("click", function() {
      deletePopup.style.display = "none";
      overlay.style.display = "none";
  });
});

// Main scripts
$(document).ready(function() {
  $('#saveChangesBtn').on('click', function() {
     var formData = {
        'tea_type': $('input[name=tea_type]:checked').val(),
        'schedule': $('input[name=schedule]:checked').val(),
        'address': $('#deliveryAddress').val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
     };

     $.ajax({
        type: 'POST',
        url: '/user/save-changes/',
        data: formData,
        success: function(response) {
           console.log(response);
           window.location.reload();
        },
        error: function(error) {
           console.log('AJAX Error:', error);
        }
     });
  });
});

$(document).ready(function() {
  $('#editProfileBtn').on('click', function() {
    $('#editProfilePopup').css('display', 'block');
    $('#overlay').css('display', 'block');
  });

  $('#closeProfilePopup').on('click', function() {
    $('#editProfilePopup').css('display', 'none');
    $('#overlay').css('display', 'none');
  });

  $('#saveProfileChangesBtn').on('click', function() {
    saveProfileChanges();
  });

  function closeProfileEditPopup() {
    $('#editProfilePopup').css('display', 'none');
    $('#overlay').css('display', 'none');
  }

  function saveProfileChanges() {
    var email = $('#editEmail').val();
    var fullname = $('#editFullname').val();
    var phoneNumber = $('#editPhoneNumber').val();

    var emailRegex = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/;

    var messageContainer = $('#messageContainer');

    messageContainer.empty();

    if (!emailRegex.test(email)) {
        messageContainer.text('Please enter a valid email address.');
        return;
    }

    if (fullname.length > 50) {
        messageContainer.text('Full name should not exceed 50 characters.');
        return;
    }

    var phoneRegex = /^\+\d{11}$/;
    if (!phoneRegex.test(phoneNumber)) {
        messageContainer.text('Please enter a phone number in the format +7XXXXXXX.');
        return;
    }

    var formData = {
        'email': email,
        'fullname': fullname,
        'phone_number': phoneNumber,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    };

    $.ajax({
        type: 'POST',
        url: '/user/save-profile-changes/',
        data: formData,
        success: function(response) {
            console.log(response);
            window.location.reload();
        },
        error: function(error) {
            console.log('AJAX Error:', error);
        }
    });
  }
});

// Additional scripts
document.getElementById('confirmUnsubscribeBtn').addEventListener('click', function(event) {
  event.preventDefault();
  var deleteUrl = this.getAttribute('data-delete-url');
  var csrf = this.getAttribute('data-csrf');
  var form = document.createElement('form');
  form.method = 'post';
  form.action = deleteUrl;
  var csrf_token = document.createElement('input');
  csrf_token.type = 'hidden';
  csrf_token.name = 'csrfmiddlewaretoken';
  csrf_token.value = csrf;
  form.appendChild(csrf_token);

  document.body.appendChild(form);
  form.submit();
});

document.getElementById('cancelUnsubscribeBtn').addEventListener('click', function(event) {
  // Handle cancel action
});
