

def power_law_pdf(x, alpha, xmin):
    C = (alpha - 1) * xmin **(alpha - 1)
    return C * x ** (- alpha)
