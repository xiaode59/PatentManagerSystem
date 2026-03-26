#!/bin/bash
# ========================================
# PatentMS 服务管理脚本
# 用于将Flask应用包装为Linux系统服务

# 停止服务
# ./stop_patentms.sh
# 启动服务
# ./patentms_service.sh start
# ========================================

set -e

# 配置
APP_NAME="patentms"
APP_DIR="/home/ubuntu/graduation/BACKUP"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
PYTHON_PATH="${APP_DIR}/venv/bin/python"
LOG_DIR="${APP_DIR}/logs"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建systemd服务文件
create_service_file() {
    print_info "创建systemd服务文件..."
    
    cat << EOF | sudo tee ${SERVICE_FILE} > /dev/null
[Unit]
Description=PatentMS - 专利知识库管理系统
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=${APP_DIR}
Environment="PATH=${APP_DIR}/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY:-}"
ExecStart=${APP_DIR}/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:5000 --access-logfile ${LOG_DIR}/access.log --error-logfile ${LOG_DIR}/error.log --capture-output PatentMS:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    print_info "服务文件已创建: ${SERVICE_FILE}"
}

# 安装服务
install_service() {
    print_info "安装PatentMS服务..."
    
    # 检查目录
    if [ ! -d "${APP_DIR}" ]; then
        print_error "应用目录不存在: ${APP_DIR}"
        exit 1
    fi
    
    # 创建日志目录
    mkdir -p ${LOG_DIR}
    
    # 检查gunicorn
    if [ ! -f "${APP_DIR}/venv/bin/gunicorn" ]; then
        print_info "安装gunicorn..."
        ${APP_DIR}/venv/bin/pip install gunicorn
    fi
    
    # 创建服务文件
    create_service_file
    
    # 重载systemd
    sudo systemctl daemon-reload
    
    print_info "服务安装完成！"
}

# 启动服务
start_service() {
    print_info "启动PatentMS服务..."
    sudo systemctl start ${APP_NAME}
    sleep 2
    check_status
}

# 停止服务
stop_service() {
    print_info "停止PatentMS服务..."
    sudo systemctl stop ${APP_NAME}
    print_info "服务已停止"
}

# 重启服务
restart_service() {
    print_info "重启PatentMS服务..."
    sudo systemctl restart ${APP_NAME}
    sleep 2
    check_status
}

# 查看状态
check_status() {
    echo ""
    sudo systemctl status ${APP_NAME} --no-pager || true
    echo ""
    
    # 显示访问地址
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    print_info "访问地址: http://${LOCAL_IP}:5000"
    print_info "AI问答页面: http://${LOCAL_IP}:5000/ai-chat"
}

# 查看日志
view_logs() {
    print_info "查看服务日志 (Ctrl+C退出)..."
    sudo journalctl -u ${APP_NAME} -f
}

# 开机自启
enable_autostart() {
    print_info "设置开机自启..."
    sudo systemctl enable ${APP_NAME}
    print_info "已设置开机自启"
}

# 禁用开机自启
disable_autostart() {
    print_info "禁用开机自启..."
    sudo systemctl disable ${APP_NAME}
    print_info "已禁用开机自启"
}

# 卸载服务
uninstall_service() {
    print_warn "即将卸载PatentMS服务..."
    read -p "确认卸载？(yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        sudo systemctl stop ${APP_NAME} 2>/dev/null || true
        sudo systemctl disable ${APP_NAME} 2>/dev/null || true
        sudo rm -f ${SERVICE_FILE}
        sudo systemctl daemon-reload
        print_info "服务已卸载"
    else
        print_info "已取消"
    fi
}

# 显示帮助
show_help() {
    echo ""
    echo "PatentMS 服务管理脚本"
    echo ""
    echo "用法: $0 {install|start|stop|restart|status|logs|enable|disable|uninstall}"
    echo ""
    echo "命令说明:"
    echo "  install    - 安装为系统服务"
    echo "  start      - 启动服务"
    echo "  stop       - 停止服务"
    echo "  restart    - 重启服务"
    echo "  status     - 查看服务状态"
    echo "  logs       - 查看服务日志"
    echo "  enable     - 设置开机自启"
    echo "  disable    - 禁用开机自启"
    echo "  uninstall  - 卸载服务"
    echo ""
}

# 主入口
case "$1" in
    install)
        install_service
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    enable)
        enable_autostart
        ;;
    disable)
        disable_autostart
        ;;
    uninstall)
        uninstall_service
        ;;
    *)
        show_help
        exit 1
        ;;
esac
