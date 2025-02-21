def factorial(param: dict):
    n = param.get("factorial number")
    match n:
        case 0 | 1:
            return 1
        case _:
            return n * factorial({"factorial number": n - 1})
