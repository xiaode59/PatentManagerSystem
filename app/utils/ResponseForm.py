class ResponseForm:
    '''统一响应格式'''
    
    @staticmethod
    def success(message='操作成功', data=None):
        return {
            'code': 200,
            'success': True,
            'message': message,
            'data': data,
            'timestamp': '2025-01-01 00:00:00'  # 实际使用时替换为当前时间
        }
    
    @staticmethod
    def error(message='操作失败', data=None):
        return {
            'code': 400,
            'success': False,
            'message': message,
            'data': data,
            'timestamp': '2025-01-01 00:00:00'
        }
