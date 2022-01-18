from source.math_x.function_reading.funtion_reading import AlgebraicFunctionReading as afr

def test_lineal_arg_int():
    target = True
    new_test = afr(2,3)
    print(f"Se esperaba otener el resultado: {target}, y se obtuvo {new_test.validate}")
    assert new_test.validate == target
    
def test_lineal_arg_float():
    target = True
    new_test = afr(2.2,3.4)
    print(f"Se esperaba otener el resultado: {target}, y se obtuvo {new_test.validate}")
    assert new_test.validate == target