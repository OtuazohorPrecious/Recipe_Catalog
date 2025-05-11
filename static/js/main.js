// Toggle chevron icon when collapsing
document.getElementById('calorieCalculator').addEventListener('show.bs.collapse', function() {
    this.previousElementSibling.querySelector('.bi-chevron-down').classList.replace('bi-chevron-down', 'bi-chevron-up');
});
document.getElementById('calorieCalculator').addEventListener('hide.bs.collapse', function() {
    this.previousElementSibling.querySelector('.bi-chevron-up').classList.replace('bi-chevron-up', 'bi-chevron-down');
});

function calculateCalories() {
    const gender = document.getElementById('gender').value;
    const activity = document.getElementById('activity').value;
    const goal = document.getElementById('goal').value;
    
    // Base calories
    let calories = (gender === 'female') ? 1800 : 2200;
    
    // Activity adjustment
    if (activity === 'moderate') calories += 200;
    if (activity === 'active') calories += 400;
    
    // Goal adjustment
    if (goal === 'lose') calories -= 500;
    if (goal === 'gain') calories += 500;
    
    // Display result
    const resultText = `Your estimated daily calorie needs: <strong>${calories} kcal</strong>`;
    document.getElementById('calorieResult').innerHTML = resultText;
    document.getElementById('result').style.display = 'block';
    
    // Optional: Scroll to result
    document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
}