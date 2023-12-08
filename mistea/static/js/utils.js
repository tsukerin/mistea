document.addEventListener('DOMContentLoaded', function() {
    var toggleSwitch = true;
    var editButton = document.getElementById('editButton');
    var inputField = document.getElementById('text-6e4a');
  
    function updateButtonText() {
      editButton.textContent = toggleSwitch ? 'Сохранить изменения' : 'Редактировать учетные данные';
    }
  
    function updateReadonly() {
      inputField.readOnly = !toggleSwitch;
    }
  
    editButton.addEventListener('click', function() {
      toggleSwitch = !toggleSwitch;
      updateButtonText();
      setTimeout(updateReadonly, 0);
    });
  });