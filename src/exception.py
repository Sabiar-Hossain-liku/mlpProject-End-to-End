import sys  
from src.logger import logging

def error_massage_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_massage =f"Error occurd in [{filename}], in line [{exc_tb.tb_lineno}] , error message[{str(error)}]"
    return error_massage


class CustomException(Exception):
    
    def __init__(self,error_message , error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_massage_detail(error_message,error_detail = error_detail)
    
    def __str__(self):
        return self.error_message

if __name__ == '__main__':

    try:
        a=1/0
    except Exception as e :
        logging.info("Divided by zero error")
        raise CustomException(e, sys)

