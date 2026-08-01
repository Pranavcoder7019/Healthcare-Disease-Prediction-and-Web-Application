document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function () {
        const age = Number(form.age?.value || 0);
        const height = Number(form.height?.value || 0);
        const weight = Number(form.weight?.value || 0);

        if (age <= 0 || age > 120) {
            alert('Age must be between 1 and 120.');
            return false;
        }

        if (height <= 0 || weight <= 0) {
            alert('Height and weight must be positive.');
            return false;
        }

        return true;
    });
});
