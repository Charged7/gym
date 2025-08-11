document.addEventListener('DOMContentLoaded', () => {
  const table = document.querySelector('table.table');
  const updateUrl = table.dataset.updateUrl;

  document.querySelectorAll('tr[data-user-id]').forEach(row => {
    const editBtn = row.querySelector('.btn-edit');
    const saveBtn = row.querySelector('.btn-save');

    // Навешиваем обработчик редактирования
    editBtn.addEventListener('click', () => {
      row.querySelectorAll('.text-view').forEach(el => el.classList.add('d-none'));
      row.querySelectorAll('.edit-input').forEach(el => el.classList.remove('d-none'));
      editBtn.classList.add('d-none');
      saveBtn.classList.remove('d-none');
    });

    // Навешиваем обработчик сохранения один раз
    saveBtn.addEventListener('click', () => {
      const gmail = row.querySelector('input[name="gmail"]').value;
      const phone = row.querySelector('input[name="phone"]').value;
      const name = row.querySelector('input[name="name"]').value;
      const surname = row.querySelector('input[name="surname"]').value;

    // Проверка имени
        const nameRegex = /^[A-Za-zА-Яа-яЁё]+$/;
        if (!nameRegex.test(name)) {
        alert("Iм'я повинно містити тільки букви");
        return;
        }


      // Проверка email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(gmail)) {
        alert('Введите корректный email с @');
        return;
      }

      // Проверка номера (только цифры и не больше 10 символов)
      const phoneRegex = /^\d{1,10}$/;
      if (!phoneRegex.test(phone)) {
        alert('Номер должен содержать только цифры и не больше 10 символов');
        return;
      }

      const userId = row.dataset.userId;
      const formData = new FormData();
      formData.append('action', 'update');
      formData.append('user_id', userId);
      formData.append('name', row.querySelector('input[name="name"]').value);
      formData.append('surname', row.querySelector('input[name="surname"]').value);
      formData.append('gmail', gmail);
      formData.append('phone', phone);
      formData.append('role', row.querySelector('select[name="role"]').value);

      fetch(updateUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) throw new Error('Ошибка сети');
        return response.text();
      })
      .then(data => {
        // Обновляем отображение текста
        row.querySelectorAll('.text-view')[0].textContent = formData.get('name');
        row.querySelectorAll('.text-view')[1].textContent = formData.get('surname');
        row.querySelectorAll('.text-view')[2].textContent = formData.get('gmail');
        row.querySelectorAll('.text-view')[3].textContent = formData.get('phone');
        row.querySelectorAll('.text-view')[4].textContent = formData.get('role');

        // Возвращаем видимость элементов
        row.querySelectorAll('.text-view').forEach(el => el.classList.remove('d-none'));
        row.querySelectorAll('.edit-input').forEach(el => el.classList.add('d-none'));
        editBtn.classList.remove('d-none');
        saveBtn.classList.add('d-none');
      })
      .catch(error => alert('Ошибка: ' + error.message));
    });
  });
});
