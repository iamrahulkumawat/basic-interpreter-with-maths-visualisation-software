import re

def evaluate_expression(expression):
    tokens = tokenize(expression)
    if not tokens:
        return "Error: Empty expression"

    result = parse_expression(tokens)
    if result is None:
        return "Error: Invalid expression"

    return round(result, 2) if isinstance(result, float) else result

def tokenize(expression):
    pattern = r'\d+\.\d+|\d+|[+\-*/()]'
    return re.findall(pattern, expression)

def parse_expression(tokens):
    if not tokens:
        return None

    result = parse_term(tokens)
    while tokens and tokens[0] in ('+', '-'):
        operator = tokens.pop(0)
        term = parse_term(tokens)
        if term is None:
            return None
        result = result + term if operator == '+' else result - term
    return result

def parse_term(tokens):
    result = parse_factor(tokens)
    while tokens and tokens[0] in ('*', '/'):
        operator = tokens.pop(0)
        factor = parse_factor(tokens)
        if factor is None or (operator == '/' and factor == 0):
            return None
        result = result * factor if operator == '*' else result / factor
    return result

def parse_factor(tokens):
    if not tokens:
        return None

    token = tokens.pop(0)
    if token == '(':
        result = parse_expression(tokens)
        if not tokens or tokens.pop(0) != ')':
            return None
    else:
        try:
            result = float(token)
        except ValueError:
            return None

    return result
