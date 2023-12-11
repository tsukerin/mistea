document.addEventListener('DOMContentLoaded', function() {
    var toggleSwitch = true;
    var editButton = document.getElementById('editButton');
    var editableFields = document.getElementsByClassName('editable-field');
    var form = document.querySelector('form');
  
    function updateButtonText() {
      editButton.textContent = toggleSwitch ? 'Сохранить изменения' : 'Редактировать учетные данные';
    }
  
    function updateReadonly() {
      for (var i = 0; i < editableFields.length; i++) {
        editableFields[i].readOnly = !toggleSwitch;
      }
    }
  
    function handleSubmit(event) {
      event.preventDefault();
      
      if (toggleSwitch) {
        form.method = 'post';
        console.log('Sending POST request...');
      }
    }
  
    editButton.addEventListener('click', function() {
      toggleSwitch = !toggleSwitch;
      updateButtonText();
      setTimeout(updateReadonly, 0);
    });
  
    form.addEventListener('submit', handleSubmit);
  });