class AlgebraicFunctionReading:
    
    def __init__(self,*args,**kwargs) -> None:
        """
        #   args:
            2 args refers to a lineal funtion example: (2,3) = fx = 2x + 3
            3 args refers to a cuadratic funtion example: (2,3,4) = fx = 2x2 + 3x + 4
            therefor the more arguments increase the grade of the function
            
        #   Keyword arguments:
        #  lineal example:
            string_function -- string ot the function example: "fx=2x+30"
            
            diccionary_function -- dictionary of the function example: {xc=2,c=30}  c -> constant
            
            list_function -- list of the function example: =[2,30]
        
        # cuadratic example:
            string_function -- string ot the function example: "fx=x2+2x+4"
            
            diccionary_function -- dictionary of the function example: {x2=1,xc=2,c=30}  c -> constant
            
            list_function -- list of the function example: =[1,2,30]
        """
        if args:
            self.grade = len(args)-1
            self.list_arg = list(args)
            self.validate = self.__validate_arg_function()
        
    def __validate_arg_function(self) -> bool:
        if not all(isinstance(n, (int,float)) for n in self.list_arg):
            return False
        return True

      
        

