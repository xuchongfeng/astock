def reformat_stock_code(stock_code):
    # 确保输入符合预期格式
    if len(stock_code) != 9 or stock_code[6] != '.':
        raise ValueError("Invalid stock code format, expected '000000.XX'")

    # 分离并重新组合字符串
    prefix = stock_code[-2:]  # 获取最后两位
    suffix = stock_code[:6]  # 获取前六位

    return f"{prefix}{suffix}"  # 返回新格式
