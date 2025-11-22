const BASE_URL_TASKS = 'http://localhost:5000';
const BASE_URL_HABITS = 'http://localhost:5001';
const BASE_URL_RECIPES = 'http://localhost:5002';
const BASE_URL_BUDGET = 'http://localhost:5003';
const BASE_URL_AVATAR_STORE = 'http://localhost:5004';
const BASE_URL_STUDY_SESSION = 'http://localhost:5005';
const BASE_URL_AUTH = 'http://localhost:5000/auth';
const BASE_URL_POMODORO = 'http://localhost:5000';

async function request(url, method = 'GET', data = null, jwtToken = null) {
  const headers = {};
  if (jwtToken) headers['Authorization'] = `Bearer ${jwtToken}`;
  if (data) headers['Content-Type'] = 'application/json';
  
  const options = {
    method,
    headers,
    body: data ? JSON.stringify(data) : null
  };

  const response = await fetch(url, options);
  return response.json();
}

// --- Task APIs ---
export async function createTask(data, jwtToken) {
  return request(`${BASE_URL_TASKS}/tasks`, 'POST', data, jwtToken);
}

export async function getTasks(userId, jwtToken) {
  return request(`${BASE_URL_TASKS}/tasks?userId=${userId}`, 'GET', null, jwtToken);
}

export async function updateTask(taskId, data, jwtToken) {
  return request(`${BASE_URL_TASKS}/tasks/${taskId}`, 'PUT', data, jwtToken);
}

export async function deleteTask(taskId, jwtToken) {
  return request(`${BASE_URL_TASKS}/tasks/${taskId}`, 'DELETE', null, jwtToken);
}

export async function reorderTasks(orderList, jwtToken) {
  return request(`${BASE_URL_TASKS}/tasks/reorder`, 'PUT', orderList, jwtToken);
}

// --- Recipe Box APIs ---
export async function addRecipe(data, jwtToken) {
  return request(`${BASE_URL_RECIPES}/recipes`, 'POST', data, jwtToken);
}

export async function updateRecipe(recipeId, data, jwtToken) {
  return request(`${BASE_URL_RECIPES}/recipes/${recipeId}`, 'PUT', data, jwtToken);
}

export async function viewRecipe(recipeId, jwtToken) {
  return request(`${BASE_URL_RECIPES}/recipes/${recipeId}`, 'GET', null, jwtToken);
}

export async function filterRecipes(categoryId, subcategoryId, jwtToken) {
  let url = `${BASE_URL_RECIPES}/recipes?`;
  if (categoryId) url += `categoryId=${categoryId}&`;
  if (subcategoryId) url += `subcategoryId=${subcategoryId}&`;
  return request(url, 'GET', null, jwtToken);
}

export async function deleteRecipe(recipeId, jwtToken) {
  return request(`${BASE_URL_RECIPES}/recipes/${recipeId}`, 'DELETE', null, jwtToken);
}

export async function addSticker(data, jwtToken) {
  return request(`${BASE_URL_RECIPES}/stickers`, 'POST', data, jwtToken);
}

// --- Habit APIs ---
export async function createHabit(data, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits`, 'POST', data, jwtToken);
}

export async function getHabits(userId, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits?userId=${userId}`, 'GET', null, jwtToken);
}

export async function updateHabit(habitId, data, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits/${habitId}`, 'PUT', data, jwtToken);
}

export async function deleteHabit(habitId, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits/${habitId}`, 'DELETE', null, jwtToken);
}

export async function habitCheckIn(habitId, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits/${habitId}/check-in`, 'POST', null, jwtToken);
}

export async function habitStreak(habitId, jwtToken) {
  return request(`${BASE_URL_HABITS}/habits/${habitId}/streak`, 'GET', null, jwtToken);
}

// --- Budget APIs ---
export async function addTransaction(data, jwtToken) {
  return request(`${BASE_URL_BUDGET}/transactions`, 'POST', data, jwtToken);
}

export async function updateTransaction(transactionId, data, jwtToken) {
  return request(`${BASE_URL_BUDGET}/transactions/${transactionId}`, 'PUT', data, jwtToken);
}

export async function viewTransaction(transactionId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/transactions/${transactionId}`, 'GET', null, jwtToken);
}

export async function listTransactions(jwtToken) {
  return request(`${BASE_URL_BUDGET}/transactions`, 'GET', null, jwtToken);
}

export async function deleteTransaction(transactionId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/transactions/${transactionId}`, 'DELETE', null, jwtToken);
}

export async function analytics(type, category, jwtToken) {
  let url = `${BASE_URL_BUDGET}/analytics?`;
  if (type) url += `type=${type}&`;
  if (category) url += `category=${category}&`;
  return request(url, 'GET', null, jwtToken);
}

export async function createSavingsGoal(data, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/goals`, 'POST', data, jwtToken);
}

export async function listSavingsGoals(userId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/goals/${userId}`, 'GET', null, jwtToken);
}

export async function getSavingsGoal(goalId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/goal/${goalId}`, 'GET', null, jwtToken);
}

export async function contributeToGoal(data, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/contribute`, 'POST', data, jwtToken);
}

export async function listGoalTransactions(goalId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/goal/${goalId}/transactions`, 'GET', null, jwtToken);
}

export async function deleteGoal(goalId, jwtToken) {
  return request(`${BASE_URL_BUDGET}/savings/goal/${goalId}`, 'DELETE', null, jwtToken);
}

// --- Auth APIs ---
export async function registerUser(data) {
  return request(`${BASE_URL_AUTH}/register`, 'POST', data);
}

export async function loginUser(data) {
  return request(`${BASE_URL_AUTH}/login`, 'POST', data);
}

export async function validateToken(data) {
  return request(`${BASE_URL_AUTH}/validate`, 'POST', data);
}

export async function logoutUser(data) {
  return request(`${BASE_URL_AUTH}/logout`, 'POST', data);
}

// --- Pomodoro APIs ---
export async function createPomodoroSession(data, jwtToken) {
  return request(`${BASE_URL_POMODORO}/pomodoro/session`, 'POST', data, jwtToken);
}

export async function getPomodoroStreak(userId, jwtToken) {
  return request(`${BASE_URL_POMODORO}/pomodoro/streak/${userId}`, 'GET', null, jwtToken);
}

// --- Study Session APIs ---
export async function logStudySession(data, jwtToken) {
  return request(`${BASE_URL_STUDY_SESSION}/study/session`, 'POST', data, jwtToken);
}

export async function viewStudySessions(userId, jwtToken) {
  return request(`${BASE_URL_STUDY_SESSION}/study/sessions/${userId}`, 'GET', null, jwtToken);
}

// --- Avatar Store APIs ---
export async function purchaseItem(data, jwtToken) {
  return request(`${BASE_URL_AVATAR_STORE}/store/purchase`, 'POST', data, jwtToken);
}

export async function getUserInventory(userId, jwtToken) {
  return request(`${BASE_URL_AVATAR_STORE}/store/inventory/${userId}`, 'GET', null, jwtToken);
}

export async function getUserGlitter(userId, jwtToken) {
  return request(`${BASE_URL_AVATAR_STORE}/store/glitter/${userId}`, 'GET', null, jwtToken);
}
