const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');
const panelLogin = document.getElementById('panel-login');
const panelRegister = document.getElementById('panel-register');
const toRegister = document.getElementById('to-register');
const toLogin = document.getElementById('to-login');

function activate(tab) {
  const isLogin = tab === 'login';
  tabLogin.classList.toggle('active', isLogin);
  tabRegister.classList.toggle('active', !isLogin);
  tabLogin.setAttribute('aria-selected', String(isLogin));
  tabRegister.setAttribute('aria-selected', String(!isLogin));
  panelLogin.classList.toggle('hidden', !isLogin);
  panelRegister.classList.toggle('hidden', isLogin);
}

tabLogin.addEventListener('click', () => activate('login'));
tabRegister.addEventListener('click', () => activate('register'));
toRegister.addEventListener('click', () => activate('register'));
toLogin.addEventListener('click', () => activate('login'));