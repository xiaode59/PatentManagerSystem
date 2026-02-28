/**
 * 登录注册前端逻辑
 */

// 显示注册表单
function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
}

// 显示登录表单
function showLogin() {
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'block';
}

// 处理登录
function doLogin() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        showMessage('请输入用户名和密码', 'danger');
        return;
    }
    
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('登录成功，正在跳转...', 'success');
            // 2秒后跳转到首页
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            showMessage(data.message, 'danger');
        }
    })
    .catch(error => {
        showMessage('网络请求失败: ' + error.message, 'danger');
    });
}

// 处理注册
function doRegister() {
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;
    
    if (!username || !email || !password || !confirmPassword) {
        showMessage('请填写所有字段', 'danger');
        return;
    }
    
    // 密码一致性检查
    if (password !== confirmPassword) {
        showMessage('两次输入的密码不一致', 'danger');
        return;
    }
    
    // 简单密码强度检查
    if (password.length < 6) {
        showMessage('密码长度至少6位', 'warning');
        return;
    }
    
    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            confirm_password: confirmPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('注册成功，即将跳转到登录', 'success');
            setTimeout(() => {
                showLogin();
                clearRegisterForm();
            }, 2000);
        } else {
            showMessage(data.message, 'danger');
        }
    })
    .catch(error => {
        showMessage('注册请求失败: ' + error.message, 'danger');
    });
}

// 清空注册表单
function clearRegisterForm() {
    document.getElementById('regUsername').value = '';
    document.getElementById('regEmail').value = '';
    document.getElementById('regPassword').value = '';
    document.getElementById('regConfirmPassword').value = '';
}

// 显示消息提示
function showMessage(message, type) {
    const messageBox = document.getElementById('messageBox');
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'warning' ? 'alert-warning' : 'alert-danger';
    
    messageBox.innerHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // 3秒后自动消失
    setTimeout(() => {
        const alert = messageBox.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 3000);
}
